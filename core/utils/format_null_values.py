

def format_value(*values):
    """Formats values to return None instead of concatenating 'None' strings."""
    cleaned_values = [str(v) for v in values if v is not None] 
    return " ".join(cleaned_values) if cleaned_values else None
