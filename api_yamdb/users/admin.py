from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from . import constants as cnst
from .models import User


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': (cnst.USERNAME, 'password')}),
        (_('Personal info'), {
            'fields': (
                cnst.FIRST_NAME,
                cnst.LAST_NAME,
                cnst.EMAIL
            )
        }),
        (_('Permissions'), {
            'fields': (
                cnst.IS_ACTIVE,
                cnst.IS_STAFF,
                cnst.IS_SUPERUSER,
                'groups',
                'user_permissions'
            ),
        }),
        (_('Important dates'), {
            'fields': (
                'last_login',
                'date_joined'
            )
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                cnst.USERNAME,
                'password1',
                'password2'
            ),
        }),
    )

    list_display = (
        cnst.USERNAME,
        cnst.EMAIL,
        cnst.FIRST_NAME,
        cnst.LAST_NAME,
        cnst.IS_STAFF,
        cnst.ROLE,
        cnst.BIO
    )
    list_filter = (
        cnst.IS_STAFF,
        cnst.IS_SUPERUSER,
        cnst.IS_ACTIVE,
        'groups'
    )
    search_fields = (
        cnst.USERNAME,
        cnst.EMAIL,
        cnst.FIRST_NAME,
        cnst.LAST_NAME,
        cnst.ROLE
    )


admin.site.register(User, CustomUserAdmin)
