from addressbook.models import Name, Phone, Birthday
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        if self.find_phone(phone):
            print(f"Phone {phone} already exists for {self.name.value}. Not adding.")
            return
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        phone_to_remove = Phone(phone)
        self.phones = [p for p in self.phones if p.value != phone_to_remove.value]

    def find_phone(self, phone):
        phone = phone.strip()
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def edit_phone(self, old_phone, new_phone):
        phone_obj = self.find_phone(old_phone)
        if phone_obj:
            phone_obj.value = Phone(new_phone).value
        else:
            raise ValueError("Phone number not found.")

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones_str = '; '.join(p.value for p in self.phones)
        birthday_str = self.birthday.value.strftime('%d.%m.%Y') if self.birthday else 'Not set'
        return f"Contact name: {self.name.value}, phones: {phones_str}, Birthday: {birthday_str}"
