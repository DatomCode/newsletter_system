from rest_framework.throttling import AnonRateThrottle

class NewsletterThrottle(AnonRateThrottle):
    scope = "subscription_service"