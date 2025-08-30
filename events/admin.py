from django.contrib import admin
from .models import Event, TicketType, Category

class TicketTypeInline(admin.TabularInline):
	model = TicketType
	extra = 1

class EventAdmin(admin.ModelAdmin):
	inlines = [TicketTypeInline]
	list_display = ('title', 'date', 'status', 'category')
	list_filter = ('status', 'category')

admin.site.register(Event, EventAdmin)
admin.site.register(Category)
