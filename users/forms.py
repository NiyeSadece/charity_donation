from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm

from .models import CustomUser as User


class RegistrationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ('first_name', 'last_name', 'email')


class ChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email',)


class LoginForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ('email',)
