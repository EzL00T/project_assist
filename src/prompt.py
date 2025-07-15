from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import InMemoryHistory

# Commands for autocompletion
commands = ['add-contact', 
            'change-phone', 
            'change-contact', 
            'delete-contact',
            'phone', 
            'add-birthday', 
            'show-birthday', 
            'birthdays', 
            'all', 
            'save',
            'load',
            'close',
            'exit', 
            'quit',
            'help',
            'hello'
            ]

completer = WordCompleter(commands, ignore_case=True)

# History in memory
history = InMemoryHistory()

session = PromptSession(history=history)


def get_help():
    return (
        "Available commands:\n"
        "add-contact <name> <phone> - add a contact\n"
        "change-contact <name> <old_phone> <new_phone> - change a phone number\n"
        "delete-contact <name> - delete a contact\n"
        "phone <name> - show phone numbers\n"
        "add-birthday <name> <DD.MM.YYYY> - add a birthday\n"
        "show-birthday <name> - show birthday\n"
        "birthdays [days] - birthdays in the coming days\n"
        "all - show all contacts\n"
        "save [filename] - save the address book\n"
        "load [filename] - load the address book\n"
        "close/exit/quit - exit\n"
        "help - show this help\n"
        "hello - greeting"
    )
