from django.contrib import admin

from . import models


@admin.register(models.SuperCategory)
class SuperCategoryAdmin(admin.ModelAdmin):
    """Admin View for SuperCategory"""

    list_display = ("name",)
    list_filter = ("name",)
    search_fields = ("name",)


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin View for Category"""

    list_display = ("name",)
    list_filter = ("name",)
    search_fields = ("name",)


@admin.register(models.Tournament)
class TournamentAdmin(admin.ModelAdmin):
    """Admin View for Tournament"""

    list_display = ("pk", "name", "created", "last_modified")
    list_filter = ("name",)
    search_fields = ("name",)


@admin.register(models.Match)
class MatchAdmin(admin.ModelAdmin):
    """Admin View for Match"""

    def get_users(self, obj):
        return [x.username for x in obj.users]

    list_display = ("tournament", "level", "get_users")
    search_fields = ("tournament",)
