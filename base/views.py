from django.shortcuts import render,redirect, get_object_or_404
from .forms import RegisterForm , AppointmentForm
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import send_mail
from .models import Appointment
# Create your views here.

def landing_view(request):
    return render(request,'landing_page.html')

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
            login(request,user)
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request,'accounts/register.html',{'form':form})

def login_view(request):
    form = RegisterForm()
    error_message = None
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            if user.is_superuser:
                return redirect('admin')
            return redirect('home')
        else:
            error_message = 'Invalid Credentials'
    return render(request,'accounts/login.html',{'form':form,'error':error_message})
def logout_view(request):
    logout(request)
    return redirect('login')
@login_required
def home_view(request):
    appointments = Appointment.objects.filter(user=request.user)
    return render(request,'home.html',{'appointments':appointments})

@login_required
def create_appointment_view(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.save()
            return redirect('home')
    else:
        form = AppointmentForm()
    return render(request,'create_appointment.html',{'form':form,'title':'Créer un rendez-vous'})
@login_required
def edit_appointment_view(request, appointment_id):
    
    appointment = get_object_or_404(Appointment, id=appointment_id, user=request.user)

    if request.method == "POST":
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()  
            return redirect('home')  

    else:
        form = AppointmentForm(instance=appointment)  
    
    return render(request, 'edit_appointment.html', {
        'form': form, 
        'title': 'Modifier un rendez-vous'
    ,"appointment":appointment})
@login_required
def delete_appointment_view(request,appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, user=request.user)

    if request.method == "POST":
        appointment.delete()
        return redirect('home')

    return render(request, 'delete_appointment.html', {'appointment': appointment})
@login_required
def admin_view(request):
    if request.user.is_staff:  
        
        appointments = Appointment.objects.all()  
        return render(request, 'admin_dashboard.html', {'appointments': appointments})

@staff_member_required
def appointment_detail_view(request, appointment_id):
    
    appointment = get_object_or_404(Appointment, id=appointment_id)

    
    if request.method == 'POST':
        action = request.POST.get('action')  

        if action == 'confirm':
            send_confirmation_email(appointment)
            appointment.status = 'confirmed'  
        elif action == 'cancel':
            send_cancellation_email(appointment)
            appointment.status = 'cancelled'  

        appointment.save()  

        return redirect('admin') 

    return render(request, 'details.html', {'appointment': appointment})

def send_confirmation_email(appointment):
    subject = 'Appointment Confirmed'
    message = f"Dear {appointment.user.username},\n\nYour appointment on {appointment.start_time} has been confirmed.\n\nThank you!"
    send_mail(subject, message, 'hamza2tounsaoui@gmail.com', [appointment.user.email])

def send_cancellation_email(appointment):
    subject = 'Appointment Cancelled'
    message = f"Dear {appointment.user.username},\n\nYour appointment on {appointment.start_time} has been cancelled.\n\nSorry for the inconvenience!"
    send_mail(subject, message, 'hamza2tounsaoui@gmail.com', [appointment.user.email])