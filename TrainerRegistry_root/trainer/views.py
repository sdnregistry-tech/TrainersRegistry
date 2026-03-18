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
from .models import Trainer, Qualification
from datetime import date

def dashboard(request):
    total_trainers = Trainer.objects.count()
    total_active = Qualification.objects.filter(validity_date__gte=date.today()).count()
    total_expired = Qualification.objects.filter(validity_date__lt=date.today()).count()

    chart_data = Qualification.objects.values('certificate_name').annotate(count=Count('id'))
    labels = [item['certificate_name'] for item in chart_data]
    data = [item['count'] for item in chart_data]

    context = {
        'total_trainers': total_trainers,
        'total_active': total_active,
        'total_expired': total_expired,
        'labels': labels,
        'data': data,
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

def resend_all_notifications(request, trainer_id):
    q = get_object_or_404(Qualification, id=trainer_id)
    trainer = q.trainer
    today = date.today()
    three_months = today + timedelta(days=90)

    if q.validity_date <= three_months:
        send_expired_notice(
            email=trainer.email,
            trainer_name=f"{trainer.first_name} {trainer.last_name}",
            certificate_name=q.certificate_name,
            validity_date=q.validity_date.strftime("%B %d, %Y")
        )
    # Redirect back to the trainer's qualifications page
    return redirect('trainer_qualifications', trainer_id=trainer.id)
