from rest_framework import serializers
from .models import BloodRequest, DonationHistory

class BloodRequestSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.id')
    accepted_by = serializers.ReadOnlyField(source='accepted_by.id')

    class Meta:
        model = BloodRequest
        fields = [
            'id',
            'created_by',
            'message',
            'blood_group_needed',
            'location',
            'status',
            'accepted_by',
            'created_at',
        ]
        read_only_fields = ['id','created_by','accepted_by','status','created_at']

class DonationHistorySerializer(serializers.ModelSerializer):
    donor = serializers.ReadOnlyField(source='donor.id')
    receiver = serializers.ReadOnlyField(source='receiver.id')
    event = serializers.ReadOnlyField(source='event.id')

    class Meta:
        model = DonationHistory
        fields = [
            'id',
            'donor',
            'receiver',
            'event',
            'date',
            'status',

        ]
        read_only_fields = ['id','donor','receiver','event','date']
        
