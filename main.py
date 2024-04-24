import pathlib
import json
import os

FILE_BASE_NAME = 'contact-book.base'
file_base_to_path = pathlib.PurePath(os.getenv('HOME'), FILE_BASE_NAME)

WELCOME_TEXT = 'Welcome to you contact book!'
MENU_TEXT = '''Select on action (enter number) and press key Enter:
1. Add contact
2. Find contact
3. Show all contacts
4. Remove contact
5. Exit'''


class UnknownAction(Exception):
    pass


class NoVerifiedContactName(Exception):
    pass


class NoVerifiedPhoneNumber(Exception):
    pass


class ExitInMainMenu(Exception):
    pass


class ContactNotFound(Exception):
    pass


class Contact:
    count_objects = 0

    @staticmethod
    def get_count() -> int:
        return Contact.count_objects

    @staticmethod
    def validate_contact_name(contact_name: str, raise_error=True) -> bool:
        try:
            if not contact_name:
                raise NoVerifiedContactName
            else:
                return True
        except NoVerifiedContactName:
            if raise_error:
                print('Sorry, you contact name not valid')
                raise
            else:
                return False

    @staticmethod
    def validate_phone_number(phone_number: str, raise_error=True) -> bool:
        try:
            if not phone_number:
                raise NoVerifiedPhoneNumber
            else:
                return True
        except NoVerifiedPhoneNumber:
            if raise_error:
                print('Sorry, you phone number not valid')
                raise
            else:
                return False

    def __init__(self, phone_number: str, contact_name: str):
        Contact.validate_contact_name(contact_name=contact_name)
        Contact.validate_phone_number(phone_number=phone_number)
        self.phone_number = phone_number
        self.contact_name = contact_name
        Contact.count_objects += 1

    def __str__(self):
        return f'{self.phone_number}:{self.contact_name}'

    def __del__(self):
        Contact.count_objects -= 1


def add_contact() -> Contact:
    contact_name = input('please, input contact name> ')
    phone_number = input(f'please, input phone number for {contact_name}> ')

    return Contact(phone_number=phone_number,
                   contact_name=contact_name)


def print_contacts(dict_contacts: dict) -> None:
    cnt_rows=0
    if dict_contacts:
        for contact_phone in dict_contacts:
            cnt_rows += 1
            if cnt_rows % 10 == 0:
                input('Press any key to continue...')
            print(dict_contacts[contact_phone])
    else:
        print('contact book is empty!')


def find_contact(dict_contacts: dict, phone_number: str) -> Contact | None:
    return dict_contacts.get(phone_number)


def main():
    action = 0
    contacts = {}

    #download_base

    print(WELCOME_TEXT)

    while True:
        print(MENU_TEXT)
        try:
            action = int(input('Select action and press the key Enter>> '))
            if action not in (1, 2, 3, 4, 5):
                raise UnknownAction

            if action == 5:
                break

            while True:
                if action == 1:
                    try:
                        contact = add_contact()
                        contacts[contact.phone_number] = contact
                        raise ExitInMainMenu
                    except (NoVerifiedContactName, NoVerifiedPhoneNumber, ExitInMainMenu):
                        if input('Add another? ("Y" - Press any key / "N" - return main menu)>> ').upper() == 'N':
                            break
                if action == 2:
                    try:
                        contact = find_contact(dict_contacts=contacts,
                                               phone_number=input('Enter phone number for find>> '))
                        if not contact:
                            raise ContactNotFound
                        else:
                            print_contacts({contact.phone_number: contact})
                            if input('repeat find? ("Y" - Press any key / "N" - return main menu)>> ').upper() == 'N':
                                break
                    except ContactNotFound:
                        if input('Sorry, contact not found. Repeat?'
                                 '("Y" - Press any key / "N" - return main menu)>> ').upper() == 'N':
                            break

                if action == 3:
                    print_contacts(contacts)
                    input('Press any key to continue...')
                    break

                if action == 4:
                    try:
                        contact = find_contact(dict_contacts=contacts,
                                               phone_number=input('Enter phone number for remove>> '))
                        if not contact:
                            raise ContactNotFound
                        else:
                            del contacts[contact.phone_number]
                            del contact
                            if input('repeat remove? ("Y" - Press any key / "N" - return main menu)>> ').upper() == 'N':
                                break
                    except ContactNotFound:
                        if input('Sorry, contact not found. Repeat?'
                                 '("Y" - Press any key / "N" - return main menu)>> ').upper() == 'N':
                            break

        except (UnknownAction, ValueError):
            if input('Sorry, you select unknown action. Repeat?'
                     '("Y" - Press any key / "N" - exit)>> ').upper() == 'N':
                break


if __name__ == '__main__':
    main()
