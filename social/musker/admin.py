from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile,Tweet


# uregister group model
admin.site.unregister(Group)

# mix admin with profile 
class ProfileToMix(admin.StackedInline):
    model = Profile

class CustomUserAdmin(admin.ModelAdmin):
    model = User
    fields = ['username']
    inlines = [ProfileToMix]

# reregister user with only field username
admin.site.unregister(User)
admin.site.register(User,CustomUserAdmin)

# register profile in admin site
# admin.site.register(Profile)

# register tweet model 
admin.site.register(Tweet)