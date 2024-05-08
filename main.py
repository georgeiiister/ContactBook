import datetime
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


class FileBaseNotCreated(Exception):
    pass


class Contact:
    count_objects = 0
    mask_date_time_creation = '%d.%m.%Y %H:%M:%S'

    @staticmethod
    def get_mask_date_time_creation():
        return Contact.mask_date_time_creation

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

    def get_format_to_dbase(self) -> str:
        return (f'{self.phone_number};{self.contact_name};'
                f'{self.date_time_creation_contact.strftime(Contact.get_mask_date_time_creation())}')

    def get_dict(self) -> dict:
        return {self.phone_number: {'phone_number': self.phone_number, 'contact_name': self.contact_name}}

    def get_contact_name(self):
        return self.contact_name

    def get_phone_number(self):
        return self.phone_number

    def get_date_time_creation_contact(self) -> datetime.datetime:
        return self.date_time_creation_contact

    def __init__(self, phone_number: str,
                 contact_name: str,
                 date_time_creation_contact: datetime.datetime):

        Contact.validate_contact_name(contact_name=contact_name)
        Contact.validate_phone_number(phone_number=phone_number)

        self.phone_number = phone_number
        self.contact_name = contact_name
        self.date_time_creation_contact = date_time_creation_contact

        Contact.count_objects += 1

    def __str__(self):
        return f'{self.contact_name} {self.phone_number}'

    def __repr__(self):
        return (f'Contact(contact_name={self.get_contact_name()}, phone_number={self.phone_number}, '
                f'date_time_creation_contact={self.date_time_creation_contact})')

    def __del__(self):
        Contact.count_objects -= 1

    def __len__(self):
        return len(self.get_phone_number())

    def __bool__(self):
        return bool(self.get_phone_number())


def sorted_dict_contacts(dict_contacts: dict) -> list:
    list_contacts = sorted(dict_contacts.items(), key=lambda i: i[1].get_contact_name())
    return list_contacts


def decorator_args_kwargs_print(func):
    def wrapper(*args, **kwargs):
        print(*args, sep='\n')
        print(*kwargs.items(), sep='\n')
        return func(*args, **kwargs)

    return wrapper


def add_contact() -> Contact:
    contact_name = input('Please, input contact name>> ')
    phone_number = input(f'Please, input phone number for {contact_name}>> ')

    return Contact(phone_number=phone_number,
                   contact_name=contact_name,
                   date_time_creation_contact=datetime.datetime.now())


def get_mark_print(len_obj: int, num_of_lines: int = 10) -> int:
    if len_obj <= num_of_lines:
        mark_print = 100
    else:
        mark_print = num_of_lines

    return 1 if mark_print == 0 else mark_print


def print_contacts(dict_contacts: dict) -> None:
    cnt_rows = 0
    if dict_contacts:
        list_contacts = sorted_dict_contacts(dict_contacts=dict_contacts)

        mark_print = get_mark_print(len_obj=len(list_contacts))

        for _, contact in list_contacts:
            print(contact)
            cnt_rows += 1
            if cnt_rows % mark_print == 0:
                input('Press any key to continue...')
    else:
        print('Contact book is empty!')


def find_contact(dict_contacts: dict,
                 phone_number: str) -> Contact | None:
    return dict_contacts.get(phone_number)


def create_file_base(path_to_file_base: pathlib.Path) -> bool | None:
    with open(path_to_file_base, 'w') as fb:
        pass
    return True


def full_download_dbase(path_to_file_base=pathlib.Path(os.getenv('HOME') + os.sep + 'contact-book.dbase')) -> tuple:
    contact = []
    base_dict = {}

    try:
        if not pathlib.Path(path_to_file_base).exists():
            raise FileBaseNotFound
    except FileBaseNotFound:
        if not create_file_base(path_to_file_base=path_to_file_base):
            return tuple()

    cnt_rows = 0
    cmask = Contact.get_mask_date_time_creation()

    with open(path_to_file_base, 'r') as fb:
        len_fb = len_obj=sum(1 for i in fb)
        mark_print = get_mark_print(len_fb)  # count rows in file

    with open(path_to_file_base, 'r') as fb:
        for rec in fb:
            contact = rec.rstrip('\n').split(';')
            base_dict[contact[0]] = Contact(phone_number=contact[0],
                                            contact_name=contact[1],
                                            date_time_creation_contact=datetime.datetime.strptime(contact[2], cmask))

            cnt_rows += 1
            if (len_fb // mark_print) >= 2 and cnt_rows % mark_print == 0:
                print(f'download {cnt_rows} rows')

    if cnt_rows > 0:
        print(f'total download {cnt_rows} rows')

    return base_dict, path_to_file_base


# @decorator_args_kwargs_print
def full_upload_dbase(dbase_dict: dict, path_to_file_base: pathlib.Path) -> None:
    try:
        if not pathlib.Path(path_to_file_base).exists():
            raise FileBaseNotFound
    except FileBaseNotFound:
        if not create_file_base(path_to_file_base=path_to_file_base):
            raise FileBaseNotCreated

    cnt_rows = 0
    len_dbase_dict = len(dbase_dict)
    mark_print = get_mark_print(len_obj=len_dbase_dict)

    with open(path_to_file_base, 'w') as fb:
        for _, contact in dbase_dict.items():
            fb.write(contact.get_format_to_dbase() + '\n')
            cnt_rows += 1
            if (len_dbase_dict // mark_print) >= 2 and cnt_rows % mark_print == 0:
                print(f'upload {cnt_rows} rows...')

    if cnt_rows > 0:
        print(f'total upload {cnt_rows} rows...')


def full_backup_dbase(dbase_dict: dict,
                      path_to_file_base=pathlib.Path(os.getenv('HOME') + os.sep + 'contact-book.backup')) -> None:
    import json
    try:
        if not pathlib.Path(path_to_file_base).exists():
            raise FileBaseNotFound
    except FileBaseNotFound:
        if not create_file_base(path_to_file_base=path_to_file_base):
            raise FileBaseNotCreated

    dict2json = {}

    cnt_rows = 0
    len_dbase_dict = len(dbase_dict)
    mark_print = get_mark_print(len_obj=len_dbase_dict)

    for _, contact in dbase_dict.items():
        dict2json = {**dict2json, **contact.get_dict()}
        cnt_rows += 1
        if (len_dbase_dict // mark_print) >= 2 and cnt_rows % mark_print == 0:
            print(f'prepared {cnt_rows} rows...')

    if cnt_rows > 0:
        print(f'total prepared {cnt_rows} rows...')

    with open(path_to_file_base, 'w') as fb:
        json.dump(dict2json, fb, indent=4)


def main():
    welcome_text = 'Welcome to you contact book!'

    menu_text = ('Select on action (enter number) and press key Enter:',
                 '1. Add contact',
                 '2. Find contact',
                 '3. Show all contacts',
                 '4. Remove contact',
                 '5. Backup contact book',
                 '6. Save contact book to disk',
                 '7. Exit')

    menu_text = '\n'.join(menu_text)

    print(welcome_text)

    action = 0
    contacts, cur_path_to_file_base = full_download_dbase()
    contacts_change = False

    while True:
        print(menu_text)
        try:
            action = int(input('Select action and press the key Enter>> '))
            if action not in (1, 2, 3, 4, 5, 6, 7):
                raise UnknownAction

            if action == 7:
                if contacts_change:
                    if not input('You have made changes. Save to disk? '
                                 '("Y" - Press any key / "N" - exit without saving)>> ').upper() == 'N':
                        full_upload_dbase(dbase_dict=contacts, path_to_file_base=cur_path_to_file_base)
                break

            while True:
                if action == 1:
                    try:
                        contact = add_contact()
                        contacts[contact.phone_number] = contact
                        contacts_change = True
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
                            contacts_change = True
                            if input('Repeat remove? ("Y" - Press any key / "N" - return main menu)>> ').upper() == 'N':
                                break
                    except ContactNotFound:
                        if input('Sorry, contact not found. Repeat?'
                                 '("Y" - Press any key / "N" - return main menu)>> ').upper() == 'N':
                            break

                if action == 5:
                    full_backup_dbase(dbase_dict=contacts)
                    input('Backup done...')
                    break

                if action == 6:
                    if contacts_change:
                        full_upload_dbase(dbase_dict=contacts, path_to_file_base=cur_path_to_file_base)
                        contacts_change = False
                    else:
                        print('There were no changes!')
                    input('Press any key to continue...')
                    break

        except (UnknownAction, ValueError):
            if input('Sorry, you select unknown action. Repeat?'
                     '("Y" - Press any key / "N" - exit)>> ').upper() == 'N':
                break


if __name__ == '__main__':
    main()
