from django.contrib import admin
from blog.models import *

admin.site.register(User)
admin.site.register(Department)
admin.site.register(Project)
admin.site.register(Config)
