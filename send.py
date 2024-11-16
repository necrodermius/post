from django.core.mail import send_mail

send_mail(
    'Тестовий лист',
    'Це тестовий лист від Django.',
    'maksym.putin.django@gmail.com',  # Вкажіть адресу відправника
    ['denys.shtoma@knu.ua'],  # Вкажіть адресу отримувача
    fail_silently=False,
)
