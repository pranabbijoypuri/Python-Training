from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

from .analytics import get_ticket_analytics
from .forms import TicketForm
from .models import Ticket
from .services import start_ticket_analysis


def ticket_create(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.analysis_status = "Pending"
            ticket.save()

            start_ticket_analysis(ticket.id)

            messages.success(request, "Ticket created successfully. Background analysis started.")
            return redirect("ticket_detail", ticket_id=ticket.id)
    else:
        form = TicketForm()

    return render(request, "tickets/ticket_form.html", {"form": form})


def ticket_list(request):
    tickets = Ticket.objects.all().order_by("-created_at")
    return render(request, "tickets/ticket_list.html", {"tickets": tickets})


def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    return render(request, "tickets/ticket_detail.html", {"ticket": ticket})


def analytics_view(request):
    analytics_data = get_ticket_analytics()
    return render(request, "tickets/analytics.html", analytics_data)