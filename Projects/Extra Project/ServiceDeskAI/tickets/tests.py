from django.test import TestCase
from .models import Ticket


class TicketModelTest(TestCase):
    def test_ticket_creation(self):
        ticket = Ticket.objects.create(
            title="Internet not working",
            description="Office internet is down since morning.",
        )
        self.assertEqual(ticket.title, "Internet not working")
        self.assertEqual(ticket.analysis_status, "Pending")