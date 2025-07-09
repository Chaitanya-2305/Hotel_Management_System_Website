from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from HotelApp.models import Tablebook, ContactTable
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .form import UserRegisterForm
from .decorator import checksuperuser
from django.core.mail import send_mail
from django.conf import settings

# ✅ Reusable helper function
def create_contact_entry(name, mail, msg):
    b_obj = ContactTable.objects.create(name=name, mail=mail, spl=msg)
    b_obj.save()

# ✅ Home view
@login_required(login_url='loginurl')
def Homeview(request):
    if request.method == 'GET':
        return render(request, 'Home.html')

# ✅ Table booking view
def Tableview(request):
    if request.method == 'GET':
        return render(request, 'Table.html')

    if request.method == 'POST':
        dt = request.POST['date']
        cnt = int(request.POST['guestcnt'])
        gname = request.POST['name']
        gnum = int(request.POST['number'])
        gmail = request.POST['mail']
        spl = request.POST['splreq']

        # Save booking
        h_obj = Tablebook.objects.create(Date=dt, count=cnt, name=gname, num=gnum, mail=gmail, spl=spl)
        h_obj.save()

        # Send booking confirmation email
        send_mail(
            subject='Table Booking Confirmation',
            message=f"Hi {gname},\n\nYour table has been booked on {dt} for {cnt} guest(s).\n\nThanks!",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[gmail],
            fail_silently=False,
        )

        # ✅ Automatically create a contact entry
        create_contact_entry(gname, gmail, spl)

        return render(request, 'Table.html', {
            'res': f'Thank You {gname} For Booking The Table. Please Check Your Mail (including spam) For Confirmation!'
        })

# ✅ Menu view
class menuview(View):
    def get(self, request):
        return render(request, 'Menu.html')

# ✅ View for admin to see bookings
@checksuperuser
def Bookingview(request):
    if request.method == 'GET':
        cust = Tablebook.objects.all()
        return render(request, 'Booking.html', {'customers': cust})

# ✅ Login view
def loginview(request):
    if request.method == 'GET':
        return render(request, 'Login.html')
    
    if request.method == 'POST':
        usr = request.POST['uname']
        psd = request.POST['pwd']
        valid_user = authenticate(request, username=usr, password=psd)
        if valid_user is None:
            messages.error(request, 'Invalid Credentials')
            return redirect('loginurl')
        else:
            login(request, valid_user)
            return redirect('homeurl')

# ✅ Logout view
def logoutview(request):
    logout(request)
    return redirect('loginurl')

# ✅ Signup view
def signupview(request):
    if request.method == 'GET':
        emptyform = UserRegisterForm()
        return render(request, 'Signup.html', {'forms': emptyform})
    if request.method == 'POST':
        dataform = UserRegisterForm(request.POST)
        if dataform.is_valid():
            dataform.save()
            return redirect('loginurl')
        else:
            return render(request, 'Signup.html', {'forms': dataform})

# ✅ About page
def aboutview(request):
    if request.method == 'GET':
        return render(request, 'about.html')

# ✅ Contact form view
def contactview(request):
    if request.method == 'GET':
        return render(request, 'contact.html')
    
    if request.method == 'POST':
        gname = request.POST['name']
        gmail = request.POST['mail']
        msg = request.POST['spl']

        # Save contact entry
        create_contact_entry(gname, gmail, msg)

        # Send confirmation email
        send_mail(
            subject='Thanks for Contacting Us!',
            message=f"Hi {gname},\n\nThank you for reaching out to us.\n\nWe received your message:\n\"{msg}\"\n\nWe'll get back to you shortly.\n\nBest regards,\nHotel Team",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[gmail],
            fail_silently=False,
        )

        return render(request, 'contact.html', {
            'con': f'Thank You {gname} For contacting us. Please check your mail for confirmation...!'
        })
