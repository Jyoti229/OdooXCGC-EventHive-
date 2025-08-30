from django.shortcuts import redirect
from django.urls import reverse

class OrganizerRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/organizer-dashboard/'):
            if not request.user.is_authenticated or getattr(request.user, 'role', None) != 'organizer':
                return redirect(reverse('login'))
        return self.get_response(request)
