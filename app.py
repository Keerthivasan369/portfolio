"""
Keerthivasan Portfolio — Flask Backend
Features: Visitor tracking, Admin panel, Contact messages, Content management
"""

from flask import (Flask, render_template, request, jsonify,
                   redirect, url_for, session)
from functools import wraps
import datetime, json, os, hashlib, uuid

app = Flask(__name__)
app.secret_key = 'keerthivasan_super_secret_2024_$#@!'

# ─────────────────────────────────────────────
#  CONFIG — change password before deploying!
# ─────────────────────────────────────────────
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD_HASH = 'c385818de2ec5e08503aa15270678de34f5b7ae2e1f1dcc663209e9bf14e19f8'
# To set a new password run:
#   python -c "import hashlib; print(hashlib.sha256(b'yourpass').hexdigest())"

DATA_DIR = os.path.dirname(os.path.abspath(__file__))

# ─────────────────────────────────────────────
#  FILE HELPERS
# ─────────────────────────────────────────────
def _path(filename):
    return os.path.join(DATA_DIR, filename)

def load_json(filename, default):
    path = _path(filename)
    if os.path.exists(path):
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except Exception:
            pass
    return default

def save_json(filename, data):
    with open(_path(filename), 'w') as f:
        json.dump(data, f, indent=2)

# ─────────────────────────────────────────────
#  DEFAULT PORTFOLIO DATA
# ─────────────────────────────────────────────
def default_portfolio():
    return {
        "hero": {
            "name": "Keerthivasan",
            "role": "Aspiring Python Developer",
            "subtitle": "Passionate about building clean, scalable web applications with Python & modern web technologies.",
            "availability": "Available for Internship",
            "social": {
                "email": "keerthivasan@email.com",
                "github": "https://github.com/keerthivasan",
                "linkedin": "https://linkedin.com/in/keerthivasan",
                "whatsapp": "https://wa.me/919999999999"
            }
        },
        "about": {
            "bio1": "I'm a second-year Computer Science student with a strong passion for Python and web development. With a CGPA of 8.5, I believe in learning by doing — every project I build teaches me something new.",
            "bio2": "My journey started with Python scripting, and I quickly fell in love with Flask for building backend systems. I'm deeply fascinated by AI/ML and how technology can solve real-world problems elegantly.",
            "bio3": "My goal is to become a skilled Python developer who can architect robust, scalable applications. I bring a designer's eye and an engineer's mindset to everything I create.",
            "cgpa": "8.5",
            "projects_count": "3+",
            "technologies_count": "5+"
        },
        "skills": [
            {"name": "HTML5",      "icon": "fab fa-html5",      "percent": 90},
            {"name": "CSS3",       "icon": "fab fa-css3-alt",   "percent": 85},
            {"name": "JavaScript", "icon": "fab fa-js-square",  "percent": 60},
            {"name": "Python",     "icon": "fab fa-python",     "percent": 80},
            {"name": "Flask",      "icon": "fas fa-flask",      "percent": 50},
            {"name": "Django",     "icon": "fas fa-layer-group","percent": 50}
        ],
        "projects": [
            {
                "id": "p1", "number": "01",
                "title": "Healthcare Access Portal",
                "description": "A patient management system for 'All is Well' hospital. Solved the problem of manual appointment scheduling using design thinking — reducing wait times and improving patient experience.",
                "tags": ["Python", "Flask", "HTML/CSS"],
                "github": "https://github.com/keerthivasan",
                "demo": "#",
                "image": "project1.jpg"
            },
            {
                "id": "p2", "number": "02",
                "title": "Education Engagement Platform",
                "description": "A human-centered platform to bridge the gap between parents, teachers, and students. Features real-time announcements, progress tracking, and community forums.",
                "tags": ["Python", "Django", "JavaScript"],
                "github": "https://github.com/keerthivasan",
                "demo": "#",
                "image": "project2.jpg"
            },
            {
                "id": "p3", "number": "03",
                "title": "Eco-Friendly Urban Housing",
                "description": "An inclusive urban housing solution platform designed with eco-consciousness. Uses design thinking to address affordability, sustainability, and accessibility.",
                "tags": ["Python", "Flask", "Figma"],
                "github": "https://github.com/keerthivasan",
                "demo": "#",
                "image": "project3.jpg"
            }
        ],
        "contact": {
            "email": "keerthivasan@email.com",
            "whatsapp": "https://wa.me/919999999999",
            "linkedin": "https://linkedin.com/in/keerthivasan",
            "github": "https://github.com/keerthivasan",
            "whatsapp_display": "+91 99999 99999",
            "linkedin_display": "linkedin.com/in/keerthivasan",
            "github_display": "github.com/keerthivasan"
        }
    }

# ─────────────────────────────────────────────
#  AUTH DECORATOR
# ─────────────────────────────────────────────
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated

# ─────────────────────────────────────────────
#  VISITOR TRACKING
# ─────────────────────────────────────────────
def track_visitor():
    visitors = load_json('visitors.json', {
        "total": 0, "today": 0, "this_week": 0, "this_month": 0,
        "daily": {}, "monthly": {}, "pages": {},
        "last_reset_day": "", "last_reset_week": "", "last_reset_month": ""
    })
    now        = datetime.datetime.now()
    today_str  = now.strftime('%Y-%m-%d')
    week_str   = now.strftime('%Y-W%W')
    month_str  = now.strftime('%Y-%m')

    if visitors.get('last_reset_day') != today_str:
        visitors['today'] = 0
        visitors['last_reset_day'] = today_str
    if visitors.get('last_reset_week') != week_str:
        visitors['this_week'] = 0
        visitors['last_reset_week'] = week_str
    if visitors.get('last_reset_month') != month_str:
        visitors['this_month'] = 0
        visitors['last_reset_month'] = month_str

    visitors['total']      += 1
    visitors['today']      += 1
    visitors['this_week']  += 1
    visitors['this_month'] += 1

    visitors['daily'][today_str] = visitors['daily'].get(today_str, 0) + 1
    if len(visitors['daily']) > 30:
        oldest = sorted(visitors['daily'].keys())[0]
        del visitors['daily'][oldest]

    visitors['monthly'][month_str] = visitors['monthly'].get(month_str, 0) + 1
    page = request.path
    visitors['pages'][page] = visitors['pages'].get(page, 0) + 1

    save_json('visitors.json', visitors)
    return visitors

# ─────────────────────────────────────────────
#  PUBLIC ROUTES
# ─────────────────────────────────────────────
@app.route('/')
def index():
    track_visitor()
    portfolio = load_json('portfolio.json', default_portfolio())
    visitors  = load_json('visitors.json', {"total": 0})
    return render_template('index.html',
                           p=portfolio,
                           visitor_count=visitors.get('total', 0))

@app.route('/contact', methods=['POST'])
def contact():
    name    = request.form.get('name', '').strip()
    email   = request.form.get('email', '').strip()
    message = request.form.get('message', '').strip()

    if not name or not email or not message:
        return jsonify({'success': False, 'message': 'All fields are required.'}), 400

    entry = {
        'id':        str(uuid.uuid4())[:8],
        'name':      name,
        'email':     email,
        'message':   message,
        'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'read':      False
    }
    msgs = load_json('messages.json', [])
    msgs.insert(0, entry)
    save_json('messages.json', msgs)

    return jsonify({'success': True,
                    'message': f"Thanks {name}! I'll get back to you soon. 🚀"})

# ─────────────────────────────────────────────
#  ADMIN AUTH
# ─────────────────────────────────────────────
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    error = None
    if session.get('admin_logged_in'):
        return redirect(url_for('admin_dashboard'))
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        pw_hash  = hashlib.sha256(password.encode()).hexdigest()
        if username == ADMIN_USERNAME and pw_hash == ADMIN_PASSWORD_HASH:
            session['admin_logged_in'] = True
            session.permanent = True
            return redirect(url_for('admin_dashboard'))
        else:
            error = 'Invalid username or password.'
    return render_template('admin/login.html', error=error)

@app.route('/admin/logout')
def admin_logout():
    session.clear()
    return redirect(url_for('admin_login'))

# ─────────────────────────────────────────────
#  ADMIN DASHBOARD
# ─────────────────────────────────────────────
@app.route('/admin')
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    visitors  = load_json('visitors.json', {
        "total": 0, "today": 0, "this_week": 0, "this_month": 0,
        "daily": {}, "monthly": {}, "pages": {}
    })
    msgs      = load_json('messages.json', [])
    portfolio = load_json('portfolio.json', default_portfolio())
    unread    = sum(1 for m in msgs if not m.get('read', False))
    return render_template('admin/dashboard.html',
                           visitors=visitors, messages=msgs,
                           unread=unread, portfolio=portfolio)

# ─────────────────────────────────────────────
#  ADMIN — MESSAGES
# ─────────────────────────────────────────────
@app.route('/admin/messages')
@login_required
def admin_messages():
    msgs = load_json('messages.json', [])
    for m in msgs:
        m['read'] = True
    save_json('messages.json', msgs)
    return render_template('admin/messages.html', messages=msgs)

@app.route('/admin/messages/delete/<msg_id>', methods=['POST'])
@login_required
def delete_message(msg_id):
    msgs = [m for m in load_json('messages.json', []) if m.get('id') != msg_id]
    save_json('messages.json', msgs)
    return jsonify({'success': True})

@app.route('/admin/messages/delete-all', methods=['POST'])
@login_required
def delete_all_messages():
    save_json('messages.json', [])
    return jsonify({'success': True})

# ─────────────────────────────────────────────
#  ADMIN — VISITORS
# ─────────────────────────────────────────────
@app.route('/admin/visitors')
@login_required
def admin_visitors():
    visitors = load_json('visitors.json', {
        "total": 0, "today": 0, "this_week": 0, "this_month": 0,
        "daily": {}, "monthly": {}, "pages": {}
    })
    return render_template('admin/visitors.html', visitors=visitors)

@app.route('/admin/visitors/reset', methods=['POST'])
@login_required
def reset_visitors():
    save_json('visitors.json', {
        "total": 0, "today": 0, "this_week": 0, "this_month": 0,
        "daily": {}, "monthly": {}, "pages": {},
        "last_reset_day": "", "last_reset_week": "", "last_reset_month": ""
    })
    return jsonify({'success': True})

# ─────────────────────────────────────────────
#  ADMIN — EDIT CONTENT
# ─────────────────────────────────────────────
@app.route('/admin/content', methods=['GET', 'POST'])
@login_required
def admin_content():
    portfolio   = load_json('portfolio.json', default_portfolio())
    success_msg = None

    if request.method == 'POST':
        section = request.form.get('section')

        if section == 'hero':
            portfolio['hero'].update({
                'name': request.form.get('name',''),
                'role': request.form.get('role',''),
                'subtitle': request.form.get('subtitle',''),
                'availability': request.form.get('availability',''),
            })
            portfolio['hero']['social'].update({
                'email':    request.form.get('s_email',''),
                'github':   request.form.get('s_github',''),
                'linkedin': request.form.get('s_linkedin',''),
                'whatsapp': request.form.get('s_whatsapp',''),
            })

        elif section == 'about':
            portfolio['about'].update({
                'bio1': request.form.get('bio1',''),
                'bio2': request.form.get('bio2',''),
                'bio3': request.form.get('bio3',''),
                'cgpa': request.form.get('cgpa',''),
                'projects_count': request.form.get('projects_count',''),
                'technologies_count': request.form.get('technologies_count',''),
            })

        elif section == 'skills':
            names    = request.form.getlist('skill_name')
            icons    = request.form.getlist('skill_icon')
            percents = request.form.getlist('skill_percent')
            portfolio['skills'] = [
                {'name': n.strip(), 'icon': ic.strip(), 'percent': int(pc or 0)}
                for n, ic, pc in zip(names, icons, percents) if n.strip()
            ]

        elif section == 'projects':
            ids    = request.form.getlist('proj_id')
            nums   = request.form.getlist('proj_number')
            titles = request.form.getlist('proj_title')
            descs  = request.form.getlist('proj_desc')
            tags_l = request.form.getlist('proj_tags')
            ghs    = request.form.getlist('proj_github')
            demos  = request.form.getlist('proj_demo')
            imgs   = request.form.getlist('proj_image')
            portfolio['projects'] = []
            for i, title in enumerate(titles):
                if title.strip():
                    tags = [t.strip() for t in (tags_l[i] if i < len(tags_l) else '').split(',') if t.strip()]
                    portfolio['projects'].append({
                        'id':          ids[i] if i < len(ids) else f'p{i+1}',
                        'number':      nums[i] if i < len(nums) else f'0{i+1}',
                        'title':       title.strip(),
                        'description': (descs[i] if i < len(descs) else '').strip(),
                        'tags':        tags,
                        'github':      (ghs[i] if i < len(ghs) else '#').strip(),
                        'demo':        (demos[i] if i < len(demos) else '#').strip(),
                        'image':       (imgs[i] if i < len(imgs) else 'project1.jpg').strip(),
                    })

        elif section == 'contact':
            portfolio['contact'].update({
                'email':            request.form.get('email',''),
                'whatsapp':         request.form.get('whatsapp',''),
                'linkedin':         request.form.get('linkedin',''),
                'github':           request.form.get('github',''),
                'whatsapp_display': request.form.get('whatsapp_display',''),
                'linkedin_display': request.form.get('linkedin_display',''),
                'github_display':   request.form.get('github_display',''),
            })

        save_json('portfolio.json', portfolio)
        success_msg = f'✅ {section.capitalize()} section updated successfully!'
        portfolio = load_json('portfolio.json', default_portfolio())

    return render_template('admin/content.html',
                           portfolio=portfolio, success_msg=success_msg)

# ─────────────────────────────────────────────
#  ADMIN — SETTINGS
# ─────────────────────────────────────────────
@app.route('/admin/settings', methods=['GET', 'POST'])
@login_required
def admin_settings():
    msg = error = None
    if request.method == 'POST':
        current = request.form.get('current_password','')
        new_pw  = request.form.get('new_password','')
        confirm = request.form.get('confirm_password','')
        if hashlib.sha256(current.encode()).hexdigest() != ADMIN_PASSWORD_HASH:
            error = 'Current password is incorrect.'
        elif new_pw != confirm:
            error = 'New passwords do not match.'
        elif len(new_pw) < 6:
            error = 'Password must be at least 6 characters.'
        else:
            new_hash = hashlib.sha256(new_pw.encode()).hexdigest()
            msg = f'Password hash: <code style="word-break:break-all">{new_hash}</code><br><br>Copy this hash and replace <code>ADMIN_PASSWORD_HASH</code> in app.py, then restart the server.'
    return render_template('admin/settings.html', msg=msg, error=error)

# ─────────────────────────────────────────────
#  ADMIN API — live stats refresh
# ─────────────────────────────────────────────
@app.route('/admin/api/stats')
@login_required
def api_stats():
    visitors = load_json('visitors.json', {
        "total": 0, "today": 0, "this_week": 0, "this_month": 0,
        "daily": {}, "monthly": {}
    })
    msgs   = load_json('messages.json', [])
    unread = sum(1 for m in msgs if not m.get('read', False))
    return jsonify({
        'total': visitors.get('total', 0),
        'today': visitors.get('today', 0),
        'this_week': visitors.get('this_week', 0),
        'this_month': visitors.get('this_month', 0),
        'daily': visitors.get('daily', {}),
        'monthly': visitors.get('monthly', {}),
        'msg_count': len(msgs),
        'unread': unread
    })

if __name__ == '__main__':
    if not os.path.exists(_path('portfolio.json')):
        save_json('portfolio.json', default_portfolio())
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
