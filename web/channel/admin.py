from django.contrib import admin
from . import models

def CustomCountryFilterFunction(attr_name, filter_title):

    class CustomCountryFilterClass(admin.SimpleListFilter):
        """Filter that shows only referenced options, i.e. options having at least a single object."""
        title = filter_title
        parameter_name = attr_name

        def lookups(self, request, model_admin):
            related_objects = set([getattr(obj, attr_name) for obj in model_admin.model.objects.all()])
            return [(related_obj.code, related_obj.name) for related_obj in related_objects]

        def queryset(self, request, queryset):
            if self.value():
                return queryset.filter(**{'%s' % attr_name: self.value()})
            else:
                return queryset

    return CustomCountryFilterClass


@admin.register(models.Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ('id', 'country')
    list_filter = (CustomCountryFilterFunction("country", "country"),)
    search_fields = ('country',)
    readonly_fields = ('slug',)

    def get_readonly_fields(self, request, obj=None):
        return [] if obj else self.readonly_fields
