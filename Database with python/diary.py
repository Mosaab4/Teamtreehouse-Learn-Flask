#!/usr/bin/env python3
from peewee import *

from collections import OrderedDict
import datetime
import sys #to capture text with new line , not to exit when Enter



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


def menu_loop():
    """show the menu"""
    choice = None 

    while choice != 'q':
        print("Enter 'q' to quit.")

        for key,value in menu.items():
            print('{}) {}'.format(key,value.__doc__))
            
        
        choice = raw_input('Action: ').lower().strip() #lowercase and remove spaces from the input
        
        if choice in menu:
            menu[choice]()


def add_entry():
    """add an entry"""

def view_entries():
    """View previous entries"""

def delete_entry(entry):
    """Delete an entry"""


menu = OrderedDict([
    ('a',add_entry),
    ('v',view_entries)
])

if __name__ =='__main__':
    initialize()
    menu_loop()

