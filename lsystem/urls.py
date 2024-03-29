
from django.urls import path,re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("",views.home, name='home'),
    path("signup",views.signup, name='singup'),
    path('verify/<str:username>/<str:uidb64>/', views.verify_email, name='verify_email'),
    path("login",views.signin, name='signin'),
    path("verification_successful",views.verification_success, name='verification_success'),
    path("verification_failed",views.failed_verification, name='verification_failed'),
    # path("verify",views.verify, name='verify'),
    # re_path(r'^users/(?P<username>[\w.@+-]+)/$', views.profile, name='profile'),
    path('usernamecheck',views.usernamecheck,name='usernamecheck'),
    path('forgot', views.forgot_password, name='forgot'),
    path('resetpassword/<str:username>/<str:uidb64>', views.reset_password, name='pass_reset'),
]
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
