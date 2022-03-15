from django.contrib import admin
from . models import Account
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class AdminAccount(UserAdmin):
    
    #Displaying the list in following format
    list_display = ('first_name', 'last_name', 'username', 'email', 'date_joined', 'is_active')
    
    #Links 
    list_display_links = ('first_name', 'last_name', 'email')
    
    #Read Only Fields
    readonlyfields = ('last_login', 'date_joined')
    
    ordering = ('-date_joined',)
    
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Account, AdminAccount)