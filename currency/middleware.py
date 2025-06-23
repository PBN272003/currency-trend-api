from .models import APILog

class APILoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.path.startswith("/api/"):
            user = request.user if request.user.is_authenticated else None
            ip_address = request.META.get('REMOTE_ADDR')
            APILog.objects.create(
                user=user,
                endpoint=request.path,
                method=request.method,
                status_code=response.status_code,
                success=response.status_code < 400,
                ip_address=ip_address
            )
        return response