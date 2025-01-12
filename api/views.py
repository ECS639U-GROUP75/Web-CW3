from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.db.models import Count
from .forms import UserForm
from .models import User

def main_spa(request: HttpRequest) -> HttpResponse:
    return render(request, 'api/spa/index.html', {})

def register_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            ))
            return redirect('main_spa')
    else:
        form = UserForm()
    return render(request, 'api/spa/register.html', {'form': form})

def login_view(request: HttpRequest) -> HttpResponse:
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
    print("get_users view called")  # Debug print
    try:
        users = User.objects.annotate(
            hobby_count=Count('Hobbies')
        ).values('username', 'first_name', 'last_name', 'hobby_count')
        
        print(f"Found users: {list(users)}")  # Debug print
        
        response = JsonResponse({
            'users': list(users)
        })
        response['Content-Type'] = 'application/json'
        return response
    except Exception as e:
        print(f"Error in get_users: {str(e)}")  # Debug print
        return JsonResponse({
            'error': str(e)
        }, status=400, content_type='application/json')