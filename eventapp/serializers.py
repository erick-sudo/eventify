from rest_framework import serializers
from .models import Booking, Event

# class CreateBookingSerializer(serializers.Serializer):
    
#     event_id = serializers.IntegerField(required=True)
    
#     class Meta:
#         model = Booking
#         fields = ['event_id', 'user_id']
        
#     def validate(self, attrs):
#         event_id = attrs.get('event_id')
        
#         if not Event.objects.filter(id=event_id).exists():
#             raise serializers.ValidationError("Event does not exist.")
        
#         return super().validate(attrs)
    
#     def create(self, validated_data):
#         event_id = validated_data['event_id']
#         request = self.context.get('request')
        
#         user = request.user
#         event = Event.objects.get(id=event_id)
        
#         if not Booking.objects.filter(event=event, user=user).exists():
#             booking = Booking.objects.create(event=event, user=user)
            
#             return booking
#         else:
#             raise serializers.ValidationError("You have already booked this event.")
        
    