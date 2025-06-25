from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User, UserProfile


class UserProfileInline(admin.StackedInline):
    """Inline admin for UserProfile"""
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile Information'
    fields = ('phone_number', 'website', 'github_username', 'twitter_username', 
             'linkedin_url', 'email_notifications', 'task_reminders', 'news_digest')


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom User admin"""
    
    inlines = (UserProfileInline,)
    
    # Fields to display in the user list
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 
                   'is_active', 'date_joined', 'avatar_preview')
    
    # Fields to filter by
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined', 
                  'preferred_weather_unit', 'preferred_timezone')
    
    # Fields to search
    search_fields = ('username', 'first_name', 'last_name', 'email', 'location')
    
    # Ordering
    ordering = ('-date_joined',)
    
    # Fields to display in the user detail form
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Personal Information', {
            'fields': ('bio', 'location', 'birth_date', 'avatar')
        }),
        ('Preferences', {
            'fields': ('preferred_timezone', 'preferred_weather_unit')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    # Fields to display when adding a new user
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Personal Information', {
            'fields': ('email', 'first_name', 'last_name')
        }),
    )
    
    # Read-only fields
    readonly_fields = ('created_at', 'updated_at', 'date_joined', 'last_login')
    
    def avatar_preview(self, obj):
        """Display avatar preview in admin list"""
        if obj.avatar:
            return format_html(
                '<img src="{}" width="30" height="30" style="border-radius: 50%;" />',
                obj.avatar.url
            )
        return "No Avatar"
    avatar_preview.short_description = "Avatar"
    
    def get_queryset(self, request):
        """Optimize queryset with select_related"""
        return super().get_queryset(request).select_related('profile')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """UserProfile admin"""
    
    list_display = ('user', 'phone_number', 'website', 'email_notifications', 
                   'task_reminders', 'news_digest')
    
    list_filter = ('email_notifications', 'task_reminders', 'news_digest')
    
    search_fields = ('user__username', 'user__email', 'phone_number', 'website')
    
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Contact Information', {
            'fields': ('phone_number', 'website')
        }),
        ('Social Media', {
            'fields': ('github_username', 'twitter_username', 'linkedin_url'),
            'classes': ('collapse',)
        }),
        ('Notification Preferences', {
            'fields': ('email_notifications', 'task_reminders', 'news_digest')
        }),
    )
    
    def get_queryset(self, request):
        """Optimize queryset with select_related"""
        return super().get_queryset(request).select_related('user')

