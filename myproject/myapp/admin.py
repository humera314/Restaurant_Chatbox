from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import MyUser

class MyUserAdmin(BaseUserAdmin):
    model = MyUser
    fieldsets = (
        (None, {'fields': ('phone_number', 'name', 'password')}),
        ('Permissions', {'fields': ('is_admin', 'is_staff')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'name', 'password1', 'password2', 'is_staff'),
        }),
    )
    list_display = ('phone_number', 'name', 'is_admin')
    search_fields = ('phone_number', 'name')
    ordering = ('phone_number',)

admin.site.register(MyUser, MyUserAdmin)
