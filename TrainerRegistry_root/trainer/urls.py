from django.urls import path
from .import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordResetConfirmView


urlpatterns = [
    path('', views.LoginPage, name='login'),
    path('Signup/',views.SignupPage,name='signup'),
    path('home/', views.HomePage, name='home'),
    path('trainer_form/', views.trainer_form, name='trainer_form'),
    path('trainers/', views.trainer_list, name='trainer_list'),
    path('trainer/<int:trainer_id>/add_qualification/', views.add_qualification, name='add_qualification'),
    path('trainer/<int:trainer_id>/qualifications/', views.trainer_qualifications, name='trainer_qualifications'),
    path('trainer/<int:trainer_id>/add_qualification/', views.add_qualification, name='add_qualification'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('qualification/<int:qualification_id>/delete/', views.delete_qualification, name='delete_qualification'),
    path('qualification/<int:qualification_id>/update/', views.update_qualification, name='update_qualification'),
    path('reports/', views.report_trainers_with_qualifications, name='reports'),
    path('export/', views.export_trainers_with_qualifications_excel, name='export_trainers_with_qualifications_excel'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path(
    'resend-all/<int:trainer_id>/',
    views.resend_all_notifications,
    name='resend_all_notifications'
),
]
