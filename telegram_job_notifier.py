"""
Telegram 9:00 AM Job Outreach & Follow-up Reporting Bot
Bot: @rabi_job_bot (https://t.me/rabi_job_bot)
Candidate: Rabiyathul Basariya B
"""

import os
import csv
import json
import time
import urllib.request
import urllib.parse
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TRACKER_CSV_PATH = os.path.join(BASE_DIR, "job_applications_tracker.csv")
CONFIG_PATH = os.path.join(BASE_DIR, "telegram_config.json")
DEFAULT_TOKEN = "9238508194:AAH9cJa7EYMY0iitofWNgZ-e9PqIRd9pWkE"

def load_config():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"bot_token": DEFAULT_TOKEN, "chat_ids": [], "last_scheduled_date": ""}

def save_config(config):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)

def telegram_api_call(method, payload=None, token=None):
    if not token:
        config = load_config()
        token = config.get("bot_token", DEFAULT_TOKEN)
    url = f"https://api.telegram.org/bot{token}/{method}"
    data = None
    headers = {}
    if payload:
        data = json.dumps(payload).encode("utf-8")
        headers = {"Content-Type": "application/json"}
    req = urllib.request.Request(url, data=data, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"[TELEGRAM API ERROR] {method}: {e}")
        return None

def fetch_and_register_chat_ids():
    """Polls Telegram updates to discover chat IDs of users who started or messaged the bot."""
    config = load_config()
    res = telegram_api_call("getUpdates")
    new_found = False
    if res and res.get("ok"):
        for item in res.get("result", []):
            msg = item.get("message", {}) or item.get("my_chat_member", {})
            chat = msg.get("chat", {})
            cid = chat.get("id")
            if cid and cid not in config.get("chat_ids", []):
                config.setdefault("chat_ids", []).append(cid)
                new_found = True
                print(f"[TELEGRAM] Discovered user chat ID: {cid} ({chat.get('first_name', '')})")
    if new_found:
        save_config(config)
    return config.get("chat_ids", [])

def send_telegram_message(chat_id, text, parse_mode="HTML"):
    """Sends message to a chat_id with automatic HTML fallback."""
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode,
        "disable_web_page_preview": True
    }
    res = telegram_api_call("sendMessage", payload)
    if not res or not res.get("ok"):
        # Fallback to plain text if HTML entity formatting had issues
        payload.pop("parse_mode", None)
        res = telegram_api_call("sendMessage", payload)
    return res and res.get("ok")

def read_applications():
    if not os.path.exists(TRACKER_CSV_PATH):
        return []
    with open(TRACKER_CSV_PATH, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def clean_text_for_tg(txt):
    if not txt:
        return ""
    txt = txt.replace("[LINEBREAK]", "\n")
    return txt.strip()

def generate_full_report_messages():
    """Generates structured report messages, neatly chunked to stay within Telegram 4096 char limits."""
    rows = read_applications()
    today_str = datetime.now().strftime("%d %b %Y")
    
    sent_list = []
    not_sent_list = []
    
    for r in rows:
        st = (r.get("Application Status") or "").strip().lower()
        if st in ["sent", "applied", "delivered", "dispatched"]:
            sent_list.append(r)
        else:
            not_sent_list.append(r)

    messages = []

    # 1. SUMMARY & SENT SECTION
    msg1 = f"☀️ <b>DAILY 9:00 AM JOB HUNT & OUTREACH REPORT</b>\n"
    msg1 += f"📅 <i>Date: {today_str} | Candidate: Rabiyathul Basariya B</i>\n"
    msg1 += f"🎯 <i>Target Roles: APM / PM / Business Analyst</i>\n"
    msg1 += f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
    msg1 += f"📊 <b>PIPELINE SNAPSHOT</b>\n"
    msg1 += f"• <b>Total Opportunities Tracked:</b> {len(rows)}\n"
    msg1 += f"• <b>Sent Automatically:</b> {len(sent_list)}\n"
    msg1 += f"• <b>Pending / Not Sent:</b> {len(not_sent_list)}\n"
    msg1 += f"• <b>Follow-ups Scheduled:</b> {len(rows)}\n\n"
    msg1 += f"━━━━━━━━━━━━━━━━━━━━━━\n"
    msg1 += f"🚀 <b>1. AUTOMATICALLY SENT / APPLIED JOBS</b>\n"
    msg1 += f"━━━━━━━━━━━━━━━━━━━━━━\n"
    if sent_list:
        for idx, s in enumerate(sent_list, 1):
            comp = s.get("Company Name", "Unknown")
            role = s.get("Role Title", "Unknown")
            date_sent = s.get("Date Contacted", "N/A")
            contact = s.get("Target Contact Person", "Hiring Team")
            email = s.get("Contact Email / Profile", "N/A")
            msg1 += f"<b>{idx}. {comp}</b>\n"
            msg1 += f"   📌 <b>Role:</b> {role}\n"
            msg1 += f"   👤 <b>Contact:</b> {contact} (<code>{email}</code>)\n"
            msg1 += f"   🕒 <b>Sent:</b> {date_sent}\n\n"
    else:
        msg1 += f"ℹ️ <i>No applications marked as 'Sent' yet.\nAll {len(not_sent_list)} identified roles are currently queued under 'Not Sent / Ready to Send' below for review or dispatch.</i>\n"
    messages.append(msg1)

    # 2. NOT SENT AUTOMATICALLY (CHUNKED SAFELY)
    chunk = (
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"⏳ <b>2. NOT SENT AUTOMATICALLY ({len(not_sent_list)} JOBS PENDING)</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"<i>Roles screened & ATS-tailored, awaiting review or portal dispatch:</i>\n\n"
    )
    for idx, ns in enumerate(not_sent_list, 1):
        comp = ns.get("Company Name", "Unknown")
        role = ns.get("Role Title", "Unknown")
        stage = ns.get("Funding / Company Stage", "N/A")
        contact = ns.get("Target Contact Person", "Talent Team")
        email = ns.get("Contact Email / Profile", "N/A")
        match = ns.get("Resume Focus & Match Score", "High")
        status = ns.get("Application Status", "Ready to Send")
        
        card = (
            f"<b>{idx}. {comp}</b> ({stage})\n"
            f"   🎯 <b>Role:</b> {role}\n"
            f"   👤 <b>Recipient:</b> {contact}\n"
            f"   ✉️ <b>Email/Link:</b> <code>{email}</code>\n"
            f"   📈 <b>Match:</b> {match}\n"
            f"   ⚠️ <b>Status:</b> {status}\n\n"
        )
        if len(chunk) + len(card) > 3400:
            messages.append(chunk)
            chunk = "⏳ <b>2. NOT SENT AUTOMATICALLY (CONTINUED)</b>\n━━━━━━━━━━━━━━━━━━━━━━\n\n" + card
        else:
            chunk += card
    if chunk.strip():
        messages.append(chunk)

    # 3. MAIL FOLLOW-UP LIST & CONTENT DETAILS (CHUNKED SAFELY)
    f_chunk = (
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📬 <b>3. MAIL FOLLOW-UP LIST & CONTENT DETAILS</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"<i>Whom to send, role, due dates, and full ready-to-copy follow-up content:</i>\n\n"
    )
    for idx, r in enumerate(rows[:8], 1):
        comp = r.get("Company Name", "Unknown")
        role = r.get("Role Title", "Unknown")
        contact = r.get("Target Contact Person", "Hiring Lead")
        email = r.get("Contact Email / Profile", "N/A")
        due_date = r.get("Follow-up Due Date", "3 days post-send")
        followup_pitch = clean_text_for_tg(r.get("Follow-up Template", ""))
        subject = r.get("Outreach Email Subject", "")

        f_card = (
            f"<b>[Follow-up #{idx}] {comp}</b>\n"
            f"• <b>To:</b> {contact} (<code>{email}</code>)\n"
            f"• <b>Role:</b> {role}\n"
            f"• <b>Follow-up Due Date:</b> <b>{due_date}</b>\n"
            f"• <b>Subject:</b> Re: {subject}\n"
            f"• <b>Content Details:</b>\n"
            f"<i>\"{followup_pitch}\"</i>\n"
            f"────────────────────\n\n"
        )
        if len(f_chunk) + len(f_card) > 3400:
            messages.append(f_chunk)
            f_chunk = "📬 <b>3. MAIL FOLLOW-UP LIST (CONTINUED)</b>\n━━━━━━━━━━━━━━━━━━━━━━\n\n" + f_card
        else:
            f_chunk += f_card
    if f_chunk.strip():
        messages.append(f_chunk)

    return messages

def broadcast_daily_report():
    """Broadcasts the 9 AM report to all registered chat IDs."""
    config = load_config()
    chat_ids = config.get("chat_ids", [])
    if not chat_ids:
        chat_ids = fetch_and_register_chat_ids()
    
    if not chat_ids:
        print("[TELEGRAM] No chat IDs found! Please open https://t.me/rabi_job_bot and send /start first.")
        return False

    print(f"[TELEGRAM] Broadcasting 9 AM report to {len(chat_ids)} user(s)...")
    messages = generate_full_report_messages()
    for cid in chat_ids:
        for msg in messages:
            send_telegram_message(cid, msg, parse_mode="HTML")
            time.sleep(0.5)
    print("[TELEGRAM] Report successfully delivered!")
    return True

def handle_user_command(chat_id, command_text):
    cmd = command_text.strip().lower()
    
    if cmd.startswith("/start") or cmd.startswith("/help"):
        welcome = (
            "👋 <b>Welcome to your Job Hunter & Outreach Intelligence Bot!</b>\n\n"
            "This bot tracks your automated job applications, pending roles, and email follow-ups.\n\n"
            "⏰ <b>Scheduled Report:</b> Every morning at <b>09:00 AM</b> sharp.\n\n"
            "<b>Interactive Commands:</b>\n"
            "• <code>/report</code> - Send complete 9:00 AM Job Intelligence Report right now\n"
            "• <code>/sent</code> - View jobs applied/sent automatically\n"
            "• <code>/pending</code> - View jobs not sent automatically (needs review)\n"
            "• <code>/followups</code> - View mail follow-up list & pitch content details\n"
            "• <code>/help</code> - Show this menu"
        )
        send_telegram_message(chat_id, welcome)
        
    elif cmd.startswith("/report"):
        send_telegram_message(chat_id, "⏳ <i>Generating full Job Application & Follow-up Intelligence Report...</i>")
        messages = generate_full_report_messages()
        for m in messages:
            send_telegram_message(chat_id, m)
            time.sleep(0.4)
            
    elif cmd.startswith("/sent"):
        rows = read_applications()
        sent = [r for r in rows if (r.get("Application Status") or "").strip().lower() in ["sent", "applied"]]
        if not sent:
            send_telegram_message(chat_id, "ℹ️ <b>0 jobs currently marked as 'Sent'.</b>\nAll 22 roles are queued under 'Ready to Send' / Pending.")
        else:
            txt = "<b>✅ AUTOMATICALLY SENT JOBS:</b>\n\n"
            for i, s in enumerate(sent, 1):
                txt += f"{i}. <b>{s.get('Company Name')}</b> — {s.get('Role Title')} (Date: {s.get('Date Contacted')})\n"
            send_telegram_message(chat_id, txt)
            
    elif cmd.startswith("/pending"):
        rows = read_applications()
        pending = [r for r in rows if (r.get("Application Status") or "").strip().lower() not in ["sent", "applied"]]
        txt = f"<b>⏳ NOT SENT AUTOMATICALLY ({len(pending)} ROLES):</b>\n\n"
        for i, p in enumerate(pending, 1):
            txt += f"{i}. <b>{p.get('Company Name')}</b>\n   Role: {p.get('Role Title')}\n   Contact: {p.get('Target Contact Person')} (<code>{p.get('Contact Email / Profile')}</code>)\n   Status: <b>{p.get('Application Status')}</b>\n\n"
        send_telegram_message(chat_id, txt)

    elif cmd.startswith("/followups"):
        rows = read_applications()
        txt = f"<b>📬 UPCOMING MAIL FOLLOW-UPS (Top 5 Active):</b>\n\n"
        for i, r in enumerate(rows[:5], 1):
            txt += f"<b>{i}. {r.get('Company Name')}</b> ({r.get('Role Title')})\n"
            txt += f"👤 <b>To:</b> {r.get('Target Contact Person')} (<code>{r.get('Contact Email / Profile')}</code>)\n"
            txt += f"📅 <b>Due:</b> {r.get('Follow-up Due Date')}\n"
            txt += f"📝 <b>Follow-up Body:</b>\n<blockquote>{clean_text_for_tg(r.get('Follow-up Template', ''))[:300]}...</blockquote>\n\n"
        send_telegram_message(chat_id, txt)
    else:
        send_telegram_message(chat_id, "🤖 Type <code>/report</code> to get your comprehensive job & follow-up report!")

def run_service_loop():
    """
    Continuous 24/7 service:
    1. Checks time: Fires daily 9:00 AM report automatically.
    2. Polls for incoming user commands (/report, /start, /pending, etc.)
    """
    print("=" * 65)
    print("TELEGRAM JOB NOTIFIER SERVICE RUNNING")
    print(f"Bot: @rabi_job_bot | Target Delivery Time: 09:00 AM Daily")
    print("=" * 65)
    
    last_update_id = 0
    config = load_config()

    while True:
        try:
            now = datetime.now()
            today_str = now.strftime("%Y-%m-%d")
            current_hour = now.hour
            current_minute = now.minute

            # Check if it's 9:00 AM and report has not run today
            if current_hour == 9 and current_minute >= 0 and current_minute <= 10:
                if config.get("last_scheduled_date") != today_str:
                    print(f"[{now.strftime('%H:%M:%S')}] Triggering scheduled 9:00 AM Report...")
                    success = broadcast_daily_report()
                    if success:
                        config["last_scheduled_date"] = today_str
                        save_config(config)

            # Poll for updates / incoming user messages
            res = telegram_api_call(f"getUpdates?offset={last_update_id + 1}&timeout=5")
            if res and res.get("ok"):
                for upd in res.get("result", []):
                    last_update_id = upd.get("update_id", last_update_id)
                    msg = upd.get("message", {})
                    chat = msg.get("chat", {})
                    cid = chat.get("id")
                    text = msg.get("text", "")

                    if cid:
                        if cid not in config.get("chat_ids", []):
                            config.setdefault("chat_ids", []).append(cid)
                            save_config(config)
                            print(f"[NEW SUBSCRIBER] Saved chat ID: {cid} ({chat.get('first_name', '')})")

                        if text:
                            print(f"[USER COMMAND] From {cid}: {text}")
                            handle_user_command(cid, text)

        except Exception as e:
            print(f"[POLL ERROR] {e}")

        time.sleep(3)

if __name__ == "__main__":
    import sys
    if "--send-now" in sys.argv:
        print("[TRIGGER] Sending report immediately...")
        broadcast_daily_report()
    elif "--register" in sys.argv:
        cids = fetch_and_register_chat_ids()
        print(f"Registered Chat IDs: {cids}")
    else:
        run_service_loop()
