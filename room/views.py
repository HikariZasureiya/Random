from django.shortcuts import render , redirect
from .models import messaging
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.utils import timezone
# from lsystem.models import pim
from django.contrib.auth import logout
# Convert the UTC time to the user's time zone



def mainroom(request):
    if not request.user.is_authenticated:
        return redirect("signin")
    
    username = request.user.username
    the_message=request.POST.get('mainarea')

    
    if request.method == 'POST' and 'logout' in request.POST:
        logout(request)
        return redirect('signin')

    if request.method=='POST':
            
        
            try:
                user_time_zone = request.session.get('user_timezone', 'UTC')
          
                utc_time = timezone.now()
                
                
                timezone.activate(user_time_zone)
                    
                user_specific_time = timezone.localtime(utc_time)
            
                timezone.deactivate()

                new_message = messaging.objects.create(user=username, message=the_message, time=user_specific_time)
            except Exception as e:
                print(f"Error occurred while creating messaging object: {e}")

    
         
    return render(request,"room.html")

def the_messages(request):
    if not request.user.is_authenticated:
        return redirect("signin")
    mess= messaging.objects.all()
    return JsonResponse({'online':list(mess.values())})

