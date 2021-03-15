from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from manager.models import Passwords, User
from manager.forms import UserAdminCreationForm, UserAdminChangeForm

# Register your models here.
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username', 'email', 'login_passphrase',  'date_joined')
    list_filter = ('username',)
    fieldsets = (
        (None, {'fields': ()}),
        ('Personal info', {'fields': ('username', 'email', 'login_passphrase', 'date_joined', )}),
        ('Permissions', {'fields': ('is_active', 'is_superuser',)}),
    )
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ()


    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'login_passphrase', 'date_joined', 'password1', 'password2', 'is_superuser', 'is_active')}
        ),
    )

@admin.register(Passwords)
class PasswordAdmin(admin.ModelAdmin):
    list_display = ('user', 'registered_email_address', 'registered_username', 'application_service_name', 'application_service_url')
    list_filter = ('application_service_name',)
    search_fields = ('registered_email_address',)
