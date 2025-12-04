from django.contrib import admin
from .models import BloodRequest, DonationHistory


@admin.register(BloodRequest)
class BloodRequestAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'created_by', 'blood_group_needed',
        'location', 'status', 'accepted_by', 'created_at'
    )

    list_filter = ('status', 'blood_group_needed')

    search_fields = ('created_by__email', 'location', 'message')

    readonly_fields = ('id', 'created_at')

    fieldsets = (
        (None, {
            'fields': (
                'id', 'created_by', 'message',
                'blood_group_needed', 'location',
                'status', 'accepted_by', 'created_at'
            )
        }),
    )


@admin.register(DonationHistory)
class DonationHistoryAdmin(admin.ModelAdmin):

    list_display = (
        'id', 'donor', 'receiver', 'event',
        'status', 'date'
    )

    list_filter = ('status',)

    search_fields = ('donor__email', 'receiver__email')

    readonly_fields = ('id', 'date')

    fieldsets = (
        (None, {
            'fields': (
                'id', 'donor', 'receiver',
                'event', 'status', 'date'
            )
        }),
    )
