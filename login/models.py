from django.db import models
from django.forms import ModelForm,Textarea
class Users_Regis(models.Model):
 	user_name=models.CharField(max_length=100)
 	email=models.CharField(max_length=100)
 	pwd=models.CharField(max_length=100)
 	
class User_Menu(models.Model):
	user_name=models.CharField(max_length=100)
	item_name=models.CharField(max_length=100)
	price=models.IntegerField()
	quantity=models.IntegerField()
	total=models.IntegerField()
	status=models.CharField(max_length=100)