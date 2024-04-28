import os
import pathlib


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


class FileBaseNotFound(Exception):
    pass


class Contact:
    count_objects = 0

    @staticmethod
    def get_count() -> int:
        return Contact.count_objects

    @staticmethod
    def validate_contact_name(contact_name: str,
                              raise_error=True) -> bool:
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
    def validate_phone_number(phone_number: str,
                              raise_error=True) -> bool:
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

    def get_format_to_base(self):
        return f'{self.phone_number}:{self.contact_name}'


    def __init__(self, phone_number: str,
                 contact_name: str):

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
    contact_name = input('Please, input contact name>> ')
    phone_number = input(f'Please, input phone number for {contact_name}>> ')

    return Contact(phone_number=phone_number,
                   contact_name=contact_name)


def print_contacts(dict_contacts: dict) -> None:
    cnt_rows = 0
    if dict_contacts:
        for contact_phone in dict_contacts:
            cnt_rows += 1
            if cnt_rows % 10 == 0:
                input('Press any key to continue...')
            print(dict_contacts[contact_phone])
    else:
        print('Contact book is empty!')


def find_contact(dict_contacts: dict,
                 phone_number: str) -> Contact | None:
    return dict_contacts.get(phone_number)


def full_download_base(path_to_file_base=pathlib.Path(os.getenv('HOME') + os.sep + 'contact-book.base')) -> tuple:
    contact = []
    base_dict = {}

    try:
        if not pathlib.Path(path_to_file_base):
            raise FileBaseNotFound
    except FileBaseNotFound:
        return tuple()

    with open(path_to_file_base, 'r') as fb:
        for rec in fb:
            contact = rec.rstrip('\n').split(':')
            base_dict[contact[0]] = Contact(phone_number=contact[0], contact_name=contact[1])

    return base_dict, path_to_file_base


def full_upload_base(base_dict: dict, path_to_file_base: pathlib.Path) -> None:
    try:
        if not pathlib.Path(path_to_file_base):
            raise FileBaseNotFound
    except FileBaseNotFound:
        raise

    with open(path_to_file_base, 'w') as fb:
        for phone_number, contact in base_dict.items():
            fb.write(contact.get_format_to_base()+'\n')


def main():
    welcome_text = 'Welcome to you contact book!'

    menu_text = '''Select on action (enter number) and press key Enter:
    1. Add contact
    2. Find contact
    3. Show all contacts
    4. Remove contact
    5. Exit'''

    action = 0
    contacts, cur_path_to_file_base = full_download_base()

    print(welcome_text)

    while True:
        print(menu_text)
        try:
            action = int(input('Select action and press the key Enter>> '))
            if action not in (1, 2, 3, 4, 5):
                raise UnknownAction

            if action == 5:
                if contacts:
                    full_upload_base(base_dict=contacts, path_to_file_base=cur_path_to_file_base)
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
                            if input('Repeat find? ("Y" - Press any key / "N" - return main menu)>> ').upper() == 'N':
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
                            if input('Repeat remove? ("Y" - Press any key / "N" - return main menu)>> ').upper() == 'N':
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
