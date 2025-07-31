from rest_framework import serializers
from IdentityManager.models import Identities
from rest_framework.fields import empty
from drf_yasg.utils import swagger_serializer_method


class IdentitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Identities
        fields = "__all__"


class IdentityContactSerailizer(serializers.ModelSerializer):
    primaryContatctId = serializers.SerializerMethodField()
    emails = serializers.SerializerMethodField()
    phoneNumbers = serializers.SerializerMethodField()
    secondaryContactIds = serializers.SerializerMethodField()

    class Meta:
        model = Identities
        fields = ("primaryContatctId", "emails", "phoneNumbers", "secondaryContactIds")

    def get_primaryContatctId(self, instance: Identities):
        return instance.id

    @swagger_serializer_method(
        serializer_or_field=serializers.ListSerializer(child=serializers.EmailField())
    )
    def get_emails(self, instance: Identities):
        linked_identites = Identities.objects.filter(linkedId=instance.id)
        emails = [instance.email] + list(
            linked_identites.exclude(email=None)
            .values_list("email", flat=True)
            .distinct()
        )
        return set(emails)

    @swagger_serializer_method(
        serializer_or_field=serializers.ListSerializer(child=serializers.CharField())
    )
    def get_phoneNumbers(self, instance: Identities):
        linked_identites = Identities.objects.filter(linkedId=instance.id)
        phone_numbers = [instance.phoneNumber] + list(
            linked_identites.exclude(phoneNumber=None)
            .values_list("phoneNumber", flat=True)
            .distinct()
        )
        return set(phone_numbers)

    @swagger_serializer_method(
        serializer_or_field=serializers.ListSerializer(child=serializers.IntegerField())
    )
    def get_secondaryContactIds(self, instance: Identities):
        linked_identites = Identities.objects.filter(linkedId=instance.id)
        return linked_identites.values_list("id", flat=True).distinct()


class IdentityContactResponseSerailizer(serializers.ModelSerializer):

    contact = serializers.SerializerMethodField()

    class Meta:
        model = Identities
        fields = ("contact",)

    @swagger_serializer_method(serializer_or_field=IdentityContactSerailizer)
    def get_contact(self, instance):
        contact_serailizer = IdentityContactSerailizer(instance=instance)
        return contact_serailizer.data


class IdentityRequestSerializer(serializers.Serializer):

    email = serializers.EmailField(allow_null=True)
    phoneNumber = serializers.CharField(allow_null=True)

    def validate(self, attrs):

        email = attrs.get("email", None)
        phoneNumber = attrs.get("phoneNumber", None)

        if email is None and phoneNumber is None:
            raise serializers.ValidationError(
                "Both email and phoneNumber cannot be null."
            )
        return attrs
