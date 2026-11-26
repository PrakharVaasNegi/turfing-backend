from django.contrib import admin

from .models import Booking, Slot


@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = ("id", "start_time", "duration_minutes", "price", "is_active")
    list_filter = ("is_active",)
    ordering = ("start_time",)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "whatsapp_number",
        "slot",
        "status",
        "notification_status",
        "created_at",
    )
    list_filter = ("status", "notification_status")
    search_fields = ("name", "whatsapp_number")
