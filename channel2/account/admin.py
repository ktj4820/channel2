from django.contrib import admin
from django.contrib.auth.models import Group
from channel2.account.models import User


class UserAdmin(admin.ModelAdmin):

    list_display = ('email', 'is_active', 'is_staff', 'last_login', 'date_joined',)
    list_filter = ('is_staff',)
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
