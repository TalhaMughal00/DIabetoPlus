from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from predictor.models import Predictions
from Glucose_Record.models import GRecords
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from Home.models import feedback
from django.db import IntegrityError

def index(request):
    user_predictions = None
    no_data_message = None
    records = None
    no_records_message = None

    if request.user.is_authenticated:
        user_predictions = Predictions.objects.filter(user=request.user).order_by('-date')
        if not user_predictions.exists():
            no_data_message = "No predictions found."

        user_records = GRecords.objects.filter(user=request.user).order_by('-date')
        if not user_records.exists():
            no_records_message = "No records found."
        else:
            paginator = Paginator(user_records, 7)
            page = request.GET.get('page')
            try:
                records = paginator.page(page)
            except PageNotAnInteger:
                records = paginator.page(1)
            except EmptyPage:
                records = paginator.page(paginator.num_pages)
            no_records_message = None
    else:
        no_data_message = "Please log in to view your predictions."
        no_records_message = "Please log in to view your records."

    return render(request, 'index.html', {
        'predictions': user_predictions,
        'no_data_message': no_data_message,
        'user_records': records,
        'no_records_message': no_records_message,
    })

def about(request):
    return render(request, 'about.html')

@login_required
def calculate_insulin(request):
    return render(request, 'calculate_insulin.html')


def new_diabtetics(request):
    return render(request, 'new_diabetics.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['pass1']
        
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            auth_login(request, user)
            messages.success(request, f"Welcome, {user.username}!")

            # Redirect admin to admin page
            if user.is_superuser or user.is_staff:
                return redirect('admin:index')  # Redirect to Django admin dashboard
            
            # Redirect to 'next' or index for regular users
            return redirect(request.POST.get('next', 'index'))
        else:
            messages.error(request, 'Invalid email or password')
    elif 'next' in request.GET:
        messages.info(request, 'You have to be Logged In')
        return render(request, 'index.html')

    return render(request, 'login.html')

def sign_up(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['pass1']
        password2 = request.POST['pass2']
        
        if not username or not email or not password1 or not password2:
            messages.error(request, 'All Fields Are Required')
            return render(request, 'sign_up.html')

        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'sign_up.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'sign_up.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'sign_up.html')
        
        # Additional password strength checks
        if len(password1) < 8:
            messages.error(request, 'Password must be at least 8 characters long')
            return render(request, 'sign_up.html')

        if not any(char.isdigit() for char in password1):
            messages.error(request, 'Password must contain at least one digit')
            return render(request, 'sign_up.html')

        if not any(char.isalpha() for char in password1):
            messages.error(request, 'Password must contain at least one letter')
            return render(request, 'sign_up.html')

        if not any(char.isupper() for char in password1):
            messages.error(request, 'Password must contain at least one uppercase letter')
            return render(request, 'sign_up.html')

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        messages.success(request, 'You have Successfully Signed Up')
        return redirect('login')
    else:
        return render(request, 'sign_up.html')
    
def logout_view(request):
    auth_logout(request)
    messages.success(request, 'You Have Logged Out')
    return redirect('index')

@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('index')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})

def send_feedback(request):
    if request.method == 'POST':
        feed = request.POST.get('feed')
        if not feed:
            messages.error(request, 'Feedback Field is Required')
            return redirect('index')
        else:
            try:
                feedback_instance = feedback(user=request.user, feed=feed)
                feedback_instance.save()
                messages.success(request, 'Feedback has been sent successfully')
            except IntegrityError as e:
                messages.error(request, 'An error occurred while sending feedback.')
            return redirect('index')
    return render(request, 'index.html')

def profile(request):
    user = request.user

    if request.method == 'POST':
        new_username = request.POST.get('username')
        new_email = request.POST.get('email')

        # Check if the username is the same
        if new_username == user.username and new_email == user.email:
            messages.warning(request, 'You have not changed your username or email.')
            return redirect('profile')

        # Validate username change
        if new_username != user.username:
            if User.objects.filter(username=new_username).exists():
                messages.error(request, 'Username already taken. Please choose a different one.')
                return redirect('profile')

        # Validate email change
        if new_email != user.email:
            if User.objects.filter(email=new_email).exists():
                messages.error(request, 'Email already registered. Please choose a different one.')
                return redirect('profile')

        # Update user details only if they are changed
        if new_username != user.username:
            user.username = new_username
        
        if new_email != user.email:
            user.email = new_email
        
        user.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')  # Redirect to a profile page or wherever you'd like

    return render(request, 'profile.html', {'user': user})