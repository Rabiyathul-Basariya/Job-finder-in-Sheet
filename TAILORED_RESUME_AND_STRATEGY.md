# 🚀 Autonomous Job Search & Application Playbook
**Prepared for:** Rabiyathul Basariya B  
**Target Roles:** Associate Product Manager (APM), Product Manager (PM), Business Analyst (BA)  
**Target Locations:** Bengaluru & Remote  
**Google Sheet Tracker:** [Job Tracker Spreadsheet](https://docs.google.com/spreadsheets/d/1XgQzSxVp8cXJDbwrrSXTDWOj5xqoHXvLv5xZZQ1Hkmk/edit?usp=sharing)  
**Master Resume:** [Google Drive Link](https://drive.google.com/file/d/1Zs6AJ0WCynOYDBA_cxV5TSv_n6MxaT5y/view?usp=sharing)

---

## 1. Profile Analysis & Competitive Edge
Based on your resume, you have a standout combination that 90% of junior PM applicants lack:
1. **Hands-on AI/LLM Implementation**: You haven't just read about AI; you built real agent workflows (*Order Status Agent* with fallback/escalation logic and *Voice of Customer Copilot* clustering 8,000+ reviews using Gemini Flash Lite).
2. **Quantifiable Product Metrics**: You lifted IVR adoption by **20% within 6 months** at SBNA Software Solution by digging into 2 years of user behavioral data.
3. **Execution Rigor (SDLC)**: Full ownership of PRDs, Jira backlog prioritization, sprint planning, and user stories.
4. **Strong Academic Pedigree**: MBA in Business Analytics & Marketing with **CGPA 9.03** from Anna University.

---

## 2. Automated System Files in Your Workspace

| File | Purpose |
| :--- | :--- |
| `profile_data.json` | Structured master profile with all your projects, metrics, and skills. |
| `job_hunter_automation.py` | Python engine for ATS keyword optimization, hidden role discovery, and outreach generator. |
| `job_applications_tracker.csv` | Initialized tracker with 6 high-growth, newly funded Bengaluru startups + ready cold emails. |
| `sync_to_google_sheets.js` | One-click Google Apps Script to format your Google Sheet and auto-generate Gmail drafts. |

---

## 3. How to Sync to Your Google Sheet in 60 Seconds

1. Open your [Google Sheet](https://docs.google.com/spreadsheets/d/1XgQzSxVp8cXJDbwrrSXTDWOj5xqoHXvLv5xZZQ1Hkmk/edit).
2. Click **Extensions** > **Apps Script**.
3. Delete any boilerplate text and paste the contents of `sync_to_google_sheets.js`.
4. Click **Save** (disk icon) and close the tab.
5. Refresh your Google Sheet.
6. A new menu **"🚀 Job Hunter Hub"** will appear in the top bar.
7. Click **"1. Populate Curated Startups & Format Sheet"** (grant authorization once when prompted).
8. The sheet will instantly format with professional headers, column widths, dropdowns, and 6 active leads!
9. (Optional) Clicking **"3. Send Outreach Email Drafts via Gmail"** will automatically create draft emails in your Gmail inbox for your review before sending!

---

## 4. How to Use the Python Tool for Any New Job

Open your terminal in `c:\Users\rabiy\OneDrive\Documents\Downloads\Test`:

### A. Tailor Your Resume for Any Job Description
```bash
python job_hunter_automation.py --tailor --company "Company Name" --role "Associate Product Manager" --jd "paste job description text here"
```
*This will immediately output:*
- ATS Keyword Match percentage.
- Missing high-frequency keywords you must add.
- A customized 3-sentence summary highlighting your exact matching projects.
- Ready-to-paste impact bullet points.

---

## 5. Curated Newly Funded Bengaluru Startups (Hidden Role Pipeline)

These startups recently raised Seed / Series A/B funding and are actively expanding their product suites:

1. **LatentForce (Enterprise Agentic AI)**
   - *Stage:* $1.7M Seed (Dec 2025/2026, Ideaspring & Yali Capital)
   - *Target:* APM / Product Analyst
   - *Contact:* `founders@latentforce.ai`
   - *Angle:* Your Gemini LLM clustering and AI agent latency evaluation match their core SLM platform.

2. **LimeChat (Conversational AI & Commerce)**
   - *Stage:* $4.5M Series A (Stellaris & pi Ventures)
   - *Target:* APM / Product Analyst
   - *Contact:* Nikhil Gupta (`nikhil@limechat.ai`)
   - *Angle:* Your *Order Status Agent* demo and *E-Commerce Return Reduction* study are direct proof-of-work.

3. **OnFinance AI (FinTech / Compliance AI Agents)**
   - *Stage:* Seed / Pre-Series A
   - *Target:* Product Manager / APM
   - *Contact:* `careers@onfinance.ai`
   - *Angle:* Your escalation logic and failure-mode mapping for AI agents.

4. **Sprinto (B2B SaaS / Infosec Compliance)**
   - *Stage:* $20M Series B (Accel, Elevation)
   - *Target:* Business Analyst / APM
   - *Contact:* Girish Redekar (`girish@sprinto.com`)
   - *Angle:* Strong PRD, SDLC, and Jira sprint management in fast-scaling B2B SaaS.

5. **Atlan (Active Metadata & Data Governance)**
   - *Stage:* $105M Series C (GIC, Insight Partners)
   - *Target:* APM / Product Analyst
   - *Contact:* Prukalpa Sankar (`prukalpa@atlan.com`)
   - *Angle:* SQL data fluency, analytics dashboards, and 8,000+ review analysis.

6. **Immunito AI (HealthTech / AI Biology)**
   - *Stage:* Pre-Series A / Series A (pi Ventures)
   - *Target:* Business Analyst / Product Specialist
   - *Contact:* Arpit Khemka (`arpit@immunitoai.com`)
   - *Angle:* Direct domain synergy with your healthcare claims processing web app at SBNA.
