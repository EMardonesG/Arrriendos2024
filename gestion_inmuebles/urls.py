from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('about/', views.about, name='about'),
    path('exito/', views.exito, name='exito'),
    path('exito_reg/', views.exito_reg, name='exito_reg'),
    path('signup/', views.sign_up, name='sign_up'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    
    # Profile management
    path('profile/update/', views.update_profile, name='update_profile'),
    path('profile/delete/', views.delete_profile, name='delete_profile'),

    # Inmueble management
    path('inmueble/update/<int:inmueble_id>/', views.update_inmueble, name='update_inmueble'),
    path('inmueble/delete/<int:inmueble_id>/', views.delete_inmueble, name='delete_inmueble'),

    # Solicitud management
    path('solicitud/cancel/<int:solicitud_id>/', views.cancel_solicitud, name='cancel_solicitud'),
    path('inmueble/create/', views.create_inmueble, name='create_inmueble'),
    path('inmueble/apply/<int:inmueble_id>/', views.apply_for_solicitud, name='apply_for_solicitud'),
    path('solicitud/manage/<int:solicitud_id>/<str:action>/', views.manage_solicitud, name='manage_solicitud'),
    path('accept_solicitud/<int:solicitud_id>/', views.manage_solicitud, {'action': 'approve'}, name='accept_solicitud'),
    path('reject_solicitud/<int:solicitud_id>/', views.manage_solicitud, {'action': 'reject'}, name='reject_solicitud'),
    path('acerca/', views.acerca, name='acerca'),
    path('contacto/', views.contacto, name='contacto'), 

]



