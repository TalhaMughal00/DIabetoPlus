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
from Home.models import feedback,NewsletterSubscriber,Profile
from django.db import IntegrityError
from recommendations.models import ER,DP

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
    return render(request, 'info/new_diabetics.html')

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

@login_required
def send_feedback(request):
    if request.method == 'POST':
        feed = request.POST.get('feed')
        if not feed:
            messages.error(request, 'Feedback Field is Required')
            return redirect('index')
        else:
            try:
                feedback_instance = feedback(user=request.user, feedback=feed)
                feedback_instance.save()
                messages.success(request, 'Feedback has been sent successfully')
            except IntegrityError as e:
                messages.error(request, 'An error occurred while sending feedback.')
            return redirect('index')
    return render(request, 'index.html')

@login_required
def profile(request):
    user = request.user
    exercise_routine = None  # Initialize exercise routine
    diet_plan = None  # Initialize diet plan

    # Attempt to get the user's exercise routine
    try:
        exercise_routine = ER.objects.get(user=user)
    except ER.DoesNotExist:
        exercise_routine = None

    # Attempt to get the user's diet plan
    try:
        diet_plan = DP.objects.get(user=user)
    except DP.DoesNotExist:
        diet_plan = None

    if request.method == 'POST':
        # Safely get username and email, default to an empty string if None
        new_username = request.POST.get('username', '').strip()
        new_email = request.POST.get('email', '').strip()

        # Check if the username and email are the same as before
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
        user.username = new_username
        user.email = new_email
        user.save()

        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')

    # Pass exercise and diet plan data to the template
    return render(request, 'profile.html', {
        'user': user,
        'intensity': exercise_routine.intensity if exercise_routine else None,
        'exercises': exercise_routine.exercises if exercise_routine else None,
        'breakfast_plan': diet_plan.breakfast_plan if diet_plan else None,
        'lunch_plan': diet_plan.lunch_plan if diet_plan else None,
        'dinner_plan': diet_plan.dinner_plan if diet_plan else None,
        'bmr': format(diet_plan.bmr, '.2f') if diet_plan else None,
        'bmi': format(diet_plan.bmi, '.2f') if diet_plan else None,
        'diet_type': diet_plan.diet_type if diet_plan else None,
    })

    
@login_required
def profile_pic(request):
    # Ensure the user has a profile
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']
            profile.save()
            messages.success(request, 'Your profile picture has been updated.')
        else:
            messages.error(request, 'Please upload a valid profile picture.')
        return redirect('profile')

    return render(request, 'profile.html')

@login_required
def subscribe_newsletter(request):
    if request.method == 'POST':
        user_email = request.user.email  # Use the logged-in user's email

        # Check if the email is already subscribed
        if NewsletterSubscriber.objects.filter(email=user_email).exists():
            messages.error(request, "This email is already subscribed to the newsletter.")
            return redirect('index')  # Redirect back to the same page or another one

        # Save the new email to the database
        subscriber = NewsletterSubscriber(email=user_email)
        subscriber.save()

        messages.success(request, "Thank you for subscribing to our newsletter!")
        return redirect('index')  # Redirect to a thank you page or homepage
    
    return render(request, 'base.html')  # Redirect to home page or any other page
