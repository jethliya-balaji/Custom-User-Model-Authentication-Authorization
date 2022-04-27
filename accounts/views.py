from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

from .form import RegistrationForm, LoginForm

from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

from .utils import send_verification_email
from .models import Account


# Create your views here.
def registration_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = RegistrationForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        messages.success(request, 'Congratulations! Your Account Is Created. Please Verify Your Email.')
        messages.success(request, f"Hey {user.first_name}, We just need to verify your email address before you can access your account therefore, we have sent you a verification email to your registered email address ({user.email}) Please check your email & If you don't receive an email, please make sure to check your spam folder. <a href='/resend_verification_email'>Resend Verification Email</a>")
        return send_verification_email(request, user.id)
        
    return render(request, 'registration/sign-up.html', context={
        'form': form,
    })

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = LoginForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password') 
        user = authenticate(email=email, password=password)
        login(request, user)
        messages.success(request, 'Welcome Back!')
        if request.GET.get('next'):  
            return redirect(request.GET.get('next')) 
        else:
            return redirect('home')


    return render(request, 'registration/sign-in.html', context={
        'form': form,
    })

def verify_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None:
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Congratulations! Your Account Is Activated. You Can Now Sign In.')
            return redirect('sign_in')
        elif user.is_active:
            messages.success(request, 'Your account is already active. Just Sign In.')
            return redirect('sign_in')
        else:
            messages.error(request, 'Something went wrong. Maybe activation link is expired.')
            return redirect('sign_in')  
    else:
        messages.error(request, 'This user does not exist.')
        return redirect('sign_in')

def resend_verification_email(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        try :
            user = Account._default_manager.get(email=email)
            if user.is_active:
                messages.success(request, 'Your account is already active. Just Sign In.')
                return redirect('sign_in')
            else:
                messages.success(request, 'We have resent you a verification email. Please check your email.')
                return send_verification_email(request, user.id)
        except Account.DoesNotExist:
            messages.error(request, 'No user with this email exists.')
            return redirect('sign_in')
    return render(request, 'registration/resend-verification-email.html')