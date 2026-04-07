from django.contrib import admin
from .models import Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "category",
        "priority",
        "status",
        "analysis_status",
        "created_at",
    )
    list_filter = ("category", "priority", "status", "analysis_status")
    search_fields = ("title", "description", "ai_summary", "ai_resolution")