import { createServer } from "node:http";
import {
  existsSync,
  mkdirSync,
  readFileSync,
  writeFileSync
} from "node:fs";
import path from "node:path";

function loadDotEnv() {
  const envPath = path.resolve(process.cwd(), ".env");
  if (!existsSync(envPath)) return;

  const lines = readFileSync(envPath, "utf8").split(/\r?\n/);
  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#")) continue;

    const eqIndex = trimmed.indexOf("=");
    if (eqIndex < 1) continue;

    const key = trimmed.slice(0, eqIndex).trim();
    const rawValue = trimmed.slice(eqIndex + 1).trim();
    const value = rawValue.replace(/^['"]|['"]$/g, "");

    if (!(key in process.env)) {
      process.env[key] = value;
    }
  }
}

loadDotEnv();

const PORT = Number(process.env.PORT || 8000);
const GEMINI_API_KEY = process.env.GEMINI_API_KEY || "";
const DEFAULT_GEMINI_MODEL = process.env.GEMINI_MODEL || "gemini-1.5-pro";
const DATA_DIR = path.resolve(process.cwd(), "backend", "data");
const LATEST_RESULT_FILE = path.join(DATA_DIR, "llm_priority_latest.json");

function setCors(res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET,POST,OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
}

function sendJson(res, status, payload) {
  setCors(res);
  res.statusCode = status;
  res.setHeader("Content-Type", "application/json; charset=utf-8");
  res.end(JSON.stringify(payload));
}

async function readJson(req) {
  const chunks = [];
  let size = 0;

  for await (const chunk of req) {
    size += chunk.length;
    if (size > 1_000_000) {
      throw new Error("Request body too large");
    }
    chunks.push(chunk);
  }

  const raw = Buffer.concat(chunks).toString("utf8").trim();
  if (!raw) return {};
  return JSON.parse(raw);
}

function ensureDataDir() {
  mkdirSync(DATA_DIR, { recursive: true });
}

function writeLatestJsonFile(payload) {
  ensureDataDir();
  writeFileSync(LATEST_RESULT_FILE, JSON.stringify(payload, null, 2));
}

function readLatestJsonFile() {
  if (!existsSync(LATEST_RESULT_FILE)) {
    throw new Error("No latest result file. Run POST /member4/llm-priority first.");
  }
  return JSON.parse(readFileSync(LATEST_RESULT_FILE, "utf8"));
}

function toIsoString(value) {
  if (!value) return null;
  const date = value instanceof Date ? value : new Date(value);
  if (Number.isNaN(date.getTime())) return null;
  return date.toISOString();
}

function clamp(value, min, max) {
  return Math.max(min, Math.min(max, value));
}

function scoreBand(score) {
  if (score >= 85) return "critical";
  if (score >= 70) return "high";
  if (score >= 45) return "medium";
  return "low";
}

function normalizeTasks(tasks) {
  if (!Array.isArray(tasks)) return [];

  return tasks.map((task, index) => ({
    id: String(task.id ?? `task-${index + 1}`),
    title: String(task.title ?? task.module ?? `Task ${index + 1}`),
    module: String(task.module ?? "General"),
    dueAt: toIsoString(task.dueAt),
    moduleWeightPercent: Number(task.moduleWeightPercent ?? 0),
    estimatedHours: Number(task.estimatedHours ?? 0),
    notes: String(task.notes ?? "")
  }));
}

function daysUntil(dueAt) {
  if (!dueAt) return 999;
  const now = Date.now();
  const due = new Date(dueAt).getTime();
  return Math.ceil((due - now) / (1000 * 60 * 60 * 24));
}

function heuristicPriority(tasks, tuning = {}) {
  const deadlineWeight = Number(tuning.deadlineWeight ?? 0.55);
  const moduleWeight = Number(tuning.moduleWeight ?? 0.35);
  const effortWeight = Number(tuning.effortWeight ?? 0.1);

  const total = deadlineWeight + moduleWeight + effortWeight || 1;
  const dw = deadlineWeight / total;
  const mw = moduleWeight / total;
  const ew = effortWeight / total;

  const ratedTasks = tasks
    .map((task) => {
      const daysLeft = daysUntil(task.dueAt);
      const urgency = clamp(100 - daysLeft * 9, 0, 100);
      const impact = clamp(task.moduleWeightPercent * 2.2, 0, 100);
      const effort = clamp(task.estimatedHours * 10, 0, 100);
      const priorityScore = Math.round(dw * urgency + mw * impact + ew * effort);

      return {
        id: task.id,
        title: task.title,
        module: task.module,
        dueAt: task.dueAt,
        moduleWeightPercent: task.moduleWeightPercent,
        priorityScore,
        priorityBand: scoreBand(priorityScore),
        reason: `Due in ${daysLeft} day(s), module weight ${task.moduleWeightPercent}%`
      };
    })
    .sort((a, b) => b.priorityScore - a.priorityScore);

  return {
    ratedTasks,
    summary: "Heuristic fallback used"
  };
}

function buildPrompt(tasks, llmConfig) {
  const customPrompt = String(llmConfig.customPrompt || "").trim();
  const basePrompt = customPrompt
    ? customPrompt
    : "Prioritize tasks by near due date and high module weighting. Return strict JSON.";

  return `${basePrompt}\n\nReturn JSON only:\n{\n  \"ratedTasks\": [{\n    \"id\": \"string\",\n    \"priorityScore\": 0-100,\n    \"priorityBand\": \"critical|high|medium|low\",\n    \"reason\": \"short reason\"\n  }],\n  \"summary\": \"short summary\"\n}\n\nTasks:\n${JSON.stringify(tasks, null, 2)}`;
}

function parseJsonText(value) {
  const raw = String(value || "").trim();
  const cleaned = raw
    .replace(/^```json\s*/i, "")
    .replace(/^```\s*/i, "")
    .replace(/```\s*$/i, "");
  return JSON.parse(cleaned);
}

function normalizeLlmOutput(llmOutput, tasks) {
  const byId = Object.fromEntries(tasks.map((task) => [task.id, task]));
  const rawRated = Array.isArray(llmOutput?.ratedTasks) ? llmOutput.ratedTasks : [];

  const ratedTasks = rawRated
    .map((entry) => {
      const id = String(entry.id || "");
      const task = byId[id];
      if (!task) return null;

      const priorityScore = clamp(Number(entry.priorityScore ?? 0), 0, 100);
      return {
        id: task.id,
        title: task.title,
        module: task.module,
        dueAt: task.dueAt,
        moduleWeightPercent: task.moduleWeightPercent,
        priorityScore,
        priorityBand: ["critical", "high", "medium", "low"].includes(entry.priorityBand)
          ? entry.priorityBand
          : scoreBand(priorityScore),
        reason: String(entry.reason || "Gemini rating")
      };
    })
    .filter(Boolean)
    .sort((a, b) => b.priorityScore - a.priorityScore);

  return {
    ratedTasks,
    summary: String(llmOutput?.summary || "Gemini prioritization complete")
  };
}

async function callGemini(tasks, llmConfig) {
  if (!GEMINI_API_KEY) {
    throw new Error("GEMINI_API_KEY is missing");
  }

  const model = String(llmConfig.model || DEFAULT_GEMINI_MODEL);
  const endpoint = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${encodeURIComponent(
    GEMINI_API_KEY
  )}`;

  const response = await fetch(endpoint, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      contents: [{ role: "user", parts: [{ text: buildPrompt(tasks, llmConfig) }] }],
      generationConfig: {
        temperature: Number(llmConfig.temperature ?? 0.2),
        responseMimeType: "application/json"
      }
    })
  });

  if (!response.ok) {
    throw new Error(`Gemini HTTP ${response.status}`);
  }

  const data = await response.json();
  const text = data?.candidates?.[0]?.content?.parts?.[0]?.text;
  if (!text) {
    throw new Error("Gemini response missing content");
  }

  return parseJsonText(text);
}

const server = createServer(async (req, res) => {
  const url = new URL(req.url || "/", `http://${req.headers.host}`);

  if (req.method === "OPTIONS") {
    setCors(res);
    res.statusCode = 204;
    res.end();
    return;
  }

  if (req.method === "GET" && url.pathname === "/health") {
    sendJson(res, 200, {
      ok: true,
      service: "member4-gemini-priority-api",
      hasGeminiKey: Boolean(GEMINI_API_KEY),
      latestResultFile: LATEST_RESULT_FILE
    });
    return;
  }

  if (req.method === "GET" && url.pathname === "/member4/llm-priority/file") {
    try {
      const fileData = readLatestJsonFile();
      sendJson(res, 200, fileData);
    } catch (error) {
      sendJson(res, 404, { error: error.message });
    }
    return;
  }

  if (req.method === "POST" && url.pathname === "/member4/llm-priority") {
    try {
      const body = await readJson(req);
      const llmConfig = body.llmConfig || {};
      const tasks = normalizeTasks(body.tasks);

      if (!tasks.length) {
        const emptyResult = {
          ratedTasks: [],
          summary: "No tasks received",
          provider: "gemini",
          model: String(llmConfig.model || DEFAULT_GEMINI_MODEL),
          fallback: true,
          generatedAt: new Date().toISOString(),
          filePath: LATEST_RESULT_FILE
        };
        writeLatestJsonFile(emptyResult);
        sendJson(res, 200, emptyResult);
        return;
      }

      let result;
      try {
        const raw = await callGemini(tasks, llmConfig);
        result = {
          ...normalizeLlmOutput(raw, tasks),
          provider: "gemini",
          model: String(llmConfig.model || DEFAULT_GEMINI_MODEL),
          fallback: false,
          generatedAt: new Date().toISOString(),
          filePath: LATEST_RESULT_FILE
        };
      } catch (llmError) {
        result = {
          ...heuristicPriority(tasks, llmConfig.tuning || {}),
          provider: "gemini",
          model: String(llmConfig.model || DEFAULT_GEMINI_MODEL),
          fallback: true,
          fallbackReason: llmError.message,
          generatedAt: new Date().toISOString(),
          filePath: LATEST_RESULT_FILE
        };
      }

      writeLatestJsonFile(result);
      sendJson(res, 200, result);
    } catch (error) {
      sendJson(res, 400, { error: error.message || "Invalid request" });
    }
    return;
  }

  sendJson(res, 404, { error: "Route not found" });
});

server.listen(PORT, "127.0.0.1", () => {
  console.log(`[member4-backend] listening on http://127.0.0.1:${PORT}`);
  console.log("[member4-backend] routes: GET /health, GET /member4/llm-priority/file, POST /member4/llm-priority");
  console.log(`[member4-backend] latest result json: ${LATEST_RESULT_FILE}`);
});
