from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserForm

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

def login_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return (HttpResponse(status=200))
            else:
                return (HttpResponse(status=401))
        except KeyError:
            return (HttpResponse(status=400))