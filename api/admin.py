from django.contrib import admin
# from .models import NutritionEntry, Food
#
# admin.site.register(NutritionEntry)
# admin.site.register(Food)

# Register your models here.


from .models import UserProfile
from django.contrib.auth import get_user_model

User = get_user_model()

admin.site.unregister(User)

class UserProfileInline(admin.TabularInline):
    model = UserProfile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = [UserProfileInline]
