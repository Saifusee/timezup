from typing import Any, List, Optional, Tuple, Union
from django.contrib import admin
from django.http.request import HttpRequest
from .models import Task, CombineDate
from django.contrib.auth import  get_user_model

# Register your models here.
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "task", "combine_date", "user", "created_at", "modified_at")
    list_display_links = ("id", "task")
    fields = ("task", "combine_date", "user", "created_at", "modified_at")
    readonly_fields = ("created_at", "modified_at")
    raw_id_fields = ("user",)
    ordering = ("id",)
    search_fields = ["id", "task", "user__username", "user__email", "combine_date__date__data", 
        "combine_date__month__data", "combine_date__year__data", "created_at", "modified_at"]


class CombineDateAdmin(admin.ModelAdmin):
    list_display = ("id", "date", "month", "year")
    list_display_links = ("id", "date", "month", "year")
    ordering = ("id",)
    search_fields = ["id", "date__data", "month__data", "year__data"]

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser or obj is None:
            return tuple()
        else:
            return ("date", "month", "year")


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "is_active", "last_login", "is_staff", "is_superuser")
    list_display_links = ("username", "email")
    fields = ("username", "email", "groups", "user_permissions", "is_active", "is_staff", "is_superuser", "last_login")
    filter_horizontal = ("groups", "user_permissions")
    readonly_fields = ("last_login",)
    ordering = ("id",)
    search_fields = ["id", "username", "email", "last_login"]


admin.site.register(Task, TaskAdmin)
admin.site.register(CombineDate, CombineDateAdmin)
admin.site.register(get_user_model(), CustomUserAdmin)
