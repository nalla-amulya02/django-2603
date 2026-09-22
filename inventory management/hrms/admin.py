from django.contrib import admin

from .models import AssetRequest, EmployeeProfile, LeaveRequest


@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "employee_id", "department", "is_active"]
    search_fields = ["employee_id", "department", "user__username", "user__first_name"]
    list_filter = ["department", "is_active"]
    ordering = ["user__username"]


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ["employee", "leave_type", "start_date", "end_date", "status"]
    search_fields = ["employee__username", "leave_type", "status"]
    list_filter = ["status", "leave_type", "start_date"]
    ordering = ["-created_at"]


@admin.register(AssetRequest)
class AssetRequestAdmin(admin.ModelAdmin):
    list_display = ["employee", "asset_type", "quantity", "status"]
    search_fields = ["employee__username", "asset_type", "status"]
    list_filter = ["status", "asset_type"]
    ordering = ["-created_at"]
