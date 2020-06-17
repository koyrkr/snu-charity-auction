from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model

class UserChange(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ['username']
