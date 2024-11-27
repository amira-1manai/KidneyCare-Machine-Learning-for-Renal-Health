from django.shortcuts import redirect

class RedirectUnauthenticatedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Check if the user is not authenticated and trying to access protected views
        if not request.user.is_authenticated and request.path in ['/doctor_dashboard/', '/patient_dashboard/']:
            return redirect('user_login')
        
        return response