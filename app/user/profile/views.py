from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from project.models import Project
from ..models import User
from django.contrib.auth.hashers import check_password


class UserProfile(View):
    template_name = 'userprofile/overview.html'

    def get(self, request, pk=None):
        context = {
            'user': User.objects.get(id=pk),
            'projects': Project.objects.filter(created_by=pk or request.user.id)  # noqa: 501
        }
        return render(request, self.template_name, context)


class OwnProfile(LoginRequiredMixin, UserProfile):
    def get(self, request):
        return super().get(request, pk=request.user.id)


class UpdateOwnProfile(LoginRequiredMixin, View):
    template_name = 'userprofile/settings.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        files = request.FILES.get("files")
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        try:
            user = User.objects.get(id=request.user.id)
            print(user)
        except User.DoesNotExist:
            user = None
        if user is None:
            return HttpResponse('Not Found', status=404)
        if fname and fname != '':
            user.first_name = fname
        if lname and lname != '':
            user.last_name = lname
        if files:
            user.avatar = files
        user.save()
        return HttpResponse('OK', status=200)


class OwnProfile(LoginRequiredMixin, UserProfile):
    def get(self, request):
        return super().get(request, pk=request.user.id)


class UpdatePass(LoginRequiredMixin, View):
    template_name = 'userprofile/settings.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        currentpass = request.POST.get("current_password")
        newpass = request.POST.get("new_password")
        try:
            user = User.objects.get(id=request.user.id)
        except User.DoesNotExist:
            user = None
        if user is None:
            return HttpResponse('Not Found', status=404)
        if check_password(currentpass, user.password):
            user.set_password(newpass)
            user.save()
            return HttpResponse('OK', status=200)
        else:
            return HttpResponse('Bad Request', status=400)
