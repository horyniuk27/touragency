import tkinter as tk
from tkinter import messagebox
from db.operations import addUser, getAllTourists

class AdminPanel:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.root.title("Admin Panel")
        self.root.geometry("600x400")

        tk.Label(root, text=f"Ласкаво просимо, {user['login']}").pack()

        tk.Button(root, text="Додати користувача", command=self.addUserScreen).pack(pady=5)
        tk.Button(root, text="Перегляд туристів", command=self.viewTourists).pack(pady=5)

    def addUserScreen(self):
        top = tk.Toplevel(self.root)
        top.title("Додати користувача")
        tk.Label(top, text="Логін").pack()
        loginEntry = tk.Entry(top)
        loginEntry.pack()

        tk.Label(top, text="Пароль").pack()
        passwordEntry = tk.Entry(top)
        passwordEntry.pack()

        tk.Label(top, text="Права доступу").pack()
        accessEntry = tk.Entry(top)
        accessEntry.pack()

        def saveUser():
            login = loginEntry.get()
            password = passwordEntry.get()
            access = accessEntry.get()
            if addUser(login, password, access):
                messagebox.showinfo("Успіх", "Користувача додано")
                top.destroy()
            else:
                messagebox.showerror("Помилка", "Користувач вже існує")

        tk.Button(top, text="Додати", command=saveUser).pack(pady=5)

    def viewTourists(self):
        tourists = getAllTourists()
        top = tk.Toplevel(self.root)
        top.title("Туристи")
        for t in tourists:
            tk.Label(top, text=f"{t.get('fullName')} | {t.get('passport')} | {t.get('category')}").pack()
