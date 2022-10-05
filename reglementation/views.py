from django.shortcuts import render, redirect


def reglementation(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')
    return render(request,'reglementation/reglementation.html')