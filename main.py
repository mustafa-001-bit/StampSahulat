import os
import json
import hashlib
import smtplib
import io
import base64
from email.message import EmailMessage
from datetime import datetime, timedelta
from fastapi import FastAPI, Request, Form, Response, Cookie, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader
import google.generativeai as genai
from supabase import create_client, Client

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

try:
    import qrcode
    HAS_QR = True
except ImportError:
    HAS_QR = False

from legal_templates import LEGAL_TEMPLATES, get_categories

# -------------------------------------------------------------
# Configuration & Environment
# -------------------------------------------------------------
def load_env_var(key: str, default: str = "") -> str:
    val = os.environ.get(key, "")
    if not val:
        env_path = os.path.join(os.path.dirname(__file__), ".env")
        if os.path.exists(env_path):
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith(f"{key}="):
                        val = line.split("=", 1)[1].strip().strip('"').strip("'")
                        break
    return val or default

GEMINI_API_KEY = load_env_var("GEMINI_API_KEY", "")
ADMIN_PASSCODE = "3284"
SUPABASE_URL = load_env_var("SUPABASE_URL", "")
SUPABASE_KEY = load_env_var("SUPABASE_KEY", "")

supabase: Client = None
if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# -------------------------------------------------------------
# Instant Admin Email Notification Engine
# -------------------------------------------------------------
def notify_admin_by_email(subject: str, message_body: str):
    smtp_email = load_env_var("SMTP_EMAIL", "")
    smtp_password = load_env_var("SMTP_PASSWORD", "")
    smtp_server = load_env_var("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(load_env_var("SMTP_PORT", "465"))

    if not smtp_email or not smtp_password:
        return

    try:
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = f"StampSahulat Alert System <{smtp_email}>"
        msg['To'] = smtp_email
        msg.set_content(message_body)

        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(smtp_email, smtp_password)
            server.send_message(msg)
    except Exception as e:
        print(f"[EMAIL ERROR] {str(e)}")

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def get_db_user_by_email(email: str):
    if not supabase: return None
    try:
        res = supabase.table("ss_users").select("*").eq("email", email.lower().strip()).execute()
        return res.data[0] if res.data else None
    except Exception:
        return None

def get_db_user_by_id(user_id: int):
    if not supabase: return None
    try:
        res = supabase.table("ss_users").select("*").eq("id", user_id).execute()
        return res.data[0] if res.data else None
    except Exception:
        return None

def get_record_by_id(rec_id: int):
    if not supabase: return None
    try:
        res = supabase.table("ss_records").select("*").eq("id", rec_id).execute()
        return res.data[0] if res.data else None
    except Exception:
        return None

def is_business_plan_active(user: dict) -> bool:
    if not user or user.get("account_type") != "business":
        return False
    if user.get("subscription_status") != "active":
        return False
    sub_end = user.get("subscription_end")
    if not sub_end:
        return False
    try:
        expiry_dt = datetime.strptime(sub_end, "%Y-%m-%d %H:%M:%S")
        return datetime.now() <= expiry_dt
    except Exception:
        return False

def check_business_quota(user_id: int, sub_start: str):
    if not supabase: return 0, 0
    today_prefix = datetime.now().strftime("%d-%m-%Y")
    try:
        res = supabase.table("ss_records").select("created_at, status").eq("user_id", user_id).eq("status", "approved").execute()
        records = res.data or []
        prints_today = sum(1 for r in records if r.get("created_at", "").startswith(today_prefix))
        prints_cycle = sum(1 for r in records if r.get("created_at", "") >= (sub_start or ""))
        return prints_today, prints_cycle
    except Exception:
        return 0, 0

def generate_qr_base64(data_text: str) -> str:
    if not HAS_QR:
        return ""
    try:
        qr = qrcode.QRCode(box_size=3, border=1)
        qr.add_data(data_text)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return base64.b64encode(buf.getvalue()).decode()
    except Exception:
        return ""

app = FastAPI(title="StampSahulat - Pakistan's 1st Legal Drafting Engine")
templates = Jinja2Templates(directory="templates")

URDU_MONTHS = {
    1: "جنوری", 2: "فروری", 3: "مارچ", 4: "اپریل",
    5: "مئی", 6: "جون", 7: "جولائی", 8: "اگست",
    9: "ستمبر", 10: "اکتوبر", 11: "نومبر", 12: "دسمبر"
}

def get_live_dates():
    now = datetime.now()
    urdu_date = f"{now.day} {URDU_MONTHS.get(now.month, '')} {now.year}ء"
    day = now.day
    if 4 <= day <= 20 or 24 <= day <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][day % 10 - 1]
    eng_date = f"{day}{suffix} {now.strftime('%B, %Y')}"
    return urdu_date, eng_date

def get_current_user_from_request(request: Request):
    user_id = request.cookies.get("user_session")
    if user_id and user_id.isdigit():
        return get_db_user_by_id(int(user_id))
    return None

# -------------------------------------------------------------
# SEO, AI Crawlers & Programmatic Pages Engine
# -------------------------------------------------------------
@app.get("/robots.txt", response_class=Response)
def get_robots_txt():
    content = """User-agent: *
Allow: /
Disallow: /system-control-3284

User-agent: GPTBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: ClaudeBot
Allow: /

Sitemap: https://stampsahulat.com/sitemap.xml
"""
    return Response(content=content, media_type="text/plain")

@app.get("/sitemap.xml", response_class=Response)
def get_sitemap_xml(request: Request):
    host_header = request.headers.get("host", "stampsahulat.com")
    protocol = "https" if "vercel.app" in host_header or "stampsahulat" in host_header else "http"
    base_url = f"{protocol}://{host_header}"

    urls = [
        f"""  <url>
    <loc>{base_url}/</loc>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>"""
    ]

    for key in LEGAL_TEMPLATES.keys():
        urls.append(f"""  <url>
    <loc>{base_url}/stamp-paper/{key}</loc>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>""")

    sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(urls)}
</urlset>"""
    return Response(content=sitemap_content, media_type="application/xml")

@app.get("/stamp-paper/{slug}", response_class=HTMLResponse)
async def serve_programmatic_seo_page(slug: str, request: Request):
    doc = LEGAL_TEMPLATES.get(slug)
    if not doc:
        return RedirectResponse(url="/")

    host_header = request.headers.get("host", "stampsahulat.com")
    protocol = "https" if "vercel.app" in host_header or "stampsahulat" in host_header else "http"
    canonical_url = f"{protocol}://{host_header}/stamp-paper/{slug}"

    return templates.TemplateResponse(
        request=request,
        name="seo_template_page.html",
        context={
            "doc": doc,
            "slug": slug,
            "canonical_url": canonical_url,
            "all_templates": LEGAL_TEMPLATES
        }
    )

# -------------------------------------------------------------
# Public Digital Verification Route (QR Scan Target)
# -------------------------------------------------------------
@app.get("/verify/{record_id}", response_class=HTMLResponse)
async def verify_document_public(record_id: int):
    rec = get_record_by_id(record_id)
    if not rec:
        return HTMLResponse("""
        <!DOCTYPE html>
        <html lang="en">
        <head><meta charset="UTF-8"><title>Verification Failed</title><script src="https://cdn.tailwindcss.com"></script></head>
        <body class="bg-slate-100 flex items-center justify-center min-h-screen p-4 font-sans">
            <div class="bg-white p-8 rounded-2xl shadow-xl max-w-md w-full text-center space-y-4 border border-rose-200">
                <div class="w-16 h-16 bg-rose-100 text-rose-600 rounded-full flex items-center justify-center mx-auto text-2xl font-bold">✕</div>
                <h2 class="text-xl font-bold text-slate-900">Record Not Found</h2>
                <p class="text-xs text-slate-500">The scanned legal document reference does not exist in StampSahulat registry database.</p>
            </div>
        </body></html>
        """, status_code=404)

    is_verified = (rec["status"] == "approved")
    status_badge = '<span class="bg-emerald-100 text-emerald-800 border border-emerald-300 font-bold px-3 py-1 rounded-full text-xs">✓ Verified & Approved</span>' if is_verified else '<span class="bg-amber-100 text-amber-800 border border-amber-300 font-bold px-3 py-1 rounded-full text-xs">⏳ Verification Pending</span>'

    return HTMLResponse(f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Digital Legal Record Verification - StampSahulat</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-slate-900 min-h-screen flex items-center justify-center p-4 font-sans text-slate-800">
        <div class="bg-white max-w-lg w-full rounded-3xl shadow-2xl overflow-hidden border border-slate-200">
            <div class="bg-gradient-to-r from-emerald-800 to-slate-900 p-6 text-white text-center space-y-1">
                <span class="text-3xl">⚖️</span>
                <h1 class="text-lg font-bold">StampSahulat Digital Verification</h1>
                <p class="text-[11px] text-emerald-200 font-mono tracking-wider">OFFICIAL REPOSITORY CERTIFICATE</p>
            </div>

            <div class="p-6 space-y-5 text-xs">
                <div class="flex justify-between items-center border-b pb-3">
                    <span class="text-slate-500">Document Registry Status:</span>
                    {status_badge}
                </div>

                <div class="space-y-2.5">
                    <div class="flex justify-between border-b pb-2">
                        <span class="text-slate-500 font-bold">Document Ref ID:</span>
                        <span class="font-mono font-bold text-slate-900">#SS-{rec['id']}</span>
                    </div>
                    <div class="flex justify-between border-b pb-2">
                        <span class="text-slate-500 font-bold">Agreement Title:</span>
                        <span class="font-bold text-slate-900 text-right">{rec['title']}</span>
                    </div>
                    <div class="flex justify-between border-b pb-2">
                        <span class="text-slate-500 font-bold">Date of Execution:</span>
                        <span class="font-mono text-slate-800">{rec['created_at']}</span>
                    </div>
                    <div class="flex justify-between border-b pb-2">
                        <span class="text-slate-500 font-bold">First Party:</span>
                        <span class="font-bold text-slate-900 text-right">{rec['p1_name']} ({rec['p1_cnic']})</span>
                    </div>
                    <div class="flex justify-between border-b pb-2">
                        <span class="text-slate-500 font-bold">Second Party:</span>
                        <span class="font-bold text-slate-900 text-right">{rec['p2_name']} ({rec['p2_cnic']})</span>
                    </div>
                    <div class="flex justify-between border-b pb-2">
                        <span class="text-slate-500 font-bold">Output Paper Mode:</span>
                        <span class="uppercase text-slate-700">{rec['paper_mode']}</span>
                    </div>
                </div>

                <div class="bg-slate-50 p-3.5 rounded-xl border text-[11px] text-slate-600 leading-relaxed text-center">
                    This document was legally drafted and digitally formatted on the StampSahulat Automation Engine under judicial Stamp Act guidelines.
                </div>
            </div>

            <div class="bg-slate-100 p-3 text-center border-t text-[10px] text-slate-400">
                Official Verification Repository &copy; StampSahulat.com
            </div>
        </div>
    </body>
    </html>
    """)

# -------------------------------------------------------------
# Auth & Subscription Endpoints
# -------------------------------------------------------------
@app.post("/api/register")
async def register_user(request: Request):
    if not supabase:
        return JSONResponse({"error": "Database disconnected! Check Supabase Keys in .env."}, status_code=500)

    try:
        data = await request.json()
        full_name = data.get("full_name", "").strip()
        email = data.get("email", "").strip().lower()
        phone = data.get("phone", "").strip()
        password = data.get("password", "")
        account_type = data.get("account_type", "personal").strip()
        terms_agreed = data.get("terms_agreed", False)

        if not full_name or not email or not password or not phone:
            return JSONResponse({"error": "تمام خانے پُر کرنا لازمی ہیں!"}, status_code=400)

        if not terms_agreed:
            return JSONResponse({"error": "قوانین و ضوابط تسلیم کرنا لازمی ہیں!"}, status_code=400)

        if get_db_user_by_email(email):
            return JSONResponse({"error": "یہ ای میل پہلے سے موجود ہے۔ لاگ ان کریں!"}, status_code=400)

        pw_hash = hash_password(password)
        now_str = datetime.now().strftime("%d-%m-%Y %I:%M %p")

        res = supabase.table("ss_users").insert({
            "full_name": full_name,
            "email": email,
            "phone": phone,
            "password_hash": pw_hash,
            "account_type": account_type,
            "created_at": now_str
        }).execute()

        if not res.data:
            return JSONResponse({"error": "Supabase rejected insert: Empty response data."}, status_code=500)

        user_id = res.data[0]["id"]
        response = JSONResponse({"success": True, "message": "Account created successfully!"})
        response.set_cookie(key="user_session", value=str(user_id), max_age=86400 * 30, httponly=True)
        return response

    except Exception as e:
        print(f"[REGISTER ERROR] {str(e)}")
        return JSONResponse({"error": f"Database Error: {str(e)}"}, status_code=500)

@app.post("/api/login")
async def login_user(request: Request):
    data = await request.json()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    user = get_db_user_by_email(email)
    if not user or user["password_hash"] != hash_password(password):
        return JSONResponse({"error": "غلط ای میل یا پاس ورڈ درج کیا گیا ہے!"}, status_code=400)

    response = JSONResponse({"success": True, "message": "Welcome back!"})
    response.set_cookie(key="user_session", value=str(user["id"]), max_age=86400 * 30, httponly=True)
    return response

@app.get("/logout")
async def logout_user():
    response = RedirectResponse(url="/")
    response.delete_cookie(key="user_session")
    return response

@app.post("/api/upload-subscription-slip")
async def upload_sub_slip(request: Request, slip_file: UploadFile = File(...)):
    user = get_current_user_from_request(request)
    if not user:
        return JSONResponse({"error": "Login required!"}, status_code=401)

    file_bytes = await slip_file.read()
    if len(file_bytes) < 2000:
        return JSONResponse({"error": "تصویر خالی یا خراب ہے، درست رسید اپلوڈ کریں۔"}, status_code=400)

    sub_b64 = base64.b64encode(file_bytes).decode("utf-8")

    supabase.table("ss_users").update({
        "subscription_status": "pending_approval",
        "sub_slip_b64": sub_b64
    }).eq("id", user["id"]).execute()

    admin_alert_body = f"""Assalam-o-Alaikum Admin,

Ek customer ne Business Plan (Rs. 5,000 / 30 Din / 60 Prints) ki payment slip upload ki hai:

User ID: #{user['id']}
Customer: {user['full_name']}
Email: {user['email']}
Mobile: {user['phone']}
Time: {datetime.now().strftime("%d-%m-%Y %I:%M %p")}

Admin panel khol kar tasdeeq karein aur 30-day membership approve karein:
https://stampsahulat.com/system-control-3284

Shukriya,
StampSahulat Notification Bot
"""
    notify_admin_by_email(
        f"🚀 NAYI BUSINESS PLAN SLIP (Rs. 5,000) - {user['full_name']}",
        admin_alert_body
    )

    return JSONResponse({
        "success": True,
        "message": "کاروباری سبسکرپشن (5,000 روپے) کی رسید موصول ہو گئی۔ ایڈمن منظوری کے بعد 30 دن کا کوٹہ فعال ہو جائے گا۔"
    })

# -------------------------------------------------------------
# Main Application Route
# -------------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    urdu_date, eng_date = get_live_dates()
    current_user = get_current_user_from_request(request)
    is_biz_active = is_business_plan_active(current_user)
    
    prints_today = 0
    prints_month = 0
    if is_biz_active:
        prints_today, prints_month = check_business_quota(current_user["id"], current_user.get("subscription_start", ""))

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "categories": get_categories(lang="ur"),
            "all_templates": LEGAL_TEMPLATES,
            "today_urdu_date": urdu_date,
            "today_en_date": eng_date,
            "current_user": current_user,
            "is_biz_active": is_biz_active,
            "prints_today": prints_today,
            "prints_month": prints_month
        }
    )

@app.get("/history", response_class=HTMLResponse)
async def view_history(request: Request):
    current_user = get_current_user_from_request(request)
    if not current_user:
        return RedirectResponse(url="/")

    records = []
    if supabase:
        res = supabase.table("ss_records").select("*").eq("user_id", current_user["id"]).order("id", desc=True).execute()
        records = res.data or []

    return templates.TemplateResponse(
        request=request,
        name="history.html",
        context={
            "documents": records,
            "current_user": current_user
        }
    )

# -------------------------------------------------------------
# Create Draft Endpoint
# -------------------------------------------------------------
@app.post("/api/create-draft")
async def create_draft_endpoint(request: Request):
    try:
        current_user = get_current_user_from_request(request)
        if not current_user:
            return JSONResponse({"error": "auth_required", "message": "پہلے لاگ ان یا سائن اپ کریں!"}, status_code=401)

        business_covered = is_business_plan_active(current_user)
        
        if business_covered:
            p_today, p_cycle = check_business_quota(current_user["id"], current_user.get("subscription_start", ""))
            if p_today >= 2:
                return JSONResponse({
                    "error": "بزنس اکاؤنٹ کی روزانہ کی حد (2 پرنٹس فی دن) مکمل ہو چکی ہے۔ اگلا پرنٹ کل صبح نکل سکے گا۔"
                }, status_code=429)
            if p_cycle >= 60:
                return JSONResponse({
                    "error": "آپ کے اس ماہ کے 60 پرنٹس کا کوٹہ مکمل ہو چکا ہے۔"
                }, status_code=429)

        form_data = await request.form()
        lang = form_data.get("lang", "ur")
        paper_mode = form_data.get("paper_mode", "physical_stamp")
        template_key = form_data.get("template_key", "farokht_car")
        selected_doc = LEGAL_TEMPLATES.get(template_key, list(LEGAL_TEMPLATES.values())[0])

        title = selected_doc["title_ur"] if lang == "ur" else selected_doc["title_en"]
        fallback_p1 = selected_doc["party1_role_ur"] if lang == "ur" else selected_doc["party1_role_en"]
        fallback_p2 = selected_doc["party2_role_ur"] if lang == "ur" else selected_doc["party2_role_en"]

        final_clauses_raw = form_data.get("final_clauses_json", "[]")
        formatted_clauses = []
        try:
            final_list = json.loads(final_clauses_raw)
            formatted_clauses = [c.strip() for c in final_list if c.strip()]
        except Exception:
            pass

        if not formatted_clauses:
            data_dict = {key: value for key, value in form_data.items()}
            raw_clauses = selected_doc["clauses_ur"] if lang == "ur" else selected_doc["clauses_en"]
            for raw in raw_clauses:
                try:
                    formatted_clauses.append(raw.format(**data_dict))
                except KeyError:
                    formatted_clauses.append(raw)

        partners_list = []
        partners_json_raw = form_data.get("partners_json", "")
        if partners_json_raw:
            try:
                partners_list = json.loads(partners_json_raw)
            except Exception:
                partners_list = []

        witness_mode = form_data.get("witness_mode", "manual")
        witness1_data = None
        witness2_data = None

        if witness_mode == "computerized":
            witness1_data = {
                "name": form_data.get("w1_name", "").strip(),
                "father_name": form_data.get("w1_father", "").strip(),
                "cnic": form_data.get("w1_cnic", "").strip()
            }
            witness2_data = {
                "name": form_data.get("w2_name", "").strip(),
                "father_name": form_data.get("w2_father", "").strip(),
                "cnic": form_data.get("w2_cnic", "").strip()
            }

        urdu_date, eng_date = get_live_dates()
        date_str = urdu_date if lang == "ur" else eng_date

        p1_name = form_data.get("p1_name", "")
        p1_cnic = form_data.get("p1_cnic", "")
        p2_name = form_data.get("p2_name", "")
        p2_cnic = form_data.get("p2_cnic", "")

        doc_payload = {
            "lang": lang,
            "title": title,
            "date_str": date_str,
            "partners": partners_list,
            "party1": {
                "name": p1_name,
                "father_name": form_data.get("p1_father", ""),
                "cnic": p1_cnic,
                "address": form_data.get("p1_address", ""),
                "role": form_data.get("p1_role", fallback_p1)
            },
            "party2": {
                "name": p2_name,
                "father_name": form_data.get("p2_father", ""),
                "cnic": p2_cnic,
                "address": form_data.get("p2_address", ""),
                "role": form_data.get("p2_role", fallback_p2)
            },
            "witness1": witness1_data,
            "witness2": witness2_data,
            "clauses": formatted_clauses
        }

        now_str = datetime.now().strftime("%d-%m-%Y %I:%M %p")
        initial_status = "approved" if business_covered else "pending_payment"

        res = supabase.table("ss_records").insert({
            "user_id": current_user["id"],
            "created_at": now_str,
            "title": title,
            "lang": lang,
            "paper_mode": paper_mode,
            "p1_name": p1_name,
            "p1_cnic": p1_cnic,
            "p2_name": p2_name,
            "p2_cnic": p2_cnic,
            "doc_data": json.dumps(doc_payload, ensure_ascii=False),
            "status": initial_status
        }).execute()

        record_id = res.data[0]["id"]

        return JSONResponse({
            "success": True,
            "record_id": record_id,
            "title": title,
            "business_unlocked": business_covered
        })
    except Exception as e:
        return JSONResponse({"error": f"Database Error: {str(e)}"}, status_code=500)

# -------------------------------------------------------------
# Instant HTML Preview (Unpaid Draft)
# -------------------------------------------------------------
@app.get("/preview-html/{record_id}")
async def get_preview_html(record_id: int, request: Request):
    rec = get_record_by_id(record_id)
    if not rec:
        return HTMLResponse("<h3>دستاویز موجود نہیں ہے۔</h3>", status_code=404)

    doc_payload = json.loads(rec["doc_data"])
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("base_document.html")
    top_margin = "3.4in" if rec["paper_mode"] == "physical_stamp" else "1.8in"

    host_header = request.headers.get("host", "stampsahulat.com")
    verify_url = f"https://{host_header}/verify/{record_id}"
    qr_b64 = generate_qr_base64(verify_url)

    rendered_html = template.render(
        lang=doc_payload["lang"],
        doc_title=doc_payload["title"],
        top_margin=top_margin,
        paper_mode=rec["paper_mode"],
        record_id=record_id,
        verify_url=verify_url,
        qr_base64=qr_b64,
        party1=doc_payload.get("party1"),
        party2=doc_payload.get("party2"),
        partners=doc_payload.get("partners", []),
        witness1=doc_payload.get("witness1"),
        witness2=doc_payload.get("witness2"),
        clauses=doc_payload["clauses"],
        date_str=doc_payload["date_str"],
        is_watermarked=True,
        auto_print=False
    )
    return HTMLResponse(rendered_html)

# -------------------------------------------------------------
# Clean Print-Ready View (Vercel Serverless PDF Replacement)
# -------------------------------------------------------------
@app.get("/document/print/{record_id}")
@app.get("/download/{record_id}")
async def print_clean_document(record_id: int, request: Request):
    rec = get_record_by_id(record_id)
    if not rec:
        return HTMLResponse("<h3>دستاویز نہیں مل سکی۔</h3>", status_code=404)

    if rec["status"] != "approved":
        return HTMLResponse(f"""
        <div style="font-family:sans-serif; text-align:center; padding:50px; direction:rtl;">
            <h2 style="color:#d97706;">ادائیگی ابھی منظور نہیں ہوئی!</h2>
            <p>ایڈمن پینل سے منظوری ملتے ہی کلین پرنٹ فعال ہو جائے گا۔</p>
            <a href="/" style="display:inline-block; margin-top:20px; background:#047857; color:white; padding:10px 20px; text-decoration:none; border-radius:8px;">پورٹل پر واپس جائیں</a>
        </div>
        """, status_code=403)

    doc_payload = json.loads(rec["doc_data"])
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("base_document.html")
    top_margin = "3.4in" if rec["paper_mode"] == "physical_stamp" else "1.8in"

    host_header = request.headers.get("host", "stampsahulat.com")
    verify_url = f"https://{host_header}/verify/{record_id}"
    qr_b64 = generate_qr_base64(verify_url)

    rendered_html = template.render(
        lang=doc_payload["lang"],
        doc_title=doc_payload["title"],
        top_margin=top_margin,
        paper_mode=rec["paper_mode"],
        record_id=record_id,
        verify_url=verify_url,
        qr_base64=qr_b64,
        party1=doc_payload.get("party1"),
        party2=doc_payload.get("party2"),
        partners=doc_payload.get("partners", []),
        witness1=doc_payload.get("witness1"),
        witness2=doc_payload.get("witness2"),
        clauses=doc_payload["clauses"],
        date_str=doc_payload["date_str"],
        is_watermarked=False,
        auto_print=True
    )
    return HTMLResponse(rendered_html)

# -------------------------------------------------------------
# Fast AI Payment Slip Scanner
# -------------------------------------------------------------
@app.post("/api/upload-slip/{record_id}")
async def upload_payment_slip(record_id: int, slip_file: UploadFile = File(...)):
    rec = get_record_by_id(record_id)
    if not rec:
        return JSONResponse({"error": "Record nahi mila!"}, status_code=404)

    file_bytes = await slip_file.read()
    if len(file_bytes) < 2000:
        return JSONResponse({"error": "تصویر خالی یا خراب ہے۔ درست رسید اپلوڈ کریں۔"}, status_code=400)

    fast_bytes = file_bytes
    if HAS_PIL:
        try:
            img = Image.open(io.BytesIO(file_bytes))
            img.thumbnail((800, 800))
            compressed_io = io.BytesIO()
            img.convert("RGB").save(compressed_io, format="JPEG", quality=75)
            fast_bytes = compressed_io.getvalue()
        except Exception:
            fast_bytes = file_bytes

    slip_b64 = base64.b64encode(fast_bytes).decode("utf-8")
    ai_verdict = {"is_slip": False, "notes": "Verification rejected"}

    try:
        genai.configure(api_key=SERVER_API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        fast_prompt = (
            "Examine this Pakistani mobile banking/wallet payment receipt (EasyPaisa, JazzCash, Nayapay, Bank). "
            "STRICT RULES: Does it show a real payment transaction with Transaction ID/TID, Amount (approx Rs 500), and Status? "
            "If it is a logo, personal selfie, random photo, meme, or empty document, return false. "
            "Output strictly raw JSON: {\"is_slip\": true, \"trx_id\": \"1234\", \"amount\": \"500\"}"
        )
        
        response = model.generate_content([
            fast_prompt,
            {"mime_type": "image/jpeg", "data": fast_bytes}
        ])
        clean_json = response.text.strip().replace("```json", "").replace("```", "").strip()
        ai_verdict = json.loads(clean_json)
    except Exception as e:
        ai_verdict = {"is_slip": False, "notes": f"AI Scanner Error: {str(e)}"}

    if not ai_verdict.get("is_slip", False):
        return JSONResponse({
            "error": "سسٹم نے تصویر مسترد کر دی ہے! یہ کسی بینک یا والٹ کی ٹرانزیکشن رسید نہیں ہے۔ اصل ادائیگی کی رسید منسلک کریں۔"
        }, status_code=400)

    supabase.table("ss_records").update({
        "slip_b64": slip_b64,
        "status": "pending_approval",
        "ai_verification_notes": json.dumps(ai_verdict, ensure_ascii=False)
    }).eq("id", record_id).execute()

    user = get_db_user_by_id(rec["user_id"]) if rec.get("user_id") else {}
    user_name = user.get("full_name", "N/A")
    user_phone = user.get("phone", "N/A")
    detected_amt = ai_verdict.get("amount") or ai_verdict.get("detected_amount", "500")
    trx_id = ai_verdict.get("trx_id", "N/A")

    admin_alert_body = f"""Assalam-o-Alaikum Admin,

StampSahulat portal par nayi payment slip tasdeeq ke liye aayi hai:

Document Ref: #{record_id}
Title: {rec['title']}
Customer: {user_name}
Mobile: {user_phone}
AI Detected Amount: Rs. {detected_amt}
Trx / TID: {trx_id}
Time: {datetime.now().strftime("%d-%m-%Y %I:%M %p")}

Admin panel khol kar check karein:
https://stampsahulat.com/system-control-3284

Shukriya,
StampSahulat Notification Bot
"""
    notify_admin_by_email(
        f"🚨 NAYI PAYMENT SLIP MOSOOL! - Ref #{record_id} ({rec['title']})",
        admin_alert_body
    )

    return JSONResponse({
        "success": True,
        "message": "رسید موصول ہو گئی ہے۔ ایڈمن تصدیق کے بعد کلین دستاویز ڈاؤن لوڈ کے لیے دستیاب ہوگی۔"
    })

# -------------------------------------------------------------
# Slip Viewer (Decodes Base64 to Image on Vercel)
# -------------------------------------------------------------
@app.get("/view-slip/{record_id}")
async def view_record_slip(record_id: int):
    rec = get_record_by_id(record_id)
    if not rec or not rec.get("slip_b64"):
        return HTMLResponse("Slip not found", status_code=404)
    img_data = base64.b64decode(rec["slip_b64"])
    return Response(content=img_data, media_type="image/jpeg")

@app.get("/view-sub-slip/{user_id}")
async def view_sub_slip(user_id: int):
    usr = get_db_user_by_id(user_id)
    if not usr or not usr.get("sub_slip_b64"):
        return HTMLResponse("Subscription slip not found", status_code=404)
    img_data = base64.b64decode(usr["sub_slip_b64"])
    return Response(content=img_data, media_type="image/jpeg")

# -------------------------------------------------------------
# Secret Admin Portal (Code: 3284)
# -------------------------------------------------------------
@app.post("/api/admin-verify")
async def verify_admin_pin(request: Request):
    data = await request.json()
    code = data.get("code", "").strip()
    if code == ADMIN_PASSCODE:
        res = JSONResponse({"success": True})
        res.set_cookie(key="sec_adm_token", value=ADMIN_PASSCODE, max_age=86400, httponly=True)
        return res
    return JSONResponse({"error": "Access Denied"}, status_code=403)

@app.get("/system-control-3284", response_class=HTMLResponse)
async def secret_admin_panel(request: Request):
    token = request.cookies.get("sec_adm_token")
    if token != ADMIN_PASSCODE:
        return HTMLResponse("<h3>404 Not Found</h3>", status_code=404)

    records = []
    biz_users = []
    users_ledger = []

    if supabase:
        r_res = supabase.table("ss_records").select("*").order("id", desc=True).execute()
        records = r_res.data or []

        u_res = supabase.table("ss_users").select("*").order("id", desc=True).execute()
        all_users = u_res.data or []
        biz_users = [u for u in all_users if u.get("account_type") == "business"]

        for u in all_users:
            u_drafts = sum(1 for r in records if r.get("user_id") == u["id"])
            u_prints = sum(1 for r in records if r.get("user_id") == u["id"] and r.get("status") == "approved")
            u["total_drafts"] = u_drafts
            u["approved_prints"] = u_prints
            users_ledger.append(u)

    user_map = {u["id"]: u for u in users_ledger}

    rows_html = ""
    for r in records:
        u_info = user_map.get(r.get("user_id"), {})
        u_name = u_info.get("full_name", "N/A")
        u_phone = u_info.get("phone", "")
        u_type = u_info.get("account_type", "personal")

        slip_link = f"<a href='/view-slip/{r['id']}' target='_blank' style='color:#38bdf8; font-weight:bold; text-decoration:underline;'>رسید دیکھیں</a>" if r.get("slip_b64") else "<span style='color:#64748b;'>بزنس پاس / فری</span>"
        status_val = r.get("status", "pending_payment")
        actions = ""
        if status_val == "pending_approval":
            actions = f"""
                <a href='/system-control-3284/approve/{r['id']}' style='background:#059669; color:white; padding:6px 12px; border-radius:6px; text-decoration:none; font-size:11px; font-weight:bold;'>منظور کریں</a>
                <a href='/system-control-3284/reject/{r['id']}' style='background:#dc2626; color:white; padding:6px 12px; border-radius:6px; text-decoration:none; font-size:11px; font-weight:bold; margin-right:5px;'>مسترد</a>
            """
        elif status_val == "approved":
            actions = f"<span style='color:#34d399; font-weight:bold;'>✓ منظور شدہ</span> | <a href='/document/print/{r['id']}' target='_blank' style='color:#38bdf8; margin-right:5px;'>پرنٹ دیکھیں</a>"
        else:
            actions = f"<span style='color:#94a3b8;'>{status_val}</span>"

        rows_html += f"""
        <tr style='border-bottom:1px solid #334155;'>
            <td style='padding:10px; font-family:monospace; color:#38bdf8;'>#{r['id']}</td>
            <td style='padding:10px;'><strong>{u_name}</strong><br><small style='color:#94a3b8;'>{u_phone} ({u_type})</small></td>
            <td style='padding:10px;'><strong>{r.get('title', '')}</strong><br><small style='color:#64748b;'>{r.get('created_at', '')}</small></td>
            <td style='padding:10px;'>{slip_link}</td>
            <td style='padding:10px;'>{actions}</td>
        </tr>
        """

    biz_rows_html = ""
    for b in biz_users:
        slip_link = f"<a href='/view-sub-slip/{b['id']}' target='_blank' style='color:#38bdf8; font-weight:bold; text-decoration:underline;'>5000 کی رسید دیکھیں</a>" if b.get("sub_slip_b64") else "رسید نہیں آئی"
        st = b.get("subscription_status", "none")
        act = ""
        if st == "pending_approval":
            act = f"<a href='/system-control-3284/approve-sub/{b['id']}' style='background:#059669; color:white; padding:6px 12px; border-radius:6px; text-decoration:none; font-size:11px; font-weight:bold;'>30 دن پاس ایکٹو کریں</a>"
        elif st == "active":
            act = f"<span style='color:#34d399; font-weight:bold;'>ایکٹو تا: {b.get('subscription_end', '')[:10]}</span>"
        else:
            act = f"<span style='color:#94a3b8;'>غیر فعال ({st})</span>"

        biz_rows_html += f"""
        <tr style='border-bottom:1px solid #334155;'>
            <td style='padding:10px; font-family:monospace; color:#38bdf8;'>U-{b['id']}</td>
            <td style='padding:10px;'><strong>{b['full_name']}</strong><br><small>{b['email']}</small></td>
            <td style='padding:10px; font-family:monospace;'>{b['phone']}</td>
            <td style='padding:10px;'>{slip_link}</td>
            <td style='padding:10px;'>{act}</td>
        </tr>
        """

    users_rows_html = ""
    for u in users_ledger:
        users_rows_html += f"""
        <tr style='border-bottom:1px solid #334155;'>
            <td style='padding:10px; font-family:monospace; color:#38bdf8;'>U-{u['id']}</td>
            <td style='padding:10px;'><strong>{u['full_name']}</strong><br><small style='color:#94a3b8;'>{u['email']}</small></td>
            <td style='padding:10px; font-family:monospace;'>{u['phone']}</td>
            <td style='padding:10px;'><span style='background:#0f172a; padding:3px 8px; border-radius:5px;'>{u['account_type'].upper()}</span></td>
            <td style='padding:10px; text-align:center;'>{u['total_drafts']}</td>
            <td style='padding:10px; text-align:center;'><strong style='color:#34d399;'>{u['approved_prints'] or 0}</strong></td>
            <td style='padding:10px; color:#94a3b8; font-size:11px;'>{u['created_at']}</td>
        </tr>
        """

    return HTMLResponse(f"""
    <!DOCTYPE html>
    <html lang="ur" dir="rtl">
    <head>
        <meta charset="UTF-8"><title>StampSahulat - Admin Terminal</title>
        <link href="https://fonts.googleapis.com/css2?family=Noto+Nastaliq+Urdu:wght@400;700&display=swap" rel="stylesheet">
        <style>
            body {{ font-family: 'Noto Nastaliq Urdu', ui-sans-serif, system-ui, sans-serif; padding: 25px; background: #0f172a; color: #f8fafc; }}
            .card {{ max-width: 1100px; margin: auto; background: #1e293b; padding: 25px; border-radius: 16px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 15px; font-size: 12px; }}
            th {{ background: #334155; color: #38bdf8; padding: 12px; text-align: right; }}
            td {{ border-bottom: 1px solid #334155; }}
            .tab-btn {{ background:#334155; color:#cbd5e1; border:none; padding:8px 16px; border-radius:8px; cursor:pointer; font-weight:bold; font-size:12px; }}
            .tab-active {{ background:#059669; color:white; }}
        </style>
    </head>
    <body>
        <div class="card">
            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #334155; padding-bottom:15px;">
                <h2 style="margin:0; color:#38bdf8;">🔒 ایڈمن کنٹرول ٹرمینل (StampSahulat)</h2>
                <a href="/" style="color:#94a3b8; text-decoration:none; font-size:12px;">← پورٹل پر واپس جائیں</a>
            </div>

            <div style="display:flex; gap:10px; margin:20px 0 15px;">
                <button onclick="showTab('approvals')" id="btnTabApp" class="tab-btn tab-active">معاہدات کی منظوری (Drafts)</button>
                <button onclick="showTab('business')" id="btnTabBiz" class="tab-btn">بزنس ممبرشپ پلانز (5,000/ماہ)</button>
                <button onclick="showTab('users')" id="btnTabUsers" class="tab-btn">تمام صارفین کا ریکارڈ (Ledger)</button>
            </div>

            <div id="tabApprovals">
                <table>
                    <thead>
                        <tr><th>نمبر</th><th>صارف و قسم</th><th>معاہدہ</th><th>رسید</th><th>ایکشن</th></tr>
                    </thead>
                    <tbody>{rows_html if records else "<tr><td colspan='5' style='text-align:center; padding:20px;'>کوئی معاہدہ موجود نہیں۔</td></tr>"}</tbody>
                </table>
            </div>

            <div id="tabBusiness" style="display:none;">
                <table>
                    <thead>
                        <tr><th>ID</th><th>کاروباری ادارہ / نام</th><th>رابطہ</th><th>5,000 روپے رسید</th><th>ایکشن</th></tr>
                    </thead>
                    <tbody>{biz_rows_html if biz_users else "<tr><td colspan='5' style='text-align:center; padding:20px;'>کوئی بزنس اکاؤنٹ موجود نہیں۔</td></tr>"}</tbody>
                </table>
            </div>

            <div id="tabUsers" style="display:none;">
                <table>
                    <thead>
                        <tr><th>ID</th><th>نام و ای میل</th><th>فون</th><th>اکاؤنٹ</th><th style="text-align:center;">کل مسودات</th><th style="text-align:center;">پرنٹس</th><th>تاریخ</th></tr>
                    </thead>
                    <tbody>{users_rows_html if users_ledger else "<tr><td colspan='7' style='text-align:center; padding:20px;'>کوئی ریکارڈ نہیں۔</td></tr>"}</tbody>
                </table>
            </div>
        </div>

        <script>
            function showTab(tab) {{
                const app = document.getElementById('tabApprovals');
                const biz = document.getElementById('tabBusiness');
                const usr = document.getElementById('tabUsers');
                const bApp = document.getElementById('btnTabApp');
                const bBiz = document.getElementById('btnTabBiz');
                const bUsr = document.getElementById('btnTabUsers');
                app.style.display = 'none'; biz.style.display = 'none'; usr.style.display = 'none';
                bApp.className = 'tab-btn'; bBiz.className = 'tab-btn'; bUsr.className = 'tab-btn';

                if (tab === 'approvals') {{
                    app.style.display = 'block'; bApp.className = 'tab-btn tab-active';
                }} else if (tab === 'business') {{
                    biz.style.display = 'block'; bBiz.className = 'tab-btn tab-active';
                }} else {{
                    usr.style.display = 'block'; bUsr.className = 'tab-btn tab-active';
                }}
            }}
        </script>
    </body>
    </html>
    """)

@app.get("/system-control-3284/approve/{record_id}")
async def approve_record(record_id: int, request: Request):
    if request.cookies.get("sec_adm_token") != ADMIN_PASSCODE:
        return HTMLResponse("Unauthorized", status_code=401)
    
    supabase.table("ss_records").update({"status": "approved"}).eq("id", record_id).execute()
    return RedirectResponse(url="/system-control-3284")

@app.get("/system-control-3284/reject/{record_id}")
async def reject_record(record_id: int, request: Request):
    if request.cookies.get("sec_adm_token") != ADMIN_PASSCODE:
        return HTMLResponse("Unauthorized", status_code=401)
    
    supabase.table("ss_records").update({"status": "rejected"}).eq("id", record_id).execute()
    return RedirectResponse(url="/system-control-3284")

@app.get("/system-control-3284/approve-sub/{user_id}")
async def approve_sub(user_id: int, request: Request):
    if request.cookies.get("sec_adm_token") != ADMIN_PASSCODE:
        return HTMLResponse("Unauthorized", status_code=401)
    
    start_dt = datetime.now()
    end_dt = start_dt + timedelta(days=30)
    start_str = start_dt.strftime("%Y-%m-%d %H:%M:%S")
    end_str = end_dt.strftime("%Y-%m-%d %H:%M:%S")

    supabase.table("ss_users").update({
        "subscription_status": "active",
        "subscription_start": start_str,
        "subscription_end": end_str
    }).eq("id", user_id).execute()

    return RedirectResponse(url="/system-control-3284")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)