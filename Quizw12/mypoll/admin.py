from django.contrib import admin
from .models import Choice,Poll

admin.site.register(Poll)
admin.site.register(Choice)
# Register your models here.
