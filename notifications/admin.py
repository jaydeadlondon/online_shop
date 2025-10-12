from django.contrib import admin
from .models import EmailLog


@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ['recipient', 'email_type', 'status', 'sent_at', 'created_at']
    list_filter = ['email_type', 'status', 'created_at']
    search_fields = ['recipient', 'subject', 'user__email']
    readonly_fields = ['created_at', 'sent_at']
