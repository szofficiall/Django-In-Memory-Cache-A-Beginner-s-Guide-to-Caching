from django.core.cache import cache, caches
from .models import YouTubeUser
from django.shortcuts import render
from django.shortcuts import render
from django.contrib import messages


def users_list(request):
    users = cache.get("user_data")

    if not users:
        print("Cache Miss: Fetching data fromk database")
        messages.info(request, "Cache Miss: Fetching data fromk database")
        users = YouTubeUser.objects.all()
        cache.set("user_data", users, timeout=20)  # 20 seconds
    else:
        print("Cache Hit: Fetching Data From Cache")
        messages.success(request, "Cache Hit: Fetching Data From Cache")

    return render(request, "cache/user_list.html", {"users": users})
