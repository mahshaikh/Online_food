from django.contrib import admin
from .models import User,UserProfile
from django.contrib.auth.admin import UserAdmin

class CustomerUserAdmin(UserAdmin):
	filter_horizontal = ()
	list_filter = ()
	fieldsets = ()

admin.site.register(User,CustomerUserAdmin)

admin.site.register(UserProfile)


