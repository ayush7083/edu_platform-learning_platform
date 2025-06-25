from django.contrib import admin
from .models import Course, Lesson, Quiz, UserProgress

admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Quiz)
admin.site.register(UserProgress)
