# club/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView, LogoutView
from .forms import RegisterForm, ResourceForm, UnitForm, EventForm
from .models import Resource, Unit, Event, AcademicYear
from datetime import date
from django.utils import timezone

def is_admin(user):
    return user.is_superuser or (hasattr(user, 'profile') and user.profile.role == 'admin')

# Public home
def home(request):
    now = timezone.now()

    upcoming_events = Event.objects.filter(start__gte=now).order_by('start')
    past_events = Event.objects.filter(start__lt=now).order_by('-start')

    return render(request, 'index.html', {
        'upcoming_events': upcoming_events,
        'past_events': past_events,
    })

# auth
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'login.html'
    def form_valid(self, form):
        # Log in user first
        response = super().form_valid(form)
        
        user = self.request.user
        # Redirect based on role
        if user.is_staff or user.is_superuser:
            return redirect('admin_dashboard')
        return redirect('home') 

class CustomLogoutView(LogoutView):
    next_page = '/'

# Admin dashboard
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    now = timezone.now()
    upcoming_events = Event.objects.filter(start__gte=now).order_by('start')
    past_events = Event.objects.filter(start__lt=now).order_by('-start')
    resources = Resource.objects.all()
    units = Unit.objects.all()
    events = Event.objects.all()
    return render(request, 'admin_dashboard.html', {
        'units': units,
        'upcoming_events': upcoming_events,
        'past_events': past_events,
    })

# Resource CRUD
@login_required
@user_passes_test(is_admin)
def resource_create(request):
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            r = form.save(commit=False)
            r.uploaded_by = request.user
            r.save()
            return redirect('admin_dashboard')
    else:
        form = ResourceForm()
    return render(request, 'resource_form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def resource_edit(request, pk):
    r = get_object_or_404(Resource, pk=pk)
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES or None, instance=r)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = ResourceForm(instance=r)
    return render(request, 'resource_form.html', {'form': form, 'object': r})

@login_required
@user_passes_test(is_admin)
def resource_delete(request, pk):
    r = get_object_or_404(Resource, pk=pk)
    if request.method == 'POST':
        if r.file:
            r.file.delete(save=False)
        r.delete()
        return redirect('admin_dashboard')
    return render(request, 'confirm_delete.html', {'object': r})

# Unit CRUD
@login_required
@user_passes_test(is_admin)
def unit_create(request):
    if request.method == 'POST':
        form = UnitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = UnitForm()
    return render(request, 'unit_form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def unit_edit(request, pk):
    unit = get_object_or_404(Unit, pk=pk)
    if request.method == 'POST':
        form = UnitForm(request.POST, instance=unit)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = UnitForm(instance=unit)
    return render(request, 'unit_form.html', {'form': form, 'object': unit})

@login_required
@user_passes_test(is_admin)
def unit_delete(request, pk):
    u = get_object_or_404(Unit, pk=pk)
    if request.method == 'POST':
        u.delete()
        return redirect('admin_dashboard')
    return render(request, 'confirm_delete.html', {'object': u})

# Event CRUD
@login_required
@user_passes_test(is_admin)
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            e = form.save(commit=False)
            e.created_by = request.user
            e.save()
            return redirect('admin_dashboard')
    else:
        form = EventForm()
    return render(request, 'event_form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def event_edit(request, pk):
    e = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=e)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = EventForm(instance=e)
    return render(request, 'event_form.html', {'form': form, 'object': e})

@login_required
@user_passes_test(is_admin)
def event_delete(request, pk):
    e = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        if e.poster:
            e.poster.delete(save=False)
        e.delete()
        return redirect('admin_dashboard')
    return render(request, 'confirm_delete.html', {'object': e})

@login_required
def academic_years(request):
    years = AcademicYear.objects.all()
    return render(request, 'academic_years.html', {'years': years})

def academic_year_list(request):
    years = AcademicYear.objects.all()
    return render(request, 'academic_year_list.html', {'years': years})

def academic_years_view(request):
    years = AcademicYear.objects.order_by('year')
    return render(request, 'academic_years.html', {'years': years})


# UNITS UNDER A YEAR
@login_required
def units_by_year(request, year_id):
    year = get_object_or_404(AcademicYear, id=year_id)
    units = Unit.objects.filter(year=year)
    return render(request, 'units_by_year.html', {'year': year, 'units': units})


# STUDY RESOURCES PAGE
@login_required
def study_resources(request):
    categories = [
        {'title': 'Lecture Notes', 'type': 'notes', 'icon': '📘'},
        {'title': 'Tutorials', 'type': 'tutorials', 'icon': '📙'},
        {'title': 'Reference Materials', 'type': 'reference', 'icon': '📗'},
        {'title': 'Past Papers', 'type': 'papers', 'icon': '📕'},
    ]
    return render(request, 'study_resources.html', {'categories': categories})


# RESOURCES FOR A CATEGORY
@login_required
def resources_by_category(request, category):
    unit_id = request.GET.get("unit")

    resources = study_resources.objects.filter(resource_type=category)

    if unit_id:
        resources = resources.filter(unit_id=unit_id)

    return render(request, "resources_list.html", {
        "resources": resources,
        "category": category,
        "unit": Unit.objects.get(pk=unit_id) if unit_id else None,
    })

@login_required
def study_resources(request):
    resources = Resource.objects.exclude(resource_type='papers')
    return render(request, 'study_resources.html', {'resources': resources})

@login_required
def past_papers(request):
    papers = Resource.objects.filter(resource_type='papers')
    return render(request, 'past_papers.html', {'papers': papers})

def events_page(request):
    today = date.today()

    upcoming_events = Event.objects.filter(event_date__gte=today, is_past=False).order_by('event_date')
    past_events = Event.objects.filter(event_date__lt=today).order_by('-event_date')

    return render(request, 'events.html', {
        'upcoming_events': upcoming_events,
        'past_events': past_events,
    })

def edit_event(request, event_id):
    event = Event.objects.get(id=event_id)

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('events_page')

    else:
        form = EventForm(instance=event)

    return render(request, 'event_edit.html', {'form': form})
