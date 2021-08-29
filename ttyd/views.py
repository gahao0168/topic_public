from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from ttyd.models import TTYDFunc, FeedTime
from ttyd.forms import RegisterForm, LoginForm, TTYDFunctionForm
# from django.contrib import messages
from ttyd.mqtt import pubAndsub as pasb
from datetime import datetime
import json

# Create your views here.
# @login_required(login_url="/login/") --> 如果沒有登入就跳轉到登入

def index(request):
	if request.method == "POST":
		pass
	return render(request, "index.html", locals())


# 註冊
def sign_up(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():	
        	form.save()
        	# messages.success(request, 'Account created successfully')

        	username = request.POST.get("username")
	        data = FeedTime()
	        user = FeedTime.objects.filter(username=username)
	        selected = user
	        data.username = username
	        data.save()

	        username = form.cleaned_data.get('username')
	        raw_password = form.cleaned_data.get('password1')
	        user = authenticate(username=username, password=raw_password)
	        login(request, user)  # 直接登入
        	return redirect("/")  # 並重新導向到首頁

    context = {
        'form': form
    }
    return render(request, "register.html", context)

# 登入
def sign_in(request):
    form = LoginForm()
    if request.method == "POST":
	    username = request.POST.get("username")
	    password = request.POST.get("password")
	    user = authenticate(request, username=username, password=password)
	    if user is not None:
	        login(request, user)
	        return redirect('/')  #重新導向到首頁
    context = {
        'form': form
    }
    return render(request, "login.html", context)

# 登出
def sign_out(request):
	logout(request)
	return redirect("/login/")

def about(request):
	ttydfunctions = TTYDFunc.objects.all()

	form = TTYDFunctionForm()

	if request.method == "POST":
		form = TTYDFunctionForm(request.POST)
		if form.is_valid():
			form.save()
		return redirect("/about/")

	context = {
		'functions':ttydfunctions,
		'form':form
	}
	return render(request, "about.html", context)

def deleteTF(request, pk):
   	ttydfunction = TTYDFunc.objects.get(id=pk)

   	if request.method == "POST":
   		ttydfunction.delete()
   		return redirect('/about/')

   	context = {
   		'function':ttydfunction
   	}
   	return render(request, "deleteTF.html", context)

def updateTF(request, pk):
   	ttydfunction = TTYDFunc.objects.get(id=pk)

   	form = TTYDFunctionForm(instance=ttydfunction)

   	if request.method == "POST":
   		form = TTYDFunctionForm(request.POST, instance=ttydfunction)
   		if form.is_valid():
   			form.save()
   		return redirect("/about/")
   	context = {
   		'form':form
   	}
   	return render(request, "updateTF.html", context)

def set(request):
	username = request.user.username
	user = FeedTime.objects.filter(username=username)
	loop3 = range(1, 4)
	hours = range(24)
	minutes = range(60)
	show_subcribe = "即刻餵食待命中"
	record_err = list()
	try:
		data = FeedTime.objects.get(username=username)
		pre_feedtime = data.pre_feedtime
	except:
		pass
	feed_time1 = str(data.feed_time1).replace(":", '')
	feed_time2 = str(data.feed_time2).replace(":", '')
	feed_time3 = str(data.feed_time3).replace(":", '')
	h1 = feed_time1[0:2]
	m1 = feed_time1[2:4]
	h2 = feed_time2[0:2]
	m2 = feed_time2[2:4]
	h3 = feed_time3[0:2]
	m3 = feed_time3[2:4]
	if request.method == "POST":
		if "now" in request.POST:
			pasb.pub("now", username)
			show_subcribe = "已成功投食"
			pre_feedtime = datetime.now().strftime('%Y-%m-%d %H:%M')
			user.update(pre_feedtime=pre_feedtime)
			return render(request, "set.html", locals())
		elif "reset" in request.POST:
			user.update(feed_time1=None)
			user.update(feed_time2=None)
			user.update(feed_time3=None)
			pasb.pub("reset", username)
			return redirect("/set/")
		elif "record" in request.POST:
			if request.POST['hours1'] == "hours" and request.POST['minutes1'] == "minutes":
				record_err.append(0)
			elif request.POST['hours1'] == "hours" or request.POST['minutes1'] == "minutes":
				record_err.append(1)
			else:
				record_err.append(0)
				selected = request.POST['hours1'].zfill(2) + ":" + request.POST['minutes1'].zfill(2)
				user.update(feed_time1=selected)
			if request.POST['hours2'] == "hours" and request.POST['minutes2'] == "minutes":
				record_err.append(0)
			elif request.POST['hours2'] == "hours" or request.POST['minutes2'] == "minutes":
				record_err.append(1)
			else:
				record_err.append(0)
				selected = request.POST['hours2'].zfill(2) + ":" + request.POST['minutes2'].zfill(2)
				user.update(feed_time2=selected)
			if request.POST['hours3'] == "hours" and request.POST['minutes3'] == "minutes":
				record_err.append(0)
			elif request.POST['hours3'] == "hours" or request.POST['minutes3'] == "minutes":
				record_err.append(1)
			else:
				record_err.append(0)
				selected = request.POST['hours3'].zfill(2) + ":" + request.POST['minutes3'].zfill(2)
				user.update(feed_time3=selected)
			hint = 0
			count = 1
			for err in record_err:
				if err == 1:
					if hint == 0:
						hints = "設定錯誤："
						hints += f'餵食時間{count}'
						hint = 1
					else:
						hints += f', 餵食時間{count}'
				count += 1
			if hint == 1:
				hints += " 的 hours 或 minutes 未選擇，不更改其原先設定。"
			return render(request, "jump.html", locals())
		elif "send" in request.POST:
			feed_time_list = list()
			feed_time1 = str(data.feed_time1).replace(":", '')
			feed_time2 = str(data.feed_time2).replace(":", '')
			feed_time3 = str(data.feed_time3).replace(":", '')
			try:
				feed_time_list.append(int(feed_time1[0:2]))
				feed_time_list.append(int(feed_time1[2:4]))
			except:
				pass
			try:
				feed_time_list.append(int(feed_time2[0:2]))
				feed_time_list.append(int(feed_time2[2:4]))
			except:
				pass
			try:
				feed_time_list.append(int(feed_time3[0:2]))
				feed_time_list.append(int(feed_time3[2:4]))
			except:
				pass
			feed_time_list_json = json.dumps(feed_time_list)
			pasb.pub(feed_time_list_json, username)
			hints = "已傳送時間給裝置"
			return render(request, "jump.html", locals())
	return render(request, "set.html", locals())