from django.shortcuts import render_to_response, render
from django.http import HttpResponse
from .forms import *
from archiveSetting.archive2 import JenkinsCustomServer


def login(req):
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
                return index(req)
            else:
                req.session['login'] = 0
                return HttpResponse('<h>userName or passWord error</h>')
        else:
            return HttpResponse('<h>login lose \'not form.is_valid()\'</h>')
    else:
        form = LoginForm()
        return render(req, 'login.html', {'form': form})


def index(req):
    try:
        isLogin = bool(req.session['login'])
    except:
        isLogin = False

    if isLogin:
        user = req.session['userName']
        pwd = req.session['passWord']
        jenkins = JenkinsCustomServer(url='http://localhost:8080/', userName=user, password=pwd)
        jobs = jenkins.jenkins_jobs()

        try:
            selectedJobName = req.session['jobName']
        except:
            selectedJob = jobs[0]
            selectedJobName = selectedJob['name']
            req.session['jobName'] = selectedJobName

        os = jenkins.jenkins_project_os(selectedJobName)
        req.session['os'] = os
        if os == 'ios':
            tagArray = ['builders', 'au.com.rayh.XCodeBuilder', 'configuration']
        else:
            tagArray = []

        config = jenkins.jenkins_job_config_xml(selectedJobName, tagArray)
        building = jenkins.jenkins_job_status(selectedJobName)
        configForm = ProjectConfig()
        return render(req, "index.html", {'jobs': jobs, 'config': config, 'configForm': configForm, 'selectJob': selectedJobName, 'building': building})
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

            user = req.session['userName']
            pwd = req.session['passWord']
            jobName = req.session['jobName']
            jenkins = JenkinsCustomServer(url='http://localhost:8080/', userName=user, password=pwd)

            newxml = jenkins.jenkins_new_job_config_xml(jobName, tagArray, queue)
            jenkins.jenkins_change_job_config(newxml, jobName)

            return index(req)
        else:
            HttpResponse('<h>login lose \'not form.is_valid()\'</h>')
    else:
        index(req)


def build(req):
    user = req.session['userName']
    pwd = req.session['passWord']
    jobName = req.session['jobName']
    jenkins = JenkinsCustomServer(url='http://localhost:8080/', userName=user, password=pwd)
    jenkins.jenkins_build_project(jobName)
    return index(req)


def job(req):
    if req.method == 'GET':
        jobName = req.GET.get('jobName')
        if jobName:
            req.session['jobName'] = jobName

    return index(req)