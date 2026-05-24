from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ["username", "email", "is_staff", "phone_number"]
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ("phone_number", "avatar")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("email", "phone_number", "avatar")}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
