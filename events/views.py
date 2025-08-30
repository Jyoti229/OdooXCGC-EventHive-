from django.shortcuts import get_object_or_404, render, redirect
from .models import Trick, Comment, Category, UserProfile
from .forms import CommentForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.hashers import check_password, make_password
from django.db.models import Q


# Home Page
def home(request):
    return render(request, 'home.html')

# About Page
def about(request):
    return render(request, 'about.html')

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

        if not all([username, email, password1, password2]):
            messages.error(request, "Please fill in all required fields.")
            return redirect('register')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        try:
            user = User.objects.create_user(username=username, email=email, password=password1)
            UserProfile.objects.create(
                user=user,
                phone=phone,
                address=address,
                city=city,
                state=state,
                country=country
            )
            messages.success(request, "Registration successful! You can now log in.")
            print("REDIRECTING TO LOGIN")
            return render(request, 'login.html')
        except IntegrityError:
            messages.error(request, "Username or email already exists.")
            return redirect('register')

    return render(request, 'register.html')

def contact_view(request):
    return render(request, 'contact.html')

# Category Listing Page
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'categories.html', {'categories': categories})

# Trick List by Category
def trick_list_by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    tricks = Trick.objects.filter(category=category)
    return render(request, 'trick_list.html', {
        'tricks': tricks,
        'category': category
    })

# Trick Detail Page + Comments
def trick_detail(request, pk):
    trick = get_object_or_404(Trick, pk=pk)
    comments = trick.comments.all().order_by('-created_at')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.trick = trick
            new_comment.user = request.user
            new_comment.save()
            return redirect('trick_detail.html', pk=pk)
    else:
        form = CommentForm()

    return render(request, 'trick_detail.html', {
        'trick': trick,
        'form': form,
        'comments': comments
    })


def trick_search(request):
    query = request.GET.get('q')
    results = []

    if query:
        results = Trick.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )

    return render(request, 'trick_search_results.html', {
        'query': query,
        'results': results
    })

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
            if check_password(password, user.password):
                # Login successful
                request.session['user_id'] = user.id
                request.session['user_name'] = user.username  # or user.get_full_name()
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect('home')
            else:
                messages.error(request, "Invalid email or password.")
        except User.DoesNotExist:
            messages.error(request, "Account not found.")
        
        return render(request, "login.html", {"message": "Login not successful"})

    return render(request, "login.html")


def logout_view(request):
    request.session.flush()
    messages.success(request, "You have been logged out.")
    return redirect('login')


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


def favorites(request):
    return render(request, 'favorites.html')