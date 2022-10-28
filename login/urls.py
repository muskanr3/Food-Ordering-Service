from django.urls import path 
from . import views 
urlpatterns = [ 
     path('',views.loginView,name='lView'), 
     path('Cart/',views.Add_Cart),
     path('bill/',views.payment),
     path('paybill/',views.payMoney),
     path('logout/',views.logout),
     path('home/',views.home),
     path('showGraph/',views.graph), 
] 