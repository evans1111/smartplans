from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from .models import Template, GeneratedPlan, UserProfile, Plan
from .serializers import TemplateSerializer, GeneratedPlanSerializer, UserProfileSerializer, PlanSerializer
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.middleware.csrf import get_token
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.views.decorators.csrf import ensure_csrf_cookie
import json
from django.core.files.storage import default_storage
from django.utils import timezone

# Create your views here.

class TemplateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Template.objects.filter(is_active=True)
    serializer_class = TemplateSerializer

class GeneratedPlanViewSet(viewsets.ModelViewSet):
    serializer_class = GeneratedPlanSerializer

    def get_queryset(self):
        return GeneratedPlan.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    try:
        data = request.data
        print("Registration attempt with data:", data)  # Debug print

        # Check if user exists
        if User.objects.filter(email=data['email']).exists():
            return Response({
                'message': 'A user with this email already exists.'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Create user
        user = User.objects.create_user(
            username=data['email'],
            email=data['email'],
            password=data['password'],
            first_name=data['name'].split()[0],
            last_name=' '.join(data['name'].split()[1:]) if len(data['name'].split()) > 1 else ''
        )

        # Authenticate and login
        authenticated_user = authenticate(username=data['email'], password=data['password'])
        if authenticated_user:
            login(request, authenticated_user)
            print(f"User registered and logged in: {user.email}")  # Debug print
            
            return Response({
                'user': {
                    'email': user.email,
                    'name': f"{user.first_name} {user.last_name}".strip()
                }
            }, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        print(f"Registration error: {str(e)}")  # Debug print
        return Response({
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    try:
        email = request.data.get('email')
        password = request.data.get('password')
        print(f"Login attempt for: {email}")  # Debug print

        user = authenticate(username=email, password=password)
        if user:
            login(request, user)
            print(f"User logged in: {email}")  # Debug print
            return Response({
                'user': {
                    'email': user.email,
                    'name': f"{user.first_name} {user.last_name}".strip()
                }
            })
        else:
            return Response({
                'message': 'Invalid credentials'
            }, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print(f"Login error: {str(e)}")  # Debug print
        return Response({
            'message': 'Login failed'
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def logout_user(request):
    try:
        logout(request)
        return Response({'message': 'Logged out successfully'})
    except Exception as e:
        print(f"Logout error: {str(e)}")  # Debug print
        return Response({'message': 'Logout failed'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@ensure_csrf_cookie
def get_user(request):
    if request.user.is_authenticated:
        return Response({
            'user': {
                'email': request.user.email,
                'name': f"{request.user.first_name} {request.user.last_name}".strip()
            }
        })
    return Response({'user': None}, status=status.HTTP_401_UNAUTHORIZED)

User = get_user_model()

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_settings(request):
    """Handle user settings"""
    user = request.user
    
    if request.method == 'GET':
        data = {
            'email': user.email,
            'business_info': {
                'name': user.business_name,
                'phone': user.business_phone,
                'address': user.business_address,
                'target_market': user.target_market,
                'value_proposition': user.value_proposition,
                'additional_context': user.additional_context
            },
            'social_media': {
                'instagram': user.instagram,
                'facebook': user.facebook,
                'tiktok': user.tiktok,
                'linkedin': user.linkedin,
                'youtube': user.youtube,
                'twitter': user.twitter,
                'threads': user.threads
            },
            'branding': {
                'primary_color': user.primary_color,
                'secondary_color': user.secondary_color,
                'brand_voice': user.brand_voice,
                'brand_description': user.brand_description
            }
        }
        print('GET request - returning data:', data)  # Debug log
        return Response(data)
    
    elif request.method == 'PUT':
        data = request.data
        print('PUT request - received data:', data)  # Debug log
        
        if 'business' in data:
            business_data = data['business']
            print('Updating business data:', business_data)  # Debug log
            user.business_name = business_data.get('name')
            user.business_phone = business_data.get('phone')
            user.business_address = business_data.get('address')
            user.target_market = business_data.get('targetMarket')
            user.value_proposition = business_data.get('valueProposition')
            user.additional_context = business_data.get('additionalContext')
        
        # Update social media
        elif 'social' in data:
            social_data = data['social']
            user.instagram = social_data.get('instagram', user.instagram)
            user.facebook = social_data.get('facebook', user.facebook)
            user.tiktok = social_data.get('tiktok', user.tiktok)
            user.linkedin = social_data.get('linkedin', user.linkedin)
            user.youtube = social_data.get('youtube', user.youtube)
            user.twitter = social_data.get('twitter', user.twitter)
            user.threads = social_data.get('threads', user.threads)
        
        # Update branding
        elif 'branding' in data:
            branding_data = data['branding']
            user.primary_color = branding_data.get('primaryColor', user.primary_color)
            user.secondary_color = branding_data.get('secondaryColor', user.secondary_color)
            user.brand_voice = branding_data.get('brandVoice', user.brand_voice)
            user.brand_description = branding_data.get('brandDescription', user.brand_description)
        
        # Save the user object with all updates
        user.save()
        print('User saved successfully')  # Debug log
        
        return Response({'status': 'success', 'message': 'Settings updated successfully'})

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def plan_list_create(request):
    if request.method == 'GET':
        plans = Plan.objects.filter(user=request.user)
        serializer = PlanSerializer(plans, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        try:
            # Print everything we can about the request
            print("\n=== DEBUG REQUEST ===")
            print("Headers:", dict(request.headers))
            print("Body:", request.body.decode('utf-8'))
            print("Data:", request.data)
            print("User:", request.user)
            print("Method:", request.method)
            print("Content Type:", request.content_type)
            
            # Create the plan with minimal required data
            plan = Plan.objects.create(
                user=request.user,
                title=f"New SmartPlan - {timezone.now().strftime('%B %d, %Y')}",
                plan_type=request.data['plan_type'],
                channels=request.data['channels'],
                timeline=request.data['timeline']
            )
            
            print("Plan created:", plan.id)
            
            # Return success response
            return Response({
                'id': plan.id,
                'message': 'Plan created successfully'
            }, status=status.HTTP_201_CREATED)
            
        except KeyError as e:
            print(f"Missing required field: {str(e)}")
            return Response({
                'error': f"Missing required field: {str(e)}"
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            print(f"Error creating plan: {str(e)}")
            import traceback
            print(traceback.format_exc())
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def plan_detail(request, plan_id):
    try:
        plan = Plan.objects.get(id=plan_id, user=request.user)
    except Plan.DoesNotExist:
        return Response({'message': 'Plan not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PlanSerializer(plan)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PlanSerializer(plan, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        plan.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
