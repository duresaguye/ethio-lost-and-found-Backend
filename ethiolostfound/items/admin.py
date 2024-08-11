# admin.py
from django.contrib import admin
from .models import Item

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'location', 'contact', 'item_type', 'user')  # Adjust fields as necessary
    list_filter = ('item_type', 'location', 'user')
    search_fields = ('title', 'description', 'location', 'contact')
