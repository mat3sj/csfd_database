from django.contrib import admin

from database.models import Actor, Movie


class ActorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)


class MovieAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)


admin.site.register(Actor, ActorAdmin)
admin.site.register(Movie, MovieAdmin)
