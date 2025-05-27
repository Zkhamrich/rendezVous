from django.urls import path
from . import views
urlpatterns = [
    path('',views.landing_view,name='landing'),
    path('register/',views.register_view,name='register'),
    path('login/',views.login_view,name='login'),
    path('logout',views.logout_view,name='logout'),
    path('home/',views.home_view,name='home'),
    path('home/create/',views.create_appointment_view,name="create_appointment"),
    path('home/edit/<int:appointment_id>/', views.edit_appointment_view, name='edit_appointment'),
    path('home/delete/<int:appointment_id>/', views.delete_appointment_view, name='delete_appointment'),
    path('dashboard',views.admin_view,name='admin'),
    path('dashboard/<int:appointment_id>/', views.appointment_detail_view, name='appointment_detail'),
]
