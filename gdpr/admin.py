from django.contrib import admin
from .models import DataRetentionSettings, UserDataDeletionRequest, DataAccessRequest


@admin.register(DataRetentionSettings)
class DataRetentionSettingsAdmin(admin.ModelAdmin):
    list_display = ('retention_period_days', 'auto_delete_inactive_users', 'notify_before_deletion_days', 'updated_at')
    list_filter = ('auto_delete_inactive_users', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(UserDataDeletionRequest)
class UserDataDeletionRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'requested_at', 'deletion_scheduled_at', 'deleted_at')
    list_filter = ('status', 'requested_at', 'processed_at')
    search_fields = ('user__email', 'user__username')
    readonly_fields = ('requested_at', 'processed_at', 'deleted_at')
    actions = ['schedule_deletion', 'cancel_deletion', 'execute_deletion']

    def schedule_deletion(self, request, queryset):
        for obj in queryset:
            obj.schedule_deletion()
    schedule_deletion.short_description = "Schedule selected deletions"

    def cancel_deletion(self, request, queryset):
        for obj in queryset:
            obj.cancel_deletion()
    cancel_deletion.short_description = "Cancel selected deletions"

    def execute_deletion(self, request, queryset):
        for obj in queryset:
            obj.execute_deletion()
    execute_deletion.short_description = "Execute selected deletions"


@admin.register(DataAccessRequest)
class DataAccessRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'requested_at', 'processed_at')
    list_filter = ('status', 'requested_at', 'processed_at')
    search_fields = ('user__email', 'user__username')
    readonly_fields = ('requested_at', 'processed_at')