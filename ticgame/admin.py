from django.contrib import admin
from .models import Game
# Register your models here.
class ticAdmin(admin.ModelAdmin):
    model = Game
admin.site.register(Game, ticAdmin)

# qaz 1e2r3t4y
# leha 2q3w4e5r