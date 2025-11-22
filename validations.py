import re

print("validations.py завантажено")

def validateLogin(login):
    """Перевірка логіна: мінімум 3 символи, лише букви і цифри"""
    if len(login) < 3:
        return False
    if not re.match(r'^[A-Za-z0-9]+$', login):
        return False
    return True

def validatePassword(password):
    """Перевірка пароля: мінімум 6 символів, має хоча б 1 цифру та 1 букву"""
    if len(password) < 6:
        return False
    if not re.search(r'[A-Za-z]', password):
        return False
    if not re.search(r'\d', password):
        return False
    return True
