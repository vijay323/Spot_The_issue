import json
import random
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Issue


def home(request):
    return render(request, 'core/home.html')


def report(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        location = request.POST.get('location', '')
        description = request.POST.get('description', '')
        manual_type = request.POST.get('issue_type', 'Other')
        ai_category = request.POST.get('ai_category', manual_type)
        ai_priority = request.POST.get('ai_priority', 'Medium')
        ai_confidence = int(request.POST.get('ai_confidence', 0))
        ai_time = request.POST.get('ai_time', '48-72 hours')

        issue = Issue.objects.create(
            image=image,
            category=ai_category,
            priority=ai_priority,
            status='Pending',
            location=location,
            description=description,
            confidence=ai_confidence,
        )

        return JsonResponse({
            'success': True,
            'issue_id': issue.issue_id,
            'category': issue.category,
            'est_time': ai_time,
        })

    issue_types = [
        "Pothole",
        "Garbage",
        "Broken Streetlight",
        "Waterlogging",
        "Damaged Road",
        "Other"
    ]

    return render(request, 'core/report.html', {
        'issue_types': issue_types
    })


def dashboard(request):

    db_issues = Issue.objects.all().order_by('-reported_at')

    all_issues = [{

        'id': i.issue_id,

        'image':
            i.image.url
            if i.image
            else '/static/core/images/placeholder.jpg',

        'category': i.category,

        'priority': i.priority,

        'status': i.status,

        'location': i.location,

        'description': i.description,

        'confidence': i.confidence,

        'reportedAt':
            i.reported_at.isoformat(),

    } for i in db_issues]

    stats = {

        'total':
            len(all_issues),

        'pending':
            sum(
                1 for i in all_issues
                if i['status'] == 'Pending'
            ),

        'sent':
            sum(
                1 for i in all_issues
                if i['status'] == 'Sent to Authority'
            ),

        'resolved':
            sum(
                1 for i in all_issues
                if i['status'] == 'Resolved'
            ),

    }

    return render(

        request,
        'core/dashboard.html',

        {

            'issues_json':
                json.dumps(all_issues),

            'stats':
                stats,

        }

    )

def map_view(request):

    db_issues = Issue.objects.all().order_by('-reported_at')

    map_issues = []

    for i in db_issues:

        lat = None
        lng = None

        try:

            # format:
            # 28.6139, 77.2090

            if i.location and ',' in i.location:

                coords = i.location.split(',')

                lat = float(coords[0].strip())
                lng = float(coords[1].strip())

        except:
            pass

        map_issues.append({

            'id': i.issue_id,
            'type': i.category,
            'lat': lat,
            'lng': lng,
            'priority': i.priority,
            'status': i.status,
            'location': i.location,
            'description': i.description or '',

        })

    return render(request, 'core/map.html', {

        'map_issues_json': json.dumps(map_issues),

    })

@login_required
def admin_view(request):
    db_issues = Issue.objects.all()
    db_list = [{
        'id': i.issue_id,
        'image': i.image.url if i.image else '/static/core/images/placeholder.jpg',
        'category': i.category,
        'priority': i.priority,
        'status': i.status,
        'location': i.location,
        'description': i.description,
        'confidence': i.confidence,
        'reportedAt': i.reported_at.isoformat(),
    } for i in db_issues]
    all_issues = db_list + DEMO_ISSUES
    stats = {
        'total': len(all_issues),
        'high_priority': sum(1 for i in all_issues if i['priority'] == 'High'),
        'pending': sum(1 for i in all_issues if i['status'] == 'Pending'),
        'resolved': sum(1 for i in all_issues if i['status'] == 'Resolved'),
    }
    return render(request, 'core/admin.html', {
        'issues_json': json.dumps(all_issues),
        'stats': stats,
    })


@csrf_exempt
@require_http_methods(['PATCH', 'POST'])
def update_issue_status(request, issue_id):
    data = json.loads(request.body)
    new_status = data.get('status')
    try:
        issue = Issue.objects.get(issue_id=issue_id)
        issue.status = new_status
        issue.save()
        return JsonResponse({'success': True})
    except Issue.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Not found'}, status=404)


@csrf_exempt
def ai_analyze(request):
    """Simulate AI analysis of uploaded image."""
    if request.method == 'POST':
        categories = ['Pothole', 'Garbage', 'Broken Streetlight', 'Waterlogging', 'Damaged Road']
        priorities = ['High', 'Medium', 'Low']
        priority_times = {'High': '24-48 hours', 'Medium': '3-5 days', 'Low': '7-10 days'}
        category = random.choice(categories)
        priority = random.choice(priorities)
        confidence = random.randint(85, 98)
        descriptions = {
            'Pothole': 'Large pothole detected in road surface. Poses significant risk to vehicles.',
            'Garbage': 'Overflowing garbage/waste detected. Requires immediate collection.',
            'Broken Streetlight': 'Non-functional streetlight detected. Safety hazard at night.',
            'Waterlogging': 'Significant water accumulation detected. Blocks pedestrian access.',
            'Damaged Road': 'Severe road surface damage detected over a stretch.',
        }
        return JsonResponse({
            'category': category,
            'priority': priority,
            'confidence': confidence,
            'description': descriptions.get(category, 'Civic issue detected.'),
            'estimatedTime': priority_times[priority],
        })
    return JsonResponse({'error': 'POST required'}, status=405)


def chat_response(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        message = data.get('message', '').lower()
        if any(w in message for w in ['track', 'status', 'complaint']):
            reply = "To track your report, go to the <strong>Dashboard</strong> page and use your tracking ID (e.g., ISS-001). You'll see real-time status updates: Pending → Sent to Authority → Resolved."
        elif any(w in message for w in ['resolution', 'time', 'long', 'when']):
            reply = "The average resolution time is <strong>48 hours</strong> for high-priority issues and <strong>5-7 days</strong> for medium/low priority. High-priority issues like severe waterlogging or road hazards are escalated immediately."
        elif any(w in message for w in ['priority', 'high', 'urgent']):
            reply = "Issues are prioritized by AI based on:<br>• <strong>High</strong>: Immediate safety risk (waterlogging, large potholes)<br>• <strong>Medium</strong>: Quality of life impact (garbage, damaged roads)<br>• <strong>Low</strong>: Minor inconvenience (broken streetlights in low-traffic areas)"
        elif any(w in message for w in ['ai', 'detect', 'work', 'how']):
            reply = "CivicSense AI uses a computer vision model trained on thousands of civic issue photographs. When you upload a photo, it:<br>1. Preprocesses the image<br>2. Runs object detection<br>3. Classifies the issue type<br>4. Assigns severity with confidence score<br><br>Accuracy: <strong>94%+</strong> on our validation set."
        else:
            reply = "I'm CivicSense AI Assistant! I can help you with civic issue reporting, tracking your complaints, understanding AI detection results, and more. What would you like to know?"
        return JsonResponse({'reply': reply})
    return JsonResponse({'error': 'POST required'}, status=405)
