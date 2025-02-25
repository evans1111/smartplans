from django.db import models
from django.contrib.auth.models import User, AbstractUser, BaseUserManager
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings

# Create your models here.

class Template(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    prompt_template = models.TextField(
        help_text="The template to use for generating the OpenAI prompt. Use {variables} for replacements."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class TemplateOption(models.Model):
    template = models.ForeignKey(Template, related_name='options', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    is_required = models.BooleanField(default=False)
    option_type = models.CharField(
        max_length=20,
        choices=[
            ('text', 'Text Input'),
            ('number', 'Number Input'),
            ('boolean', 'Yes/No Choice'),
            ('select', 'Select from Options')
        ]
    )
    default_value = models.JSONField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.template.name} - {self.name}"

class GeneratedPlan(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='generated_plans'
    )
    plan = models.ForeignKey('Plan', on_delete=models.CASCADE, related_name='generated_plans')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Plan for {self.user.username} using {self.plan.name}"

class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    phone = models.CharField(max_length=20, blank=True)
    
    # Business Details
    business_name = models.CharField(max_length=255, blank=True)
    website = models.URLField(blank=True)
    business_description = models.TextField(blank=True)
    service_areas = models.CharField(max_length=255, blank=True)
    years_in_business = models.IntegerField(null=True, blank=True)
    
    # Social Media
    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    youtube = models.URLField(blank=True)
    
    # Branding
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    primary_color = models.CharField(max_length=7, default='#485fc7')  # Hex color
    secondary_color = models.CharField(max_length=7, default='#00d1b2')  # Hex color
    
    def __str__(self):
        return f"{self.user.email}'s Profile"

class Plan(models.Model):
    PLAN_TYPES = [
        ('past-clients', 'Past Clients SmartPlan'),
        ('open-house', 'Open House SmartPlan')
    ]
    TIMELINE_CHOICES = [
        ('30days', '30 Days'),
        ('60days', '60 Days'),
        ('90days', '90 Days')
    ]
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('generating', 'Generating'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='plans')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPES)
    channels = models.JSONField(default=list)
    timeline = models.CharField(max_length=20, choices=TIMELINE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    content = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255, blank=True)
    
    # Business Information
    business_name = models.CharField(max_length=255, blank=True, null=True)
    business_phone = models.CharField(max_length=20, blank=True, null=True)
    business_address = models.JSONField(default=dict, blank=True, null=True)
    target_market = models.TextField(blank=True, null=True)
    value_proposition = models.TextField(blank=True, null=True)
    additional_context = models.TextField(blank=True, null=True)
    
    # Social Media
    instagram = models.URLField(max_length=255, blank=True, null=True)
    facebook = models.URLField(max_length=255, blank=True, null=True)
    tiktok = models.URLField(max_length=255, blank=True, null=True)
    linkedin = models.URLField(max_length=255, blank=True, null=True)
    youtube = models.URLField(max_length=255, blank=True, null=True)
    twitter = models.URLField(max_length=255, blank=True, null=True)
    threads = models.URLField(max_length=255, blank=True, null=True)
    
    # Branding
    primary_color = models.CharField(max_length=7, blank=True, null=True)
    secondary_color = models.CharField(max_length=7, blank=True, null=True)
    brand_voice = models.CharField(max_length=50, blank=True, null=True)
    brand_description = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()

    def __str__(self):
        return self.email
