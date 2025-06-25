import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .forms import CourseForm
from .models import Lesson
from django.contrib import messages

from .models import Course, Lesson, Quiz, UserProgress
from .serializers import (
    CourseSerializer,
    LessonSerializer,
    QuizSerializer,
    UserProgressSerializer,
)

# ===========================================
# 📦 API ViewSets (JWT / Auth Protected APIs)
# ===========================================

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]

class UserProgressViewSet(viewsets.ModelViewSet):
    queryset = UserProgress.objects.all()
    serializer_class = UserProgressSerializer
    permission_classes = [IsAuthenticated]

# =============================
# 🌐 Page Views (HTML Templates)
# =============================

@login_required(login_url='login')
def home(request):
    return render(request, 'courses/home.html')

@login_required(login_url='login')
def lesson_list(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    lessons = Lesson.objects.filter(course=course)
    return render(request, 'courses/lesson_list.html', {
        'course': course,
        'lessons': lessons
    })

@login_required(login_url='login')
def course_list(request):
    courses = Course.objects.all()

    if not courses.exists():
        instructor = request.user if request.user.is_authenticated else None
        if instructor:
            Course.objects.create(
                title='Intro to Python',
                description='Beginner friendly Python course.',
                instructor=instructor
            )
            Course.objects.create(
                title='Web Development',
                description='Learn HTML, CSS, JS, and Django.',
                instructor=instructor
            )
            courses = Course.objects.all()

    return render(request, 'courses/course_list.html', {'courses': courses})
@login_required(login_url='login')
def quiz_page(request, lesson_id):
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    quizzes = Quiz.objects.filter(lesson=lesson)

    for quiz in quizzes:
        # Split choices by comma and strip whitespace for neat display
        quiz.choice_list = [choice.strip() for choice in quiz.choices.split(',')] if quiz.choices else []

    return render(request, 'courses/quiz_list.html', {
        'lesson': lesson,
        'quizzes': quizzes
    })

@login_required(login_url='login')
def quizzes_redirect(request):
    first_lesson = Lesson.objects.first()
    if first_lesson:
        return redirect('quiz_page', lesson_id=first_lesson.id)

    messages.warning(request, "No lessons available to show quizzes.")
    return render(request, 'courses/quiz_list.html')  # ✅ This works





# =============================
# 🔐 Auth Views (Login / Logout / Register)
# =============================

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'courses/login.html', {'error': 'Invalid username or password.'})

    return render(request, 'courses/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not username or not email or not password:
            return render(request, 'courses/register.html', {'error': 'All fields are required.'})

        if User.objects.filter(username=username).exists():
            return render(request, 'courses/register.html', {'error': 'Username already exists.'})

        User.objects.create_user(username=username, email=email, password=password)
        return redirect('login')

    return render(request, 'courses/register.html')

# =============================
# 📲 API (for mobile / external)
# =============================

@api_view(['POST'])
def register_user(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if not username or not email or not password:
        return Response({'error': 'All fields are required.'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

    User.objects.create_user(username=username, email=email, password=password)
    return Response({'message': 'User registered successfully.'}, status=status.HTTP_201_CREATED)

@login_required(login_url='login')
def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.save()
            return redirect('course_list')
    else:
        form = CourseForm()
    return render(request, 'courses/add_course.html', {'form': form})

# =============================
# 🛠️ Lessons Redirect (No course_id fallback)
# =============================

@login_required(login_url='login')
def lessons_redirect(request):
    first_course = Course.objects.first()
    if first_course:
        return redirect('lesson_list', course_id=first_course.id)
    return redirect('course_list')


