from IdentityManager import models as identity_models
from IdentityManager import choices as identity_choices
from django.db.models import Q


def handle_identity_contacts(
    email=None, phoneNumber=None
) -> identity_models.Identities:
    """
    This is main method to handle the
    contact identites by using email and phoneNumber

    This returns the primary Indentity of the given email
    and phoneNumber

    Need to handle below cases.

        if with the given email and phoneNumber
        no entry exists we need to create a new instance.

        in all the realted entries with the same
        email and phoneNumber the oldest one should be
        marked as primary all the other should be marked as
        secondary and there linked_id should be updated to
        primary id.


    """
    if email is None and phoneNumber is None:
        # In case both are None nothing can be done.
        return None

    # Finding all the Identities where the email and phoneNumber is mathcing
    # with the provide details.
    related_identities = identity_models.Identities.objects.filter(
        Q(email=email) | Q(phoneNumber=phoneNumber)
    ).order_by("createdAt")

    # Getting the first entry which is also primary identity
    primary_identity = related_identities.first()

    if primary_identity is None:
        # This mean there exists no entry by this email and phoneNumber
        # So we must create a new entry in db for this.
        current_identity = identity_models.Identities.objects.create(
            phoneNumber=phoneNumber,
            email=email,
            linkPrecedence=identity_choices.LinkPrecedence.PRIMARY,
        )

        return current_identity

    # There already exists some entries with the provided
    # email and phoneNumber, the first one in this will be
    # set as the primary contact, and the remaining one as
    # secondary and set their as linkedId primary_identity id.

    secondary_identites = related_identities.exclude(id=primary_identity.id)

    secondary_identites.update(
        linkedId=primary_identity.id,
        linkPrecedence=identity_choices.LinkPrecedence.SECONDARY,
    )

    # Last check is wheter their exists any entry with the provided.
    # email and PhoneNumber, if it does not exists than create one
    current_identity = identity_models.Identities.objects.filter(
        email=email, phoneNumber=phoneNumber
    ).first()

    if current_identity is None and phoneNumber is not None and email is not None:
        current_identity = identity_models.Identities.objects.create(
            phoneNumber=phoneNumber,
            email=email,
            linkPrecedence=identity_choices.LinkPrecedence.SECONDARY,
            linkedId=primary_identity,
        )

    return primary_identity
