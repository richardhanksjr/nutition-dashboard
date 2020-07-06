from django.contrib import admin
from api.models import MeditationEvent
from django.contrib.auth.admin import UserAdmin


from .models import UserProfile
from django.contrib.auth import get_user_model

User = get_user_model()

admin.site.unregister(User)


class UserProfileInline(admin.TabularInline):
    model = UserProfile


@admin.register(User)
class UserAdmin(UserAdmin):
    inlines = [UserProfileInline]


@admin.register(MeditationEvent)
class MeditationAdmin(admin.ModelAdmin):
    pass
