# 🚀 Keerthivasan — Personal Portfolio

A premium, fully responsive Python Flask portfolio website.

## 📁 Project Structure
```
portfolio/
├── app.py                  # Flask application
├── requirements.txt        # Python dependencies
├── messages.json           # Auto-created contact messages store
├── templates/
│   └── index.html          # Main HTML template (Jinja2)
├── static/
│   ├── css/
│   │   └── style.css       # Premium dark theme CSS
│   ├── js/
│   │   └── script.js       # Animations, typing, form handling
│   └── images/
│       ├── profile.jpg     ← Add your profile photo here
│       ├── project1.jpg    ← Add project screenshots here
│       ├── project2.jpg
│       ├── project3.jpg
│       └── resume.pdf      ← Add your resume PDF here
```

## ⚙️ Setup & Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Add your images to static/images/
#    - profile.jpg  (your photo, ideally 500x500px)
#    - project1.jpg, project2.jpg, project3.jpg (project screenshots)
#    - Copy your resume.pdf to static/

# 3. Update your real links in templates/index.html:
#    - Email, GitHub, LinkedIn, WhatsApp URLs
#    - Social links in hero + contact + footer sections

# 4. Run the app
python app.py

# 5. Visit http://localhost:5000
```

## ✨ Features
- 🌙 Dark/Light theme toggle (persists with localStorage)
- ⌨️  Typing animation hero text
- 📊 Animated skill progress bars (scroll-triggered)
- 🎴 Glassmorphism cards throughout
- 📱 Fully mobile responsive (mobile-first)
- 📬 Contact form with Flask backend (stores to messages.json)
- ⬆️  Scroll progress bar
- 🔄 Page loading animation
- 🎯 Active navbar highlighting
- 🖱️ Smooth scrolling + reveal animations

## 🎨 Customization
- Update name, bio, links in `templates/index.html`
- Add real project images to `static/images/`
- Update skill percentages in the HTML data attributes
- Modify colors in `:root` CSS variables in `style.css`
