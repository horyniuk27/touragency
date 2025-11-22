import tkinter as tk
from tkinter import messagebox
from db.operations import checkLogin
from ui.adminPanel import AdminPanel
from ui.operatorPanel import OperatorPanel
from ui.userPanel import UserPanel
from ui.guestPanel import GuestPanel

class LoginScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Вхід у систему")
        self.root.geometry("300x200")

        tk.Label(root, text="Логін").pack()
        self.loginEntry = tk.Entry(root)
        self.loginEntry.pack()

        tk.Label(root, text="Пароль").pack()
        self.passwordEntry = tk.Entry(root, show="*")
        self.passwordEntry.pack()

        tk.Button(root, text="Вхід", command=self.login).pack(pady=10)

    def login(self):
        login = self.loginEntry.get()
        password = self.passwordEntry.get()
        user = checkLogin(login, password)
        if user:
            messagebox.showinfo("Успіх", f"Вхід успішний! Роль: {user['accessRight']}")
            self.root.destroy()
            self.openPanel(user)
        else:
            messagebox.showerror("Помилка", "Неправильний логін або пароль")

    def openPanel(self, user):
        root = tk.Tk()
        if user["accessRight"] == "admin":
            AdminPanel(root, user)
        elif user["accessRight"] == "operator":
            OperatorPanel(root, user)
        elif user["accessRight"] == "user":
            UserPanel(root, user)
        else:
            GuestPanel(root, user)
        root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginScreen(root)
    root.mainloop()
