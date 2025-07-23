from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
  class Meta(UserCreationForm.Meta):
    model = CustomUser
    fields = ('username','email','userFirstName', 'userLastName', 'userFullName', 'userWorkArea', 'userRole', 'userIdentityCard', 'userBirthday', 'userLocalPhone', 'userMobilePhone', 'userCountry', 'userTownship', 'userVillage', 'userNeighbor', 'userStreet', 'userSection', 'userLane', 'userAlley', 'userNumber', 'userFloor', 'userPublicOrPrivate', ) # new


class CustomUserChangeForm(UserChangeForm):
  class Meta:
    model = CustomUser
    fields = ('username','email','userFirstName', 'userLastName', 'userFullName', 'userWorkArea', 'userRole', 'userIdentityCard', 'userBirthday', 'userLocalPhone', 'userMobilePhone', 'userCountry', 'userTownship', 'userVillage', 'userNeighbor', 'userStreet', 'userSection', 'userLane', 'userAlley', 'userNumber', 'userFloor', 'userPublicOrPrivate', ) # new