import tkinter as tk
from tkinter import messagebox

from validations import validateLogin, validatePassword
from db.operations import getUser

print("main.py запущено")

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("400x250")

        tk.Label(root, text="Логін:").pack(pady=5)
        self.loginEntry = tk.Entry(root)
        self.loginEntry.pack(pady=5)

        tk.Label(root, text="Пароль:").pack(pady=5)
        self.passEntry = tk.Entry(root, show="*")
        self.passEntry.pack(pady=5)

        tk.Button(root, text="Увійти", command=self.login).pack(pady=10)

    def login(self):
        login = self.loginEntry.get()
        password = self.passEntry.get()

        if not validateLogin(login):
            messagebox.showerror("Помилка", "Невірний логін")
            return
        if not validatePassword(password):
            messagebox.showerror("Помилка", "Невірний пароль")
            return

        user = getUser(login)
        if not user or user["password"] != password:
            messagebox.showerror("Помилка", "Невірний логін або пароль")
            return

        # Закриваємо вікно логіну
        self.root.destroy()

        # Відкриваємо панель відповідно до ролі
        from ui.adminPanel import AdminPanel

        rootPanel = tk.Tk()
        AdminPanel(rootPanel, user)
        rootPanel.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()
