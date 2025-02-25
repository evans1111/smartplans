from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Plan, GeneratedPlan, UserProfile

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'business_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Business Information', {
            'fields': ('business_name', 'business_phone', 'business_address', 
                      'target_market', 'value_proposition', 'additional_context')
        }),
        ('Social Media', {
            'fields': ('instagram', 'facebook', 'tiktok', 'linkedin', 
                      'youtube', 'twitter', 'threads')
        }),
        ('Branding', {
            'fields': ('primary_color', 'secondary_color', 'brand_voice', 
                      'brand_description')
        }),
    )

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
