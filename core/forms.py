from django.forms import Form, URLField, ValidationError
from django.utils.translation import gettext_lazy as _
from urllib.parse import urlparse


def ValidateURL(value):
    url = urlparse(value)
    if url.hostname.lower() not in ["instagram.com", "www.instagram.com"]:
        raise ValidationError(_("This is not an Instagram URL."))


class ContentURLForm(Form):
    content_url = URLField(label=_("Content URL"),
                           required=True, validators=[ValidateURL])
