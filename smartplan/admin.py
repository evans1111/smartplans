from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Plan, GeneratedPlan, UserProfile

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'full_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('full_name',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email', 'full_name')
    ordering = ('email',)

class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'description')

class GeneratedPlanAdmin(admin.ModelAdmin):
    list_display = ('plan', 'user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content',)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username', 'user__email')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Plan, PlanAdmin)
admin.site.register(GeneratedPlan, GeneratedPlanAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
