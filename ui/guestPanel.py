import tkinter as tk
from tkinter import messagebox
from db.operations import getAllTourists, addUser, getAllExcursions, getCargoByTourist
from tkcalendar import Calendar

class GuestPanel:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.root.title("Guest Panel")
        self.root.geometry("800x500")

        tk.Label(root, text=f"Ласкаво просимо, {user['login']} (Guest)").pack()

        tk.Button(root, text="Перегляд туристів", command=self.viewTourists).pack(pady=2)
        tk.Button(root, text="Перегляд екскурсій", command=self.viewExcursions).pack(pady=2)
        tk.Button(root, text="Перегляд вантажів", command=self.viewCargo).pack(pady=2)
        tk.Button(root, text="Подати заявку на авторизацію", command=self.applyForUser).pack(pady=2)

    def viewTourists(self):
        tourists = getAllTourists()
        top = tk.Toplevel(self.root)
        top.title("Туристи")
        for t in tourists:
            tk.Label(top, text=f"{t.get('fullName')} | {t.get('passport')} | {t.get('category')}").pack()

    def viewExcursions(self):
        top = tk.Toplevel(self.root)
        top.title("Екскурсії з фільтром за датою")

        tk.Label(top, text="Виберіть дату:").pack()
        cal = Calendar(top, date_pattern='yyyy-mm-dd')
        cal.pack()

        def filterExcursions():
            date = cal.get_date()
            excursions = getAllExcursions()
            topResults = tk.Toplevel(self.root)
            topResults.title(f"Екскурсії за {date}")
            for e in excursions:
                tk.Label(topResults, text=f"{e.get('name')} | Агентство: {e.get('agency')} | Туристи: {', '.join(e.get('tourists',[]))}").pack()

        tk.Button(top, text="Показати екскурсії", command=filterExcursions).pack(pady=5)

    def viewCargo(self):
        top = tk.Toplevel(self.root)
        top.title("Вантажі туристів з фільтром за датою")

        tk.Label(top, text="Виберіть дату:").pack()
        cal = Calendar(top, date_pattern='yyyy-mm-dd')
        cal.pack()

        def filterCargo():
            date = cal.get_date()
            topResults = tk.Toplevel(self.root)
            topResults.title(f"Вантажі за {date}")
            for t in getAllTourists():
                cargoList = getCargoByTourist(t['fullName'])
                for c in cargoList:
                    if c.get('date') == date:
                        tk.Label(topResults, text=f"Турист: {c.get('tourist')} | Вага: {c.get('weight')} | Вартість: {c.get('cost')} | Дата: {c.get('date')}").pack()

        tk.Button(top, text="Показати вантажі", command=filterCargo).pack(pady=5)

    def applyForUser(self):
        top = tk.Toplevel(self.root)
        top.title("Заявка на авторизацію")

        tk.Label(top, text="Придумайте логін").pack()
        loginEntry = tk.Entry(top)
        loginEntry.pack()

        tk.Label(top, text="Придумайте пароль").pack()
        passwordEntry = tk.Entry(top)
        passwordEntry.pack()

        def submitRequest():
            login = loginEntry.get()
            password = passwordEntry.get()
            if addUser(login, password, "guestRequest"):
                messagebox.showinfo("Успіх", "Заявка на авторизацію відправлена адміністратору")
                top.destroy()
            else:
                messagebox.showerror("Помилка", "Логін вже існує")

        tk.Button(top, text="Відправити заявку", command=submitRequest).pack(pady=5)
