from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import redirect, render

# Needed only by the commented class-based reference views further down:
# from django.contrib.auth.views import LoginView, LogoutView
# from django.urls import reverse_lazy

from .forms import AssetRequestForm, EmployeeProfileForm, LeaveRequestForm, RegistrationForm
from .models import AssetRequest, EmployeeProfile, LeaveRequest


def home(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return render(request, "hrms/home.html")


def register_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            EmployeeProfile.objects.create(
                user=user,
                employee_id=f"EMP-{user.id:04d}",
                department="General",
            )
            messages.success(request, "Registration successful. Please log in.")
            return redirect("login")
    else:
        form = RegistrationForm()
    return render(request, "hrms/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        messages.error(request, "Invalid username or password")
    return render(request, "hrms/login.html")


# --- REFERENCE: class-based equivalent of login_view -------------------------
# Django ships LoginView, which does the same authenticate() + login() work we
# do above. Swapping to it would give us three things we currently lack:
#   1. ?next= handling  - after logging in, the user lands on the page they
#      originally asked for instead of always the dashboard.
#   2. AuthenticationForm - rejects inactive users and renders field-level
#      errors, so login.html would use {{ form.username }} / {{ form.password }}
#      instead of the hand-written <input> tags.
#   3. redirect_authenticated_user - an already-logged-in user hitting /login/
#      is bounced straight to the dashboard.
#
# To switch: uncomment this class, drop `login_view`, and in urls.py use
#     path("login/", views.HRMSLoginView.as_view(), name="login"),
#
# class HRMSLoginView(LoginView):
#     template_name = "hrms/login.html"
#     redirect_authenticated_user = True
#
#     def get_success_url(self):
#         # Honour ?next= when present; fall back to the dashboard.
#         return self.get_redirect_url() or reverse_lazy("dashboard")
#
#     def form_invalid(self, form):
#         # Keep our messages-framework style of showing errors.
#         messages.error(self.request, "Invalid username or password")
#         return super().form_invalid(form)
# ---------------------------------------------------------------------------


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("login")


# --- REFERENCE: class-based equivalent of logout_view ------------------------
# LogoutView has been POST-only since Django 5.0. That matters: our view above
# logs a user out on a plain GET, so any other site could embed
# <img src="http://our-host/logout/"> and silently log our users out (a CSRF
# logout). LogoutView refuses GET and validates the CSRF token on POST.
#
# To switch: uncomment this class, drop `logout_view`, and in urls.py use
#     path("logout/", views.HRMSLogoutView.as_view(), name="logout"),
# The navbar link in templates/partials/_navbar.html must then become a form,
# because a plain <a href> can only issue a GET:
#     <form method="post" action="{% url 'logout' %}" class="logout-form">
#         {% csrf_token %}
#         <button type="submit">Logout</button>
#     </form>
#
# class HRMSLogoutView(LogoutView):
#     next_page = reverse_lazy("login")
#
#     def dispatch(self, request, *args, **kwargs):
#         # Only announce the logout to someone who was actually logged in.
#         if request.user.is_authenticated:
#             messages.info(request, "You have been logged out.")
#         return super().dispatch(request, *args, **kwargs)
# ---------------------------------------------------------------------------


@login_required
def change_password_view(request):
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Password changed successfully.")
            return redirect("profile")
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, "hrms/change_password.html", {"form": form})


@login_required
def profile_view(request):
    profile, _ = EmployeeProfile.objects.get_or_create(
        user=request.user,
        defaults={"employee_id": f"EMP-{request.user.id:04d}", "department": "General"},
    )
    if request.method == "POST":
        form = EmployeeProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("profile")
    else:
        form = EmployeeProfileForm(instance=profile)

    return render(request, "hrms/profile.html", {"form": form, "profile": profile})


@login_required
def dashboard(request):
    total_employees = User.objects.count()
    total_leaves = LeaveRequest.objects.count()
    approved_leaves = LeaveRequest.objects.filter(status="approved").count()
    pending_assets = AssetRequest.objects.filter(status="pending").count()

    return render(
        request,
        "hrms/dashboard.html",
        {
            "total_employees": total_employees,
            "total_leaves": total_leaves,
            "approved_leaves": approved_leaves,
            "pending_assets": pending_assets,
        },
    )


@login_required
def employee_list_view(request):
    employees = User.objects.select_related("profile").all()
    q = request.GET.get("q")
    if q:
        employees = employees.filter(
            Q(username__icontains=q)
            | Q(first_name__icontains=q)
            | Q(last_name__icontains=q)
            | Q(profile__department__icontains=q)
        )
    return render(request, "hrms/employees.html", {"employees": employees, "q": q})


@login_required
def create_employee_view(request):
    if not request.user.is_staff:
        messages.error(request, "Only admin can create employees.")
        return redirect("dashboard")

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            EmployeeProfile.objects.create(
                user=user,
                employee_id=f"EMP-{user.id:04d}",
                department=request.POST.get("department", "General"),
            )
            messages.success(request, "Employee created successfully.")
            return redirect("employees")
    else:
        form = RegistrationForm()
    return render(request, "hrms/create_employee.html", {"form": form})


@login_required
def toggle_employee_status_view(request, pk):
    if not request.user.is_staff:
        messages.error(request, "Only admin can manage employee status.")
        return redirect("dashboard")

    user = User.objects.get(pk=pk)
    profile = user.profile
    profile.is_active = not profile.is_active
    profile.save()
    messages.success(request, "Employee status updated.")
    return redirect("employees")


@login_required
def leave_request_view(request):
    leaves = LeaveRequest.objects.select_related("employee").all().order_by("-created_at")
    status = request.GET.get("status")
    date = request.GET.get("date")

    if status:
        leaves = leaves.filter(status=status)
    if date:
        leaves = leaves.filter(start_date__lte=date, end_date__gte=date)

    form = LeaveRequestForm()
    if request.method == "POST":
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.employee = request.user
            leave.save()
            messages.success(request, "Leave request submitted.")
            return redirect("leave_requests")

    return render(
        request,
        "hrms/leaves.html",
        {"leaves": leaves, "form": form, "status": status, "date": date},
    )


@login_required
def leave_action_view(request, pk, action):
    if not request.user.is_staff:
        messages.error(request, "Only admin can approve or reject leave requests.")
        return redirect("leave_requests")

    leave = LeaveRequest.objects.get(pk=pk)
    if action == "approve":
        leave.status = "approved"
    elif action == "reject":
        leave.status = "rejected"
    elif action == "cancel":
        leave.status = "cancelled"
    leave.save()
    messages.success(request, f"Leave request marked as {leave.status}.")
    return redirect("leave_requests")


@login_required
def asset_request_view(request):
    assets = AssetRequest.objects.select_related("employee").all().order_by("-created_at")
    form = AssetRequestForm()

    if request.method == "POST":
        form = AssetRequestForm(request.POST)
        if form.is_valid():
            asset = form.save(commit=False)
            asset.employee = request.user
            asset.save()
            messages.success(request, "Asset request submitted.")
            return redirect("asset_requests")

    return render(request, "hrms/assets.html", {"assets": assets, "form": form})


@login_required
def asset_action_view(request, pk, action):
    if not request.user.is_staff:
        messages.error(request, "Only admin can manage asset requests.")
        return redirect("asset_requests")

    asset = AssetRequest.objects.get(pk=pk)
    if action == "approve":
        asset.status = "approved"
    elif action == "reject":
        asset.status = "rejected"
    elif action == "assign":
        asset.status = "assigned"
    asset.save()
    messages.success(request, f"Asset request marked as {asset.status}.")
    return redirect("asset_requests")
