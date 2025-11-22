from db.operations import getAllTourists, getAllHotels, getAllExcursions

def calculateProfit():
    """
    Розрахунок рентабельності представництва
    """
    # Псевдокод, можна замінити на реальні дані
    totalIncome = sum([float(t.get('income',0)) for t in getAllTourists()])
    totalExpenses = sum([float(t.get('expenses',0)) for t in getAllTourists()])
    return totalIncome / totalExpenses if totalExpenses > 0 else 0

def popularExcursions():
    excursions = getAllExcursions()
    count = {}
    for e in excursions:
        count[e['name']] = len(e.get('tourists', []))
    return sorted(count.items(), key=lambda x: x[1], reverse=True)
