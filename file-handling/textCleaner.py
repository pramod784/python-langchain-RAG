from bs4 import  BeautifulSoup
import bleach

def cleanTextWithBS4(html_content):
    """
    Strips all HTML/PHP tags from a string, similar to PHP's strip_tags().
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.get_text()


def cleanTextWithBleach(html_content, allowed_tags=[]):
    """
    Strips HTML/PHP tags from a string, allowing only specified tags.
    """
    # HTML comments and PHP tags are always stripped by bleach by default.
    clean_text = bleach.clean(html_content, tags=allowed_tags, strip=True)
    return clean_text