#!/usr/bin/env python3
from peewee import *

from collections import OrderedDict
import datetime
import sys #to capture text with new line , not to exit when Enter
import os




db = SqliteDatabase('diary.db')


class Entry(Model):
    content = TextField()
    #var char field had to have max_length
    timestamp = DateTimeField(default = datetime.datetime.now)
    #now not now() because default see that it's a function
    class Meta:
        database = db

def initialize():
    """create the database and the table if they don't exist"""
    db.connect()
    db.create_tables([Entry], safe=True)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def menu_loop():
    """show the menu"""
    choice = None 

    while choice != 'q':
        clear()

        print("Enter 'q' to quit.")

        for key,value in menu.items():
            print('{}) {}'.format(key,value.__doc__))
            
        
        choice = raw_input('Action: ').lower().strip() #lowercase and remove spaces from the input
        
        if choice in menu:
            clear()
            menu[choice]()


def add_entry():
    """add an entry"""

    print("Enter your entry. Press ctrl+d when finished")
    data = sys.stdin.read().strip() #read text with new lines , and strip spaces from sides

    if data :
        if raw_input('Save entry? [Yn]').lower() != 'n':
            Entry.create(content = data )
            print('Saved successfully!')


def view_entries(search_query = None):
    """View previous entries"""
    entries = Entry.select().order_by(Entry.timestamp.desc())

    if search_query :
        entries = entries.where(Entry.content.contains(search_query))

    for entry in entries:
        timestamp = entry.timestamp.strftime('%A %B %d, %Y %I:%M%p')#day month number , year hour minute am/pm

        clear()
        
        print(timestamp)
        print('=' *len(timestamp))
        print(entry.content)
        
        print('\n\n' + '='*len(timestamp))

        print('n) next entry')
        print('d) delete entry')
        print('q) return to main menu')

        next_action = raw_input('Action: [Ndq]').lower().strip()

        if next_action == 'q':
            break
        elif next_action == 'd':
            delete_entry(entry)


def search_entries():
    """Search entries for a string"""
    view_entries(raw_input('Search query: '))

def delete_entry(entry):
    """Delete an entry"""
    if raw_input('Are you sure? [yN] ').lower() == 'y':
        entry.delete_instance()
        print("Entry Deleted!")


menu = OrderedDict([
    ('a',add_entry),
    ('v',view_entries),
    ('s',search_entries)
])

if __name__ =='__main__':
    initialize()
    menu_loop()


