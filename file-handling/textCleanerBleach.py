import bleach
def strip_tags_allowed_python(html_content, allowed_tags=[]):
    """
    Strips HTML/PHP tags from a string, allowing only specified tags.
    """
    # HTML comments and PHP tags are always stripped by bleach by default.
    clean_text = bleach.clean(html_content, tags=allowed_tags, strip=True)
    return clean_text