from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, ServerListing, Tag, Game


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email',)
    model = CustomUser


@admin.register(ServerListing)
class ServerListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'game', 'status',  'created_on', 'updated_on')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('status', 'created_on')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('name',)


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('name',)
