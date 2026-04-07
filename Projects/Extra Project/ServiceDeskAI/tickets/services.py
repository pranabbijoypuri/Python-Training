import logging
import threading
from django.db import close_old_connections

from .models import Ticket

logger = logging.getLogger("tickets")

analysis_lock = threading.Lock()


def classify_category(text: str) -> str:
    text = text.lower()

    if any(word in text for word in ["wifi", "network", "internet", "lan", "router"]):
        return "Network"
    if any(word in text for word in ["install", "application", "software", "crash", "bug"]):
        return "Software"
    if any(word in text for word in ["keyboard", "screen", "laptop", "mouse", "printer"]):
        return "Hardware"
    if any(word in text for word in ["login", "password", "access", "permission", "account"]):
        return "Access"
    if any(word in text for word in ["mail", "email", "outlook", "inbox"]):
        return "Email"
    if any(word in text for word in ["virus", "malware", "phishing", "security", "hack"]):
        return "Security"

    return "Other"


def suggest_priority(text: str) -> str:
    text = text.lower()

    if any(word in text for word in ["server down", "production down", "critical", "urgent", "security breach"]):
        return "Critical"
    if any(word in text for word in ["unable to work", "system down", "blocked", "not working"]):
        return "High"
    if any(word in text for word in ["slow", "intermittent", "issue", "error"]):
        return "Medium"

    return "Low"


def generate_summary(title: str, description: str) -> str:
    desc = description.strip()
    short_desc = desc[:180] + ("..." if len(desc) > 180 else "")
    return f"Ticket about '{title}'. Issue details: {short_desc}"


def suggest_resolution(category: str) -> str:
    resolution_map = {
        "Network": "Check router connectivity, verify network cables, restart the system, and confirm internet access.",
        "Software": "Reinstall or update the software, review error logs, and verify compatibility with the operating system.",
        "Hardware": "Inspect the physical device, reconnect hardware, run diagnostics, and replace faulty components if necessary.",
        "Access": "Reset password, verify user permissions, confirm account status, and retry login.",
        "Email": "Check mail server connectivity, verify mailbox settings, restart the mail client, and confirm credentials.",
        "Security": "Isolate the device, scan for threats, reset credentials, and escalate to the security team immediately.",
        "Other": "Review the issue manually, collect more details, and assign to the appropriate support team.",
    }
    return resolution_map.get(category, resolution_map["Other"])


def analyze_ticket(ticket_id: int) -> None:
    """
    Background thread function to analyze a ticket.
    """
    close_old_connections()

    try:
        with analysis_lock:
            ticket = Ticket.objects.get(id=ticket_id)
            text = f"{ticket.title} {ticket.description}"

            category = classify_category(text)
            priority = suggest_priority(text)
            summary = generate_summary(ticket.title, ticket.description)
            resolution = suggest_resolution(category)

            ticket.category = category
            ticket.priority = priority
            ticket.ai_summary = summary
            ticket.ai_resolution = resolution
            ticket.analysis_status = "Completed"
            ticket.save()

            logger.info("Ticket %s analyzed successfully.", ticket_id)

    except Ticket.DoesNotExist:
        logger.error("Ticket %s does not exist.", ticket_id)

    except Exception as exc:
        logger.exception("Error analyzing ticket %s: %s", ticket_id, exc)
        try:
            ticket = Ticket.objects.get(id=ticket_id)
            ticket.analysis_status = "Failed"
            ticket.save()
        except Exception:
            logger.exception("Could not update failed status for ticket %s", ticket_id)


def start_ticket_analysis(ticket_id: int) -> None:
    thread = threading.Thread(
        target=analyze_ticket,
        args=(ticket_id,),
        daemon=True,
    )
    thread.start()