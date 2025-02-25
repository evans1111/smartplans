from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'templates', views.TemplateViewSet)
router.register(r'plans', views.GeneratedPlanViewSet, basename='plan')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', views.register_user, name='register'),
    path('auth/login/', views.login_user, name='login'),
    path('auth/logout/', views.logout_user, name='logout'),
    path('auth/user/', views.get_user, name='user'),
    path('users/settings/', views.user_settings, name='user_settings'),
    path('plans/', views.plan_list_create, name='plan-list-create'),
    path('plans/<int:plan_id>/', views.plan_detail, name='plan-detail'),
] 