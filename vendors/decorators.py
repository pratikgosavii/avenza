from django.shortcuts import redirect
from functools import wraps

def admin_login_required(view_func_or_class):
    """
    A decorator to ensure that the user is an admin.
    """
    if hasattr(view_func_or_class, 'dispatch'):
        # Class-based view
        original_dispatch = view_func_or_class.dispatch

        @wraps(original_dispatch)
        def _wrapped_dispatch(self, request, *args, **kwargs):
            if not request.user.is_authenticated or request.user.role != 'admin':
                return redirect('adminLogin')  # Redirect if not authenticated or not admin

            return original_dispatch(self, request, *args, **kwargs)

        view_func_or_class.dispatch = _wrapped_dispatch
        return view_func_or_class
    else:
        # Function-based view
        @wraps(view_func_or_class)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated or request.user.role != 'admin':
                return redirect('adminLogin')  # Redirect if not authenticated or not admin

            return view_func_or_class(request, *args, **kwargs)

        return _wrapped_view


def vendor_or_admin_login_required(view_func_or_class):
    """
    A decorator to ensure that the user is either a vendor or admin.
    """
    if hasattr(view_func_or_class, 'dispatch'):
        # Class-based view
        original_dispatch = view_func_or_class.dispatch

        @wraps(original_dispatch)
        def _wrapped_dispatch(self, request, *args, **kwargs):
            if not request.user.is_authenticated or request.user.role not in ['vendor', 'admin']:
                return redirect('vendorLogin')  # Redirect if not authenticated or not vendor/admin

            return original_dispatch(self, request, *args, **kwargs)

        view_func_or_class.dispatch = _wrapped_dispatch
        return view_func_or_class
    else:
        # Function-based view
        @wraps(view_func_or_class)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated or request.user.role not in ['vendor', 'admin']:
                return redirect('login')  # Redirect if not authenticated or not vendor/admin

            return view_func_or_class(request, *args, **kwargs)

        return _wrapped_view
