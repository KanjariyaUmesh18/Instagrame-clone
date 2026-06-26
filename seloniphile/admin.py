from django.contrib import admin
from .models import * 
# Register your models here.
class InstaUserAdmin(admin.ModelAdmin):
    list_display = ["id","username","email","created_at"]
    search_fields = ["username","email"]
    list_display_links = ["username"]
    list_per_page = 10  
    list_filter = ["created_at"]
    list_order_by_desc = ["created_at"]

class instapostadmin(admin.ModelAdmin):
    list_display=["id","caption"]



admin.site.register(InstaUser,InstaUserAdmin)
admin.site.register(instapost,instapostadmin)
admin.site.register(FollowUserd)
admin.site.register(Notification)
admin.site.register(LikeUnlike)
admin.site.register(Comment)
admin.site.register(CreateReel)
admin.site.register(CreateStory)