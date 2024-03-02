
from django.urls import path
from . import views

urlpatterns = [
    path("mainroom",views.mainroom, name='mainroom'),    
    path('supersecretmessagejson',views.the_messages, name='j'),
]
