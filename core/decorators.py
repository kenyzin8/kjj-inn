from django.http import Http404, HttpResponse, JsonResponse
from functools import wraps
from django.core.cache import cache
from django.shortcuts import render
import functools

def staff_required(function):
    @wraps(function)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or not (request.user.is_superuser or request.user.is_staff):
            raise Http404("Page not found")
        return function(request, *args, **kwargs)
    return _wrapped_view

def rate_limit(requests, period):
    def decorator(view_func):
        @functools.wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            ip = request.META.get('REMOTE_ADDR')
            key = f"{ip}:{view_func.__name__}"

            expire = 60 if period == 'min' else 3600

            current_count = cache.get(key, 0)
            if current_count >= requests:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'error': 'Rate limit exceeded'}, status=429)
                else:
                    return render(request, 'errors/429.html', status=429)

            cache.set(key, current_count + 1, expire)
            return view_func(request, *args, **kwargs)

        return _wrapped_view
    return decorator