from django.db import models
from django.urls import reverse

from django.core.validators import (
    MaxValueValidator, validate_comma_separated_integer_list,
)
from django.conf import settings

class Course(models.Model):
    """docstring for AbstractCourse"""

    title       = models.CharField(max_length=254, unique=True)
    description = models.CharField(max_length=254, blank=True, null=True)
    #duration    = models.DurationField()

    def __str__(self):
        return self.title

    def get_url(self):
        return reverse("home", kwargs={"id": self.id})

    class Meta:
        verbose_name="Courses"
        verbose_name_plural="Courses"

class ProgressManager(models.Manager):

    def new_progress(self, user):
        new_progress = self.create(user=user,
                                   score="")
        new_progress.save()
        return new_progress

class Progress(models.Model):

    course_user = models.OneToOneField(settings.AUTH_USER_MODEL, 
                                       verbose_name=("User"),
                                       related_name="course_user",
                                       on_delete=models.CASCADE)

    score = models.CharField(max_length=1024,
                             verbose_name=("Score"),
                             validators=[validate_comma_separated_integer_list])

    objects = ProgressManager()

    class Meta:
        verbose_name = ("User Progress")
        verbose_name_plural = ("User progress records")
