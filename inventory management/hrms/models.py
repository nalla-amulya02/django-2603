from django.contrib.auth.models import User
from django.db import models


class EmployeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    employee_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True, null=True)
    photo = models.ImageField(upload_to="profile_photos/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.employee_id}"


class LeaveRequest(models.Model):
    LEAVE_TYPES = [
        ("sick", "Sick Leave"),
        ("casual", "Casual Leave"),
        ("earned", "Earned Leave"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("cancelled", "Cancelled"),
    ]

    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="leave_requests")
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPES)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.username} - {self.leave_type} - {self.status}"


class AssetRequest(models.Model):
    ASSET_CHOICES = [
        ("laptop", "Laptop"),
        ("monitor", "Monitor"),
        ("keyboard", "Keyboard"),
        ("headset", "Headset"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("assigned", "Assigned"),
    ]

    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="asset_requests")
    asset_type = models.CharField(max_length=20, choices=ASSET_CHOICES)
    quantity = models.PositiveIntegerField(default=1)
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.username} - {self.asset_type} - {self.status}"
