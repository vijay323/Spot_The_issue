from django.contrib import admin
from .models import Issue

@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ['issue_id', 'category', 'priority', 'status', 'location', 'confidence', 'reported_at']
    list_filter = ['priority', 'status', 'category']
    search_fields = ['issue_id', 'location', 'description']
    readonly_fields = ['issue_id', 'reported_at', 'updated_at']
