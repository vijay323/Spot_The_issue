from django.db import models
import random
import string


def generate_issue_id():
    num = random.randint(100, 999)
    return f"ISS-{num:03d}"


class Issue(models.Model):
    PRIORITY_CHOICES = [
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Sent to Authority', 'Sent to Authority'),
        ('Resolved', 'Resolved'),
    ]
    CATEGORY_CHOICES = [
        ('Pothole', 'Pothole'),
        ('Garbage', 'Garbage'),
        ('Broken Streetlight', 'Broken Streetlight'),
        ('Waterlogging', 'Waterlogging'),
        ('Damaged Road', 'Damaged Road'),
        ('Other', 'Other'),
    ]

    issue_id = models.CharField(max_length=20, unique=True, default=generate_issue_id)
    image = models.ImageField(upload_to='issues/', null=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Other')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Medium')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Pending')
    location = models.CharField(max_length=255, default='')
    description = models.TextField(blank=True, default='')
    confidence = models.IntegerField(default=0)
    reported_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-reported_at']

    def __str__(self):
        return f"{self.issue_id} — {self.category} ({self.priority})"
