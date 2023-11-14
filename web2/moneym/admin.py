from django.contrib import admin
from .models import *  # Import the Transactions model

# Register the Transactions model
admin.site.register(Transaction)
admin.site.register(Account)
admin.site.register(Subcategory)
admin.site.register(Category)
admin.site.register(Transfer)
