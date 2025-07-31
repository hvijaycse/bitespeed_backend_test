from django.db import models


class KLinkPrecedence(models.TextChoices):

    PRIMARY = "primary", "primary"
    SECONDARY = "secondary", "secondary"
