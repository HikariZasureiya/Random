from django.http import JsonResponse
from django.shortcuts import render, redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.contrib import messages
from room.models import online
# from .models import pim
from .forms import signinform, loginform


from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from django.contrib.auth import get_user_model
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

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

User = get_user_model()

def send_verification_email(user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    verification_url = f"http://random-uo5k.onrender.com/verify/{uid}/{token}/"
    subject = 'Verify your email'
    message = f'Hello {user.username} Click the link below to verify your email: {verification_url}'
    recipient_email = user.email
    send_mail(subject, message, 'modnar694200@gmail.com', [recipient_email])

def verify_email(request, uidb64, token):

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True  
        user.save()
        return redirect('verification_success')
    else:
        return redirect('verification_failed')
    

def verification_success(request):
    return render(request,'is_verified.html')


def failed_verification(request):
    return render(request,'failed_verification.html')


def verify(request):
    return render(request,'verify.html')



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
                return redirect('signin')
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
                        return redirect('verify')
                else:
                    print('Invalid credentials')
                    the_form = loginform()
                    messages.error(request, "Wrong credentials")
                    # return redirect('verify')
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
