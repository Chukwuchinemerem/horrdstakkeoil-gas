from django import template
from decimal import Decimal, InvalidOperation

register = template.Library()

@register.filter
def split(value, delimiter):
    """Split a string by delimiter."""
    return value.split(delimiter)

@register.filter
def currency(value, decimals=2):
    """
    Format a number with thousands commas and fixed decimal places.
    e.g.  5000       -> 5,000.00
          5000000    -> 5,000,000.00
    Usage: {{ profile.balance|currency }}   {{ total_spent|currency:0 }}
    """
    try:
        val = Decimal(str(value))
        return f"{val:,.{int(decimals)}f}"
    except (InvalidOperation, TypeError, ValueError):
        return value
