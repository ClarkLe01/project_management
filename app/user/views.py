from django.db.models import Q
from django.shortcuts import redirect
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth import logout
from rest_framework import generics
from .models import User
from .serializers import UserSerializer


# Create your views here.
class HomeView(TemplateView):
    template_name = 'homepage/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class LogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
        return redirect('/signin')


class CollaboratorViewSetAPI(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        if self.request.user.id is None:
            return User.objects.filter(Q(is_active=True))
        return User.objects.filter(Q(is_active=True) & ~Q(id=self.request.user.id)) # noqa: 501

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
