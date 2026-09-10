from .serializers import NewsletterSubscriberSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .throttles import NewsletterThrottle

# Create your views here.
class SubscribeView(APIView):
    permission_classes =[AllowAny]
    throttle_classes = [NewsletterThrottle]

    def post(self, request):
        serializer = NewsletterSubscriberSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Susscessfully Subscribed to newsletter"}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)