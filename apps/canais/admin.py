from django.contrib import admin
from .models import Canal, Grupo


class AdminCanal(admin.ModelAdmin):
    list_display = ['id', 'name', 'group_title', 'status']
    search_fields = ['name', 'group_title', 'status']
    list_filter = ['status']

    def change_status_to_one(self, request, queryset):
        queryset.update(status=1)


class AdminGrupo(admin.ModelAdmin):
    pass

admin.site.register(Canal, AdminCanal)
admin.site.register(Grupo, AdminGrupo)

