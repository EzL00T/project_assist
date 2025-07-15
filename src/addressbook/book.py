from collections import UserDict
from .record import Record
from datetime import datetime, timedelta
import pickle
from .models import Birthday

class AddressBook(UserDict):
    def add_record(self, record):
        if not isinstance(record, Record):
            raise TypeError("Only Record instances can be added.")
        self.data[record.name.value] = record
    def find(self, name):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Name must be a non-empty string.")
        if name.strip() not in self.data:
            return None
        return self.data[name.strip()]
    def delete(self, name):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Name must be a non-empty string.")
        name = name.strip()
        if name in self.data:
            del self.data[name]
        else:
            raise KeyError(f"Contact '{name}' not found.")   
    def get_upcoming_birthday(self, period_days=7):
        today = datetime.today()
        upcoming_birthdays = []

        for user in self.data.values():
            if not user.birthday:
                continue
            # Ensure birthday is a datetime object
            if not isinstance(user.birthday, Birthday):
                raise ValueError("Birthday must be an instance of Birthday class.")
            if not user.birthday.value:
                continue
            # Calculate the next birthday
            birthday = user.birthday.value
            birthday_this_year = birthday.replace(year=today.year)  
            # if birthday was before today, set it to next year
            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)

            days_until_birthday = (birthday_this_year - today).days
            if days_until_birthday <= period_days:
                if datetime.weekday(birthday_this_year) == 5:  # if birthday is on Saturday, move it to Monday
                    birthday_this_year += timedelta(days=2)
                elif datetime.weekday(birthday_this_year) == 6:  # if birthday is on Sunday, move it to Monday
                    birthday_this_year += timedelta(days=1)
                upcoming_birthdays.append(user)
        return upcoming_birthdays
    
    def save(self, args):
        filename = None
        if len(args) > 0:
            filename = args[0]
        if not filename:
            filename = "addressbook.pkl"
        with open(filename, "wb") as f:
            pickle.dump(self, f)

    def load(self, args):
        if len(args) >0:
            filename = args[0]
        else:
            filename = "addressbook.pkl"
        try:
            with open(filename, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            create_new = input("No saved data found. Start with an empty address book? [Y/N]")
            if create_new.lower() == 'y':
                return AddressBook()
            else:
                print("Staying with the current address book.")
                return self

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return """Invalid input. Format: 
            add <name> <phone_number>
            change <name> <old_phone> <new_phone>
            phone <name>
            add-birthday <name> <DD.MM.YYYY>
            show-birthday <name>
            birthdays
            all"""
        except IndexError: # not used now
            return "Invalid input. Format: phone <name>."
        except KeyError: # not used now
            return "Contact not found."
        except Exception as e:
            return f"An unexpected error occurred: {e}"
    return inner

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if len(args) > 1:
        for phone in args[1:]:
            record.add_phone(phone)
    return message

@input_error
def delete_contact(args, book: AddressBook):
    name = None
    if len(args) == 0:
        return "Please provide a name to delete."
    name, *_ = args
    if not name:
        return "Please provide a name to delete."
    try:
        book.delete(name)
        return f"Contact '{name}' deleted."
    except KeyError as e:
        return str(e)

@input_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone = args
    record = book.find(name)
    if record is None:
        return "Contact not found."
    user_phone = record.find_phone(old_phone)
    if user_phone is None:
        return "Phone number not found."
    record.edit_phone(old_phone, new_phone)
    return "Contact updated."

@input_error
def show_phone(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record is None:
        return "Contact not found."
    return record

@input_error
def show_all(book: AddressBook):
    if not book.data:
        return "No contacts available."
    result = ["📗 All contacts: 📗\n"]
    for name, record in book.data.items():
        result.append(str(record))
    return "\n".join(result)

@input_error
def add_birthday(args, book: AddressBook):
    name, birthday = args
    record = book.find(name)
    if record is None:
        return "Contact not found."
    record.add_birthday(birthday)
    return "Birthday added."

@input_error
def contact_birthday(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record is None:
        return "Contact not found."
    if record.birthday is None:
        return "Birthday not set."
    birthday = record.birthday.value
    return f"{record.name.value}'s birthday is on {birthday.strftime('%d.%m.%Y')}."

@input_error
def upcoming_birthdays(args, book: AddressBook):
    days = 7  # Default period for upcoming birthdays
    if len(args) > 0:
        days = int(args[0])
    upcoming_birthdays = book.get_upcoming_birthday(days)
    if not upcoming_birthdays:
        return "No upcoming birthdays."
    result = ["🎉 Upcoming birthdays: 🎉"]
    for record in upcoming_birthdays:
        birthday = record.birthday.value
        result.append(f"{record.name.value}: {birthday.strftime('%d.%m')}")
    return "\n".join(result)