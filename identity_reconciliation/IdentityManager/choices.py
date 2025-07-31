from django.db import models


class LinkPrecedence(models.TextChoices):

    PRIMARY = "primary", "primary"
    SECONDARY = "secondary", "secondary"
