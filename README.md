# CivicSense AI — Django

Full conversion of the CivicSense AI platform from Next.js/React to Django + Python. All features preserved, same UI/UX.

## Features
- 🏠 Landing page with hero, features, testimonials, CTA
- 📸 Report Issue page with drag-and-drop upload + AI analysis simulation
- 📊 Dashboard with filter by category & priority
- 🗺️ Interactive map view with pin filtering
- 🛡️ Admin panel with status management + analytics charts
- 💬 AI chat assistant (floating widget, all pages)
- 🌙 Dark theme matching original design exactly

## Quick Start

```bash
# 1. Create & activate virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run migrations
python manage.py migrate

# 4. Create superuser (optional, for /admin/)
python manage.py createsuperuser

# 5. Run development server
python manage.py runserver
```

Open http://localhost:8000

## Pages

| URL | Description |
|-----|-------------|
| `/` | Landing page |
| `/report/` | Report a civic issue (upload + AI) |
| `/dashboard/` | View & filter all reports |
| `/map/` | Interactive map with issue pins |
| `/admin-panel/` | Admin complaints + analytics |
| `/admin/` | Django built-in admin |

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/analyze/` | POST | Simulated AI image analysis |
| `/api/chat/` | POST | AI chat assistant response |
| `/api/issues/<id>/status/` | POST | Update issue status |

## Project Structure

```
civicsense_django/
├── civicsense/          # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/                # Main app
│   ├── models.py        # Issue model
│   ├── views.py         # All views + API endpoints
│   ├── urls.py          # URL routing
│   ├── admin.py         # Django admin config
│   ├── migrations/      # DB migrations
│   └── templates/core/  # HTML templates
│       ├── base.html    # Shared layout, navbar, footer, chat widget
│       ├── home.html    # Landing page
│       ├── report.html  # Issue reporting
│       ├── dashboard.html
│       ├── map.html
│       └── admin.html
├── media/               # Uploaded images
├── manage.py
└── requirements.txt
```

## Notes

- Uses **SQLite** by default (zero config). Switch to PostgreSQL in `settings.py` for production.
- AI analysis is **simulated** (random category/priority/confidence). To use real YOLOv8, integrate the `ai/` module from the original project into `core/views.py → ai_analyze()`.
- Images uploaded via the report form are saved to `media/issues/`.
- The `SECRET_KEY` in settings.py must be changed for production deployment.
