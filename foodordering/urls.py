from django.contrib import admin 
from django.urls import path,include 
from login import views 
urlpatterns = [ 
    path('',include('login.urls')),
 	path('admin/', admin.site.urls),
	path('Regis/',views.Registration),
	path('Logins/',views.Login_User),
 ]
