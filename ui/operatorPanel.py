import tkinter as tk
from tkinter import messagebox
from db.operations import (
    addTourist, getAllTourists, deleteTourist, updateTourist,
    addHotel, getAllHotels,
    addExcursion, getAllExcursions,
    addCargo, getCargoByTourist
)
from bson.objectid import ObjectId
from tkcalendar import Calendar

class OperatorPanel:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        self.root.title("Operator Panel")
        self.root.geometry("900x600")

        tk.Label(root, text=f"Ласкаво просимо, {user['login']} (Operator)").pack()

        # Кнопки для всіх CRUD
        tk.Button(root, text="Додати туриста", command=self.addTouristScreen).pack(pady=2)
        tk.Button(root, text="Перегляд/редагування туристів", command=self.viewTourists).pack(pady=2)
        tk.Button(root, text="Додати готель", command=self.addHotelScreen).pack(pady=2)
        tk.Button(root, text="Перегляд готелів", command=self.viewHotels).pack(pady=2)
        tk.Button(root, text="Додати екскурсію", command=self.addExcursionScreen).pack(pady=2)
        tk.Button(root, text="Перегляд екскурсій", command=self.viewExcursions).pack(pady=2)
        tk.Button(root, text="Додати вантаж", command=self.addCargoScreen).pack(pady=2)
        tk.Button(root, text="Перегляд вантажів", command=self.viewCargo).pack(pady=2)

    # ---------------- TOURISTS ---------------- #
    def addTouristScreen(self):
        top = tk.Toplevel(self.root)
        top.title("Додати туриста")

        fields = ["ПІБ", "Паспорт", "Стать", "Вік", "Діти", "Готель", "Категорія"]
        entries = {}
        for f in fields:
            tk.Label(top, text=f).pack()
            entry = tk.Entry(top)
            entry.pack()
            entries[f] = entry

        # Додати календар для дати народження
        tk.Label(top, text="Дата народження").pack()
        cal = Calendar(top, date_pattern='yyyy-mm-dd')
        cal.pack()

        def saveTourist():
            data = {
                "fullName": entries["ПІБ"].get(),
                "passport": entries["Паспорт"].get(),
                "gender": entries["Стать"].get(),
                "age": entries["Вік"].get(),
                "children": entries["Діти"].get(),
                "hotel": entries["Готель"].get(),
                "category": entries["Категорія"].get(),
                "birthDate": cal.get_date()
            }
            addTourist(data)
            messagebox.showinfo("Успіх", "Туриста додано")
            top.destroy()

        tk.Button(top, text="Додати", command=saveTourist).pack(pady=5)

    def viewTourists(self):
        tourists = getAllTourists()
        top = tk.Toplevel(self.root)
        top.title("Туристи")

        for t in tourists:
            text = f"{t.get('fullName')} | {t.get('passport')} | {t.get('category')} | {t.get('birthDate','')}"
            frame = tk.Frame(top)
            frame.pack()
            tk.Label(frame, text=text).pack(side=tk.LEFT)
            tk.Button(frame, text="Видалити", command=lambda id=t['_id']: self.deleteTourist(id, top)).pack(side=tk.LEFT)
            tk.Button(frame, text="Редагувати", command=lambda t=id: self.editTourist(t, top)).pack(side=tk.LEFT)

    def deleteTourist(self, touristId, window):
        deleteTourist(touristId)
        messagebox.showinfo("Успіх", "Туриста видалено")
        window.destroy()
        self.viewTourists()

    def editTourist(self, tourist, window):
        window.destroy()
        top = tk.Toplevel(self.root)
        top.title("Редагування туриста")

        fields = ["fullName", "passport", "gender", "age", "children", "hotel", "category"]
        entries = {}
        for f in fields:
            tk.Label(top, text=f).pack()
            entry = tk.Entry(top)
            entry.pack()
            entry.insert(0, tourist.get(f))
            entries[f] = entry

        # Календар для дати народження
        tk.Label(top, text="Дата народження").pack()
        cal = Calendar(top, date_pattern='yyyy-mm-dd')
        cal.pack()
        cal.set_date(tourist.get('birthDate','2025-01-01'))

        def saveChanges():
            updatedData = {f: entries[f].get() for f in fields}
            updatedData["birthDate"] = cal.get_date()
            updateTourist(str(tourist["_id"]), updatedData)
            messagebox.showinfo("Успіх", "Зміни збережено")
            top.destroy()
            self.viewTourists()

        tk.Button(top, text="Зберегти", command=saveChanges).pack(pady=5)

    # ---------------- HOTELS ---------------- #
    def addHotelScreen(self):
        top = tk.Toplevel(self.root)
        top.title("Додати готель")
        fields = ["Назва", "Адреса", "Кількість номерів"]
        entries = {}
        for f in fields:
            tk.Label(top, text=f).pack()
            entry = tk.Entry(top)
            entry.pack()
            entries[f] = entry

        def saveHotel():
            data = { "name": entries["Назва"].get(), "address": entries["Адреса"].get(), "rooms": entries["Кількість номерів"].get() }
            addHotel(data)
            messagebox.showinfo("Успіх", "Готель додано")
            top.destroy()

        tk.Button(top, text="Додати", command=saveHotel).pack(pady=5)

    def viewHotels(self):
        hotels = getAllHotels()
        top = tk.Toplevel(self.root)
        top.title("Готелі")
        for h in hotels:
            tk.Label(top, text=f"{h.get('name')} | {h.get('address')} | {h.get('rooms')} номерів").pack()

    # ---------------- EXCURSIONS ---------------- #
    def addExcursionScreen(self):
        top = tk.Toplevel(self.root)
        top.title("Додати екскурсію")
        fields = ["Назва", "Агентство"]
        entries = {}
        for f in fields:
            tk.Label(top, text=f).pack()
            entry = tk.Entry(top)
            entry.pack()
            entries[f] = entry

        def saveExcursion():
            data = {"name": entries["Назва"].get(), "agency": entries["Агентство"].get(), "tourists": []}
            addExcursion(data)
            messagebox.showinfo("Успіх", "Екскурсію додано")
            top.destroy()

        tk.Button(top, text="Додати", command=saveExcursion).pack(pady=5)

    def viewExcursions(self):
        excursions = getAllExcursions()
        top = tk.Toplevel(self.root)
        top.title("Екскурсії")
        for e in excursions:
            tourists = ", ".join(e.get('tourists', []))
            tk.Label(top, text=f"{e.get('name')} | Агентство: {e.get('agency')} | Туристи: {tourists}").pack()

    # ---------------- CARGO ---------------- #
    def addCargoScreen(self):
        top = tk.Toplevel(self.root)
        top.title("Додати вантаж")
        fields = ["Турист", "Вага", "Вартість"]
        entries = {}
        for f in fields:
            tk.Label(top, text=f).pack()
            entry = tk.Entry(top)
            entry.pack()
            entries[f] = entry

        tk.Label(top, text="Дата відправлення").pack()
        cal = Calendar(top, date_pattern='yyyy-mm-dd')
        cal.pack()

        def saveCargo():
            data = {"tourist": entries["Турист"].get(), "weight": entries["Вага"].get(), "cost": entries["Вартість"].get(), "date": cal.get_date()}
            addCargo(data)
            messagebox.showinfo("Успіх", "Вантаж додано")
            top.destroy()

        tk.Button(top, text="Додати", command=saveCargo).pack(pady=5)

    def viewCargo(self):
        top = tk.Toplevel(self.root)
        top.title("Вантажі туристів")
        tourists = getAllTourists()
        for t in tourists:
            cargoList = getCargoByTourist(t['fullName'])
            for c in cargoList:
                tk.Label(top, text=f"Турист: {c.get('tourist')} | Вага: {c.get('weight')} | Вартість: {c.get('cost')} | Дата: {c.get('date')}").pack()
