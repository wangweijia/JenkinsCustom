import json
from django.shortcuts import render_to_response, render
from django.http import HttpResponse, HttpResponseRedirect
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
                    req.session['userDepartment'] = u.department.departmentName
                return HttpResponseRedirect('/index')
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

        userId = req.session['userID']
        userDepartment = req.session['userDepartment']
        name = User.objects.get(id=userId)

        commitAble = userDepartment == '开发部门'
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

        if commitAble:
            commit = MyCommit(userId, userDepartment, selectedJobName).commit_by_user().get(selectedJobName)
            commits = {name: commit}
        else:
            commit = MyCommit(userId, userDepartment, selectedJobName).all_commit()
            commits = {}
            for uid, com in commit.items():
                jobCommit = com.get(selectedJobName)
                if jobCommit:
                    uname = User.objects.get(id=int(uid)).name
                    commits[uname] = jobCommit

        content = {'jobs': jobs,
                   'config': config,
                   'configForm': configForm,
                   'selectJob': selectedJobName,
                   'buildable': buildable,
                   'commits': commits,
                   'commitAble': commitAble}

        return render(req, "index.html", content)
    else:
        return HttpResponseRedirect('/login')


def config(req):
    if req.method == 'POST':
        form = ProjectConfig(req.POST)
        if form.is_valid():
            queue = req.POST.get('queue')

            if req.session['os'] == 'ios':
                tagArray = ['builders', 'au.com.rayh.XCodeBuilder', 'configuration']
            elif req.session['os'] == 'android':
                tagArray = []

            jobName = req.session['jobName']
            jenkins = JenkinsCustomServer()

            newxml = jenkins.jenkins_new_job_config_xml(jobName, tagArray, queue)
            jenkins.jenkins_change_job_config(newxml, jobName)

            return HttpResponseRedirect('/index')
        else:
            HttpResponse('<h>login lose \'not form.is_valid()\'</h>')
    else:
        return HttpResponseRedirect('/index')


def build(req):
    jobName = req.session['jobName']
    jenkins = JenkinsCustomServer()
    jenkins.jenkins_build_project(jobName)
    return HttpResponseRedirect('/index')


def job(req):
    if req.method == 'GET':
        jobName = req.GET.get('jobName')
        if jobName:
            req.session['jobName'] = jobName

    return HttpResponseRedirect('/index')


def commit(req):
    if req.method == 'POST':
        commitTxt = req.POST.get('commitTxt')
        userId = req.session['userID']
        jobName = req.session['jobName']
        userDepartment = req.session['userDepartment']
        cm = MyCommit(userId, userDepartment, jobName)
        cm.add_commit(commitTxt)

        return HttpResponseRedirect('/index')


def dele_commit(req):
    if req.method == 'GET':
        deleK = req.GET.get('k')
        userId = req.session['userID']
        jobName = req.session['jobName']
        userDepartment = req.session['userDepartment']
        cm = MyCommit(userId, userDepartment, jobName)
        cm.dele_commit(deleK)

        return HttpResponseRedirect('/index')


def job_commit_json(req):
    if req.method == 'GET':
        jobName = req.GET.get('jobName')
        try:
            deleJob = int(req.GET.get('deleJob'))
        except:
            deleJob = False

        cm = MyCommit(None, None, jobName)
        commit = cm.all_commit()
        commits = {}
        for uid, com in commit.items():
            jobCommit = com.get(jobName)
            if jobCommit:
                uname = User.objects.get(id=int(uid)).name
                commits[uname] = jobCommit

        if bool(deleJob):
            cm.dele_job_commit()
        return HttpResponse(json.dumps(commits), content_type="application/json")
