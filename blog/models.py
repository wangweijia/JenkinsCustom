from django.db import models


# 部门表
class Department(models.Model):
    departmentName = models.CharField(max_length=50)

    def __unicode__(self):
        return self.departmentName

    def __str__(self):
        return self.departmentName


# 项目表
class Project(models.Model):
    projectName = models.CharField(max_length=50)

    def __unicode__(self):
        return self.projectName

    def __str__(self):
        return self.projectName


# 用户表
class User(models.Model):
    userName = models.CharField(max_length=50)
    passWord = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    mail = models.CharField(max_length=50)
    department = models.ForeignKey(Department)
    projects = models.ManyToManyField(Project)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


# 配置字段表
class Config(models.Model):
    configName = models.CharField(max_length=50)

    def __unicode__(self):
        return self.configName

    def __str__(self):
        return self.configName
