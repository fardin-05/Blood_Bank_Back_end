from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['id','email','first_name','last_name','address','phone_number','is_active']
    list_filter = ['is_staff','is_active']
    fieldsets=(
        (None,{'fields':('email','password')}),
        ('Personal Info',{'fields':('first_name','last_name','address','phone_number')}),
        ('Permissions',{'fields':('is_staff','is_active','is_superuser','groups','user_permissions')}),
        ('Important Dates',{'fields':('last_login','date_joined')}),
    )
    add_fieldsets=(
        (None,{
            'classes':('wide',),
            'fields':('email','first_name','last_name','address','phone_number','password1','password2','is_staff','is_active')
        }),
    )
    search_fields=('email',)
    ordering=('email',)

admin.site.register(CustomUser,CustomUserAdmin)