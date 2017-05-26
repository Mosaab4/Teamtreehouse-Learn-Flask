from peewee import *

db = SqliteDatabase('diary.db')

class Entry(Model):
    #content
    #timestamp

    class Meta:
        database = db

def menu_loop():
    """show the menu"""

def add_entry():
    """add an entry"""

def view_entries():
    """View previous entries"""

def delete_entry(entry):
    """Delete an entry"""


if __name__ =='__main__':
    menu_loop()

