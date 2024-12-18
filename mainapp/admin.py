from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms.home import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser,Account,Post,Following

# Register your models here.
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ("email", "is_trusted",
                    "is_active"
                    )

    list_filter = ("email", "is_trusted",
                   "is_active"
                   )
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_trusted",
                    "is_staff",
                    "is_active",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_trusted",
                    "is_active",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Account)
admin.site.register(Post)
admin.site.register(Following)