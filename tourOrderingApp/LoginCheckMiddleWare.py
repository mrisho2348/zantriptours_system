from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseRedirect
from django.urls import reverse

class LoginCheckMiddleWare(MiddlewareMixin):

    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__
        user = request.user

        # Allow access to login/logout pages and authentication-related views
        if request.path in [reverse("login"), reverse("DoLogin"), reverse("logout_user")] or modulename.startswith("django.contrib.auth.views"):
            return None

        if user.is_authenticated:
            if user.user_type == "1":
                # Admin user type
                if modulename in ["tourOrderingApp.adminView", "tourOrderingApp.views", "django.views.static"]:
                    pass
                else:
                    return HttpResponseRedirect(reverse("admin_dashboard"))

            elif user.user_type == "2":
                # Tourist user type
                if modulename in ["tourOrderingApp.TouristViews", "tourOrderingApp.views", "django.views.static"]:
                    pass
                else:
                    return HttpResponseRedirect(reverse("tourist_dashboard"))
            else:
                return HttpResponseRedirect(reverse("home"))
        else:
            # If the user is not authenticated, allow access to tourOrderingApp.views and specific paths
            if modulename == "django.contrib.auth.views" or modulename == "tourOrderingApp.views" or  modulename == "django.views.static" or request.path in [reverse("login"), reverse("DoLogin"), reverse("logout_user")]:
                pass
            else:
                return HttpResponseRedirect(reverse("home"))

        return None
