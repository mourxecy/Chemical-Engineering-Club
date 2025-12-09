# club/models.py
from django.db import models
from django.contrib.auth.models import User

ROLE_CHOICES = (
    ('student', 'Student'),
    ('admin', 'Admin'),
)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')

    def __str__(self):
        return f"{self.user.username} ({self.role})"
    

class AcademicYear(models.Model):
    YEAR_CHOICES = [
        (1, "1st Year"),
        (2, "2nd Year"),
        (3, "3rd Year"),
        (4, "4th Year"),
        (5, "5th Year"),
    ]

    year = models.PositiveIntegerField(choices=YEAR_CHOICES, unique=True)

    def __str__(self):
        return dict(self.YEAR_CHOICES).get(self.year, "Unknown Year")
    
    
class Unit(models.Model):
    year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='units')
    title = models.CharField(max_length=100)
    code = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ['year','title']

    def __str__(self):
        return f"{self.title} - Year {self.year}"

class Resource(models.Model):
    RESOURCE_TYPES = [
        ('notes','Lecture Notes'),
        ('tutorials','Tutorials'),
        ('reference','Reference Material'),
        ('papers','Past Papers'),
        ('poster','Event Poster'),
    ]
    title = models.CharField(max_length=150)
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, blank=True)
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES)
    file = models.FileField(upload_to='resources/')
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.title

class Event(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    event_date = models.DateField(null=True, blank=True)
    # To manually mark past events
    is_past = models.BooleanField(default=False)
    start = models.DateTimeField()
    end = models.DateTimeField(null=True, blank=True)
    poster = models.ImageField(upload_to='events/posters/', null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-start']

    def __str__(self):
        return self.title
    
    @property
    def has_elapsed(self):
        from datetime import date
        return self.event_date < date.today()
