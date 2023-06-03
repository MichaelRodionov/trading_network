from django.contrib import admin

from core.models import User


# ----------------------------------------------------------------
# user admin model
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Model representing a user admin

    Attrs:
        - list_display: defines collection of fields to display
        - search_fields: defines collection of fields to search
        - exclude: defines fields to be hidden
        - readonly_fields: defines fields only to read
        - fieldsets: defines custom subsections
    """
    list_display = ('username', 'email', 'first_name', 'last_name')
    search_fields = ('username',)
    exclude = ('password', )
    readonly_fields = ('last_login', 'date_joined')

    fieldsets = (
        ('Personal Info', {
            'fields': ('username', 'email', 'first_name', 'last_name')
        }),
        ('Status', {
            'fields': ('is_active', 'is_staff', 'is_superuser')
        }),
        ('Dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )
