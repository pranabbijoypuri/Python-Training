import pandas as pd
from .models import Ticket


def get_ticket_analytics():
    queryset = Ticket.objects.all().values(
        "id",
        "title",
        "category",
        "priority",
        "status",
        "analysis_status",
        "created_at",
    )

    data = list(queryset)

    if not data:
        return {
            "total_tickets": 0,
            "category_counts": {},
            "priority_counts": {},
            "status_counts": {},
            "analysis_status_counts": {},
            "recent_tickets": [],
        }

    df = pd.DataFrame(data)

    category_counts = df["category"].value_counts().to_dict()
    priority_counts = df["priority"].value_counts().to_dict()
    status_counts = df["status"].value_counts().to_dict()
    analysis_status_counts = df["analysis_status"].value_counts().to_dict()

    recent_tickets = (
        Ticket.objects.all()
        .order_by("-created_at")[:5]
    )

    return {
        "total_tickets": len(df),
        "category_counts": category_counts,
        "priority_counts": priority_counts,
        "status_counts": status_counts,
        "analysis_status_counts": analysis_status_counts,
        "recent_tickets": recent_tickets,
    }