from django.db import models
from django.utils import timezone

class Student(models.Model):
    student_name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20, unique=True)
    course = models.CharField(max_length=100)
    current_year = models.PositiveIntegerField()
    current_semester = models.PositiveIntegerField()
    phone_number = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=128, blank=True, null=True)
    created = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_name} ({self.roll_number})"

class Staff(models.Model):
    staff_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=128, blank=True, null=True)
    created = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.staff_id})"

class LostItem(models.Model):
    item_name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=50)
    date_lost = models.DateField(default=timezone.now)
    location = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    image = models.ImageField(upload_to='lost_item_images')
    user_id = models.IntegerField(default=0)


    def __str__(self):
        return f"{self.item_name} lost at {self.location} on {self.date_lost}"

    class Meta:
        verbose_name = "Lost Item"
        verbose_name_plural = "Lost Items"
        ordering = ['-date_lost']

class FoundItem(models.Model):
    item_name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=50)
    date_found = models.DateField(default=timezone.now)
    location = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    image = models.ImageField(upload_to='found_item_images')
    user_id = models.IntegerField(default=0)


    def __str__(self):
        return f"{self.item_name} found at {self.location} on {self.date_found}"

    class Meta:
        verbose_name = "Found Item"
        verbose_name_plural = "Found Items"
        ordering = ['-date_found']
