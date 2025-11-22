from db.operations import addUser

# Додаємо адміністратора
login = "admin"
password = "admin123"
role = "admin"

if addUser(login, password, role):
    print("Адміністратор створений успішно!")
else:
    print("Користувач вже існує.")
