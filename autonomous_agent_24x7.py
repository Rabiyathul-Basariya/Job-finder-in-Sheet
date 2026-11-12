"""
24/7 Autonomous Job Search, Dynamic Resume Tailoring, & Cold Outreach Agent
Candidate: Rabiyathul Basariya B
Target Roles: Associate Product Manager (APM), Product Manager (PM), Business Analyst (BA)
Locations: Bengaluru / Remote
"""

import os
import re
import csv
import json
import time
import urllib.request
import urllib.parse
from datetime import datetime, timedelta
from collections import Counter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROFILE_PATH = os.path.join(BASE_DIR, "profile_data.json")
TRACKER_CSV_PATH = os.path.join(BASE_DIR, "job_applications_tracker.csv")
SEEN_JOBS_PATH = os.path.join(BASE_DIR, "seen_jobs.json")
RESUMES_DIR = os.path.join(BASE_DIR, "tailored_resumes")
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbyW28NHdIVKTuUjWHWg-3VG7iUzjxsnL6QKCZ8AuH1Kr9C1IPUXX3B5Uyjt5B7mJWFP5Q/exec"

os.makedirs(RESUMES_DIR, exist_ok=True)

TARGET_ROLES_KEYWORDS = [
    "product manager", "associate product manager", "apm", 
    "business analyst", "product analyst", "technical product manager"
]

TARGET_LOCATIONS = [
    "bengaluru", "bangalore", "remote", "anywhere", "india", "hybrid"
]

MONITORED_COMPANIES = [
    {"name": "LatentForce", "type": "startup", "domain": "latentforce.ai", "funding": "Seed ($1.7M)", "contact": "Founding Team", "email": "founders@latentforce.ai"},
    {"name": "OnFinance AI", "type": "startup", "domain": "onfinance.ai", "funding": "Seed / Pre-Series A", "contact": "Kunal & Priyesh", "email": "careers@onfinance.ai"},
    {"name": "LimeChat", "type": "startup", "domain": "limechat.ai", "funding": "Series A ($4.5M)", "contact": "Nikhil Gupta", "email": "nikhil@limechat.ai"},
    {"name": "Sprinto", "type": "startup", "domain": "sprinto.com", "funding": "Series B ($20M)", "contact": "Girish Redekar", "email": "girish@sprinto.com"},
    {"name": "Atlan", "type": "startup", "domain": "atlan.com", "funding": "Series C ($105M)", "contact": "Prukalpa Sankar", "email": "prukalpa@atlan.com"},
    {"name": "Immunito AI", "type": "startup", "domain": "immunitoai.com", "funding": "Pre-Series A", "contact": "Arpit Khemka", "email": "arpit@immunitoai.com"},
    {"name": "Instawork", "type": "greenhouse", "slug": "instawork", "contact": "Talent Team", "email": "careers@instawork.com"},
    {"name": "Stripe", "type": "greenhouse", "slug": "stripe", "contact": "Hiring Team", "email": "recruiting@stripe.com"}
]

def load_json(filepath, default):
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return default
    return default

def save_json(filepath, data):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def fetch_greenhouse_jobs(slug):
    url = f"https://api.greenhouse.io/v1/boards/{slug}/jobs?content=true"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("jobs", [])
    except Exception as e:
        print(f"[CRAWLER] Greenhouse fetch failed for {slug}: {e}")
        return []

def is_matching_job(title, location_name):
    t_lower = title.lower()
    loc_lower = location_name.lower()
    
    role_match = any(rk in t_lower for rk in TARGET_ROLES_KEYWORDS)
    loc_match = any(loc in loc_lower for loc in TARGET_LOCATIONS)
    return role_match and loc_match

def extract_ats_keywords(text):
    text_lower = text.lower()
    keywords = [
        "prd", "prds", "user stories", "roadmap", "agile", "scrum", "jira", "sprint planning",
        "backlog", "kpi", "kpis", "a/b testing", "user research", "user interviews",
        "figma", "sql", "mixpanel", "analytics", "data analysis", "stakeholder management",
        "0-to-1", "llm", "llms", "generative ai", "ai agents", "agentic workflows", "rag",
        "apis", "customer journey", "retention", "b2b", "saas", "healthcare", "fintech"
    ]
    found = [kw for kw in keywords if kw in text_lower]
    return list(set(found))

def generate_tailored_resume_file(company_name, job_title, jd_text, profile):
    matched_kw = extract_ats_keywords(jd_text)
    kw_str = ", ".join(matched_kw[:8]) if matched_kw else "PRDs, SQL, Agile, AI Workflows"
    
    tailored_text = f"""================================================================================
RABIYATHUL BASARIYA B
+91 6379946980 | rabiya1828@gmail.com | Bengaluru, India (Open to Remote)
Target Role: {job_title} at {company_name}
Target Keywords Matched: {kw_str}
================================================================================

PROFESSIONAL SUMMARY
Product Analyst with 3 years of experience driving 0-to-1 product discovery, 
requirement specs (PRDs), and metric-driven execution. Proven track record in 
leveraging SQL, user analytics, and Agentic AI workflows to optimize funnels 
(boosted IVR visits by 20% in 6 months at SBNA) and cluster 8,000+ customer reviews 
using Gemini LLMs. Tailored for high-impact execution as {job_title} at {company_name}.

CORE COMPETENCIES & KEYWORDS
• Product: PRDs, User Stories, Roadmapping, Backlog Grooming, Jira, Agile/Scrum, A/B Testing
• AI & Analytics: Agentic AI, Multi-Agent Systems, Gemini LLMs, SQL, Mixpanel, Prompt Engineering
• Business Analysis: Requirements Gathering, KPI Dashboards, User Journeys, Process Mapping

PROFESSIONAL EXPERIENCE
Business Analyst – SBNA Software Solution (07/2024 – Present)
• Led end-to-end SDLC of a Healthcare claims processing web application across requirements, workflows, and release cycles.
• Lifted IVR visits by 20% within 6 months by analyzing 2 years of user behavioral data to eliminate friction drop-offs.
• Authored comprehensive PRDs, Jira epics, user stories, and acceptance criteria; led cross-functional sprint planning.
• Designed executive dashboards, tracked product KPIs, and conducted live client demos and pre-sales presentations.

Market Research Executive – Apple Holidays (11/2022 – 05/2023)
• Managed B2B client relationships, analyzed customer preference data, and supported product promotion initiatives.

NOTABLE AI & PRODUCT PROJECTS
1. Voice of Customer Copilot (AI/LLM Project)
   - Built an LLM pipeline clustering 8,000+ Play Store reviews (Swiggy, IRCTC, PhonePe) using Python + Gemini Flash Lite.
2. Order Status Agent (Customer Support Agent)
   - Built a multi-agent order tracking bot with ambiguity resolution, failure-mode mapping, and latency benchmarking.
3. E-commerce Platform - Reducing Returns (Product Case Study)
   - Conducted 25+ user interviews & 100+ surveys to reduce post-order friction and RTO drop-offs.
4. Hydra Desk (0-to-1 Productivity App)
   - Shipped Windows app end-to-end; organic user adoption.

EDUCATION & CERTIFICATIONS
• MBA – Business Analytics & Marketing (CGPA 9.03), Anna University (2023 – 2025)
• B.Com with Computer Application, Lady Doak College (2018 – 2021)
• Certifications: IBM Prompt Engineering, Google AI Essentials, Intro to LLMs, AI for Product Management
================================================================================
"""
    clean_name = re.sub(r'[^a-zA-Z0-9_]', '_', company_name)
    clean_role = re.sub(r'[^a-zA-Z0-9_]', '_', job_title)
    resume_path = os.path.join(RESUMES_DIR, f"Tailored_Resume_{clean_name}_{clean_role}.txt")
    with open(resume_path, "w", encoding="utf-8") as f:
        f.write(tailored_text)
    return resume_path, kw_str

def generate_cold_outreach(company, role, contact_name, funding_or_stage, kw_str, profile):
    first_name = contact_name.split()[0]
    subject = f"Building 0-to-1 Product at {company} | Intro from Rabiyathul ({role})"
    body = f"""Hi {first_name},

I have been following {company}'s impressive growth in {funding_or_stage}. Given your product roadmap, you likely need a product builder who can own user discovery, PRDs, and sprint execution from Day 1 without handholding.

What I bring:
1. 0-to-1 Product Execution: Currently driving product requirements & SDLC for a healthcare claims web app at SBNA, where I boosted IVR visits by 20% in 6 months through user flow optimization.
2. Hands-on AI Agent Building: Built a 'Voice of Customer Copilot' (clustered 8,000+ reviews with Gemini LLMs) and an 'Order Status Agent' with automated fallback/escalation logic.
3. Data & Specs Rigor: Expert in PRDs, Jira backlog prioritization, SQL, and user interviews.

I have tailored my resume specifically for {company} (attached/linked) and would love to support your product delivery as an {role} (Bengaluru / Remote).

Open to a brief 10-minute chat this week?

Best regards,
Rabiyathul Basariya B
+91 6379946980 | rabiya1828@gmail.com
"""

    followup = f"""Hi {first_name},

Circling back on my note from earlier this week. I know you are super busy scaling {company}.

I put together a quick breakdown of how I approached reducing user drop-offs and designing AI escalation logic in my recent projects:
• 20% IVR metric lift in 6 months
• 8,000+ reviews sentiment clustering using Gemini Flash Lite
• 25+ deep user interviews on post-purchase friction

Would love to share these notes if an {role} profile fits your roadmap. Let me know if a quick 10-min chat next week works.

Best,
Rabiyathul Basariya B
+91 6379946980
"""
    return subject, body, followup

def push_to_google_sheet(payload):
    try:
        data_bytes = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            WEB_APP_URL,
            data=data_bytes,
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status == 200
    except Exception as e:
        print(f"[SHEET SYNC] Error pushing to Google Sheet: {e}")
        return False

def append_to_local_tracker(row):
    file_exists = os.path.exists(TRACKER_CSV_PATH)
    headers = [
        "Company Name", "Role Title", "Location", "Funding / Company Stage",
        "Target Contact Person", "Contact Email / Profile", "Outreach Email Subject",
        "Tailored Cold Pitch", "Follow-up Template", "Resume Focus & Match Score",
        "Application Status", "Date Contacted", "Follow-up Due Date", "Notes"
    ]
    with open(TRACKER_CSV_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)

def process_single_opportunity(opp, profile, seen_jobs):
    job_id = f"{opp['company']}_{opp['role']}"
    if job_id in seen_jobs:
        return False

    print(f"\n[NEW JOB FOUND] {opp['company']} - {opp['role']} ({opp['location']})")
    
    # 1. Dynamically tailor resume
    resume_path, kw_str = generate_tailored_resume_file(
        opp['company'], opp['role'], opp.get('description', opp['role']), profile
    )
    print(f"[RESUME TAILORED] Saved tailored resume: {os.path.basename(resume_path)}")

    # 2. Generate personalized cold outreach
    subject, body, followup = generate_cold_outreach(
        opp['company'], opp['role'], opp['contact_person'], opp['stage'], kw_str, profile
    )

    today_str = datetime.now().strftime("%Y-%m-%d")
    followup_date = (datetime.now() + timedelta(days=4)).strftime("%Y-%m-%d")

    # 3. Append to local CSV
    row = {
        "Company Name": opp["company"],
        "Role Title": opp["role"],
        "Location": opp["location"],
        "Funding / Company Stage": opp["stage"],
        "Target Contact Person": opp["contact_person"],
        "Contact Email / Profile": opp["contact_email"],
        "Outreach Email Subject": subject,
        "Tailored Cold Pitch": body,
        "Follow-up Template": followup,
        "Resume Focus & Match Score": f"Keywords: {kw_str}",
        "Application Status": "Ready to Send",
        "Date Contacted": today_str,
        "Follow-up Due Date": followup_date,
        "Notes": f"Apply URL: {opp.get('apply_url', 'Direct Outreach')} | Tailored Resume: {os.path.basename(resume_path)}"
    }
    append_to_local_tracker(row)

    # 4. Push to Google Sheet
    sheet_payload = {
        "company": opp["company"],
        "role": opp["role"],
        "location": opp["location"],
        "funding": opp["stage"],
        "contact_person": opp["contact_person"],
        "email": opp["contact_email"],
        "subject": subject,
        "pitch": body,
        "followup": followup,
        "ats_match": kw_str,
        "notes": row["Notes"]
    }
    pushed = push_to_google_sheet(sheet_payload)
    if pushed:
        print(f"[GOOGLE SHEET] Successfully synced {opp['company']} to live Google Sheet!")

    # 4b. Push Alert to Telegram Bot
    try:
        from telegram_job_notifier import send_telegram_message, load_config
        tg_cfg = load_config()
        for cid in tg_cfg.get("chat_ids", []):
            alert = (
                f"⚡ <b>New Opportunity Added to Tracker!</b>\n"
                f"🏢 <b>{opp['company']}</b> — {opp['role']}\n"
                f"📍 {opp['location']} | <i>{opp['stage']}</i>\n"
                f"👤 {opp['contact_person']} (<code>{opp['contact_email']}</code>)\n"
                f"📄 Resume Tailored: <code>{os.path.basename(resume_path)}</code>\n"
                f"⚠️ Status: Ready to Send"
            )
            send_telegram_message(cid, alert)
    except Exception as e:
        pass

    # 5. Mark as seen
    seen_jobs[job_id] = {
        "discovered_at": today_str,
        "company": opp["company"],
        "role": opp["role"],
        "tailored_resume": resume_path
    }
    save_json(SEEN_JOBS_PATH, seen_jobs)
    return True

def run_crawler_cycle(profile, seen_jobs):
    print(f"\n--- [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Running Autonomous Scan Cycle ---")
    new_jobs_count = 0

    for comp in MONITORED_COMPANIES:
        if comp["type"] == "startup":
            # Target startup pipeline
            opp = {
                "company": comp["name"],
                "role": "Associate Product Manager / Product Analyst",
                "location": "Bengaluru / Remote",
                "stage": comp.get("funding", "High Growth Tech"),
                "contact_person": comp["contact"],
                "contact_email": comp["email"],
                "apply_url": f"https://{comp.get('domain', comp['name'])}",
                "description": "PRD SQL Agile Jira LLM AI agents metrics"
            }
            if process_single_opportunity(opp, profile, seen_jobs):
                new_jobs_count += 1

        elif comp["type"] == "greenhouse":
            # Live Greenhouse Career Portal
            jobs = fetch_greenhouse_jobs(comp["slug"])
            for j in jobs:
                title = j.get("title", "")
                loc = j.get("location", {}).get("name", "")
                if is_matching_job(title, loc):
                    opp = {
                        "company": comp["name"],
                        "role": title,
                        "location": loc,
                        "stage": "Enterprise ATS Portal",
                        "contact_person": comp["contact"],
                        "contact_email": comp["email"],
                        "apply_url": j.get("absolute_url", ""),
                        "description": j.get("content", title)
                    }
                    if process_single_opportunity(opp, profile, seen_jobs):
                        new_jobs_count += 1

    print(f"[CYCLE COMPLETE] New opportunities processed & synced: {new_jobs_count}")

def main_loop(poll_interval_seconds=1800):
    """
    Runs 24/7 background agent with continuous monitoring.
    Default interval: 1800 seconds (30 minutes).
    """
    print("=" * 70)
    print("AUTONOMOUS 24/7 JOB HUNTER & TAILORING ENGINE ACTIVATED")
    print(f"Monitoring APM / PM / BA roles across Bengaluru & Remote")
    print(f"Poll Interval: {poll_interval_seconds} seconds")
    print("=" * 70)

    profile = load_json(PROFILE_PATH, {})
    seen_jobs = load_json(SEEN_JOBS_PATH, {})

    while True:
        try:
            run_crawler_cycle(profile, seen_jobs)
        except Exception as e:
            print(f"[ERROR IN CYCLE] {e}")
        
        print(f"\n[SLEEPING] Next scan in {poll_interval_seconds // 60} minutes... (Press Ctrl+C to pause)")
        time.sleep(poll_interval_seconds)

if __name__ == "__main__":
    import sys
    # If run with --once, execute one cycle and exit. Otherwise run 24/7 loop.
    if "--once" in sys.argv:
        profile = load_json(PROFILE_PATH, {})
        seen_jobs = load_json(SEEN_JOBS_PATH, {})
        run_crawler_cycle(profile, seen_jobs)
    else:
        main_loop(poll_interval_seconds=1800)
