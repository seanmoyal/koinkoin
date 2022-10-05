from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout, authenticate

User = get_user_model()

def signup(request):
    user = request.user
    if user.is_authenticated:
        return redirect('page-profil')

    if request.method == "POST":
        # traiter le formulaire
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = User.objects.create_user(username=username,password=password)
        login(request, user)
        return redirect('page-profil')
    return render(request, 'accounts/signup.html')

def login_user(request):
    user = request.user
    if user.is_authenticated:
        return redirect('page-profil')

    if request.method == 'POST':
        #connecter l'user
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username,password=password)
        if user:
            login(request,user)
            return redirect('page-profil')
    return render(request, 'accounts/login.html')


def logout_user(request):
    logout(request)
    return redirect('login')

