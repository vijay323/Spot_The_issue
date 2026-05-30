# CivicSense AI — Django + Real YOLOv8

## Setup (3 steps)

```bash
# 1. Activate your existing venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# 2. Install AI dependencies (if not already)
pip install ultralytics torch torchvision opencv-python-headless

# 3. Run migrations + start server
python manage.py migrate
python manage.py runserver
```

Open http://localhost:8000

---

## Model File ✅

Your `best.pt` is already in place at:
```
ai_models/best.pt   (65MB — real trained weights)
```

**Detectable classes:**
| Class | Display Name |
|-------|-------------|
| 0 | Garbage |
| 1 | Pothole |
| 2 | Waterlogging |
| 3 | Broken Streetlight |

---

## New Features Added

### Report Page
- **Real YOLOv8 detection** — uploads photo, runs `best.pt`, returns class + bbox
- **Bounding box drawn on preview** — green box shows what was detected
- **`🤖 YOLOv8 Real` / `🔮 Smart Mock` badge** — tells you which mode ran
- **Manual override** — 11 issue type buttons (AI detects 4, you can pick any)
- **AI status pill** — top of page shows model status + detectable classes
- **GPS coordinates** — capture exact lat/lng for map placement
- **Submit only when**: image + location + type all filled

### Issue Types (11 total)
AI-detectable (4): Pothole, Garbage, Waterlogging, Broken Streetlight
Manual (7): Damaged Road, Encroachment, Sewage Overflow, Stray Animals,
            Illegal Dumping, Noise Pollution, Other

### API Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/analyze/` | POST | Real YOLOv8 inference |
| `/api/chat/` | POST | AI chatbot |
| `/api/issues/<id>/status/` | POST | Update status |
| `/api/issues/<id>/delete/` | POST | Delete issue (admin) |
| `/api/ai-status/` | GET | Model load status + classes |

---

## If YOLOv8 isn't installed yet

```bash
pip install ultralytics
```

The app works without it (smart mock mode) — same UI, deterministic fake results.
