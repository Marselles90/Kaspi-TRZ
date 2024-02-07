from django.db import models, transaction
from .utils import validate_phone, validate_email
from django.forms import ValidationError

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=15, validators=[validate_phone], unique=True)
    email = models.EmailField(validators=[validate_email], blank=True, null=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f'{self.first_name}, {self.balance}'
    
    def debit(self, amount):
        self.balance -= amount
        self.save()


    def credit(self, amount):
        self.balance += amount
        self.save()


class Transaction(models.Model):
    sender = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='sender')
    reseiver = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='reseiver')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.sender == self.reseiver:
            raise ValidationError('Нельзя отправлять самому себе !')
        if self.sender.balance < self.amount:
            raise ValidationError('Недостаточно средств для отправки !')
        if self.amount < 0:
            raise ValidationError('Сумма должна быть положительной !')

    def save(self, *args, **kwargs):
        with transaction.atomic():
            self.sender.debit(self.amount)
            self.reseiver.credit(self.amount)
            super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.sender} -> {self.reseiver} {self.amount}'
    

class TransactionByPhone(models.Model):
    sender = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='sender_phone')
    reseiver = models.CharField(max_length=15, validators=[validate_phone])
    amount = models.DecimalField(max_digits=7, decimal_places=2, default=0e)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender} - > {self.reseiver} {self.amount}'
    
    def clean(self):
        if self.sender.balance < self.amount:
            raise ValidationError('Недостаточно средств для отправки')
        if self.amount < 0 or not self.amount:
            raise ValidationError('Сумма должна быть больше 0')
        if not Customer.objects.filter(phone=self.reseiver).exists():
            raise ValidationError('Неверный номер телефона')
        if self.sender.phone == self.reseiver:
            raise ValidationError('Нельзя переводить самому себе')
        

    def save(self, *args, **kwargs):
        reseiver = Customer.objects.get(phone=self.reseiver)
        self.sender.debit(self.amount)
        reseiver.credit(self.amount)
        super().save(*args, **kwargs)