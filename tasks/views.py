from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from tasks.forms import EventForm, CategoryForm, ParticipantForm
from tasks.models import *
from datetime import date ,timedelta
from django.db.models import Q, Count, Sum, Avg, Max, Min
from django.contrib import messages
from django.utils.timezone import localdate, now
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings


# Create your views here.
def home(request):
    return render(request, 'dashboard/home.html') 

def manager_dashboard(request):
    query_type = request.GET.get('type', 'all')
    today = localdate()
    tomorrow = today + timedelta(days=1)

    start_of_today = now().replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_today = now().replace(hour=23, minute=59, second=59, microsecond=999999)

    base_query = Event.objects.select_related('category').prefetch_related('participants').annotate(
        participant_count=Count('participants')
    )

    event_stats = base_query.aggregate(
        total_events=Count('id'),
        past_events=Count('id', filter=Q(date__lt=today)),
        today_events=Count('id', filter=Q(date__range=(start_of_today, end_of_today))),
        upcoming_events=Count('id', filter=Q(date__gte=tomorrow)),
    )

    if query_type == 'total_participants':
        total_participants = User.objects.aggregate(total_participants=Count('id'))['total_participants'] #
        events = base_query.none() 
    elif query_type == 'all_events':
        events = base_query
    elif query_type == 'past_events':
        events = base_query.filter(date__lt=today)
    elif query_type == 'today_events':
        events = base_query.filter(date__range=(start_of_today, end_of_today))
    elif query_type == 'upcoming_events':
        events = base_query.filter(date__gte=tomorrow)
    else:  # Default: show all events
        events = base_query

    total_participants = event_stats.get('total_participants', 0)

    context = {
        'events': events,
        'total_events': event_stats['total_events'],
        'past_events': event_stats['past_events'],
        'today_events': event_stats['today_events'],
        'upcoming_events': event_stats['upcoming_events'],
        'total_participants': total_participants,
    }

    return render(request, "dashboard/manager_dashboard.html", context)
# Create your views here.


def organizer_dashboard(request):
    query_type = request.GET.get('type', 'all')
    today = localdate()
    tomorrow = today + timedelta(days=1)

    start_of_today = now().replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_today = now().replace(hour=23, minute=59, second=59, microsecond=999999)

    base_query = Event.objects.select_related('category').prefetch_related('participants').annotate(
        participant_count=Count('participants')
    )

    event_stats = base_query.aggregate(
        total_events=Count('id'),
        past_events=Count('id', filter=Q(date__lt=today)),
        today_events=Count('id', filter=Q(date__range=(start_of_today, end_of_today))),
        upcoming_events=Count('id', filter=Q(date__gte=tomorrow)),
    )

    if query_type == 'total_participants':
        total_participants = User.objects.aggregate(total_participants=Count('id'))['total_participants'] #
        events = base_query.none() 
    elif query_type == 'all_events':
        events = base_query
    elif query_type == 'past_events':
        events = base_query.filter(date__lt=today)
    elif query_type == 'today_events':
        events = base_query.filter(date__range=(start_of_today, end_of_today))
    elif query_type == 'upcoming_events':
        events = base_query.filter(date__gte=tomorrow)
    else:  # Default: show all events
        events = base_query

    total_participants = event_stats.get('total_participants', 0)

    context = {
        'events': events,
        'total_events': event_stats['total_events'],
        'past_events': event_stats['past_events'],
        'today_events': event_stats['today_events'],
        'upcoming_events': event_stats['upcoming_events'],
        'total_participants': total_participants,
    }

    return render(request, "dashboard/organizer_dashboard.html", context)


# Create your views here.

def create_event(request):
    form = EventForm()
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Event created successfully!")
            return redirect('create_event')  
    return render(request, 'dashboard/create_event.html', {'create_event': form})



def update_event(request, id):
    event = get_object_or_404(Event, id=id)
    form = EventForm(instance=event)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event updated successfully!")
            return redirect('update_event',id)  
    return render(request, 'dashboard/create_event.html', {'create_event': form})

         
def delete_event(request, id):
    if request.method == 'POST':
        event = get_object_or_404(Event, id=id) 
        event.delete()
        messages.success(request, "Event deleted successfully")
        return redirect("manager-dashboard")  
    else:
        messages.error(request, "Event not deleted")
        return redirect("manager-dashboard")


def event_list(request):
    events = Event.objects.all()
    return render(request, 'dashboard/create_event.html', {'events': events})

# 
def create_participant(request):
    form = ParticipantForm()
    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.email  
            user.set_password("defaultpassword") 
            user.save()
            form.save_m2m()

            viewer_group = Group.objects.get(name='Participant')
            user.groups.add(viewer_group)
            user.save() 

            user.event_participants.set(form.cleaned_data['events'])  
            user.save()

            messages.success(request, "User created successfully!")
            return redirect('participant_list')
        else:
            messages.error(request, "Error creating user. Please check the form.")
    else:
        form = ParticipantForm()
    return render(request, 'dashboard/create_participant.html', {'form': form})


# 
def participant_list(request):

    participants = User.objects.prefetch_related('event_participants').all()

    context = {
        'participants': participants,  
    }
    return render(request, 'dashboard/participant_list.html', context)



def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category created successfully!")
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'dashboard/create_category.html', {'create_category': form})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'dashboard/category_list.html', {'categories': categories})





def home(request):
    events = Event.objects.all()  
    return render(request, 'home.html', {'events': events})

def event_page(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', '')


    events = Event.objects.all()


    if query:
        events = events.filter(name__icontains=query)
    if category_id:
        events = events.filter(category_id=category_id)


    categories = Category.objects.all()

    return render(request, 'dashboard/event.html', {
        'events': events,
        'categories': categories,
        'query': query,
        'selected_category': category_id,
    })

@login_required
def rsvp_event(request, id):
    event = get_object_or_404(Event, id=id)

    if request.user in event.rsvp_users.all():
        messages.warning(request, "You have already RSVPed to this event.")
    else:
        event.rsvp_users.add(request.user)
        messages.success(request, f"You have successfully RSVPed for {event.name}.")

        # Send confirmation email
        send_mail(
            subject="RSVP Confirmation",
            message=f"Hi {request.user.first_name},\n\nYou have successfully RSVP'd for {event.name} on {event.date} at {event.time}.",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[request.user.email],
            fail_silently=False,
        )

    return redirect('event_detail', id=id) 

def event_detail(request, id):
    event = get_object_or_404(Event, id=id)
    return render(request, 'dashboard/event_detail.html', {'event': event})

