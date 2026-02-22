import React from "react";
import TaskCard from "../../../shared/components/TaskCard";
import useMember4ViewModel from "../viewmodels/useMember4ViewModel";

export default function Member4Dashboard() {
  const vm = useMember4ViewModel();

  return (
    <section className="dashboard">
      <div className="stack">
        <section className="panel">
          <h2>Runner Config</h2>
          <label htmlFor="apiBaseUrl">Backend API Base URL (optional)</label>
          <input
            id="apiBaseUrl"
            type="text"
            placeholder="http://localhost:8010"
            value={vm.apiBaseUrl}
            onChange={(event) => vm.setApiBaseUrl(event.target.value)}
          />
          <p className="small">
            If URL is empty or endpoint fails, the UI auto-falls back to mock mode.
          </p>

          <div className="row" style={{ marginTop: 10 }}>
            <button type="button" className="primary" onClick={vm.loadData}>
              Load Data
            </button>
            <button type="button" className="secondary" onClick={vm.loadJobs}>
              Load Jobs
            </button>
          </div>

          <div className="row" style={{ marginTop: 10 }}>
            <div>
              <label htmlFor="jobKeywords">Job Keywords</label>
              <input
                id="jobKeywords"
                type="text"
                placeholder="software engineer"
                value={vm.jobKeywords}
                onChange={(event) => vm.setJobKeywords(event.target.value)}
              />
            </div>
            <div>
              <label htmlFor="jobLimit">Job Limit</label>
              <input
                id="jobLimit"
                type="number"
                min="1"
                max="20"
                value={vm.jobLimit}
                onChange={(event) => vm.setJobLimit(event.target.value)}
              />
            </div>
          </div>

          <div style={{ marginTop: 8 }}>
            <label htmlFor="jobLocation">Job Location</label>
            <input
              id="jobLocation"
              type="text"
              placeholder="Toronto"
              value={vm.jobLocation}
              onChange={(event) => vm.setJobLocation(event.target.value)}
            />
          </div>

          <div style={{ marginTop: 12 }}>
            <label htmlFor="moodleHtml">Moodle HTML (optional raw input)</label>
            <textarea
              id="moodleHtml"
              placeholder="Paste captured Moodle HTML here"
              value={vm.moodleHtml}
              onChange={(event) => vm.setMoodleHtml(event.target.value)}
            />
          </div>

          <div style={{ marginTop: 12 }}>
            <label htmlFor="careerJson">Career JSON Inject (optional)</label>
            <textarea
              id="careerJson"
              placeholder='[{"company":"HSBC","role":"Summer Internship"}]'
              value={vm.injectedCareerJson}
              onChange={(event) => vm.setInjectedCareerJson(event.target.value)}
            />
          </div>

          <div style={{ marginTop: 12 }}>
            <label htmlFor="moduleWeightsJson">Module Weighting JSON (%)</label>
            <textarea
              id="moduleWeightsJson"
              placeholder='{"Business Essay": 40, "Math": 20}'
              value={vm.moduleWeightsJson}
              onChange={(event) => vm.setModuleWeightsJson(event.target.value)}
            />
          </div>

          <h3 style={{ marginTop: 16 }}>LLM Tuning</h3>
          <p className="small">
            Gemini-only tuning. Adjust these to change priority behavior without changing code.
          </p>

          <div className="row" style={{ marginTop: 8 }}>
            <div>
              <label>LLM Provider</label>
              <input type="text" value="Google Gemini" disabled />
            </div>
            <div>
              <label htmlFor="llmTemperature">Temperature</label>
              <input
                id="llmTemperature"
                type="number"
                min="0"
                max="1"
                step="0.05"
                value={vm.llmTemperature}
                onChange={(event) => vm.setLlmTemperature(event.target.value)}
              />
            </div>
          </div>

          <div style={{ marginTop: 8 }}>
            <label htmlFor="llmModel">Model</label>
            <input
              id="llmModel"
              type="text"
              placeholder="gemini-1.5-pro"
              value={vm.llmModel}
              onChange={(event) => vm.setLlmModel(event.target.value)}
            />
          </div>

          <div style={{ marginTop: 8 }}>
            <label htmlFor="llmApiKey">Gemini API Key (optional, direct mode only)</label>
            <input
              id="llmApiKey"
              type="password"
              placeholder="Gemini API key"
              value={vm.llmApiKey}
              onChange={(event) => vm.setLlmApiKey(event.target.value)}
            />
          </div>

          <div style={{ marginTop: 8, display: "flex", gap: 8, alignItems: "center" }}>
            <input
              id="allowDirectApi"
              type="checkbox"
              checked={vm.allowDirectApi}
              onChange={(event) => vm.setAllowDirectApi(event.target.checked)}
              style={{ width: "auto" }}
            />
            <label htmlFor="allowDirectApi" style={{ margin: 0 }}>
              Allow direct Gemini API calls from browser
            </label>
          </div>

          <div className="small" style={{ marginTop: 4 }}>
            Use backend proxy in production. Browser direct mode exposes your key to client-side code.
          </div>

          <div style={{ marginTop: 8 }}>
            <label htmlFor="llmPrompt">Custom Priority Prompt</label>
            <textarea
              id="llmPrompt"
              placeholder="Describe exactly how priority should be ranked..."
              value={vm.llmCustomPrompt}
              onChange={(event) => vm.setLlmCustomPrompt(event.target.value)}
            />
          </div>

          <div className="row" style={{ marginTop: 8 }}>
            <div>
              <label htmlFor="deadlineWeight">Deadline Weight</label>
              <input
                id="deadlineWeight"
                type="number"
                min="0"
                max="1"
                step="0.05"
                value={vm.deadlineWeight}
                onChange={(event) => vm.setDeadlineWeight(event.target.value)}
              />
            </div>
            <div>
              <label htmlFor="moduleWeight">Module Weight</label>
              <input
                id="moduleWeight"
                type="number"
                min="0"
                max="1"
                step="0.05"
                value={vm.moduleWeight}
                onChange={(event) => vm.setModuleWeight(event.target.value)}
              />
            </div>
          </div>

          <div style={{ marginTop: 8 }}>
            <label htmlFor="effortWeight">Effort Weight</label>
            <input
              id="effortWeight"
              type="number"
              min="0"
              max="1"
              step="0.05"
              value={vm.effortWeight}
              onChange={(event) => vm.setEffortWeight(event.target.value)}
            />
          </div>
        </section>

        <section className="panel">
          <div className="row" style={{ marginBottom: 8 }}>
            <div>
              <h2 style={{ marginBottom: 6 }}>Member 4 Tasks</h2>
              <p className="small">Progress: {vm.overallProgress}%</p>
            </div>
            <button type="button" className="secondary" onClick={vm.resetAll}>
              Reset
            </button>
          </div>

          <div className="stack">
            {vm.tasks.map((task) => (
              <TaskCard
                key={task.id}
                title={task.title}
                description={task.description}
                state={vm.taskState[task.id]}
                onRun={() => vm.runTask(task.id)}
              />
            ))}
          </div>
        </section>
      </div>

      <aside className="stack">
        <section className="panel">
          <h3>Live Data Snapshot</h3>
          <p className="small">Last outputs from each run step.</p>
          <div className="log-box">
            <pre className="log-line">{JSON.stringify(vm.dataStore, null, 2)}</pre>
          </div>
        </section>

        <section className="panel">
          <h3>Run Log</h3>
          <div className="log-box">
            {vm.logs.map((line, index) => (
              <p className="log-line" key={`${line}-${index}`}>
                {line}
              </p>
            ))}
          </div>
        </section>
      </aside>
    </section>
  );
}
