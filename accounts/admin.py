from django.contrib import admin
from .models import Customer, Transaction, TransactionByPhone

admin.site.register(Customer)
admin.site.register(Transaction)
admin.site.register(TransactionByPhone)

