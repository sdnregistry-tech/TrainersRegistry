from django.shortcuts import render
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Trainer
from django.shortcuts import render, get_object_or_404, redirect
from .forms import QualificationForm
from django.shortcuts import render, get_object_or_404
from .models import Trainer, Qualification
from datetime import datetime
from django.http import HttpResponse
import openpyxl
from .forms import AssessorQualificationForm


@login_required(login_url='login')

def HomePage(request):
    return render (request,'home.html')

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("Your password and confrom password are not Same!!")
        else:

            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
        
    return render (request,'signup.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'login.html')

def resend_all_notifications(request):
    return redirect('resend_all_notifications')

def PasswordResetView(request):
    return redirect('password_reset')

def PasswordResetDoneView(request):
    return redirect('password_reset_done')

def PasswordResetConfirmView(request):
    return redirect('password_reset_confirm')

def PasswordResetCompleteView(request):
    return redirect('password_reset_complete')

def report_trainers_with_qualifications(request):
    return redirect('reports')

def export_trainers_with_qualifications_excel(request):
    return redirect('export_trainers_with_qualifications_excel')

def LogoutPage(request):
    return redirect('login')

def trainer_form(request):
    return redirect('trainer_form.html')

def trainer_list(request):
    return redirect('trainer_list.html')

def dashboard(request):
    return redirect('dashboard.html')

def add_qualification(request, trainer_id):
    trainer = get_object_or_404(Trainer, pk=trainer_id)
    if request.method == 'POST':
        form = QualificationForm(request.POST)
        if form.is_valid():
            qualification = form.save(commit=False)
            qualification.trainer = trainer
            qualification.save()
        return redirect('trainer_list') 
    else:
       
        form = QualificationForm()
    return render(request, 'trainer/add_qualification.html', {'form': form, 'trainer': trainer}) 
  
def trainer_form(request):
    search_query = request.GET.get("query", "")  

    if search_query:
        trainers = Trainer.objects.filter(
            Q(first_name__icontains=search_query) |
            Q(middle_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )
    else:
        trainers = Trainer.objects.all()

    if request.method == "POST":
        if "create" in request.POST:
            Trainer.objects.create(
                first_name=request.POST.get("first_name"),
                middle_name=request.POST.get("middle_name"),
                last_name=request.POST.get("last_name"),
                gender=request.POST.get("gender"),
                address=request.POST.get("address"),
                birthdate=request.POST.get("birthdate"),
                email=request.POST.get("email"),
                contact_number=request.POST.get("contact_number"),
            )
            messages.success(request, "Trainer added successfully")
            return redirect("trainer_form")

        elif "update" in request.POST:
            trainer = Trainer.objects.get(id=request.POST.get("id"))
            trainer.first_name = request.POST.get("first_name")
            trainer.middle_name = request.POST.get("middle_name")
            trainer.last_name = request.POST.get("last_name")
            trainer.gender = request.POST.get("gender")
            trainer.address = request.POST.get("address")
            trainer.birthdate = request.POST.get("birthdate")
            trainer.email = request.POST.get("email")
            trainer.contact_number = request.POST.get("contact_number")
            trainer.save()
            messages.success(request, "Trainer updated successfully")
            return redirect("trainer_form")

        elif "delete" in request.POST:
            Trainer.objects.get(id=request.POST.get("id")).delete()
            messages.success(request, "Trainer deleted successfully")
            return redirect("trainer_form")

    context = {
        "trainers": trainers,
        "search_query": search_query,
    }
    return render(request, "trainer_form.html", context)


def trainer_list(request):
    trainers = Trainer.objects.all()
    return render(request, 'trainer_list.html', {'trainers': trainers})

def trainer_qualifications(request, trainer_id):
    trainer = get_object_or_404(Trainer, id=trainer_id)
    qualifications = Qualification.objects.filter(trainer=trainer)

    return render(request, 'trainer/trainer_qualifications.html', {
        'trainer': trainer,
        'qualifications': qualifications,
    })

def update_qualification_modal(request, qualification_id):
    qualification = get_object_or_404(Qualification, id=qualification_id)

    if request.method == 'POST':
        certificate_name = request.POST.get('certificate_name')
        nttc_number = request.POST.get('nttc_number')
        validity_date = request.POST.get('validity_date')

        # Basic validation (optional)
        if certificate_name and nttc_number and validity_date:
            qualification.certificate_name = certificate_name
            qualification.nttc_number = nttc_number
            qualification.validity_date = datetime.strptime(validity_date, "%Y-%m-%d").date()
            qualification.status = qualification.status()
            qualification.save()

            messages.success(request, "Qualification updated successfully.")
        else:
            messages.error(request, "All fields are required.")

        return redirect('trainer_qualifications', trainer_id=qualification.trainer.id)
    
from django.shortcuts import render
from .models import Trainer, Qualification
from django.db.models import Count


def delete_qualification(request, qualification_id):
    qualification = get_object_or_404(Qualification, id=qualification_id)
    trainer_id = qualification.trainer.id  # Keep trainer ID for redirection

    if request.method == 'POST':
        qualification.delete()
        messages.success(request, "Qualification deleted successfully.")
        return redirect('trainer_qualifications', trainer_id=trainer_id)

    return render(request, 'trainer/delete_qualification.html', {'qualification': qualification})

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Qualification
from .forms import QualificationForm

def update_qualification(request, qualification_id):
    qualification = get_object_or_404(Qualification, id=qualification_id)

    if request.method == 'POST':
        form = QualificationForm(request.POST, instance=qualification)
        if form.is_valid():
            updated_qualification = form.save(commit=False)
            # Avoid calling the method as if it's a function
            # The status will be recomputed when accessed, no need to assign it
            updated_qualification.save()
            messages.success(request, "Qualification updated successfully.")
            return redirect('trainer_qualifications', trainer_id=updated_qualification.trainer.id)
    else:
        form = QualificationForm(instance=qualification)

    return render(request, 'update_qualification.html', {
        'form': form,
        'qualification': qualification
    })

from django.shortcuts import render
from .models import Trainer, Assessor, Qualification, AssessorQualification
from datetime import date
from django.db.models import Count, Q

def dashboard(request):
    today = date.today()

    # Trainers
    total_trainers = Trainer.objects.count()
    total_active_trainers = Qualification.objects.filter(validity_date__gte=today).count()
    total_expired_trainers = Qualification.objects.filter(validity_date__lt=today).count()

    # Assessors
    total_assessors = Assessor.objects.count()
    # Ignore NULL validity_date
    total_active_assessors = AssessorQualification.objects.filter(validity_date__isnull=False, validity_date__gte=today).count()
    total_expired_assessors = AssessorQualification.objects.filter(validity_date__isnull=False, validity_date__lt=today).count()

    # Chart data for trainer qualifications
    trainer_chart_data = Qualification.objects.values('certificate_name').annotate(count=Count('id'))
    trainer_labels = [item['certificate_name'] for item in trainer_chart_data]
    trainer_data = [item['count'] for item in trainer_chart_data]

    # Chart data for assessor qualifications
    assessor_chart_data = AssessorQualification.objects.values('certificate_name').annotate(count=Count('id'))
    assessor_labels = [item['certificate_name'] for item in assessor_chart_data]
    assessor_data = [item['count'] for item in assessor_chart_data]

    context = {
        'total_trainers': total_trainers,
        'total_active_trainers': total_active_trainers,
        'total_expired_trainers': total_expired_trainers,
        'total_assessors': total_assessors,
        'total_active_assessors': total_active_assessors,
        'total_expired_assessors': total_expired_assessors,
        'trainer_labels': trainer_labels,
        'trainer_data': trainer_data,
        'assessor_labels': assessor_labels,
        'assessor_data': assessor_data,
    }

    return render(request, 'dashboard.html', context)

def trainer_list(request):
    q = request.GET.get('q', '')

    trainers = Trainer.objects.all()

    if q:
        trainers = trainers.filter(
            Q(first_name__icontains=q) |
            Q(middle_name__icontains=q) |
            Q(last_name__icontains=q) |
            Q(email__icontains=q) |
            Q(contact_number__icontains=q)
        )

    return render(request, 'trainer_list.html', {
        'trainers': trainers
    })

# views.py
from django.shortcuts import render
from django.http import HttpResponse
from .models import Qualification
from .forms import QualificationReportForm
from datetime import date
import openpyxl
from django.db.models import Q
from openpyxl.utils import get_column_letter

def report_trainers_with_qualifications(request):
    form = QualificationReportForm(request.GET or None)
    qualifications = Qualification.objects.select_related('trainer').all()

    if form.is_valid():
        name = form.cleaned_data.get('name')
        cert = form.cleaned_data.get('certificate_name')
        date_from = form.cleaned_data.get('date_from')
        date_to = form.cleaned_data.get('date_to')

        if name:
            qualifications = qualifications.filter(
                Q(trainer__first_name__icontains=name) | Q(trainer__last_name__icontains=name)
            )
        if cert:
            qualifications = qualifications.filter(certificate_name__icontains=cert)
        if date_from:
            qualifications = qualifications.filter(validity_date__gte=date_from)
        if date_to:
            qualifications = qualifications.filter(validity_date__lte=date_to)

    # Export to Excel
    if 'export' in request.GET:
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Qualifications"
        ws.append(['Full Name', 'Email', 'Contact', 'Certificate', 'NTTC', 'Validity Date', 'Status'])

        for q in qualifications:
            status = "Expired" if q.validity_date < date.today() else "Valid"
            ws.append([
                f"{q.trainer.first_name} {q.trainer.last_name}",
                q.trainer.email,
                q.trainer.contact_number,
                q.certificate_name,
                q.nttc_number,
                q.validity_date.strftime("%b %d, %Y"),
                status
            ])
            

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=qualification_report.xlsx'
        wb.save(response)
        return response

    return render(request, 'reports.html', {
        'form': form,
        'qualifications': qualifications,
        'today': date.today(),

    })

# trainer/views.py
from django.shortcuts import get_object_or_404, redirect
from datetime import date, timedelta
from .models import Qualification
from .utils import send_expired_notice

def resend_all_notifications(request, qualification_id):
    qualification = get_object_or_404(Qualification, id=qualification_id)
    trainer = qualification.trainer

    if request.method not in ["POST", "GET"]:
        messages.error(request, "Invalid request method for resend.")
        return redirect('trainer_qualifications', trainer_id=trainer.id)

    try:
        sent = send_expired_notice(qualification, force_resend=True)
        if sent:
            messages.success(request, f"Notification resent to {trainer.email}.")
        else:
            messages.error(request, "Notification could not be resent.")
    except Exception as exc:
        messages.error(request, f"Failed to resend expiration notice: {exc}")

    return redirect('trainer_qualifications', trainer_id=trainer.id)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Assessor

def assessor_form(request):
    search_query = request.GET.get('query', '')
    if search_query:
        assessors = Assessor.objects.filter(first_name__icontains=search_query) | \
                    Assessor.objects.filter(last_name__icontains=search_query) | \
                    Assessor.objects.filter(email__icontains=search_query)
    else:
        assessors = Assessor.objects.all()

    if request.method == 'POST':
        assessor_id = request.POST.get('id')

        # CREATE new assessor
        if 'create' in request.POST:
            first_name = request.POST.get('first_name')
            middle_name = request.POST.get('middle_name', '')
            last_name = request.POST.get('last_name')
            gender = request.POST.get('gender')
            address = request.POST.get('address', '')
            birthdate = request.POST.get('birthdate') or None
            qualification = request.POST.get('qualification')
            email = request.POST.get('email')
            contact_number = request.POST.get('contact_number', '')

            if not qualification:
                messages.error(request, 'Qualification is required!')
            else:
                Assessor.objects.create(
                    first_name=first_name,
                    middle_name=middle_name,
                    last_name=last_name,
                    gender=gender,
                    address=address,
                    birthdate=birthdate,
                    qualification=qualification,
                    email=email,
                    contact_number=contact_number
                )
                messages.success(request, 'Assessor added successfully!')
            return redirect('assessor_form')

        # UPDATE existing assessor
        elif 'update' in request.POST:
            assessor = get_object_or_404(Assessor, id=assessor_id)
            assessor.first_name = request.POST.get('first_name')
            assessor.middle_name = request.POST.get('middle_name', '')
            assessor.last_name = request.POST.get('last_name')
            assessor.gender = request.POST.get('gender')
            assessor.address = request.POST.get('address', '')
            assessor.birthdate = request.POST.get('birthdate') or None
            assessor.qualification = request.POST.get('qualification')
            assessor.email = request.POST.get('email')
            assessor.contact_number = request.POST.get('contact_number', '')
            assessor.save()
            messages.success(request, 'Assessor updated successfully!')
            return redirect('assessor_form')

        # DELETE existing assessor
        elif 'delete' in request.POST:
            assessor = get_object_or_404(Assessor, id=assessor_id)
            assessor.delete()
            messages.success(request, 'Assessor deleted successfully!')
            return redirect('assessor_form')

    return render(request, 'assessor_form.html', {
        'assessors': assessors,
        'search_query': search_query
    })
from django.db.models import Q

def assessor_list(request):
    search_query = request.GET.get('query', '')

    if search_query:
        assessors = Assessor.objects.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    else:
        assessors = Assessor.objects.all()

    if request.method == 'POST':
        if 'update' in request.POST:
            assessor_id = request.POST.get('id')
            assessor = get_object_or_404(Assessor, pk=assessor_id)

            assessor.first_name = request.POST.get('first_name')
            assessor.middle_name = request.POST.get('middle_name', '')
            assessor.last_name = request.POST.get('last_name')
            assessor.gender = request.POST.get('gender')
            assessor.address = request.POST.get('address', '')
            assessor.birthdate = request.POST.get('birthdate') or None
            assessor.qualification = request.POST.get('qualification')
            assessor.email = request.POST.get('email')
            assessor.contact_number = request.POST.get('contact_number', '')
            assessor.save()

            messages.success(request, 'Assessor updated successfully!')
            return redirect('assessor_list')

        elif 'delete' in request.POST:
            assessor_id = request.POST.get('id')
            assessor = get_object_or_404(Assessor, pk=assessor_id)
            assessor.delete()

            messages.success(request, 'Assessor deleted successfully!')
            return redirect('assessor_list')

        elif 'create' in request.POST:
            Assessor.objects.create(
                first_name=request.POST.get('first_name'),
                middle_name=request.POST.get('middle_name', ''),
                last_name=request.POST.get('last_name'),
                gender=request.POST.get('gender'),
                address=request.POST.get('address', ''),
                birthdate=request.POST.get('birthdate') or None,
                qualification=request.POST.get('qualification'),
                email=request.POST.get('email'),
                contact_number=request.POST.get('contact_number', '')
            )
            messages.success(request, 'Assessor added successfully!')
            return redirect('assessor_list')

    return render(request, 'assessor_list.html', {
        'assessors': assessors,
        'search_query': search_query
    })

from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .models import Assessor

def delete_assessor(request, assessor_id):
    assessor = get_object_or_404(Assessor, id=assessor_id)
    assessor.delete()
    messages.success(request, 'Assessor deleted successfully!')
    return redirect('assessor_list')
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from datetime import datetime
from .models import Assessor, AssessorQualification

def add_assessor_qualification(request, assessor_id):
    assessor = get_object_or_404(Assessor, id=assessor_id)

    if request.method == 'POST':
        certificate_name = request.POST.get('certificate_name')
        nttc_number = request.POST.get('nttc_number')
        validity_date_str = request.POST.get('validity_date')

        if not certificate_name or not certificate_name.strip():
            messages.error(request, "Certificate Name is required.")
            return render(request, 'trainer/add_assessor_qualification.html', {'assessor': assessor})

        validity_date = None
        if validity_date_str:
            try:
                validity_date = datetime.strptime(validity_date_str, '%Y-%m-%d').date()
            except ValueError:
                messages.error(request, "Invalid date format. Use YYYY-MM-DD.")
                return render(request, 'trainer/add_assessor_qualification.html', {'assessor': assessor})

        AssessorQualification.objects.create(
            assessor=assessor,
            certificate_name=certificate_name,
            nttc_number=nttc_number or None,
            validity_date=validity_date
        )

        messages.success(request, 'Qualification added successfully!')
        return redirect('assessor_qualifications', assessor_id=assessor.id)
    return render(request, 'trainer/add_assessor_qualification.html', {'assessor': assessor})

from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from .models import AssessorQualification


def resend_assessor_qualification_email(request, qualification_id):
    qualification = get_object_or_404(AssessorQualification, id=qualification_id)
    assessor = qualification.assessor

    # ✅ Safety check
    if not assessor:
        messages.error(request, "No assessor linked to this qualification.")
        return redirect('assessor_list')

    if not assessor.email:
        messages.error(request, f"{assessor.first_name} has no email set.")
        return redirect('assessor_qualifications', assessor_id=assessor.id)

    # ✅ FIX: removed .title (does not exist)
    subject = f"Qualification Reminder: {qualification.certificate_name}"

    message = f"""
Dear {assessor.first_name} {assessor.last_name},

This is a reminder regarding your qualification:

Certificate: {qualification.certificate_name}
Expiry Date: {qualification.validity_date.strftime('%B %d, %Y') if qualification.validity_date else 'N/A'}
Status: {qualification.status if hasattr(qualification, 'status') else 'N/A'}

Please take action if necessary.

Best regards,
TESDA Provincial Office Surigao Del Norte
"""

    send_mail(
        subject,
        message,
        'sdnregistry@gmail.com',
        [assessor.email],
        fail_silently=False
    )

    messages.success(request, f"Email sent to {assessor.first_name} ({assessor.email}).")

    return redirect('assessor_qualifications', assessor_id=assessor.id)
from .models import Assessor

def edit_assessor(request, assessor_id):
    assessor = get_object_or_404(Assessor, id=assessor_id)

    if request.method == 'POST':
        assessor.first_name = request.POST.get('first_name')
        assessor.middle_name = request.POST.get('middle_name', '')
        assessor.last_name = request.POST.get('last_name')
        assessor.gender = request.POST.get('gender')
        assessor.address = request.POST.get('address', '')
        assessor.birthdate = request.POST.get('birthdate') or None
        assessor.qualification = request.POST.get('qualification')
        assessor.email = request.POST.get('email')
        assessor.contact_number = request.POST.get('contact_number', '')
        assessor.save()
        messages.success(request, 'Assessor updated successfully!')
        return redirect('assessor_list')

    return render(request, 'edit_assessor.html', {'assessor': assessor})

def delete_assessor(request, assessor_id):
    assessor = Assessor.objects.get(id=assessor_id)
    if request.method == "POST":
        assessor.delete()
        messages.success(request, "Assessor deleted successfully!")
        return redirect('assessor_list')

from django.shortcuts import render, get_object_or_404
from .models import Assessor

def assessor_qualifications(request, assessor_id):
    assessor = get_object_or_404(Assessor, id=assessor_id)
    
    qualifications = assessor.qualifications.all()  
    context = {
        'assessor': assessor,
        'qualifications': qualifications,
    }

    return render(request, 'trainer/assessor_qualifications.html', context)

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from datetime import datetime
from .models import AssessorQualification


def edit_qualification(request, qualification_id):
    qualification = get_object_or_404(AssessorQualification, id=qualification_id)

    if request.method == 'POST':
        certificate_name = request.POST.get('certificate_name')
        nttc_number = request.POST.get('nttc_number')
        validity_date_str = request.POST.get('validity_date')

        if certificate_name:
            qualification.certificate_name = certificate_name
            qualification.nttc_number = nttc_number or None

            if validity_date_str:
                try:
                    qualification.validity_date = datetime.strptime(validity_date_str, '%Y-%m-%d').date()
                except ValueError:
                    messages.error(request, "Invalid date format. Use YYYY-MM-DD.")
                    return render(request, 'trainer/edit_qualification.html', {
                        'qualification': qualification
                    })

            qualification.save()
            messages.success(request, "Qualification updated successfully!")

           
            if qualification.assessor:
                return redirect('assessor_qualifications', assessor_id=qualification.assessor.id)
            else:
                messages.error(request, "No assessor linked.")
                return redirect('assessor_list')

        else:
            messages.error(request, "Certificate Name is required.")

    return render(request, 'trainer/edit_qualification.html', {
        'qualification': qualification
    })

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import AssessorQualification

def delete_assessor(request, assessor_id):
    qualification = get_object_or_404(AssessorQualification, id=assessor_id)
    assessor_id = qualification.assessor.id
    qualification.delete()
    messages.success(request, "Qualification deleted successfully!")
    return redirect('assessor_qualifications', assessor_id=assessor_id)
    
