from django.db import models

# Create your models here.


class KLinkPrecedence(models.TextChoices):

    PRIMARY = "primary", "primary"
    SECONDARY = "secondary", "secondary"


class Identities(models.Model):

    class Meta:
        db_table = "bite_speed_indentities"
    
    phoneNumber = models.CharField(max_length=10, null=True)
    email = models.EmailField(null=True)               
    linkedId = models.OneToOneField(
        "self",
        null=True,      
        on_delete=models.SET_NULL,
        blank=True,
        related_name='linked_by'
    )
    linkPrecedence = models. CharField(choices=KLinkPrecedence.choices, max_length=10)
    createdAt = models.DateTimeField(auto_now=True)
    updatedAt= models.DateTimeField(auto_now_add=True)              
    deletedAt=models.DateTimeField(null=True)