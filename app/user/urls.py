from django.urls import path
from user.login.views import LoginView
from user.register.views import RegisterView
from user.profile.views import UserProfile, UpdateOwnProfile, OwnProfile, UpdatePass
from user.resetpassword.views import forgotPassword, resetpassword_validate, resetPassword # noqa: 501
from .views import CollaboratorViewSetAPI, LogoutView, HomeView, trigger_error


app_name = 'user'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('sentry-debug', trigger_error),
    path('signin/', LoginView.as_view(), name='signin'),
    path('signup/', RegisterView.as_view(), name='signup'),
    path('signout/', LogoutView.as_view(), name='signout'),
    path('profile/', OwnProfile.as_view(), name='profile'),
    path('updatepass/', UpdatePass.as_view(), name='updatepass'),
    path('updateprofile/', UpdateOwnProfile.as_view(), name='updateprofile'),
    path('userprofile/<int:pk>', UserProfile.as_view(), name='userprofile'),
    path('collaborator/', CollaboratorViewSetAPI.as_view(), name='collaborator'), # noqa: 501
    path('forgotPassword/', forgotPassword, name='forgotPassword'),
    path('resetpassword_validate/<uidb64>/<token>/', resetpassword_validate, name='resetpassword_validate'), # noqa: 501
    path('resetPassword/', resetPassword, name='resetPassword'),

]
