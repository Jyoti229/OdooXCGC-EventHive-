from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.db import IntegrityError
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.db import models
from django.contrib.auth.decorators import login_required
from .models import Event, Category, UserProfile, Comment
from .forms import CommentForm, EventForm


# Basic Pages
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def contact_view(request):
    return render(request, 'contact.html')

def favorites(request):
    return render(request, 'favorites.html')


# Category Listing Page
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'categories.html', {'categories': categories})


# Event List by Category
def event_list_by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    if request.user.is_authenticated:
        events = Event.objects.filter(category=category).filter(
            (Q(status='PUBLISHED')) | (Q(status='DRAFT', organizer=request.user))
        )
    else:
        events = Event.objects.filter(category=category, status='PUBLISHED')
    return render(request, 'event_list.html', {'events': events, 'category': category})


# Event Detail Page + Comments
def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    comments = event.comments.all().order_by('-created_at')

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to comment.")
            return redirect('login')

        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.event = event
            new_comment.user = request.user
            new_comment.save()
            return redirect('event_detail', pk=pk)
    else:
        form = CommentForm()

    return render(request, 'event_detail.html', {'event': event, 'form': form, 'comments': comments})


# Event Search
def event_search(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    location = request.GET.get('location')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    rating_min = request.GET.get('rating_min')
    trending = request.GET.get('trending')

    results = Event.objects.all()
    if query:
        results = results.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if category_id:
        results = results.filter(category_id=category_id)
    if date_from:
        results = results.filter(date__gte=date_from)
    if date_to:
        results = results.filter(date__lte=date_to)
    if location:
        results = results.filter(location__icontains=location)
    if price_min or price_max:
        from events.models import TicketType
        event_ids = TicketType.objects.all()
        if price_min:
            event_ids = event_ids.filter(price__gte=price_min)
        if price_max:
            event_ids = event_ids.filter(price__lte=price_max)
        results = results.filter(id__in=event_ids.values_list('event_id', flat=True))
    if rating_min:
        results = results.filter(feedbacks__rating__gte=rating_min)
    if trending:
        # Example: trending = '1' means sort by most bookings
        from bookings.models import Booking
        event_ids = Booking.objects.values('event').annotate(num= models.Count('id')).order_by('-num').values_list('event', flat=True)
        results = results.filter(id__in=event_ids)

    if request.user.is_authenticated:
        results = results.filter((Q(status='PUBLISHED')) | (Q(status='DRAFT', organizer=request.user)))
    else:
        results = results.filter(status='PUBLISHED')

    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    paginator = Paginator(results.distinct(), 10)  # 10 events per page
    page = request.GET.get('page')
    try:
        paged_results = paginator.page(page)
    except PageNotAnInteger:
        paged_results = paginator.page(1)
    except EmptyPage:
        paged_results = paginator.page(paginator.num_pages)

    categories = Category.objects.all()
    return render(request, 'event_search_results.html', {
        'query': query,
        'results': paged_results,
        'categories': categories,
        'selected_category': category_id,
        'date_from': date_from,
        'date_to': date_to,
        'location': location,
        'price_min': price_min,
        'price_max': price_max,
        'rating_min': rating_min,
        'trending': trending,
        'page_obj': paged_results,
    })


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect('home')  # Redirect to home page after login
            else:
                messages.error(request, "Invalid email or password.")
        except User.DoesNotExist:
            messages.error(request, "No account found with this email.")
    return render(request, "login.html")

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')

        # Validation
        if not all([username, email, password1, password2]):
            messages.error(request, "Please fill in all required fields.")
            return redirect('register')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        try:
            # Create user
            user = User.objects.create_user(username=username, email=email, password=password1)
            
            # Create profile
            UserProfile.objects.create(
                user=user,
                phone=phone,
                address=address,
                city=city,
                state=state,
                country=country
            )
            messages.success(request, "Registration successful! Please log in.")
            return redirect('login')
        except IntegrityError:
            messages.error(request, "Username or email already exists.")
            return redirect('register')

    return render(request, "register.html")

# Logout
def logout_view(request):
    request.session.flush()
    messages.success(request, "You have been logged out.")
    return redirect('login')


# Forgot Password
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        confirm = request.POST['confirm']

        if password != confirm:
            return render(request, 'forgot_password.html', {'message': 'Passwords do not match.'})

        try:
            user = User.objects.get(email=email)
            user.password = make_password(password)
            user.save()
            return render(request, 'login.html', {'message': 'Password reset successful. Please login.'})
        except User.DoesNotExist:
            return render(request, 'forgot_password.html', {'message': 'No account found with that email.'})

    return render(request, 'forgot_password.html')

# def event_create(request):
#     if request.method == 'POST':
#         form = EventForm(request.POST)
#         if form.is_valid():
#             event = form.save(commit=False)
#             event.organizer = request.user
#             event.save()
#             messages.success(request, "Event created successfully!")
#             return redirect('event_detail', pk=event.pk)
#     else:
#         form = EventForm()
#     return render(request, 'event_form.html', {'form': form})