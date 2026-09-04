from django.contrib import admin
from .models import YouTubeUser
from django.core.cache import cache
from django.contrib import messages


@admin.action(description="Clear The cahce")
def clear_user_cache(modeladmin, request, queryset):
    cache.delete("user_data")
    messages.success(request, "Clear Cache Sucessfully")


@admin.register(YouTubeUser)
class AdminYouTubeUser(admin.ModelAdmin):
    list_display = ["name", "email", "subscribers"]
    actions = [clear_user_cache]
