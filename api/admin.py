from django.contrib import admin
from .models import User, Hobby
from .forms import UserForm
from django.contrib.auth.admin import UserAdmin

# Register your models here
class Admin(UserAdmin):
    add_form = UserForm
    model = User

    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Custom Fields', {
                'fields': (
                    'Hobbies',
                )
            }
        )
    )

admin.site.register(User, Admin)
admin.site.register(Hobby)