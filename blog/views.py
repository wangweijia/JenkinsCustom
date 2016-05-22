from django.shortcuts import render_to_response, render
from django.http import HttpResponse
from .forms import *
from .models import *
from archiveSetting.archive2 import JenkinsCustomServer
from archiveSetting.commit import MyCommit


def login(req):
    if req.method == 'POST':
        form = LoginForm(req.POST)
        if form.is_valid():
            user = req.POST.get('userName')
            pwd = req.POST.get('passWord')

            user = User.objects.filter(userName__exact=user, passWord__exact=pwd)
            if user:
                req.session['login'] = 1
                for u in user:
                    req.session['userID'] = u.id
                    req.session['userDepartment'] = u.department
                return index(req)
            else:
                prompt = '用户名或密码错误!'
                return render(req, 'login.html', {'form': form, 'prompt': prompt})
        else:
            prompt = '请正确填写信息!'
            return render(req, 'login.html', {'form': form, 'prompt': prompt})
    else:
        form = LoginForm()
        return render(req, 'login.html', {'form': form})


def index(req):
    try:
        isLogin = bool(req.session['login'])
    except:
        isLogin = False

    if isLogin:
        jenkins = JenkinsCustomServer()
        jobs = jenkins.jenkins_jobs()

        try:
            selectedJobName = req.session['jobName']
        except:
            selectedJob = jobs[0]
            selectedJobName = selectedJob['name']
            req.session['jobName'] = selectedJobName

        os = jenkins.jenkins_job_os(selectedJobName)
        req.session['os'] = os
        if os == 'ios':
            tagArray = ['builders', 'au.com.rayh.XCodeBuilder', 'configuration']
        else:
            tagArray = []

        config = jenkins.jenkins_job_config_xml(selectedJobName, tagArray)
        buildable = jenkins.jenkins_job_buildable(selectedJobName)
        configForm = ProjectConfig()

        content = {'jobs': jobs,
                   'config': config,
                   'configForm': configForm,
                   'selectJob': selectedJobName,
                   'buildable': buildable,
                   'commits': {},
                   'commitAble': True}
        return render(req, "index.html", content)
    else:
        return login(req)


def config(req):
    if req.method == 'POST':
        form = ProjectConfig(req.POST)
        if form.is_valid():
            queue = req.POST.get('queue')

            if req.session['os'] == 'ios':
                tagArray = ['builders', 'au.com.rayh.XCodeBuilder', 'configuration']
            else:
                tagArray = []

            jobName = req.session['jobName']
            jenkins = JenkinsCustomServer()

            newxml = jenkins.jenkins_new_job_config_xml(jobName, tagArray, queue)
            jenkins.jenkins_change_job_config(newxml, jobName)

            return index(req)
        else:
            HttpResponse('<h>login lose \'not form.is_valid()\'</h>')
    else:
        index(req)


def build(req):
    jobName = req.session['jobName']
    jenkins = JenkinsCustomServer()
    jenkins.jenkins_build_project(jobName)
    return index(req)


def job(req):
    if req.method == 'GET':
        jobName = req.GET.get('jobName')
        if jobName:
            req.session['jobName'] = jobName

    return index(req)


def commit(req):
    if req.method == 'POST':
        userId = req.session['userID']
        userDepartment = req.session['userDepartment']
        c = MyCommit(userId, userDepartment)
