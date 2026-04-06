from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Auth / Login / Signup
    path('', views.LoginPage, name='login'),
    path('Signup/', views.SignupPage, name='signup'),
    path('home/', views.HomePage, name='home'),

    # Trainer URLs
    path('trainer_form/', views.trainer_form, name='trainer_form'),
    path('trainers/', views.trainer_list, name='trainer_list'),
    path('trainer/<int:trainer_id>/add_qualification/', views.add_qualification, name='add_qualification'),
    path('trainer/<int:trainer_id>/qualifications/', views.trainer_qualifications, name='trainer_qualifications'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('qualification/<int:qualification_id>/delete/', views.delete_qualification, name='delete_qualification'),
    path('qualification/<int:qualification_id>/update/', views.update_qualification, name='update_qualification'),
    path('reports/', views.report_trainers_with_qualifications, name='reports'),
    path('export/', views.export_trainers_with_qualifications_excel, name='export_trainers_with_qualifications_excel'),
    
    # Password reset
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),

    # Notification URLs
    path('qualification/<int:qualification_id>/resend/', views.resend_all_notifications, name='resend_all_notifications'),
    path('resend-all/<int:qualification_id>/', views.resend_all_notifications, name='resend_all_notifications_legacy'),

    # Assessor URLs
     path('assessor/register/', views.assessor_form, name='assessor_form'),
    path('assessor/list/', views.assessor_list, name='assessor_list'),

path('assessor/<int:assessor_id>/qualifications/', views.assessor_qualifications, name='assessor_qualifications'),
path('assessor/<int:assessor_id>/delete/', views.delete_assessor, name='delete_assessor'),
path('assessor/qualification/<int:qualification_id>/resend/', views.resend_assessor_qualification_email,name='resend_assessor_qualification_email'),
path('assessors/', views.assessor_list, name='assessor_list'),
path('assessor/<int:assessor_id>/edit/', views.edit_assessor, name='edit_assessor'),
path('assessor/<int:assessor_id>/add_assessor_qualification/', views.add_assessor_qualification, name='add_assessor_qualification'),
path('assessor/qualification/<int:qualification_id>/update/', views.edit_qualification, name='edit_qualification'),
]
