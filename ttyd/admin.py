from django.contrib import admin
from ttyd.models import TTYDFunc, FeedTime

# Register your models here.

class TTYDFuncAdmin(admin.ModelAdmin):
    list_display = ('name', 'content')
admin.site.register(TTYDFunc, TTYDFuncAdmin)

class FeedTimeAdmin(admin.ModelAdmin):
    list_display = ('username','feed_time1', 'feed_time2', 'feed_time3', 'pre_feedtime')
admin.site.register(FeedTime, FeedTimeAdmin)