from django.db import models
from IdentityManager import choices as IndentityChoices

# Create your models here.


class Identities(models.Model):

    class Meta:
        db_table = "bite_speed_indentities"

    phoneNumber = models.CharField(max_length=10, null=True, db_index=True)
    email = models.EmailField(null=True, db_index=True)
    linkedId = models.ForeignKey(
        "self",
        null=True,
        on_delete=models.SET_NULL,
        blank=True,
    )
    linkPrecedence = models.CharField(
        choices=IndentityChoices.LinkPrecedence.choices, max_length=10
    )
    createdAt = models.DateTimeField(auto_now=True)
    updatedAt = models.DateTimeField(auto_now_add=True)
    deletedAt = models.DateTimeField(null=True)
