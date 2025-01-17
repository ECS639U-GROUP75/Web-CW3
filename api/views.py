from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.db.models import Count, F, Q
from .forms import UserForm
from .models import User, Hobby, Friends
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token
import json
from django.db import models
from datetime import date
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

def main_spa(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        return redirect('login')
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

@login_required(login_url='/login/')
def get_users(request: HttpRequest) -> JsonResponse:
    try:
        logged_in_user = request.user
        min_age = request.GET.get('min_age', '0')
        max_age = request.GET.get('max_age', '100')
        page_number = request.GET.get('page', 1)

        min_age = int(min_age) if min_age.isdigit() else 0
        max_age = int(max_age) if max_age.isdigit() else 100

        current_year = date.today().year

        users = User.objects.exclude(id=logged_in_user.id).annotate(
            common_hobby_count=Count('Hobbies', filter=models.Q(Hobbies__in=logged_in_user.Hobbies.all())),
            age=(current_year - F('date_of_birth__year'))
        ).filter(age__gte=min_age, age__lte=max_age).order_by('-common_hobby_count')

        users_values = users.values('username', 'first_name', 'last_name', 'common_hobby_count', 'age')

        paginator = Paginator(users_values, 5)
        page_users = paginator.get_page(page_number)

        users_data = list(page_users)

        response = JsonResponse({
            'users': users_data,
            'has_next': page_users.has_next(),
            'has_previous': page_users.has_previous(),
            'current_page': page_users.number,
            'total_pages': paginator.num_pages,
        })
        response['Content-Type'] = 'application/json'
        return response
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=400, content_type='application/json')

@login_required(login_url='/login/')
def get_all_hobbies(request: HttpRequest) -> JsonResponse:
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    try:
        hobbies = Hobby.objects.all().values_list('name', flat=True)
        return JsonResponse({
            'hobbies': list(hobbies)
        })
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=500)
    
@login_required(login_url='/login/')
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

@login_required(login_url='/login/')
def update_profile(request: HttpRequest) -> JsonResponse:
    if request.method == 'POST' and request.user.is_authenticated:
        user = request.user
        body = json.loads(request.body)
        
        user.username = body.get("username")
        user.email = body.get("email")
        user.bio = body.get("bio")
        user.date_of_birth = body.get("dob")
        
        new_password = body.get("password")
        if new_password:
            user.set_password(new_password)  
        
        user.save()
        
        profile_data = {
            'username': user.username,
            'email': user.email,
            'bio': user.bio,
            'date_of_birth': user.date_of_birth,
        }
        return JsonResponse({'success': True, 'profile': profile_data}) 
    return JsonResponse({'error': 'Unauthorized'}, status=401)

def logout_view(request: HttpRequest) -> JsonResponse:
    if request.method == 'POST':
        logout(request)
        return JsonResponse({
            'success': True,
            'message': 'Logged out',
            'redirect_url': '/login/'
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required(login_url='/login/')
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

@login_required(login_url='/login/')
def get_friend_requests(request: HttpRequest) -> JsonResponse:
    if request.method == 'GET' and request.user.is_authenticated:
        requests = Friends.objects.filter(friend=request.user, status='pending').select_related('user')
        requests_data = [{'id': req.id, 'user__username': req.user.username} for req in requests]
        return JsonResponse({'requests': requests_data})
    return JsonResponse({'error': 'Unauthorized'}, status=401)

@login_required(login_url='/login/')
def get_current_friends(request: HttpRequest) -> JsonResponse:
    if request.method == 'GET' and request.user.is_authenticated:
        friends = Friends.objects.filter(
            (Q(user=request.user) | Q(friend=request.user)),
            status='accepted'
        ).select_related('user', 'friend')

        friends_data = []
        for friendship in friends:
            if friendship.user == request.user:
                friend_username = friendship.friend.username
            else:
                friend_username = friendship.user.username
            
            friends_data.append({'friend__username': friend_username})

        return JsonResponse({'friends': friends_data})
    
    return JsonResponse({'error': 'Unauthorized'}, status=401)

@login_required(login_url='/login/')
def accept_friend_request(request: HttpRequest, request_id: int) -> JsonResponse:
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            friendship = Friends.objects.get(id=request_id, friend=request.user, status='pending')
            friendship.status = 'accepted'
            friendship.save()
            return JsonResponse({'success': True, 'message': 'Friend request accepted'})
        except Friends.DoesNotExist:
            return JsonResponse({'error': 'Friend request not found or already accepted'}, status=404)
    return JsonResponse({'error': 'Unauthorized'}, status=401)

@login_required(login_url='/login/')
def reject_friend_request(request: HttpRequest, request_id: int) -> JsonResponse:
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            friendship = Friends.objects.get(id=request_id, friend=request.user, status='pending')
            friendship.status = 'rejected'
            friendship.save()
            return JsonResponse({'success': True, 'message': 'Friend request rejected'})
        except Friends.DoesNotExist:
            return JsonResponse({'error': 'Friend request not found or already processed'}, status=404)
    return JsonResponse({'error': 'Unauthorized'}, status=401)

@login_required(login_url='/login/')
def send_friend_request(request, username):
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            friend_user = User.objects.get(username=username)

            existing_friendship = Friends.objects.filter(
                user=request.user,
                friend=friend_user,
                status='accepted'
            ).exists()

            if existing_friendship:
                return JsonResponse({'message': 'Friendship already exists'})

            pending_request = Friends.objects.filter(
                user=request.user,
                friend=friend_user,
                status='pending'
            ).exists()

            if pending_request:
                return JsonResponse({'message': 'Friend request already sent'})

            rejected_request = Friends.objects.filter(
                user=request.user,
                friend=friend_user,
                status='rejected'
            ).exists()

            if rejected_request:
                return JsonResponse({'message': 'Friend request was rejected previously'})

            Friends.objects.create(user=request.user, friend=friend_user, status='pending')
            return JsonResponse({ 'message': 'Friend request sent'})
        except User.DoesNotExist:
            return JsonResponse({'message': 'User not found'}, status=404)
    return JsonResponse({'message': 'Unauthorized'}, status=401)

@login_required(login_url='/login/')
def remove_hobby(request: HttpRequest) -> JsonResponse:
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    if request.method == 'POST':
        data = json.loads(request.body)
        hobby_name = data.get('name')

        try:
            hobby = Hobby.objects.get(name=hobby_name)
            request.user.Hobbies.remove(hobby)
            return JsonResponse({'success': True, 'message': 'Hobby removed successfully'})
        except Hobby.DoesNotExist:
            return JsonResponse({'error': 'Hobby not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid method'}, status=405)
