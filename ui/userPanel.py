import tkinter as tk
from tkinter import messagebox
from db.operations import getAllTourists, getAllExcursions, getCargoByTourist
from tkcalendar import Calendar

class UserPanel:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.root.title("User Panel")
        self.root.geometry("900x600")

        tk.Label(root, text=f"Ласкаво просимо, {user['login']} (User)").pack()

        tk.Button(root, text="Перегляд туристів", command=self.viewTourists).pack(pady=2)
        tk.Button(root, text="Перегляд екскурсій", command=self.viewExcursions).pack(pady=2)
        tk.Button(root, text="Перегляд вантажу", command=self.viewCargo).pack(pady=2)
        tk.Button(root, text="Пошук туриста", command=self.searchTouristScreen).pack(pady=2)

    # ---------------- TOURISTS ---------------- #
    def viewTourists(self):
        tourists = getAllTourists()
        top = tk.Toplevel(self.root)
        top.title("Туристи")
        for t in tourists:
            text = f"{t.get('fullName')} | {t.get('passport')} | {t.get('category')} | {t.get('birthDate','')}"
            tk.Label(top, text=text).pack()

    def searchTouristScreen(self):
        top = tk.Toplevel(self.root)
        top.title("Пошук туриста")

        tk.Label(top, text="Введіть ім'я або категорію:").pack()
        entry = tk.Entry(top)
        entry.pack()

        def search():
            key = entry.get().lower()
            results = []
            for t in getAllTourists():
                if key in t.get('fullName','').lower() or key in t.get('category','').lower():
                    results.append(t)
            for widget in top.winfo_children():
                if isinstance(widget, tk.Label) and widget not in [entry]:
                    widget.destroy()
            for r in results:
                tk.Label(top, text=f"{r.get('fullName')} | {r.get('passport')} | {r.get('category')}").pack()

        tk.Button(top, text="Пошук", command=search).pack(pady=5)

    # ---------------- EXCURSIONS ---------------- #
    def viewExcursions(self):
        top = tk.Toplevel(self.root)
        top.title("Екскурсії з фільтром за датою")

        tk.Label(top, text="Фільтрувати за датою:").pack()
        cal = Calendar(top, date_pattern='yyyy-mm-dd')
        cal.pack()

        tk.Label(top, text="Агентство (необов'язково):").pack()
        agencyEntry = tk.Entry(top)
        agencyEntry.pack()

        def filterExcursions():
            date = cal.get_date()
            agency = agencyEntry.get().lower()
            excursions = getAllExcursions()
            for widget in top.winfo_children():
                if isinstance(widget, tk.Label) and widget not in [agencyEntry]:
                    widget.destroy()
            for e in excursions:
                tourists_dates = e.get('tourists', [])
                if (not agency or agency in e.get('agency','').lower()):
                    tk.Label(top, text=f"{e.get('name')} | Агентство: {e.get('agency')} | Туристи: {', '.join(tourists_dates)}").pack()

        tk.Button(top, text="Фільтрувати", command=filterExcursions).pack(pady=5)

    # ---------------- CARGO ---------------- #
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
