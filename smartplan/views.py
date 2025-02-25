from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes, authentication_classes
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
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from django.utils.decorators import method_decorator

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

User = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    try:
        email = request.data.get('email')
        password = request.data.get('password')
        full_name = request.data.get('full_name', '')

        if not email or not password:
            return Response({'error': 'Email and password are required'}, 
                          status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email already registered'}, 
                          status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            email=email,
            password=password,
            full_name=full_name
        )
        
        token, _ = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user': {
                'id': user.id,
                'email': user.email,
                'full_name': user.full_name
            }
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
@ensure_csrf_cookie
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        user = User.objects.get(email=email)
        if user.check_password(password):
            token, _ = Token.objects.get_or_create(user=user)
            response = Response({
                'token': token.key,
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'full_name': user.full_name
                }
            })
            response['X-CSRFToken'] = get_token(request)
            return response
        else:
            return Response({'error': 'Invalid credentials'}, 
                          status=status.HTTP_401_UNAUTHORIZED)
    except User.DoesNotExist:
        return Response({'error': 'Invalid credentials'}, 
                       status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    request.user.auth_token.delete()
    return Response({'message': 'Successfully logged out'})

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user(request):
    try:
        user = request.user
        return Response({
            'user': {
                'id': user.id,
                'email': user.email,
                'name': f"{user.first_name} {user.last_name}".strip(),
                'business_name': user.business_name
            }
        })
    except Exception as e:
        print(f"Get user error: {str(e)}")
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
@ensure_csrf_cookie
def user_settings(request):
    user = request.user
    
    if request.method == 'GET':
        return Response({
            'email': user.email,
            'full_name': user.full_name,
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
                'brand_description': user.brand_description,
                'logo': user.logo.url if user.logo else None
            }
        })
    
    elif request.method == 'PUT':
        try:
            # Handle multipart form data for file uploads
            if request.content_type and 'multipart/form-data' in request.content_type:
                if 'branding' in request.data:
                    branding_data = json.loads(request.data['branding'])
                    user.primary_color = branding_data.get('primaryColor', user.primary_color)
                    user.secondary_color = branding_data.get('secondaryColor', user.secondary_color)
                    user.brand_voice = branding_data.get('brandVoice', user.brand_voice)
                    user.brand_description = branding_data.get('brandDescription', user.brand_description)
                
                if 'logo' in request.FILES:
                    if user.logo:
                        default_storage.delete(user.logo.path)
                    user.logo = request.FILES['logo']
            
            # Handle JSON data
            else:
                data = request.data
                
                # Update business info
                if 'business' in data:
                    business = data['business']
                    user.business_name = business.get('name', user.business_name)
                    user.business_phone = business.get('phone', user.business_phone)
                    user.business_address = business.get('address', user.business_address)
                    user.target_market = business.get('target_market', user.target_market)
                    user.value_proposition = business.get('value_proposition', user.value_proposition)
                    user.additional_context = business.get('additional_context', user.additional_context)
                
                # Update social media
                if 'social' in data:
                    social = data['social']
                    user.instagram = social.get('instagram', user.instagram)
                    user.facebook = social.get('facebook', user.facebook)
                    user.tiktok = social.get('tiktok', user.tiktok)
                    user.linkedin = social.get('linkedin', user.linkedin)
                    user.youtube = social.get('youtube', user.youtube)
                    user.twitter = social.get('twitter', user.twitter)
                    user.threads = social.get('threads', user.threads)
            
            user.save()
            return Response({
                'message': 'Settings updated successfully',
                'updated_fields': request.data.keys()
            })
            
        except Exception as e:
            print("Error saving settings:", str(e))
            return Response({
                'error': str(e)
            }, status=400)

@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def plan_list_create(request):
    if request.method == 'GET':
        plans = Plan.objects.filter(user=request.user)
        serializer = PlanSerializer(plans, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        try:
            # Print everything we can about the request for debugging
            print("\n=== DEBUG REQUEST ===")
            print("Headers:", dict(request.headers))
            print("Body:", request.body.decode('utf-8'))
            print("Data:", request.data)
            print("User:", request.user)
            print("Method:", request.method)
            print("Content Type:", request.content_type)
            print("Auth:", request.auth)
            
            # Validate required fields
            plan_type = request.data.get('plan_type')
            channels = request.data.get('channels', [])
            timeline = request.data.get('timeline')
            
            if not plan_type:
                return Response({'error': 'plan_type is required'}, status=status.HTTP_400_BAD_REQUEST)
            if not channels:
                return Response({'error': 'channels is required'}, status=status.HTTP_400_BAD_REQUEST)
            if not timeline:
                return Response({'error': 'timeline is required'}, status=status.HTTP_400_BAD_REQUEST)
                
            # Validate plan_type
            if plan_type not in [choice[0] for choice in Plan.PLAN_TYPES]:
                return Response({'error': f'Invalid plan_type. Must be one of: {[choice[0] for choice in Plan.PLAN_TYPES]}'}, 
                              status=status.HTTP_400_BAD_REQUEST)
                
            # Validate timeline
            if timeline not in [choice[0] for choice in Plan.TIMELINE_CHOICES]:
                return Response({'error': f'Invalid timeline. Must be one of: {[choice[0] for choice in Plan.TIMELINE_CHOICES]}'}, 
                              status=status.HTTP_400_BAD_REQUEST)
            
            # Create the plan
            plan = Plan.objects.create(
                user=request.user,
                title=f"New SmartPlan - {timezone.now().strftime('%B %d, %Y')}",
                plan_type=plan_type,
                channels=channels,
                timeline=timeline,
                status='draft'  # Initial status
            )
            
            print("Plan created:", plan.id)
            
            # Return success response with plan data
            return Response({
                'id': plan.id,
                'title': plan.title,
                'plan_type': plan.plan_type,
                'channels': plan.channels,
                'timeline': plan.timeline,
                'status': plan.status,
                'created_at': plan.created_at,
                'message': 'Plan created successfully'
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            print("Error creating plan:", str(e))
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
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
