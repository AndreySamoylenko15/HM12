from collections import UserDict
from datetime import datetime
import pickle
from typing import List
import cmd 
from pathlib import Path

class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value
    
    @property
    def value(self):
        return self.__value


    @value.setter
    def value(self, value):
        self.__value = value

    
    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Name cannot be empty")
        super().__init__(value)

class Phone(Field):
    @Field.value.setter
    
    def is_valid_phone(self, value):
        """return boolean from check"""
        return value.isdigit() and len(value) == 10
    def validate(self, value):
        if len(value) != 10 or not value.isdigit():
            raise ValueError('Phone should be 10 digits')
            super().validate(value) 
            self.validate(value)
            super().__init__(value)
   
class Birthday(Field):
    @Field.value.setter
    
    def value(self, value: str):
        self.__value = datetime.strptime(value, '%Y.%m.%d').date()
    
class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        if birthday:
            self.birthday = Birthday(birthday)

    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
    
    def is_valid_phone(self, value):
        """return boolean from check"""
        return value.isdigit() and len(value) == 10
    
    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
    
    def add_phone(self, phone_number: str):
        phone = Phone(phone_number)
        phone.validate(phone_number)
        if phone not in self.phones:
            self.phones.append(phone)


    def find_phone(self, phone_number: str):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
    
    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                return
        raise ValueError(f"Phone number '{old_phone}' not found")
    def remove_phone(self, phone):
        for record_phone in self.phones:
            try:
                record_phone.value == phone
                self.phones.remove(record_phone)
                return True
            except ValueError:
                return f'{phone} does not exist'
             
    def days_to_birthday(self):
        if not self.birthday:
                return -1

        today = datetime.now().date()
        next_birthday = datetime.strptime(self.birthday.value, "%Y-%m-%d").date().replace(year=today.year)
        if today > next_birthday:
            next_birthday = next_birthday.replace(year=today.year + 1)

        days_until_birthday = (next_birthday - today).days
        return days_until_birthday

    
class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record
    
    def find(self, name):
        if name in self.data:
            return self.data[name]
        else:
            return None
    def delete(self, name):
        if name in self.data:
            del self.data[name]
    def iterator(self, item_number):
        counter = 0
        result = ''
        for item, record in self.data.items():
            result += f'{item}: {record}'
            counter += 1
            if counter >= item_number:
                yield result
                counter = 0
                result = ''

    def dump(self):
        with open(self.file, "wb") as file:
            pickle.dump((self.record_id, dict(self.data)), file)

    def load(self):
        if not self.file.exists():
            return
        with open(self.file, "rb") as file:
            self.record_id, data = pickle.load(file)
            self.data.update(data)

    def find_by_term(self, term: str) -> List[Record]:
        matching_records = []

        # Check if the term matches any phone number
        for record in self.data.values():
            for phone in record.phones:
                if term in phone.value:
                    matching_records.append(record)
        # Check if the term matches any contact name
        matching_records.extend(
            record for record in self.data.values() if term.lower() in record.name.value.lower()
        )
        return matching_records

    def find(self, term):
            matching_records = self.find_by_term(term)
            if matching_records:
                return matching_records
            else:
                return None
class Controller(cmd.Cmd):
    def __init__(self):
        super().__init__()
        self.book = AddressBook
        self.prompt = ">>>>>"
        self.intro = "Ласкаво просимо до Адресної Книги"

    def exit(self, arg):
        self.book.dump()
        print("Вихід...")
        return True
    def save(self, arg):
        self.book.dump()
        print("Адресна книга збережена!")
    def load(self, arg):
        self.book.load()
        print("Адресна книга відновлена")

if __name__ == '__main__':

    controller = Controller()
    controller.cmdloop()

    
    phone_field = Phone("1234567890")
    print(phone_field.value)  
    try:
        phone_field.value = "995-604-821"  
    except ValueError as e:
        print(e)
    birthday_field = Birthday("1993-12-15")
    print(birthday_field.value)  
    try:
        birthday_field.value = "1993/12/15"  
    except ValueError as e:
        print(e)
    book = AddressBook()
      