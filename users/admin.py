from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from import_export.admin import ImportExportModelAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

# class CustomUserAdmin(UserAdmin):
# 	add_form = CustomUserCreationForm
# 	form = CustomUserChangeForm
# 	list_display = ['email', 'username']
# 	model = CustomUser

# admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(CustomUser)
class CustomUserAdmin(ImportExportModelAdmin):
  list_display=("userFirstName","userLastName","userFullName","userWorkArea","userRole","userIdentityCard","userBirthday","userLocalPhone","userMobilePhone","userCountry","userTownship","userVillage","userNeighbor","userStreet","userSection","userLane","userAlley","userNumber","userFloor","userPublicOrPrivate","userFloor","userPublicOrPrivate")
  pass