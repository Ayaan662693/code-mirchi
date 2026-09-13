import collections
from functools import wraps
import hmac
import json
import logging
import os
import re
import threading
import time
from flask import Flask, jsonify, request, send_from_directory, redirect, Response
from flask_cors import CORS
import database
import backup

# --- Structured Security Logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [SECURITY] %(message)s"
)
security_logger = logging.getLogger("codemirchi.security")

app = Flask(__name__, static_folder=".")

# Hardened CORS policy: Scope API routes to designated web origins
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://127.0.0.1:*",
            "http://localhost:*",
            "https://launchpadindia.dev",
            "https://*.launchpadindia.dev"
        ]
    }
})

# Ensure database is initialized
database.init_db()

# --- Rate Limiting Infrastructure ---
rate_limit_records = collections.defaultdict(list)

def is_rate_limited(key, max_requests, window_seconds):
    now = time.time()
    timestamps = rate_limit_records[key]
    # Prune expired timestamps
    rate_limit_records[key] = [ts for ts in timestamps if now - ts < window_seconds]
    if len(rate_limit_records[key]) >= max_requests:
        return True
    rate_limit_records[key].append(now)
    return False

def rate_limit(max_requests=30, window_seconds=60):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            ip = request.headers.get("X-Forwarded-For", request.remote_addr or "127.0.0.1").split(",")[0].strip()
            key = f"{ip}:{request.endpoint}"
            if is_rate_limited(key, max_requests, window_seconds):
                security_logger.warning(f"Rate limit exceeded for IP: {ip} on endpoint: {request.endpoint}")
                return jsonify({
                    "error": "Too Many Requests. Please slow down.",
                    "retry_after_seconds": window_seconds
                }), 429
            return f(*args, **kwargs)
        return wrapped
    return decorator

# --- Admin Authorization ---
ADMIN_API_KEY = os.environ.get("ADMIN_API_KEY", "launchpad-admin-secret-key-2026")

def require_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        provided_key = request.headers.get("X-Admin-Key") or request.args.get("api_key")
        if not provided_key or not hmac.compare_digest(str(provided_key), ADMIN_API_KEY):
            ip = request.headers.get("X-Forwarded-For", request.remote_addr or "127.0.0.1").split(",")[0].strip()
            security_logger.warning(f"Unauthorized admin access attempt from IP: {ip} on {request.path}")
            return jsonify({"error": "Unauthorized. Provide a valid X-Admin-Key header."}), 401
        return f(*args, **kwargs)
    return decorated

# --- HTTPS & Security Headers Middleware ---

@app.before_request
def enforce_https():
    # In production behind proxies (Cloudflare, Render, AWS, Heroku)
    # redirect HTTP to HTTPS
    if request.headers.get("X-Forwarded-Proto") == "http":
        url = request.url.replace("http://", "https://", 1)
        return redirect(url, code=301)

@app.after_request
def add_security_headers(response):
    # HSTS (Strict-Transport-Security)
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"
    # Prevent MIME-type sniffing
    response.headers["X-Content-Type-Options"] = "nosniff"
    # Clickjacking protection
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    # Referrer policy
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    # Permissions policy
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    # Content Security Policy
    response.headers["Content-Security-Policy"] = (
        "default-src 'self' https:; "
        "font-src 'self' https://fonts.gstatic.com data:; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
        "script-src 'self' 'unsafe-inline' https://esm.sh; "
        "img-src 'self' data: https:; "
        "connect-src 'self' http://127.0.0.1:* http://localhost:* https: https://esm.sh;"
    )
    return response

# --- Static & SEO Routes (Hardened Whitelisting) ---

ALLOWED_PUBLIC_FILES = {
    "robots.txt", "sitemap.xml", "favicon.ico", "roadmap.html", "roadmaps_data.js", "india_map_data.js",
    "logo.svg", "logo.png",
    "degree-roadmaps", "find-a-hackathon", "team-finder", "squad-up", "internships", "hiring-board", "freshers-hiring", "freshers-guide", "resource-shelf",
    "project-vault", "projects", "blueprints", "project-ideas",
    "resume-builder", "ats-checker", "portfolio-builder", "portfolio", "resume-audit"
}
ALLOWED_PUBLIC_EXTENSIONS = {".html", ".css", ".js", ".png", ".jpg", ".jpeg", ".svg", ".webp", ".ico", ".json", ".xml", ".txt", ".woff", ".woff2"}
DENIED_EXTENSIONS = {".db", ".py", ".sh", ".env", ".sqlite", ".sqlite3", ".bak", ".tar", ".gz", ".zip", ".md", ".log"}

@app.route("/")
@app.route("/degree-roadmaps")
@app.route("/find-a-hackathon")
@app.route("/team-finder")
@app.route("/squad-up")
@app.route("/internships")
@app.route("/hiring-board")
@app.route("/freshers-hiring")
@app.route("/project-vault")
@app.route("/projects")
@app.route("/blueprints")
@app.route("/project-ideas")
@app.route("/resume-builder")
@app.route("/ats-checker")
@app.route("/portfolio-builder")
@app.route("/portfolio")
@app.route("/resume-audit")
@app.route("/freshers-guide")
@app.route("/resource-shelf")
def index():
    return send_from_directory(".", "index.html")

@app.route("/roadmap")
@app.route("/roadmap.html")
@app.route("/roadmaps")
def roadmap_redirect():
    return redirect("/degree-roadmaps", code=302)

@app.route("/robots.txt")
def robots():
    return send_from_directory(".", "robots.txt", mimetype="text/plain")

@app.route("/sitemap.xml")
def sitemap():
    return send_from_directory(".", "sitemap.xml", mimetype="application/xml")

@app.route("/<path:path>")
def static_files(path):
    normalized_path = os.path.normpath(path).lstrip("/")
    # Block path traversal, hidden files, and restricted backup directories
    if normalized_path.startswith("..") or "backups" in normalized_path.split(os.sep) or normalized_path.startswith("."):
        security_logger.warning(f"Blocked directory traversal attempt: {path}")
        return jsonify({"error": "Access denied"}), 403

    ext = os.path.splitext(normalized_path)[1].lower()
    if ext in DENIED_EXTENSIONS or normalized_path in {"app.py", "database.py", "backup.py", "run.sh", "launchpad.db"}:
        security_logger.warning(f"Blocked forbidden file download attempt: {normalized_path}")
        return jsonify({"error": "Access to internal system files is forbidden"}), 403

    if (normalized_path in ALLOWED_PUBLIC_FILES or ext in ALLOWED_PUBLIC_EXTENSIONS) and os.path.exists(normalized_path):
        return send_from_directory(".", normalized_path)
    return send_from_directory(".", "index.html")

# --- Health Check ---

@app.route("/api/health", methods=["GET"])
def health_endpoint():
    return jsonify({"status": "ok", "service": "CODE MIRCHI", "version": "2.0"})

# --- Events API ---

@app.route("/api/events", methods=["GET"])
def get_events():
    events = database.get_all_events()
    return jsonify({"events": events, "count": len(events)})

@app.route("/api/events", methods=["POST"])
@rate_limit(max_requests=10, window_seconds=60)
def create_event():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON payload"}), 400

    name = str(data.get("name", "")).strip()
    start = str(data.get("start", "")).strip()
    end = str(data.get("end", "")).strip()
    url = str(data.get("url", "")).strip()

    if not name or not start or not end:
        return jsonify({"error": "Name, start date, and end date are required"}), 400

    if len(name) > 200:
        return jsonify({"error": "Event name exceeds 200 characters limit"}), 400

    # Validate URL scheme to prevent XSS (e.g. javascript:) and enforce http/https
    if url and url != "#":
        if not (url.startswith("https://") or url.startswith("http://")):
            security_logger.warning(f"Invalid URL scheme rejected: {url}")
            return jsonify({"error": "Event URL must start with http:// or https://"}), 400
        if len(url) > 500:
            return jsonify({"error": "Event URL exceeds 500 characters limit"}), 400

    cleaned_data = {
        "name": name,
        "organizer": str(data.get("organizer", "Student Chapter")).strip()[:200],
        "mode": str(data.get("mode", "Offline")).strip()[:50],
        "city": str(data.get("city", "Pan-India")).strip()[:100],
        "start": start[:20],
        "end": end[:20],
        "tags": data.get("tags") or "Innovation",
        "url": url or "#",
        "note": str(data.get("note", "Verified opportunity")).strip()[:500]
    }

    event_id = database.add_event(cleaned_data)
    security_logger.info(f"New event created: id={event_id}, name={name}")
    return jsonify({
        "success": True,
        "id": event_id,
        "message": "Hackathon added successfully"
    }), 201

# --- Squad Up (Hackathon Teammate Finder) API ---

@app.route("/api/squads", methods=["GET"])
def get_squads_endpoint():
    role_filter = request.args.get("role")
    hackathon_filter = request.args.get("hackathon")
    squads = database.get_all_squads(role_filter=role_filter, hackathon_filter=hackathon_filter)
    return jsonify({"squads": squads, "count": len(squads)})

@app.route("/api/squads", methods=["POST"])
@rate_limit(max_requests=10, window_seconds=60)
def create_squad_endpoint():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON payload"}), 400

    project_title = str(data.get("project_title", "")).strip()
    hackathon_name = str(data.get("hackathon_name", "")).strip()
    leader_name = str(data.get("leader_name", "")).strip()
    description = str(data.get("description", "")).strip()
    contact_value = str(data.get("contact_value", "")).strip()

    if not project_title or not hackathon_name or not leader_name or not description or not contact_value:
        return jsonify({"error": "Project title, hackathon name, leader name, description, and contact info are required"}), 400

    if len(project_title) > 200:
        return jsonify({"error": "Project title exceeds 200 characters limit"}), 400
    if len(hackathon_name) > 200:
        return jsonify({"error": "Hackathon name exceeds 200 characters limit"}), 400
    if len(leader_name) > 100:
        return jsonify({"error": "Leader name exceeds 100 characters limit"}), 400
    if len(description) > 1500:
        return jsonify({"error": "Description exceeds 1500 characters limit"}), 400

    roles_raw = data.get("roles_needed")
    if isinstance(roles_raw, list):
        roles_needed = [str(r).strip()[:50] for r in roles_raw if str(r).strip()][:8]
    elif isinstance(roles_raw, str) and roles_raw.strip():
        roles_needed = [r.strip()[:50] for r in roles_raw.split(",") if r.strip()][:8]
    else:
        roles_needed = ["Full-Stack Dev"]

    tech_raw = data.get("tech_stack")
    if isinstance(tech_raw, list):
        tech_stack = [str(t).strip()[:50] for t in tech_raw if str(t).strip()][:8]
    elif isinstance(tech_raw, str) and tech_raw.strip():
        tech_stack = [t.strip()[:50] for t in tech_raw.split(",") if t.strip()][:8]
    else:
        tech_stack = ["React", "Python"]

    try:
        current_members = max(1, min(10, int(data.get("current_members", 1))))
        team_size = max(current_members, min(10, int(data.get("team_size", 4))))
    except (ValueError, TypeError):
        current_members = 1
        team_size = 4

    contact_type = str(data.get("contact_type", "Discord")).strip()[:30]
    if contact_type not in {"Discord", "LinkedIn", "Telegram", "Email", "GitHub", "Twitter"}:
        contact_type = "Discord"

    # Safety check on contact_value to prevent javascript: or dangerous URI schemes
    if contact_value.lower().startswith("javascript:") or contact_value.lower().startswith("data:"):
        return jsonify({"error": "Invalid contact information provided"}), 400

    cleaned_data = {
        "hackathon_id": str(data.get("hackathon_id", "")).strip()[:100],
        "hackathon_name": hackathon_name,
        "project_title": project_title,
        "leader_name": leader_name,
        "leader_college": str(data.get("leader_college", "Campus Developer")).strip()[:150],
        "roles_needed": roles_needed,
        "current_members": current_members,
        "team_size": team_size,
        "tech_stack": tech_stack,
        "description": description,
        "contact_type": contact_type,
        "contact_value": contact_value[:200],
        "status": "Open"
    }

    squad_id = database.add_squad_post(cleaned_data)
    security_logger.info(f"New squad pitch created: id={squad_id}, title={project_title}")
    return jsonify({
        "success": True,
        "id": squad_id,
        "message": "Squad pitch posted successfully"
    }), 201

@app.route("/api/squads/<squad_id>/toggle", methods=["POST"])
@rate_limit(max_requests=30, window_seconds=60)
def toggle_squad_status_endpoint(squad_id):
    new_status = database.toggle_squad_status(squad_id)
    if not new_status:
        return jsonify({"error": "Squad post not found"}), 404
    return jsonify({"id": squad_id, "status": new_status})

# --- Freshers Internships & Off-Campus Hiring Board API ---

@app.route("/api/opportunities", methods=["GET"])
def get_opportunities_endpoint():
    type_filter = request.args.get("type")
    batch_filter = request.args.get("batch")
    category_filter = request.args.get("category")
    search_query = request.args.get("q")
    opps = database.get_all_opportunities(
        type_filter=type_filter,
        batch_filter=batch_filter,
        category_filter=category_filter,
        search_query=search_query
    )
    return jsonify({"opportunities": opps, "count": len(opps)})

@app.route("/api/opportunities/<opp_id>", methods=["GET"])
def get_opportunity_detail_endpoint(opp_id):
    opp = database.get_opportunity_by_id(opp_id)
    if not opp:
        return jsonify({"error": "Opportunity not found"}), 404
    return jsonify(opp)

@app.route("/api/opportunities", methods=["POST"])
@rate_limit(max_requests=10, window_seconds=60)
def create_opportunity_endpoint():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON payload"}), 400

    company = str(data.get("company", "")).strip()
    role_title = str(data.get("role_title") or data.get("title") or "").strip()
    apply_url = str(data.get("apply_url", "")).strip()
    description = str(data.get("description", "")).strip()

    if not company or not role_title or not apply_url:
        return jsonify({"error": "Company name, role title, and application URL are required"}), 400

    if len(company) > 100:
        return jsonify({"error": "Company name exceeds 100 characters"}), 400
    if len(role_title) > 200:
        return jsonify({"error": "Role title exceeds 200 characters"}), 400
    if len(description) > 2000:
        return jsonify({"error": "Description exceeds 2000 characters"}), 400

    if not (apply_url.startswith("http://") or apply_url.startswith("https://")):
        return jsonify({"error": "Application URL must start with http:// or https://"}), 400

    batches = data.get("eligible_batches") or data.get("batches")
    if isinstance(batches, list):
        eligible_batches = [str(b).strip()[:30] for b in batches if str(b).strip()][:5]
    elif isinstance(batches, str) and batches.strip():
        eligible_batches = [b.strip()[:30] for b in batches.split(",") if b.strip()][:5]
    else:
        eligible_batches = ["2026 Batch", "2027 Batch"]

    skills_raw = data.get("skills")
    if isinstance(skills_raw, list):
        skills = [str(s).strip()[:40] for s in skills_raw if str(s).strip()][:8]
    elif isinstance(skills_raw, str) and skills_raw.strip():
        skills = [s.strip()[:40] for s in skills_raw.split(",") if s.strip()][:8]
    else:
        skills = ["DSA", "Problem Solving"]

    cleaned_data = {
        "company": company,
        "role_title": role_title,
        "opportunity_type": str(data.get("opportunity_type") or data.get("type") or "Summer Internship").strip()[:50],
        "eligible_batches": eligible_batches,
        "role_category": str(data.get("role_category") or data.get("category") or "Software Engineering").strip()[:50],
        "location": str(data.get("location", "Pan-India / Remote")).strip()[:100],
        "stipend_or_ctc": str(data.get("stipend_or_ctc") or data.get("stipend") or "Competitive").strip()[:50],
        "apply_url": apply_url[:500],
        "deadline": str(data.get("deadline", "Rolling Apply")).strip()[:50],
        "description": description,
        "skills": skills,
        "selection_process": str(data.get("selection_process") or data.get("rounds") or "Online Assessment + Technical Interviews").strip()[:500],
        "status": "Active",
        "featured": 0
    }

    opp_id = database.add_opportunity(cleaned_data)
    security_logger.info(f"New opportunity created: id={opp_id}, company={company}")
    return jsonify({
        "success": True,
        "id": opp_id,
        "message": "Opportunity posted successfully"
    }), 201

@app.route("/api/saved-opportunities", methods=["GET"])
def get_saved_opportunities_endpoint():
    saved_ids = database.get_saved_opportunities()
    return jsonify({"saved": saved_ids, "saved_ids": saved_ids, "count": len(saved_ids)})

@app.route("/api/saved-opportunities/<opp_id>/toggle", methods=["POST"])
@rate_limit(max_requests=60, window_seconds=60)
def toggle_saved_opportunity_endpoint(opp_id):
    saved = database.toggle_saved_opportunity(opp_id)
    return jsonify({"opportunity_id": opp_id, "saved": saved})

# --- Project Idea Vault & Architecture Blueprints API ---

@app.route("/api/projects", methods=["GET"])
def get_projects_endpoint():
    level = request.args.get("level")
    domain = request.args.get("domain")
    search = request.args.get("search") or request.args.get("q")
    projects = database.get_all_projects(level=level, domain=domain, search=search)
    return jsonify({"projects": projects, "count": len(projects)})

@app.route("/api/projects/<project_id>", methods=["GET"])
def get_project_detail_endpoint(project_id):
    proj = database.get_project_by_id(project_id)
    if not proj:
        return jsonify({"error": "Project blueprint not found"}), 404
    return jsonify({"project": proj})

@app.route("/api/projects", methods=["POST"])
@rate_limit(max_requests=20, window_seconds=60)
def create_project_endpoint():
    data = request.get_json() or {}
    title = data.get("title", "").strip()
    tagline = data.get("tagline", "").strip()
    problem = data.get("problem_statement", "").strip()

    if not title:
        return jsonify({"error": "Project title is required."}), 400
    if not problem and not tagline:
        return jsonify({"error": "Tagline or Problem Statement is required."}), 400

    new_id = database.add_project(data)
    created = database.get_project_by_id(new_id)
    return jsonify({
        "success": True,
        "id": new_id,
        "project": created,
        "message": "Architecture Blueprint published to Community Vault!"
    }), 201

@app.route("/api/saved-projects", methods=["GET"])
def get_saved_projects_endpoint():
    saved_ids = database.get_saved_projects()
    return jsonify({"saved": saved_ids, "saved_ids": saved_ids, "count": len(saved_ids)})

@app.route("/api/saved-projects/<project_id>/toggle", methods=["POST"])
@rate_limit(max_requests=60, window_seconds=60)
def toggle_saved_project_endpoint(project_id):
    saved = database.toggle_saved_project(project_id)
    return jsonify({"project_id": project_id, "saved": saved})

# --- Bookmarks API ---

@app.route("/api/saved-events", methods=["GET"])
def get_saved_events():
    saved_ids = database.get_saved_event_ids()
    return jsonify({"saved": saved_ids})

@app.route("/api/saved-events/<event_id>/toggle", methods=["POST"])
@rate_limit(max_requests=60, window_seconds=60)
def toggle_saved(event_id):
    saved = database.toggle_saved_event(event_id)
    return jsonify({
        "event_id": event_id,
        "saved": saved,
        "message": "Event saved" if saved else "Event removed from saved"
    })

# --- Resources API ---

@app.route("/api/resources", methods=["GET"])
def get_resources():
    category = request.args.get("category", "all")
    resources = database.get_all_resources(category)
    return jsonify({"resources": resources})

@app.route("/api/resources/<int:resource_id>/like", methods=["POST"])
@rate_limit(max_requests=30, window_seconds=60)
def like_resource_endpoint(resource_id):
    new_likes = database.like_resource(resource_id)
    return jsonify({"id": resource_id, "likes": new_likes})

# --- Degrees & 8-Semester Roadmaps API ---

@app.route("/api/degrees", methods=["GET"])
def get_degrees_endpoint():
    degrees = database.get_degrees()
    prefs = database.get_user_preferences()
    selected_degree = prefs.get("selected_degree", "btech_cse")
    return jsonify({"degrees": degrees, "selected_degree": selected_degree})

@app.route("/api/roadmap", methods=["GET"])
def get_degree_roadmap_endpoint():
    prefs = database.get_user_preferences()
    default_degree = prefs.get("selected_degree", "btech_cse")
    degree_id = request.args.get("degree", default_degree)
    semester_num = request.args.get("semester")

    data = database.get_degree_roadmap(degree_id, semester_num)
    return jsonify(data)

@app.route("/api/roadmap/toggle", methods=["POST"])
@rate_limit(max_requests=60, window_seconds=60)
def toggle_task_endpoint():
    data = request.get_json() or {}
    task_id = data.get("task_id")
    degree_id = data.get("degree_id", "btech_cse")
    semester_num = data.get("semester_number")

    if not task_id:
        return jsonify({"error": "task_id is required"}), 400

    completed = data.get("completed")
    new_status = database.toggle_task(task_id, completed)

    roadmap_data = database.get_degree_roadmap(degree_id, semester_num)
    return jsonify({
        "task_id": task_id,
        "completed": new_status,
        "roadmap": roadmap_data
    })

# --- Preferences API ---

@app.route("/api/preferences", methods=["GET", "POST"])
def preferences_endpoint():
    if request.method == "POST":
        data = request.get_json() or {}
        for k, v in data.items():
            database.set_user_preference(str(k)[:50], str(v)[:100])
        return jsonify({"success": True, "preferences": database.get_user_preferences()})
    return jsonify(database.get_user_preferences())

# --- Global Stats API ---

@app.route("/api/stats", methods=["GET"])
def get_stats_endpoint():
    degree_id = request.args.get("degree", "btech_cse")
    stats = database.get_stats(degree_id)
    return jsonify(stats)

# --- Freshers ATS Resume Checker & Portfolio Builder APIs ---

@app.route("/api/portfolio/sample", methods=["GET"])
def get_portfolio_sample():
    role = request.args.get("role", "fullstack").lower()
    samples = {
        "fullstack": {
            "name": "Arjun Mehta",
            "role": "Full-Stack & Distributed Systems Developer",
            "tagline": "Building high-throughput web architectures, real-time sync engines, and production APIs.",
            "location": "Bengaluru / Delhi NCR, India",
            "available_for": "Summer 2026 SDE Internship / 6-Month Co-op",
            "github": "https://github.com/arjunmehta-dev",
            "linkedin": "https://linkedin.com/in/arjunmehtadev",
            "twitter": "https://x.com/arjun_codes",
            "email": "arjun.mehta.codes@gmail.com",
            "website": "https://arjunmehta.dev",
            "skills": {
                "languages": ["TypeScript", "Go (Golang)", "Python", "C++", "SQL"],
                "frameworks": ["React", "Next.js", "Node.js", "FastAPI", "TailwindCSS"],
                "databases": ["PostgreSQL", "Redis", "MongoDB", "ClickHouse"],
                "devops": ["Docker", "Kubernetes", "AWS (S3/EC2)", "Kafka", "GitHub Actions", "Prometheus"]
            },
            "projects": [
                {
                    "title": "Distributed Rate Limiter & Reverse Proxy",
                    "description": "High-throughput token-bucket & sliding-window edge proxy capable of throttling 100k+ req/sec with sub-millisecond atomic Lua operations in Redis.",
                    "stack": ["Go", "Redis", "Lua", "Docker", "Prometheus"],
                    "live_url": "https://proxy.arjunmehta.dev",
                    "github_url": "https://github.com/arjunmehta-dev/edge-rate-limiter",
                    "metric": "Throttles 100k+ req/sec with p99 latency <1.4ms across 3 distributed nodes."
                },
                {
                    "title": "Real-Time Collaborative Canvas (CRDTs)",
                    "description": "Multiplayer whiteboard supporting concurrent freehand drawing, sticky notes, and conflict-free real-time state synchronization using Yjs and WebSockets.",
                    "stack": ["TypeScript", "React", "Node.js", "WebSockets", "Yjs", "Redis"],
                    "live_url": "https://canvas.arjunmehta.dev",
                    "github_url": "https://github.com/arjunmehta-dev/collab-canvas",
                    "metric": "Maintains sub-50ms peer update propagation for 60+ simultaneous room participants."
                },
                {
                    "title": "UPI Microservices Payment Gateway Switch",
                    "description": "Financial routing engine simulating high-availability UPI transactions with Saga distributed orchestrations, idempotency locks, and dead-letter queues.",
                    "stack": ["Java", "Spring Boot", "Kafka", "PostgreSQL", "Resilience4j"],
                    "live_url": "https://pay.arjunmehta.dev",
                    "github_url": "https://github.com/arjunmehta-dev/upi-switch",
                    "metric": "Achieves zero double-debit anomalies across 50,000 simulated concurrent orders."
                }
            ],
            "education": {
                "college": "Delhi Technological University (DTU)",
                "degree": "B.Tech in Computer Science & Engineering",
                "batch": "2022 - 2026",
                "cgpa": "8.8 / 10.0",
                "highlight": "National Finalist, Smart India Hackathon 2024 • Top 1.5% in LeetCode (Knight, 1950+ Rating)"
            }
        },
        "aiml": {
            "name": "Priya Sharma",
            "role": "AI/ML Systems & GenAI Research Engineer",
            "tagline": "Crafting cross-lingual RAG pipelines, fine-tuned transformer architectures, and low-latency inference endpoints.",
            "location": "Hyderabad / Pune, India",
            "available_for": "Summer 2027 AI Internship / Research Fellow",
            "github": "https://github.com/priyasharma-ai",
            "linkedin": "https://linkedin.com/in/priyasharma-ai",
            "twitter": "https://x.com/priya_ml",
            "email": "priya.sharma.ml@gmail.com",
            "website": "https://priyasharma.ai",
            "skills": {
                "languages": ["Python", "C++", "SQL", "TypeScript"],
                "frameworks": ["PyTorch", "FastAPI", "Hugging Face", "LangChain", "vLLM"],
                "databases": ["pgvector", "Qdrant", "ChromaDB", "PostgreSQL", "Redis"],
                "devops": ["Docker", "Triton Server", "MLflow", "Weights & Biases", "GCP Vertex AI"]
            },
            "projects": [
                {
                    "title": "Multilingual Legal RAG Engine",
                    "description": "Cross-lingual document question-answering system for Indian legal statutes & govt gazettes across Hindi, Tamil, Telugu, and English with verifiable citations.",
                    "stack": ["Python", "FastAPI", "pgvector", "BGE-M3", "Llama-3", "Docker"],
                    "live_url": "https://legal-rag.priyasharma.ai",
                    "github_url": "https://github.com/priyasharma-ai/multilingual-rag",
                    "metric": "Delivers 94.2% retrieval recall across 15,000 gazette pages with <850ms time-to-first-token."
                },
                {
                    "title": "Automated AST Code Vulnerability Auditor",
                    "description": "Static analysis bot parsing syntax trees with Tree-sitter to detect OWASP security flaws, enriched with quantized local LLMs for suggested patches.",
                    "stack": ["Python", "Tree-sitter", "FastAPI", "GitHub API", "Ollama"],
                    "live_url": "https://auditbot.priyasharma.ai",
                    "github_url": "https://github.com/priyasharma-ai/ast-sec-bot",
                    "metric": "Detected 32 zero-day regex injection risks in open-source collegiate repositories."
                }
            ],
            "education": {
                "college": "IIIT Hyderabad",
                "degree": "B.Tech in Artificial Intelligence & Machine Learning",
                "batch": "2023 - 2027",
                "cgpa": "9.1 / 10.0",
                "highlight": "Published undergraduate preprint on cross-lingual embedding quantization."
            }
        }
    }
    selected = samples.get(role, samples["fullstack"])
    return jsonify(selected)

@app.route("/api/resume/analyze", methods=["POST"])
@rate_limit(max_requests=40, window_seconds=60)
def analyze_resume():
    data = request.get_json() or {}
    text = data.get("text", "").strip()

    if not text:
        return jsonify({"error": "No resume text provided for analysis"}), 400

    lower_text = text.lower()
    word_count = len(text.split())

    # Heuristic Checks
    # 1. Live URLs & Repos
    has_github = bool(re.search(r"github\.com/[a-zA-Z0-9_\-]+", text))
    has_linkedin = bool(re.search(r"linkedin\.com/in/[a-zA-Z0-9_\-]+", text))
    live_deploy_domains = ["vercel.app", "netlify.app", "render.com", "railway.app", "github.io", "fly.dev", "onrender.com", "herokuapp.com", "surge.sh", "pages.dev"]
    found_live_urls = [dom for dom in live_deploy_domains if dom in lower_text]
    generic_url_matches = re.findall(r"https?://[^\s<>\"']+", text)

    # 2. Action Verbs
    strong_verbs = [
        "architected", "engineered", "designed", "implemented", "benchmarked",
        "containerized", "reduced", "accelerated", "orchestrated", "automated",
        "integrated", "spearheaded", "refactored", "optimized", "streamlined",
        "deployed", "migrated", "scaled", "profiled", "secured", "constructed"
    ]
    found_strong_verbs = list(set([v for v in strong_verbs if re.search(r"\b" + v + r"\b", lower_text)]))

    # Weak/Passive Verbs
    weak_verbs = [
        "worked on", "responsible for", "helped in", "assisted with",
        "learned", "tried", "participated in", "involved in", "handled basics", "familiar with"
    ]
    found_weak_verbs = [w for w in weak_verbs if w in lower_text]

    # 3. Measurable Metrics (XYZ formula)
    metric_patterns = [
        r"\b\d+%\b",               # percentages (e.g. 40%)
        r"\b\d+\+?\s?ms\b",        # latency (e.g. 50ms)
        r"\b\d+k\+?\b",            # k scale (e.g. 10k, 50k+)
        r"\b\d+\s?(req/s|rps|tps)\b", # throughput
        r"\b(top\s\d+|rank\s\d+)\b",  # rankings
        r"\b\d+\+?\s?(users|teams|stars|forks|downloads)\b" # counts
    ]
    found_metrics = []
    for pat in metric_patterns:
        matches = re.findall(pat, lower_text)
        if matches:
            found_metrics.extend(matches)

    # 4. Fresher Red Flags
    red_flag_triggers = {
        "High School Board / Roll No": [r"\b(10th|12th|cbse|icse|matriculation|intermediate|ssc|hsc)\b"],
        "Declaration Clause": [r"\bhereby declare\b", r"\btrue to the best of my knowledge\b", r"\bdeclaration\b"],
        "Personal Details Clutter": [r"\bfather'?s? name\b", r"\bmarital status\b", r"\bdate of birth\b", r"\bd\.o\.b\b", r"\bpermanent address\b"],
        "Vague Hobbies": [r"\bhobbies:? (listening to music|cricket|watching movies|reading books|travelling)\b"],
        "Skill Bars / Percentages": [r"(proficiency:?\s?\d+%)", r"(rating:?\s?\d+/10)"]
    }
    found_red_flags = []
    for label, patterns in red_flag_triggers.items():
        for pat in patterns:
            if re.search(pat, lower_text):
                found_red_flags.append(label)
                break

    # 5. ATS Section Headers
    standard_headers = ["education", "experience", "projects", "skills", "technical skills", "achievements", "certifications"]
    found_headers = [h for h in standard_headers if h in lower_text]

    # Score Calculation (Total 100)
    score_proof = 0
    if has_github: score_proof += 10
    if has_linkedin: score_proof += 5
    if found_live_urls or len(generic_url_matches) >= 2: score_proof += 10
    score_proof = min(25, score_proof)

    score_metrics = min(25, len(found_metrics) * 6 + (5 if len(found_strong_verbs) >= 4 else 0))

    score_verbs = min(25, len(found_strong_verbs) * 5 - len(found_weak_verbs) * 4)
    score_verbs = max(0, score_verbs)

    score_structure = 15
    if len(found_headers) >= 3: score_structure += 10
    if found_red_flags: score_structure -= len(found_red_flags) * 5
    score_structure = max(0, min(25, score_structure))

    total_score = score_proof + score_metrics + score_verbs + score_structure
    total_score = max(5, min(100, total_score))

    if total_score >= 88:
        grade = "Top 5% Recruiter Magnet 🔥"
        badge_class = "grade-elite"
        summary = "Exceptional fresher resume. Demonstrates live project proof, quantifiable XYZ impact metrics, and clean ATS parser formatting."
    elif total_score >= 72:
        grade = "Competitive Candidate ⚡"
        badge_class = "grade-competitive"
        summary = "Solid baseline. Add 1-2 live deployed project URLs and replace passive phrasing with specific benchmarks."
    elif total_score >= 50:
        grade = "Needs Measurable Proof ⚠️"
        badge_class = "grade-warning"
        summary = "Contains generic descriptions. Lacks verified live URLs or quantifiable scale metrics (%, ms, req/sec)."
    else:
        grade = "High ATS Rejection Risk 🚨"
        badge_class = "grade-danger"
        summary = "Critical red flags detected. Contains high-school clutter or passive language that will get filtered out by modern ATS parsers."

    bullet_rewrites = [
        {
            "weak": "Worked on a food delivery app using React and Node.js.",
            "strong": "Architected a full-stack food delivery app with React and Node.js; cut checkout latency by 35% through Redis query caching."
        },
        {
            "weak": "Responsible for machine learning model training and testing.",
            "strong": "Engineered a multilingual RAG pipeline using FastAPI and pgvector, achieving 94% retrieval accuracy across 5,000 documents."
        },
        {
            "weak": "Made a chat application using socket programming.",
            "strong": "Implemented a real-time collaborative chat engine with WebSockets and Redis Pub/Sub, sustaining 1,500 concurrent connections at <45ms jitter."
        }
    ]

    return jsonify({
        "score": total_score,
        "grade": grade,
        "badge_class": badge_class,
        "summary": summary,
        "word_count": word_count,
        "breakdown": {
            "proof_score": score_proof,
            "metrics_score": score_metrics,
            "verbs_score": score_verbs,
            "structure_score": score_structure
        },
        "findings": {
            "has_github": has_github,
            "has_linkedin": has_linkedin,
            "live_urls_detected": len(found_live_urls) > 0 or len(generic_url_matches) >= 2,
            "strong_verbs_count": len(found_strong_verbs),
            "strong_verbs_list": found_strong_verbs[:6],
            "weak_verbs_found": found_weak_verbs,
            "metrics_found_count": len(found_metrics),
            "red_flags": found_red_flags
        },
        "bullet_rewrites": bullet_rewrites
    })

@app.route("/api/portfolio/generate", methods=["POST"])
@rate_limit(max_requests=30, window_seconds=60)
def generate_portfolio_bundle():
    data = request.get_json() or {}
    name = data.get("name") or "Your Name"
    role = data.get("role") or "Full-Stack Developer"
    tagline = data.get("tagline") or "Building high-performance software and distributed systems."
    location = data.get("location") or "India"
    github = data.get("github") or "https://github.com"
    linkedin = data.get("linkedin") or "https://linkedin.com"
    twitter = data.get("twitter") or ""
    email = data.get("email") or "developer@example.com"
    website = data.get("website") or ""

    skills = data.get("skills") or {}
    projects = data.get("projects") or []
    education = data.get("education") or {}

    md_lines = []
    md_lines.append(f"# Hi there, I'm {name} 👋")
    md_lines.append(f"### {role} • 📍 {location}\n")
    md_lines.append(f"> {tagline}\n")

    md_lines.append("## 📬 Connect With Me")
    social_badges = []
    if github:
        social_badges.append(f"[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)]({github})")
    if linkedin:
        social_badges.append(f"[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)]({linkedin})")
    if twitter:
        social_badges.append(f"[![X](https://img.shields.io/badge/X-000000?style=for-the-badge&logo=x&logoColor=white)]({twitter})")
    if email:
        social_badges.append(f"[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:{email})")
    md_lines.append(" ".join(social_badges) + "\n")

    md_lines.append("## 🛠️ Technical Skills")
    for category, skill_list in skills.items():
        if skill_list:
            formatted_cat = category.capitalize()
            skills_str = " • ".join([f"`{s}`" for s in skill_list])
            md_lines.append(f"- **{formatted_cat}**: {skills_str}")
    md_lines.append("")

    md_lines.append("## 🚀 Featured Engineering Projects")
    for p in projects:
        title = p.get("title", "Project")
        desc = p.get("description", "")
        stack_str = ", ".join(p.get("stack", []))
        metric = p.get("metric", "")
        live_url = p.get("live_url", "")
        repo_url = p.get("github_url", "")

        md_lines.append(f"### ⚡ [{title}]({live_url or repo_url or '#'})")
        md_lines.append(f"{desc}")
        if metric:
            md_lines.append(f"- 📈 **Key Metric / Impact**: {metric}")
        if stack_str:
            md_lines.append(f"- 🧩 **Tech Stack**: `{stack_str}`")
        links = []
        if live_url: links.append(f"[🌐 Live Demo]({live_url})")
        if repo_url: links.append(f"[💻 GitHub Repository]({repo_url})")
        if links:
            md_lines.append(f"- 🔗 {' | '.join(links)}")
        md_lines.append("")

    if education:
        md_lines.append("## 🎓 Education & Credentials")
        col = education.get("college", "")
        deg = education.get("degree", "")
        batch = education.get("batch", "")
        cgpa = education.get("cgpa", "")
        hl = education.get("highlight", "")
        md_lines.append(f"- **{deg}** — {col} ({batch})")
        if cgpa: md_lines.append(f"- **Academic Score**: {cgpa}")
        if hl: md_lines.append(f"- **Notable Recognition**: {hl}")
        md_lines.append("")

    md_lines.append("---\n*Generated with [CODE MIRCHI](https://launchpadindia.dev) • Built for ambitious Indian engineering students.*")
    generated_markdown = "\n".join(md_lines)

    return jsonify({
        "success": True,
        "markdown": generated_markdown
    })

# --- Database Backups API (Protected by @require_admin) ---

@app.route("/api/admin/backup", methods=["POST"])
@require_admin
@rate_limit(max_requests=5, window_seconds=60)
def trigger_backup_endpoint():
    security_logger.info("Admin initiated manual database backup snapshot")
    result = backup.create_backup()
    status_code = 200 if result.get("success") else 500
    return jsonify(result), status_code

@app.route("/api/admin/backups", methods=["GET"])
@require_admin
def list_backups_endpoint():
    backups = backup.list_backups()
    return jsonify({"backups": backups, "count": len(backups)})

# --- Automated Background Backup Scheduler ---

def scheduled_backup_worker():
    """Background worker that takes a snapshot every 12 hours."""
    while True:
        try:
            time.sleep(12 * 3600)  # 12 hours
            backup.create_backup()
        except Exception as e:
            security_logger.error(f"Error in automated backup schedule: {e}")

# Start background backup thread as daemon
backup_thread = threading.Thread(target=scheduled_backup_worker, daemon=True)
backup_thread.start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))
    print(f"🌶️ CODE MIRCHI running on http://127.0.0.1:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)
