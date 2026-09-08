from rest_framework import serializers
from .models import NewsletterSubscriber


class NewsletterSubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscriber
        fields = __all__

    #strip the eamil to lower case
    def validate(self, value):
        clean_email = value.lower()
        return clean_email
