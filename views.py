from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import User, UserProfile
from .forms import UserRegistrationForm, UserLoginForm, UserUpdateForm, UserProfileForm


def register_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('accounts:login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data.get('remember_me', False)
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                
                # Set session expiry based on remember_me
                if not remember_me:
                    request.session.set_expiry(0)  # Session expires when browser closes
                
                messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
                
                # Redirect to next page or dashboard
                next_page = request.GET.get('next', 'dashboard')
                return redirect(next_page)
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """User logout view"""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('accounts:login')


@login_required
def profile_view(request):
    """User profile view"""
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    context = {
        'user': user,
        'profile': profile,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def edit_profile_view(request):
    """Edit user profile view"""
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, request.FILES, instance=user)
        profile_form = UserProfileForm(request.POST, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('accounts:profile')
    else:
        user_form = UserUpdateForm(instance=user)
        profile_form = UserProfileForm(instance=profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'accounts/edit_profile.html', context)


class UserDetailView(DetailView):
    """Public user profile view"""
    model = User
    template_name = 'accounts/user_detail.html'
    context_object_name = 'profile_user'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        profile, created = UserProfile.objects.get_or_create(user=user)
        context['profile'] = profile
        return context


@login_required
def dashboard_view(request):
    """User dashboard view"""
    user = request.user
    
    # Get recent activities (placeholder for now)
    context = {
        'user': user,
        'recent_tasks': [],  # Will be populated when tasks app is implemented
        'weather_data': {},  # Will be populated when weather app is implemented
        'recent_posts': [],  # Will be populated when blog app is implemented
    }
    
    return render(request, 'accounts/dashboard.html', context)


@require_http_methods(["POST"])
@login_required
def update_preferences_ajax(request):
    """AJAX view to update user preferences"""
    try:
        user = request.user
        preference = request.POST.get('preference')
        value = request.POST.get('value')
        
        if preference == 'timezone':
            user.preferred_timezone = value
            user.save()
        elif preference == 'weather_unit':
            user.preferred_weather_unit = value
            user.save()
        elif preference in ['email_notifications', 'task_reminders', 'news_digest']:
            profile, created = UserProfile.objects.get_or_create(user=user)
            setattr(profile, preference, value.lower() == 'true')
            profile.save()
        
        return JsonResponse({'status': 'success', 'message': 'Preference updated successfully'})
    
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


def user_list_view(request):
    """Public user list view"""
    users = User.objects.filter(is_active=True).order_by('-date_joined')[:20]
    return render(request, 'accounts/user_list.html', {'users': users})

