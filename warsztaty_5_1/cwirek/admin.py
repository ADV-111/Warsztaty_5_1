from django.contrib import admin
from .models import Tweet, User, Profile, Messages, Comments
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


admin.site.register(Profile)


def content_display_thirty_signs(obj):
    return str(obj.content)[0:30]


content_display_thirty_signs.short_description = 'content'


def deleted(model_admin, request, query_set):
    query_set.update(deleted=True)


deleted.short_description = "Ukryj element w widoku"


@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', content_display_thirty_signs, 'creation_date', 'deleted']
    list_filter = ['user', 'creation_date', 'deleted']
    actions = [deleted, ]


@admin.register(Messages)
class MessagesAdmin(admin.ModelAdmin):
    list_display = ['id', 'send_date', 'send_from', 'send_to', content_display_thirty_signs, 'read', 'deleted']
    list_filter = ['send_date', 'deleted']
    actions = [deleted, ]


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ['id', 'creation_date', 'tweet', 'user', content_display_thirty_signs, 'deleted']
    list_filter = ['creation_date', 'user', 'deleted']
    actions = [deleted, ]
