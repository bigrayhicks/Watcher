from django.contrib import admin
from .models import Alert, Site, Subscriber


def custom_titled_filter(title):
    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance

    return Wrapper


@admin.register(Alert)
class Alert(admin.ModelAdmin):
    list_display = ['id', 'type', 'site', 'new_ip', 'new_ip_second', 'new_MX_records', 'new_mail_A_record_ip', 'old_ip', 'old_ip_second', 'old_MX_records', 'old_mail_A_record_ip', 'difference_score',
                    'status', 'created_at']
    list_filter = ('site', ('status', custom_titled_filter('Active Status')))
    search_fields = ['id', 'new_ip', 'new_ip_second', 'old_ip', 'old_ip_second', 'difference_score', 'new_MX_records', 'new_mail_A_record_ip', 'old_MX_records', 'old_mail_A_record_ip']

    def make_disable(self, request, queryset):
        rows_updated = queryset.update(status=False)

        if rows_updated == 1:
            message_bit = "1 alert was"
        else:
            message_bit = "%s alerts were" % rows_updated
        self.message_user(request, "%s successfully marked as disable." % message_bit)

    make_disable.short_description = "Disable selected alerts"

    def make_enable(self, request, queryset):
        rows_updated = queryset.update(status=True)

        if rows_updated == 1:
            message_bit = "1 alert was"
        else:
            message_bit = "%s alerts were" % rows_updated
        self.message_user(request, "%s successfully marked as enable." % message_bit)

    make_enable.short_description = "Enable selected alerts"

    actions = [make_disable, make_enable]


@admin.register(Site)
class Site(admin.ModelAdmin):
    list_display = ['rtir', 'domain_name', 'ip', 'ip_second', 'monitored', 'web_status', 'misp_event_id',
                    'the_hive_case_id', 'created_at', 'expiry']
    list_filter = ['created_at', 'expiry', 'monitored', 'web_status']
    search_fields = ['rtir', 'domain_name', 'ip', 'ip_second', 'the_hive_case_id', 'misp_event_id']


@admin.register(Subscriber)
class Subscriber(admin.ModelAdmin):
    list_display = ['user_rec', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user_rec']
