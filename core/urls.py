from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('report/', views.report, name='report'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('map/', views.map_view, name='map'),
    path('admin-panel/', views.admin_view, name='admin_panel'),
    # API endpoints
    path('api/analyze/', views.ai_analyze, name='ai_analyze'),
    path('api/chat/', views.chat_response, name='chat_response'),
    path('api/issues/<str:issue_id>/status/', views.update_issue_status, name='update_status'),
    path(
    'admin-login/',
    auth_views.LoginView.as_view(
        template_name='core/admin_login.html'
    ),
    name='admin_login'
),
]
