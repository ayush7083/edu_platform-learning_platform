from django.urls import path, include
from rest_framework.routers import DefaultRouter
from courses.views import quiz_page, quizzes_redirect
from .views import (
    CourseViewSet,
    LessonViewSet,
    QuizViewSet,
    UserProgressViewSet,
    register_user,
    login_view,
    logout_view,
    register_view,
    home,
    lesson_list,
    course_list,
    quiz_page,          # ✅ Included once
    add_course,
    lessons_redirect,
    quizzes_redirect,   # ✅ Included once
)

# ✅ API Routers
router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'lessons', LessonViewSet, basename='lesson')
router.register(r'quizzes', QuizViewSet, basename='quiz')
router.register(r'progress', UserProgressViewSet, basename='progress')

# ✅ URL Patterns
urlpatterns = [
    # 🌐 API Endpoints
    path('api/', include(router.urls)),
    path('api/register/', register_user, name='register_user'),

    # 🔐 Auth Views
    path('', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),

    # 🏠 Course Views
    path('home/', home, name='home'),
    path('courses/', course_list, name='course_list'),
    path('courses/add/', add_course, name='add_course'),

    # 📘 Lesson Views
    path('lessons/<int:course_id>/', lesson_list, name='lesson_list'),
    path('lessons/', lessons_redirect, name='lessons_redirect'),

    # 🎯 Quiz Views
    path('quizzes/<int:lesson_id>/', quiz_page, name='quiz_page'),
    path('quizzes/', quizzes_redirect, name='quizzes_redirect')  # ✅ Fixed

]
