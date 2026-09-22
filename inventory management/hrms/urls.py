from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    # Class-based alternative (see the REFERENCE blocks in views.py):
    # path("login/", views.HRMSLoginView.as_view(), name="login"),
    # path("logout/", views.HRMSLogoutView.as_view(), name="logout"),
    path("change-password/", views.change_password_view, name="change_password"),
    path("profile/", views.profile_view, name="profile"),

    path("employees/", views.employee_list_view, name="employees"),
    path("employees/create/", views.create_employee_view, name="create_employee"),
    path("employees/<int:pk>/toggle-status/", views.toggle_employee_status_view, name="toggle_employee_status"),

    path("leaves/", views.leave_request_view, name="leave_requests"),
    path("leaves/<int:pk>/action/<str:action>/", views.leave_action_view, name="leave_action"),

    path("assets/", views.asset_request_view, name="asset_requests"),
    path("assets/<int:pk>/action/<str:action>/", views.asset_action_view, name="asset_action"),
]
