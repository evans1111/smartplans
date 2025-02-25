from rest_framework import serializers
from .models import Template, TemplateOption, GeneratedPlan, Plan
from django.contrib.auth.models import User
from .models import UserProfile

class TemplateOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplateOption
        fields = ['id', 'name', 'description', 'is_required', 'option_type', 'default_value']

class TemplateSerializer(serializers.ModelSerializer):
    options = TemplateOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Template
        fields = ['id', 'name', 'description', 'options', 'created_at']

class GeneratedPlanSerializer(serializers.ModelSerializer):
    template_name = serializers.CharField(source='template.name', read_only=True)

    class Meta:
        model = GeneratedPlan
        fields = ['id', 'template_name', 'content', 'options_used', 'created_at']
        read_only_fields = ['content', 'created_at']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ['user']

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'profile']

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['id', 'user', 'title', 'plan_type', 'channels', 'timeline', 
                 'status', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_channels(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("Channels must be a list")
        valid_channels = ['email', 'voicemail', 'video', 'text']
        for channel in value:
            if channel not in valid_channels:
                raise serializers.ValidationError(f"Invalid channel: {channel}")
        return value

    def validate_timeline(self, value):
        valid_timelines = ['30days', '60days', '90days']
        if value not in valid_timelines:
            raise serializers.ValidationError("Invalid timeline selection")
        return value

    def validate_plan_type(self, value):
        valid_types = ['past-clients', 'open-house']
        if value not in valid_types:
            raise serializers.ValidationError("Invalid plan type")
        return value

    def validate_status(self, value):
        valid_statuses = ['draft', 'generating', 'completed', 'failed']
        if value not in valid_statuses:
            raise serializers.ValidationError("Invalid status")
        return value

    def create(self, validated_data):
        print("Creating plan with validated data:", validated_data)  # Debug print
        return super().create(validated_data)

    def validate(self, data):
        print("Validating data:", data)  # Debug print
        return data
