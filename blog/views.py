from django.shortcuts import render_to_response, render
from django.http import HttpResponse
from .forms import LoginForm
from archiveSetting.archive2 import JenkinsCustomServer

# admin wwj123456

def index(req):
	if req.method == 'POST':
		form = LoginForm(req.POST)
		if form.is_valid():
			user = req.POST.get('userName')
			pwd = req.POST.get('passWord')

			jenkins = JenkinsCustomServer(url='http://localhost:8080/', userName=user, password=pwd)

			if jenkins.jenkins_login():
				req.session['login'] = 1
				req.session['userName'] = user
				req.session['passWord'] = pwd
				return render_to_response('index.html', {})
			else:
				req.session['login'] = 0
				return HttpResponse('<h>userName or passWord error</h>')
		else:
			return HttpResponse('<h>login lose</h>')
	else:
		try:
			isLogin = bool(req.session['login'])
		except:
			isLogin = False
		if isLogin:
			user = req.session['userName']
			pwd = req.session['passWord']
			jenkins = JenkinsCustomServer(url='http://localhost:8080/', userName=user, password=pwd)

			jobs = jenkins.jenkins_jobs()

			return render_to_response('index.html', {'jobs': jobs})
		else:
			form = LoginForm()
			return render(req, 'login.html', {'form': form})
			# return render_to_response('login.html', {'form': form})
