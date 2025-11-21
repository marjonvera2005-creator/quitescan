from django.shortcuts import redirect


class AdminGateMiddleware:
    """Require passing the admin gate before accessing /admin/login/"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        # Only check admin login paths, not other admin paths
        # Skip the gate if user is already authenticated
        if path == '/admin/login/' and not request.session.get('admin_gate_ok') and not request.user.is_authenticated:
            return redirect('admin_gate')
        return self.get_response(request)


