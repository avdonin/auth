from django.contrib import admin

from .models import Course, Progress

class ProgressAdmin(admin.ModelAdmin):
    """
    to do:
            create a user section
    """
    search_fields = ('course_user', 'score', )

admin.site.register(Course)
admin.site.register(Progress, ProgressAdmin)