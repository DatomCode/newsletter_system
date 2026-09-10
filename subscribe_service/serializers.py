from rest_framework import serializers
from .models import NewsletterSubscriber


class NewsletterSubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscriber
        fields = ['email']

    # Normalise email to lowercase before saving
    def validate_email(self, value):
        return value.strip().lower()
