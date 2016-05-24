"""Jenkins URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from blog import views as blog_views

urlpatterns = [
    # admin wwj123456
    url(r'^admin/', admin.site.urls),
    url(r'^login$', blog_views.login),
    url(r'^index$', blog_views.index),
    url(r'^config$', blog_views.config),
    url(r'^build$', blog_views.build),
    url(r'^index/job$', blog_views.job),
    url(r'^index/commit$', blog_views.commit),
    url(r'^index/deleCommit$', blog_views.dele_commit),
    url(r'^jobCommit.json$', blog_views.job_commit_json),
]
