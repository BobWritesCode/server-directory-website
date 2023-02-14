"""
Default Django admin view
"""

from django.contrib import admin

from .models import (
    CustomUser, ServerListing, Tag, Game, Bumps
)


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """
    A class to represent a CustomUser.

    ...

    Decorator
    ----------
    admin.register(CustomUser)

    Attributes
    ----------
    list_display :
        ('id', 'email', 'username')
    model :
        CustomUser
    list_filter :
        ()
    search_fields :
        ('id', 'email', 'username')
    ordering :
        ('email',)

    Methods
    -------
    None
    """
    list_display = ('id', 'email', 'username')
    model = CustomUser
    list_filter = ()
    search_fields = ('id', 'email', 'username')
    ordering = ('email',)


@admin.register(ServerListing)
class ServerListingAdmin(admin.ModelAdmin):
    """
    A class to represent a ServerListing.

    ...

    Decorator
    ----------
    admin.register(ServerListing)

    Attributes
    ----------
    list_display :
        ('title', 'game', 'owner', 'status')
    prepopulated_fields :
        {'slug': ('title',)}
    list_filter :
        ('status', 'game')
    search_fields :
        ('title', 'owner')
    ordering :
        ('title',)

    Methods
    -------
    None
    """
    list_display = ('title', 'game', 'owner', 'status')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('status', 'game')
    search_fields = ('title', 'owner')
    ordering = ('title',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    A class to represent a Tag.

    ...

    Decorator
    ----------
    admin.register(Tag)

    Attributes
    ----------
    list_display :
        ('id', 'name')
    prepopulated_fields :
        {'slug': ('name',)}
    list_filter :
        ()
    search_fields :
        ('name',)
    ordering :
        ('name',)

    Methods
    -------
    None
    """
    list_display = ('id', 'name')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ()
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    """
    A class to represent a Game.

    ...

    Decorator
    ----------
    admin.register(Game)

    Attributes
    ----------
    list_display :
        ('id', 'name', 'status')
    prepopulated_fields :
        {'slug': ('name',)}
    list_filter :
        ('status',)
    search_fields :
        ('name',)
    ordering :
        ('name',)

    Methods
    -------
    None
    """
    list_display = ('id', 'name', 'status')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('status',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Bumps)
class BumpsAdmin(admin.ModelAdmin):
    """
    A class to represent Bumps.

    ...

    Decorator
    ----------
    admin.register(Bumps)

    Attributes
    ----------
    list_display :
        ('listing', 'user', 'date_added', 'expiry')
    prepopulated_fields :
        {}
    list_filter :
        ('date_added', 'expiry')
    search_fields :
        ('listing', 'user')

    Methods
    -------
    None
    """
    list_display = ('listing', 'user', 'date_added', 'expiry')
    prepopulated_fields = {}
    list_filter = ('date_added', 'expiry')
    search_fields = ('listing', 'user')
