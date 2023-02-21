from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Account
# Create your views here.

def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        data = request.POST
        email = data['email']
        password = data['password']
        next_url = data['next_url']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            if next_url == '':
                return redirect('home')
            else:
                return redirect(next_url)
        else:
            messages.error(request, "Couldn't Login. Please check your credentials.")
    return render(request, 'userauth/login.html')

def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        data = request.POST
        fullname = data['fullname']
        email = data['email']

        is_ideator = True
        is_IC = False
        is_IG_admin = False

        password = data['password']
        password2 = data['password2']
        if password == password2:
            if Account.objects.filter(email=email).exists():
                messages.info(request, 'Email already in use. Please use another email.')
                return redirect('signup')
            else:
                user=Account.objects.create_user(fullname=fullname, email=email, is_ideator=is_ideator, is_IC=is_IC, is_IG_admin=is_IG_admin, password=password)
                user.save()
                login(request, user)
                messages.info(request, 'Account created successfully.')
                return redirect('login')
        else:
            messages.error(request, 'Please make sure the passwords match.')
            return redirect('signup')
    return render(request, 'userauth/signup.html')

def signup_IC(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        data = request.POST
        fullname = data['fullname']
        email = data['email']

        is_ideator = False
        is_IC = True
        is_IG_admin = False

        password = data['password']
        password2 = data['password2']
        if password == password2:
            if Account.objects.filter(email=email).exists():
                messages.info(request, 'Email already in use. Please use another email.')
                return redirect('signup')
            else:
                user=Account.objects.create_user(fullname=fullname, email=email, is_ideator=is_ideator, is_IC=is_IC, is_IG_admin=is_IG_admin, password=password)
                user.save()
                login(request, user)
                messages.info(request, 'Account created successfully.')
                return redirect('login')
        else:
            messages.error(request, 'Please make sure the passwords match.')
            return redirect('signup')
    email = request.GET.get('email', '')
    context = {
        'email':email,
    }
    return render(request, 'userauth/signup_IC.html', context)

def logout_user(request):
    if request.method == 'POST' and request.user.is_authenticated:
        logout(request)
        messages.info(request, 'You have been logged out.')
        return redirect('home')
    if not request.user.is_authenticated:
        return redirect('home')
    return redirect('home')

from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

def password_reset_request(request):
    if request.method == 'POST':
        data = request.POST
        email = data['email']
        associated_users = Account.objects.filter(Q(email=email))
        if associated_users.exists():
            for user in associated_users:
                subject = "Password Reset Requested at Bridgestone Innovation Garage"
                email_template_name = "userauth/password_reset/password_reset_email.txt"
                c = {
                "email":user.email,
                'domain':'127.0.0.1:8000',
                'site_name': 'Bridgestone Innovation Garage',
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "user": user,
                'token': default_token_generator.make_token(user),
                'protocol': 'http',
                }
                email = render_to_string(email_template_name, c)
                try:
                    send_mail(subject, email, 'omkarj3602@gmail.com' , [user.email], fail_silently=False)
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                return redirect ("/password_reset/done/")
        else:
            messages.info(request, 'Please enter a email that already exists.')
    return render(request=request, template_name="userauth/password_reset/password_reset.html")