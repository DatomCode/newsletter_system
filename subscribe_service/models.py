from django.db import models

# Create your models here.
class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(blank=True, null = True)
    subscribed_at = models.DateTimeField(blank=True, null=True)
    unsubsribed_at = models.DateTimeField(blank=True, null = True)

    def __str__(self):
        return self.email