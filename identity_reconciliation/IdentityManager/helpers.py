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

    # Finding all the Identities where the email and phoneNumber is mathcing
    # with the provide details.
    related_identities = identity_models.Identities.objects.filter(
        Q(email=email) | Q(phoneNumber=phoneNumber)
    ).order_by("createdAt")

    if not related_identities.exists():
        # This mean there exists no entry by this email and phoneNumber
        # So we must create a new entry in db for this.
        current_identity = identity_models.Identities.objects.create(
            phoneNumber=phoneNumber,
            email=email,
            linkPrecedence=identity_choices.LinkPrecedence.PRIMARY,
        )

        return current_identity

    # Getting the primary identities
    primary_identities = related_identities.filter(
        linkPrecedence=identity_choices.LinkPrecedence.PRIMARY
    )

    if primary_identities.exists():
        # There exists atleast one primary identity in the search
        # space, this is out main primary instance.
        primary_identity = primary_identities.first()
    else:
        # There exists no primary identity in the search
        # space, so we select the first seconday identity,
        # then we get the primary identity from it.
        secondary_identity = related_identities.first()
        primary_identity = secondary_identity.linkedId

    # There already exists some entries with the provided
    # email and phoneNumber, the oldest primary one  will be
    # kept as the primary contact, and the remaining one as
    # secondary and set their as linkedId primary_identity id.
    secondary_identites = related_identities.exclude(id=primary_identity.id)

    secondary_identites.update(
        linkedId=primary_identity,
        linkPrecedence=identity_choices.LinkPrecedence.SECONDARY,
    )

    # Now with the provided details, if phone Number or
    # email is None then we don't need to create new entry
    # in the database as there is no new data.
    if phoneNumber is None or email is None:
        return primary_identity

    # Last check is wether both email and PhoneNumber exists in the database
    #  if even one of them does not exists we create a new entry.
    email_does_not_exists = not identity_models.Identities.objects.filter(
        email=email
    ).exists()
    phoneNumber_does_not_exists = not identity_models.Identities.objects.filter(
        phoneNumber=phoneNumber
    ).exists()

    if email_does_not_exists or phoneNumber_does_not_exists:
        # Either the email or phoneNumber does not exists
        # in the database.
        current_identity = identity_models.Identities.objects.create(
            phoneNumber=phoneNumber,
            email=email,
            linkPrecedence=identity_choices.LinkPrecedence.SECONDARY,
            linkedId=primary_identity,
        )

    return primary_identity
