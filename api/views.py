from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.db.models import Count
from .forms import UserForm
from .models import User, Hobby
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token
import json
from django.db import models

def main_spa(request: HttpRequest) -> HttpResponse:
    return render(request, 'api/spa/index.html', {})

def register_view(request: HttpRequest) -> HttpResponse:
    if request.headers.get('Content-Type') == 'application/json':
        if request.method == 'POST':
            try:
                data = json.loads(request.body)
                user = User.objects.create_user(
                    username=data['username'],
                    password=data['password'],
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    email=data['email']
                )
                user.date_of_birth = data['date_of_birth']
                user.save()
                return JsonResponse({
                    'success': True,
                    'message': 'Registration successful'
                })
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'message': str(e)
                }, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@ensure_csrf_cookie
def login_view(request: HttpRequest) -> HttpResponse:
    if request.headers.get('Content-Type') == 'application/json':
        if request.method == 'POST':
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return JsonResponse({
                    'success': True,
                    'message': 'Login successful',
                    'user': {
                        'username': user.username,
                        'first_name': user.first_name,
                        'last_name': user.last_name
                    }
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Invalid credentials'
                }, status=400)
        
        return JsonResponse({'csrfToken': get_token(request)})
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main_spa')
        else:
            return render(request, 'api/spa/login.html', {'error': 'Invalid credentials'})
    return render(request, 'api/spa/login.html', {})

def get_users(request: HttpRequest) -> JsonResponse:
    try:
        logged_in_user = request.user
        
        users = User.objects.exclude(id=logged_in_user.id).annotate(
            common_hobby_count=Count('Hobbies', filter=models.Q(Hobbies__in=logged_in_user.Hobbies.all()))
        ).values('username', 'first_name', 'last_name', 'common_hobby_count')
        
        response = JsonResponse({
            'users': list(users)
        })
        response['Content-Type'] = 'application/json'
        return response
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=400, content_type='application/json')
    
def profile_view(request: HttpRequest) -> JsonResponse:
    if request.method == 'GET' and request.user.is_authenticated:
        user = request.user
        profile_data = {
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'date_of_birth': user.date_of_birth,
            'bio': user.bio,
            'hobbies': list(user.Hobbies.values_list('name', flat=True))
        }
        return JsonResponse(profile_data)
    
    return JsonResponse({'error': 'Unauthorized'}, status=401)

def logout_view(request: HttpRequest) -> JsonResponse:
    if request.method == 'POST':
        logout(request)
        return JsonResponse({
            'success': True,
            'message': 'Logged out '
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)

def add_hobby(request: HttpRequest) -> JsonResponse:
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
        
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid method'}, status=405)
        
    try:
        data = json.loads(request.body)
        hobby_name = data.get('name')
        
        if not hobby_name:
            return JsonResponse({'error': 'Hobby name is required'}, status=400)
            
        # Create hobby if it doesn't exist
        hobby, created = Hobby.objects.get_or_create(name=hobby_name)
        
        # Add hobby to user's hobbies
        request.user.Hobbies.add(hobby)
        
        return JsonResponse({
            'success': True,
            'message': 'Hobby added successfully',
            'hobby': {'name': hobby.name}
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})