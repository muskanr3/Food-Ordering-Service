from django.shortcuts import render
from .models import Users_Regis
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate
from .models import User_Menu
from django.db.models import Sum
import pandas as pd
import matplotlib.pyplot as plt, mpld3
import urllib, base64
import io
from io import BytesIO
import base64
def loginView(request):
	return render(request,'home.html')
def Registration(request):
	flag=False
	ids=request.POST.get("rusername")
	emailM=request.POST.get("remail")
	pwds=request.POST.get("rpassword")
	cpwds=request.POST.get("rconfirmpwd")
	if Users_Regis.objects.filter(user_name=ids).exists():
		return render(request, "home.html", {"user_exists": "Please enter different username"})
	else:
		if pwds==cpwds:
			sref=Users_Regis(user_name=ids,email=emailM,pwd=pwds)
			sref.save()
			flag=True
	if flag == True:
		return render(request,'home.html',{"RegisConfirmMsg":"REGISTRATION SUCCESSFUL!!"})
	else:
		return render(request,'home.html',{"RegisInvalid":"ENTERED PASSWORD AND CONFIRMED PASSWORD DO NOT MATCH. PLEASE TRY AGAIN."})

def Login_User(request):
	users = Users_Regis.objects.all()
	lflag=True
	funame=request.POST.get("lusername")
	fpwd=request.POST.get("lpwd")
	print(funame,fpwd)
	print(users)
	if Users_Regis.objects.filter(user_name=funame,pwd=fpwd).exists():
		return render(request,"menu.html",{"loggedinUser":funame})
	else:
		return render(request, "home.html", {"invalid": "INVALID DETAILS. PLEASE TRY AGAIN."})
		
def Add_Cart(request):
	UserName=request.POST.get("uname")
	IName=request.POST.get("itemName")
	Iprice=str(request.POST.get("itemPrice")).split(":")
	Iprice=int(Iprice[1])
	quantity=int(request.POST.get("qty"))
	print("price",Iprice)
	tot=Iprice *quantity
	print("t",quantity)
	sref=User_Menu(user_name=UserName,item_name=IName, price=Iprice,quantity=quantity,total=tot,status='C')
	sref.save()
	return render(request, "menu.html", {"loggedinUser":UserName})
	
	
def payment(request):
	UserName=request.POST.get("uname")
	print("payment:",UserName)
	itemRec = User_Menu.objects.filter(user_name=UserName,status='C')
	ubill = User_Menu.objects.filter(user_name=UserName,status='C').aggregate(Sum('total'))
	print("payment:",UserName,ubill)
	return render(request, "payment.html", {"bildet": itemRec, "totbill": ubill, "loggedinUser": UserName})
	
def payMoney(request):
	tbill=request.POST.get("totbill")
	uName=request.POST.get("uname")
	print("final",uName)
	itemRec = User_Menu.objects.filter(user_name=uName,status='C').update(status='D')
	return render(request, "end.html", {"totbill": tbill, "clientName":uName})

def logout(request):
	return render(request, "home.html")

def home(request):
	return render(request, "home.html")
	
def graph(request):
   
    for items in User_Menu.objects.all():
        result = User_Menu.objects.values('item_name').filter(status='D').annotate(Sum('quantity'))
    print ('res',result)
    df=pd.DataFrame(result)
    #df = pd.DataFrame(User_Menu.objects.filter(status='D').aggregate(Sum('quantity')))
    #df = pd.DataFrame(User_Menu.objects.all().values())
    print(df)
    df.plot.bar(x="item_name", y="quantity__sum", title="Total Quantity Ordered", color=['lightblue', 'powderblue', 'palegreen', 'plum', 'mistyrose', 'lavender', 'gold', 'silver'],\
                edgecolor=['gold', 'blue', 'red', 'darkmagenta', 'deeppink', 'dodgerblue', 'green', 'red'])
    plt.xlabel('Items')
    plt.ylabel('Times ordered')
    plt.tight_layout()
    df.plot
    fig=plt.gcf()
    buf = BytesIO()
    fig.savefig(buf, format='png', dpi=100)
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read())
    uri = 'data:image/png;base64,' + urllib.parse.quote(image_base64)
    print(uri)
    return render(request,"graph.html", {"graphlib": uri})