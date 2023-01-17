from django.contrib.auth.models import AnonymousUser

from .models import Notification


def notifications(request):
    if not isinstance(request.user, AnonymousUser):
        return {'notifications': Notification.objects.filter(user=request.user).order_by('-created')}
    else:
        return {}
