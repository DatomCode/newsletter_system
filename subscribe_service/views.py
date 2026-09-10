from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from .serializers import NewsletterSubscriberSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework.permissions import AllowAny
from rest_framework.exceptions import Throttled
from .throttles import NewsletterThrottle


class SubscribeView(APIView):
    """Subscribe an email address to the newsletter."""

    # permission_classes = [AllowAny]
    throttle_classes = [NewsletterThrottle]
    def throttled(self, request, wait):
             
        # We create a custom dictionary with our specific message for this view
        custom_message = {
            "error": "Rate limit reached",
            "message": f"Too many attempts, Please wait {int(wait)} seconds and try again.",
            "retry_after": int(wait)
        }
        
        raise Throttled(detail=custom_message) #return the custom message
    
    @extend_schema(
        summary="Subscribe to newsletter",
        description=(
            "Submit an email address to subscribe to the newsletter. "
            "Emails are normalised to lowercase before storage. "
            "Duplicate submissions are rejected with a 400 response. "
            "Rate-limited to **5 requests per minute** per IP address."
        ),
        request=NewsletterSubscriberSerializer,
        responses={
            201: OpenApiResponse(
                description="Subscription successful",
                examples=[
                    OpenApiExample(
                        "Success",
                        value={"message": "Successfully Subscribed to newsletter"},
                    )
                ],
            ),
            400: OpenApiResponse(
                description="Validation error (e.g. invalid or duplicate email)",
                examples=[
                    OpenApiExample(
                        "Duplicate email",
                        value={"email": ["newsletter subscriber with this email already exists."]},
                    ),
                    OpenApiExample(
                        "Invalid email",
                        value={"email": ["Enter a valid email address."]},
                    ),
                ],
            ),
            429: OpenApiResponse(description="Rate limit exceeded — try again later"),
        },
        tags=["Subscription"],
    )

    
        
    def post(self, request):
        serializer = NewsletterSubscriberSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Successfully Subscribed to newsletter"},
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    