from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.contrib.auth import authenticate, login
from user.forms import RegisterForm
from ..models import User


class RegisterView(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/')
        context = {"registerform": RegisterForm()}
        return render(request, 'authentication/signup/signup.html', context)

    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if User.objects.filter(email=email).exists():
            return HttpResponse('Conflict', status=409)
        User.objects.create_user(
            username=email, email=email,
            first_name=first_name, last_name=last_name,
            password=password
        )
        check_user = authenticate(username=email, password=password)
        login(request, check_user)
        return HttpResponse('Success', status=200)
