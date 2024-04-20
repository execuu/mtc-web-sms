# main/signals.py

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from .models import Student, Coaches

@receiver(post_save, sender=Student)
def create_student_user(sender, instance, created, **kwargs):
    if created:
        user = User.objects.create_user(username=instance.email, password=instance.studentNumber)
        student_group = Group.objects.get(name='Students')
        user.groups.add(student_group)
        user.idNumber = instance.studentNumber
        user.save()

@receiver(post_save, sender=Coaches)
def create_coach_user(sender, instance, created, **kwargs):
    if created:
        user = User.objects.create_user(username=instance.email, password=instance.coachNumber)
        coach_group = Group.objects.get(name='Coaches')
        user.groups.add(coach_group)
        user.idNumber = instance.coachNumber
        user.save()

@receiver(post_delete, sender=Student)
def delete_student_user(sender, instance, **kwargs):
    try:
        user = User.objects.get(username=instance.email)
        user.delete()
    except User.DoesNotExist:
        pass

@receiver(post_delete, sender=Coaches)
def delete_coach_user(sender, instance, **kwargs):
    try:
        user = User.objects.get(username=instance.email)
        user.delete()
    except User.DoesNotExist:
        pass    