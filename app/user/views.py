import bugsnag
import rollbar
import sentry_sdk
from django.db.models import Q
from django.http import HttpResponse
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


def trigger_error(request):
    try:
        division_by_zero = 1 / 0 # noqa
        return HttpResponse('Success', status=200)
    except ZeroDivisionError:
        rollbar.report_exc_info()
        bugsnag.notify(ZeroDivisionError("Zero Dvision Error"))
        sentry_sdk.capture_exception(ZeroDivisionError("Zero Dvision Error"))
        return HttpResponse('Bad Request', status=400)


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
        return User.objects.filter(Q(is_active=True) & ~Q(id=self.request.user.id))  # noqa: 501

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
