# HackLondon Idea

AI as a study partner 

[INITIAL](https://www.notion.so/INITIAL-30e14f0e855c80609e44fde1c2152f86?pvs=21)

# 🇬🇧 Project: Beacon — The Adaptive Student OS (UK Edition)

**Tagline:** The AI Chief-of-Staff for the UK Student. From Moodle to Graduate Schemes.

## 🔴 The Problem: The "UK Degree" Pressure Cooker

- **The Moodle Maze:** UK universities (UCL, KCL, Manchester, etc.) use Moodle as a dumping ground for "Essential Reading" and modular assessments that are hard to track.
- **The Graduate Scheme Sprint:** UK internship and "Grad Scheme" windows (HSBC, BBC, Civil Service) are notoriously early and rigid. Students miss out simply because they are buried in coursework.
- **Mental Health Crisis:** 1 in 3 UK students disclose mental health conditions. Rigid "to-do lists" contribute to burnout rather than solving it.
- **The "Human-in-the-Loop" Policy:** UK universities now have strict "AI Guidance" (Russell Group principles). Students need tools that help them *think*, not just tools that *write* for them.

## 🟢 The Solution

Beacon is a **biometric-aware OS** that synchronizes your UK academic life with the national career calendar. It uses the **Socratic Mirror** to act as a "tutor" that complies with UK academic integrity standards by fostering genuine understanding.

---

## 🛠 The UK-Specific Pillars

### 1. The "Grad Scheme" CRM (Career & Career)

- **Bright Network & TargetJobs Integration:** Beacon auto-syncs with major UK internship deadlines. If an **HSBC Summer Internship** closes on Feb 22nd, Beacon moves your LeetCode prep for that role to the top of your feed.
- **UCAS to CV Bridge:** For first-years, Aura helps translate A-Level achievements into a first-year "Spring Week" ready CV.

### 2. The Socratic Mirror (Russell Group Compliant Learning)

- **Feynman-Based Active Recall:** Instead of summarizing a lecture, Aura asks you to explain the **"Three-Lens Framework"** or specific UK case laws.
- **Viva Voce Prep:** In the UK, high-level understanding is tested via discussion. Aura’s **ElevenLabs** voice acts as a mock "Viva" examiner, prepping you for the British style of academic defense.

### 3. Biometric Well-Tech (The "Student Minds" Layer)

- **Presage SDK for Duty of Care:** Aura aligns with the **University Mental Health Charter**.
    - **Focus High:** It suggests a 2-hour "Deep Work" block on your dissertation.
    - **Stress High (Detected via Webcam):** Aura suggests a walk to the nearest park or a "Low-Stakes" task, like updating your LinkedIn.

---

## 🏆 Sponsor Prize Strategy (UK Focus)

- **Gemini:** For UK-specific curriculum alignment (e.g., matching tasks to the **QAA Higher Education Framework**).
- **ElevenLabs:** Using a "British Professional" voice (e.g., 'Brian' or 'Alice') to make the personal assistant feel localized.
- **MongoDB Atlas:** Managing the "UK Knowledge Graph"—linking UK university modules to London/Manchester-based job opportunities.
- **Vultr:** Localized hosting in London/Manchester data centers for ultra-low latency during live demos.

---

## 🎯 The "Wow" Demo Moment

1. **The London Briefing:** Aura (in a calm British accent): *"Good morning. You have a coursework deadline for 'Macroeconomics' at 4 PM. I noticed you’ve been scrolling LinkedIn—I've blocked it until you finish your Socratic check on the Bank of England's latest report."*
2. **The Career Hook:** Drag a **BBC Graduate Scheme** posting into Aura. It instantly analyzes your Moodle module list and says: *"You’re a 85% match based on your 'Digital Media' module, but you need to practice 2 more Python patterns for the technical test."*

---

## 💻 Tech Stack (The UK Stack)

- **Frontend:** React + Tailwind (Clean, minimalist "British" design).
- **Backend:** FastAPI hosted on **Vultr (London Region)**.
- **Scraping:** **Playwright** specifically tuned for UK University SSO (Single Sign-On).
- **Intelligence:** **Gemini 1.5 Pro** + **ElevenLabs** (British English voices).

---

### ✅ UK-Specific MVP Checklist

- [ ]  **SSO Handshake:** Ensure your Playwright script can handle a standard UK University "Microsoft/Okta" login.
- [ ]  **Bright Network Scraper:** A simple script to pull "Top 5 Deadlines" from UK career sites.
- [ ]  **Socratic "Viva" Mode:** Prompt Gemini to act like a UK University Don—academic, rigorous, but encouraging.

---

### 👥 The Roles (The Strike Team)

- **Member 1: The "Intelligence" Lead (Gemini & ElevenLabs)**
    - **Focus:** API Orchestration & Prompt Engineering.
    - **Goal:** Ensure the AI actually sounds like a Socratic tutor and correctly chunks messy data.
- **Member 2: The "Infrastructure" Lead (Backend & Vultr)**
    - **Focus:** FastAPI/Node, MongoDB Atlas, and Deployment.
    - **Goal:** Create the "Plumbing" so data actually saves and the frontend has a URL to talk to.
- **Member 3: The "Experience" Lead (Frontend)**
    - **Focus:** React, Tailwind CSS, and Biometrics.
    - **Goal:** Build the "Cyber-Academic"
- **Member 4: The "Data" Lead (Moodle & Career Scraping)**
    - **Focus:** Playwright/Scraping and Data Cleaning.
    - **Goal:** Be the "Pipe." Feed real (or high-quality mock) data into the system.

---

### ⏱️ The Sprint Schedule

### **Phase 1: The "Great Connection" (First 3 Hours)**

- **Member 1:** Draft the **Socratic System Prompt** in the Google AI Studio. Test it with complex topics.
- **Member 2:** Spin up the **Vultr** instance and connect **MongoDB Atlas**. Create the `/tasks` and `/user-state` endpoints.
- **Member 3:** Scaffold the React app with a dark-mode theme. Integrate the **Presage SDK** camera feed component.
- **Member 4:** Use **Playwright** to log into a Moodle test account. Capture the HTML of the "Upcoming Events" or "Grades" page.

### **Phase 2: The "Deep Integration" (Hours 3–8)**

- **Member 1:** Connect **ElevenLabs**. Write a function that takes Gemini’s response and converts it to a "British Professional" voice stream.
- **Member 2:** Build the **"State-Aware" logic**: An endpoint that takes the Presage "Stress Score" and re-sorts the MongoDB task list.
- **Member 3:** Build the **Socratic Mirror UI** (a clean chat interface with a "Pulse" animation that syncs with the user's focus levels).
- **Member 4:** Build the **Career Scraper** (or a JSON injector) for LeetCode stats and Bright Network deadlines. Map these to the MongoDB schema.

### **Phase 3: The "Polish & Pitch" (Hours 8–End)**

- **Member 1 & 2:** Squash bugs in the Gemini-ElevenLabs loop (latency is the enemy!).
- **Member 3:** Add "Wow" factors: Framer Motion animations, "Stress Alerts," and a sleek "Daily Briefing" modal.
- **Member 4:** Prepare the **Demo Data**. If scraping is flaky, hardcode a "Golden Path" for the demo that looks real (e.g., using your actual university modules).

---

### 🛠️ The "Aura" Task Checklist (By Owner)

| **Owner** | **Task** | **Tech** |
| --- | --- | --- |
| **Intel** | Create "Feynman Mode" prompt for Socratic learning. | Gemini Pro |
| **Intel** | Map ElevenLabs voices to different "Aura" moods. | ElevenLabs |
| **Infra** | Set up **Vector Search** in MongoDB for the Socratic Mirror. | MongoDB Atlas |
| **Infra** | Deploy the backend on Vultr with SSL. | Vultr / Nginx |
| **UX** | Implement "State-Driven" UI (colors change based on stress). | React / Tailwind |
| **UX** | Integrate Presage SDK and map 0-1 scores to "UI Intensity." | Presage SDK |
| **Data** | Scrape Moodle "Assignment Brief" PDFs. | Playwright |
| **Data** | Create a "Job Description" parser for the career gap feature. | Gemini / Regex |

---

### 💡 Pro-Tip for the Team

**The "10-Minute Rule":** If any member is stuck on a bug (especially Moodle login or SDK issues) for more than 10 minutes, **pivot to a hardcoded mock.** At a hackathon, a working "fake" feature is worth 100x more than a broken "real" one.

**Would you like me to generate the "Golden Path" script for your demo so the team knows exactly what to show the judges?**