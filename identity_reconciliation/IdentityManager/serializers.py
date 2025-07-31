from rest_framework import serializers
from IdentityManager.models import Identities
from rest_framework.fields import empty


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

    def get_emails(self, instance: Identities):
        linked_identites = Identities.objects.filter(linkedId=instance.id)
        emails = instance.email + list(linked_identites.values_list("email", flat=True))
        return emails

    def get_phoneNumbers(self, instance: Identities):
        linked_identites = Identities.objects.filter(linkedId=instance.id)
        phone_numbers = instance.phoneNumber + list(
            linked_identites.values_list("phoneNumber", flat=True)
        )
        return phone_numbers

    def get_secondaryContactIds(self, instance: Identities):
        linked_identites = Identities.objects.filter(linkedId=instance.id)
        return linked_identites.values_list("id", flat=True)


class IdentityContactResponseSerailizer(serializers.ModelSerializer):

    contact = IdentityContactSerailizer()

    class Meta:
        model = Identities
        fields = ("contact",)


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
