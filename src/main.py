from storage import save_data, load_data
from colorama import Fore, Style, init
import os
import prompt
from addressbook.book import (
    parse_input, add_contact, 
    change_contact, delete_contact,
    show_phone, show_all, add_birthday,
    contact_birthday, upcoming_birthdays
)

def print_welcome():
    if os.name == 'nt':
        os.system('cls')
    else:
        # For Unix-like systems (Linux, macOS)
        os.system('clear')
    cobra = r"""

                /^\/^\
                _|__|  O|
        \/     /~     \_/ \
        \____|__________/  \
                \_______      \
                        `\     \                 \
                        |     |                  \
                        /      /                    \
                        /     /                       \\
                    /      /                         \ \
                    /     /                            \  \
                /     /             _----_            \   \
                /     /           _-~      ~-_         |   |
                (      (        _-~    _--_    ~-_     _/   |
                \      ~-____-~    _-~    ~-_    ~-_-~    /
                    ~-_           _-~          ~-_       _-~
                    ~--______-~                ~-___-~
        """
    print(f"{Fore.GREEN}{Style.BRIGHT}{cobra}")
    print(" "*18, f" {Fore.GREEN}{Style.BRIGHT}Welcome to the Assistant Bot!")
    print(" ")
    print(" "*15, f" {Fore.GREEN}{Style.BRIGHT}Type '{Fore.RED}help{Fore.GREEN}' for a list of commands.")
    print(" ")

# Assistant Bot for Address Book Management
def main():
    init(autoreset=True) # Initialize colorama for colored output
    print_welcome() 
    # Load the address book data from file or create a new one
    book = load_data()

    while True:
        user_input = prompt.session.prompt("Enter a command >>> ", completer=prompt.completer, complete_while_typing=False)
        if not user_input.strip():
            print("Please enter a command.")
            continue
        command, *args = parse_input(user_input)

        if command in ["close", "exit", "quit"]:
            save_data(book)
            print("Data saved. Exiting the assistant bot.")
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add-contact":
            print(add_contact(args, book))
        elif command == "change-contact":
            print(change_contact(args, book))
        elif command == "delete-contact":
            print(delete_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            show_all(book)
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(contact_birthday(args, book))
        elif command == "birthdays":
            upcoming_birthdays(args, book)
        elif command == "save":
            book.save(args)
            print("Data saved.")
        elif command == "load":
            book = book.load(args)
            print("Data loaded.")
        elif command == "help":
           print(prompt.get_help())
        elif command == "about":
            print(f"{Fore.LIGHTBLACK_EX}Produced by Serpent Rise Team©")
            #TODO
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()


