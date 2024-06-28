from django.contrib import admin
from app.models import Student, Staff, LostItem, FoundItem

admin.site.register(Student)
admin.site.register(Staff)
admin.site.register(LostItem)
admin.site.register(FoundItem)
