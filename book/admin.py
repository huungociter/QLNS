from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Sach)
admin.site.register(Person)
admin.site.register(HoaDon)
admin.site.register(ChiTietHoaDon)
