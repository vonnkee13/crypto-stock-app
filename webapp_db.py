from deta import Deta

DETA_KEY = "c0pzay8s_Wa8nDP7t24PjDYkpysNSR2zj5uJETDJm"

#Initialize with a project keys
deta = Deta(DETA_KEY)

#This is how to create/connect a database

db = deta.Base("webapp_db")

def insert_period(period, incomes, expenses, comment):
    """Returns the report on a successful creation, otherwise raises an error"""
    return db.put({"key": period, "incomes":incomes, "expenses":expenses,"comment":comment})

def fetch_all_periods():
    """Reseturns a dict of all periods"""
    res = db.fetch()
    return res.items

def get_period(period):
    """If not found, the function will return None"""
    return db.get(period)
