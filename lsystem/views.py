from django.http import JsonResponse
from django.shortcuts import render, redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.contrib import messages
from room.models import online
from .models import cred
from .forms import signinform, loginform , resetform


from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from django.contrib.auth import get_user_model
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.urls import reverse
#from django.http import HttpResponse

from room.views import mainroom


#from 
from django.contrib.auth import get_user_model, login, authenticate
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.shortcuts import redirect, render
from django.core.mail import send_mail
from django.contrib import messages
import pyotp


User = get_user_model()


def send_verification_email(user):
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

    # Generate OTP
    base32secret3232 = pyotp.random_base32()
    otp = pyotp.TOTP(base32secret3232, interval=600, digits=6)
    otp_val = otp.now()
    # user.save()
    try:
        user1 = cred.objects.get(username=user.username)
        user1.otp_secret=base32secret3232
        user1.save()
    except:
        auser = cred.objects.create(otp_secret=base32secret3232,username=user.username)
        auser.save()
    

    subject = 'verification OTP'
    message = f'Hello {user.username}. your One Time Password (OTP) is: {otp_val}. \n this OTP will expire in 10 minutes. \n DO NOT  share your password with anyone.'
    recipient_email = user.email
    send_mail(subject, message, 'modnar694200@gmail.com', [recipient_email])


def send_verification_forgot(user):
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

    # Generate OTP
    
    base32secret3232 = pyotp.random_base32()
    otp = pyotp.TOTP(base32secret3232, interval=600, digits=6)
    otp_val = otp.now()
    user.save()
    try:
        auser = cred.objects.get(username=user.username)
        auser.otp_ver=base32secret3232
        auser.save()
    except cred.DoesNotExist:
        pass

    

    subject = 'Password reset OTP'
    message = f'Hello {user.username}. your One Time Password (OTP) is: {otp_val}. \n this OTP will expire in 10 minutes. \n DO NOT  share your password with anyone.'
    recipient_email = user.email
    send_mail(subject, message, 'modnar694200@gmail.com', [recipient_email])


def verify_email(request, username, uidb64):
    if request.method == 'POST':
        otp = request.POST.get('otp', None)
        if otp:
            try:
                
                uid = force_str(urlsafe_base64_decode(uidb64))
                user = User.objects.get(pk=uid)

                # username = user.username
                
                cred_instance = cred.objects.get(username=username)
                otp_verified = pyotp.TOTP(cred_instance.otp_secret, interval=600, digits=6).verify(otp)


                if otp_verified:
                    
                    user.is_active = True
                    user.save()
                    return HttpResponse('Email verification successful. You can now log in.')
                else:
                    return HttpResponse('Invalid OTP. Please try again.')
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                return HttpResponse('Invalid user ')
    else:
        return render(request, 'verify.html')








def verification_success(request):
    return render(request,'is_verified.html')


def failed_verification(request):
    return render(request,'failed_verification.html')


# def verify(request):
    
#     return render(request,'verify.html')



def signup(request):
    if request.method == 'POST':
        the_form=signinform(request.POST)
        if the_form.is_valid():

            username = the_form.cleaned_data['username']
            email = the_form.cleaned_data['email']
            password = the_form.cleaned_data['password']
            stripped_username=username.strip()



        # Create the user but set it as inactive
            try:
                auser = User.objects.create_user(username=stripped_username, email=email, password=password, is_active=False)
                auser.save()

                send_verification_email(auser)

                uidb64 = urlsafe_base64_encode(force_bytes(auser.pk))
                verification_url = reverse('verify_email', kwargs={'username':username,'uidb64': uidb64})
                
                return redirect(verification_url)

            except:
                print('no')
    else:
        the_form=signinform()

    return render(request, "signup.html",{'form':the_form})

def signin(request):
    if request.user.is_authenticated:
        return redirect("mainroom")
    
    if request.method == 'POST':
        the_form = loginform(request.POST)
        if the_form.is_valid():
            username = the_form.cleaned_data['username']
            password = the_form.cleaned_data['password']

            # Authenticate the user

            try:
                user1=User.objects.get(username=username)
                user = authenticate(username=username, password=password)
            
            
            
                if user1 is not None:
                    if user1.is_active:
                            login(request, user)
                            request.session['username'] = username
                            return redirect('mainroom')
                        
                    else:
                        print("User is not verified")
                        send_verification_email(user1)

                        uidb64 = urlsafe_base64_encode(force_bytes(user1.pk))
                        verification_url = reverse('verify_email', kwargs={'username':username,'uidb64': uidb64})
                
                        return redirect(verification_url)
                        #return redirect('verify')
                else:
                    print('Invalid credentials')
                    the_form = loginform()
                    messages.error(request, "Wrong credentials")

            except:
                print('Invalid credentials')
                the_form = loginform()
                messages.error(request, "Wrong credentials")
        else:
            print('Invalid form data')

            messages.error(request, "Invalid form data")
    else:
        the_form = loginform()

    return render(request, "login.html", {'form': the_form})


def usernamecheck(request):
    username=request.GET.get('username',None)
    data={}

    if username:
        existence=User.objects.filter(username=username).exists()

        if existence:
            data['available']=False
        else:
            data['available']=True
    else:
        data['available']=False
    return JsonResponse(data)


    
    


def home(request):
    return render(request, "index.html")

def forgot_password(request):
    if request.method=='POST':
        username = request.POST.get('forgot',None)
        stripped_username=username.strip()
        
    try:
        user1 = User.objects.get(username=stripped_username)
        send_verification_forgot(user1)
        uidb64 = urlsafe_base64_encode(force_bytes(user1.pk))
        verification_url = reverse('pass_reset', kwargs={'username':username,'uidb64': uidb64})
                
        return redirect(verification_url)
    except:
        HttpResponse("user doesn't exist")

    return render(request, "forgot.html")


def reset_password(request, username , uidb64):
    if request.method == 'POST':
        the_form=resetform(request.POST)
        if the_form.is_valid():
            otp = the_form.cleaned_data['otp']
            password = the_form.cleaned_data['password']

            if otp:
                try:
                    
                    uid = force_str(urlsafe_base64_decode(uidb64))
                    user = User.objects.get(pk=uid)

                    # username = user.username    
                
                    cred_instance = cred.objects.get(username=username)
                    otp_verified = pyotp.TOTP(cred_instance.otp_ver, interval=600, digits=6).verify(otp)
                    

                    if otp_verified:
                        user.set_password(password)
                        user.save()
                        return HttpResponse("successful")
                    else:
                        return HttpResponse("invalid otp")
                
                except:
                    return HttpResponse("something went wrong")
    else:
        the_form = resetform()
    
    return render(request, "reset.html", {'form': the_form})
    

            

    


    

