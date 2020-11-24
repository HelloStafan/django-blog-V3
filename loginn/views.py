from django.shortcuts import render,redirect
from django.urls import reverse

from .models import User
import json
'''
	注意以下两种方法
	# 1. return redirect(reverse("home:home"))  reverse方法
	# 2. return redirect(request.META.get('HTTP_REFERER'), 
	# 			{"msg": "该用户不存在！"})
'''

def dowhat(request):
	# 记录之前浏览的页面
	user_before_view = request.META.get('HTTP_REFERER')
	request.session["user_before_view"] = user_before_view

	dowhat = request.GET.get("dowhat")
	if dowhat == "loginout":
		return redirect("/user/loginout")
	elif dowhat == "register":
		return render(request, "register.html")
	else:
		# 不传参数是登录，即默认是登录 
		return render(request, "login.html")
		

def register(request):


	username = request.POST.get('username')
	password = request.POST.get('password')

	user = User.objects.filter(name = username)

	# 用户已存在
	if user:
		return render(request, "register.html", {"msg": "该用户名已被占用！"})
	else:
		user = User(name=username, password=password)
		user.save()
		request.session["userid"] = user.id
		return redirect(request.session["user_before_view"])

		

def login(request):
	

	username = request.POST.get('username')
	password = request.POST.get('password')

	user = User.objects.filter(name = username)

	if user:
		if password == user[0].password:
		
			request.session["userid"] = user[0].id
			return redirect(request.session["user_before_view"])
		else:
			return render(request, "login.html", {"msg": "密码错误！"})
	else:
		return render(request, "login.html", {"msg": "该用户不存在！"})
			

def login_out(request):
	try:
		del request.session["userid"]
	except KeyError:
		pass
	return redirect(request.META.get('HTTP_REFERER'))
	 