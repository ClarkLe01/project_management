from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.contrib.auth import authenticate, login
from ..forms import LoginForm


class LoginView(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/')
        context = {"loginform": LoginForm()}
        return render(request, 'authentication/signin/signin.html', context)

    # khi nào add data in querystring và khi nào add data in body
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        check_user = authenticate(username=email, password=password)
        if check_user is None:
            return HttpResponse('Unauthorized', status=401)
        login(request, check_user)
        return HttpResponse('Success', status=200)
