from django.contrib import admin
from django.urls import path, include
from courses.views import (
    home,
    register_view,
    login_view,
    course_list,
    lesson_list,
    quiz_page,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),

    # 🔐 Authentication Pages
    path('', register_view, name='register'),
    path('login/', login_view, name='login'),

    # 🏠 Pages after login
    path('home/', home, name='home'),
    path('courses/', course_list, name='course_list'),
    path('lessons/', lesson_list, name='lesson_list'),
    path('quizzes/', quiz_page, name='quiz_page'),

    # 🔗 API Endpoints
    path('api/', include('courses.urls')),

    # 🔐 JWT Token Endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
