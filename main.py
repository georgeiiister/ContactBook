import datetime
import os
import pathlib



class ExceptionContactBook(Exception):
    pass


class UnknownAction(ExceptionContactBook):
    pass


class NoVerifiedContactName(ExceptionContactBook):
    pass


class NoneContactName(NoVerifiedContactName):
    pass


class NoVerifiedPhoneNumber(ExceptionContactBook):
    pass


class NonePhoneNumber(NoVerifiedPhoneNumber):
    pass


class NoVerifiedPhoneNumberOnOnlyDigits(NoVerifiedPhoneNumber):
    pass


class ExitInMainMenu(ExceptionContactBook):
    pass


class ContactNotFound(ExceptionContactBook):
    pass


class FileBaseNotFound(ExceptionContactBook):
    pass


class FileBaseNotCreated(ExceptionContactBook):
    pass


class ContactExistInFileDBase(ExceptionContactBook):
    pass


class Contact(object):
    __count_objects = 0
    __mask_date_time_creation = '%d.%m.%Y %H:%M:%S'

    @classmethod
    def mask_date_time_creation(cls):
        return cls.__mask_date_time_creation

    @classmethod
    def count(cls) -> int:
        return cls.__count_objects

    @classmethod
    def validate_contact_name(cls,
                              contact_name: str,
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

    @classmethod
    def validate_phone_number(cls,
                              phone_number: str,
                              raise_error=True) -> bool:
        try:

            if not phone_number:
                raise NoVerifiedPhoneNumber

            _ = phone_number[1:] if phone_number.startswith('+') else phone_number
            import string
            if tuple(filter(lambda i: not (i in string.digits), _)):
                raise NoVerifiedPhoneNumberOnOnlyDigits
            return True

        except (NoVerifiedPhoneNumber, NoVerifiedPhoneNumberOnOnlyDigits, NonePhoneNumber):
            if raise_error:
                print('Sorry, you phone number not valid')
                raise
            else:
                return False

    def __init__(self,
                 phone_number: str,
                 contact_name: str,
                 date_time_creation_contact: datetime.datetime,
                 validate=True):

        if validate:
            Contact.validate_contact_name(contact_name=contact_name)
            Contact.validate_phone_number(phone_number=phone_number)

        self.__phone_number = phone_number
        self.__contact_name = contact_name
        self.__date_time_creation_contact = date_time_creation_contact

        Contact.__count_objects += 1

    def __str__(self):
        return f'{self.__contact_name} {self.__phone_number}'

    def __repr__(self):
        return (f'Contact(contact_name={self.contact_name}, phone_number={self.phone_number}, '
                f'date_time_creation_contact={self.get_date_time_creation_contact()})')

    def __del__(self):
        Contact.__count_objects -= 1

    def __len__(self):
        return len(self.phone_number)

    def __bool__(self):
        return bool(self.phone_number)

    def __eq__(self, other):
        return self.phone_number == other.phone_number

    @property
    def contact_name(self):
        return self.__contact_name

    @property
    def phone_number(self):
        return self.__phone_number

    def get_date_time_creation_contact(self) -> datetime.datetime:
        return self.__date_time_creation_contact

    def get_str_date_time_creation_contact(self) -> str:
        return self.get_date_time_creation_contact().strftime(Contact.mask_date_time_creation())

    def get_format_to_dbase(self) -> str:
        return (f'{self.phone_number};{self.contact_name};'
                f'{self.get_str_date_time_creation_contact()}')

    def get_dict(self) -> dict:
        return {self.phone_number: {'phone_number': self.phone_number,
                                    'contact_name': self.contact_name}}


def sorted_dict_contacts(dict_contacts: dict) -> list:
    list_contacts = sorted(dict_contacts.items(), key=lambda i: i[1].contact_name)
    return list_contacts


def decorator_args_kwargs_print(func):
    def wrapper(*args, **kwargs):
        print(*args, sep='\n')
        print(*kwargs.items(), sep='\n')
        return func(*args, **kwargs)

    return wrapper


def find_contact_by_phone(dict_contacts: dict,
                 phone_number: str) -> Contact | None:
    return dict_contacts.get(phone_number)


def create_contact() -> Contact:
    contact_name = input('Please, input contact name>> ')
    Contact.validate_contact_name(contact_name=contact_name)

    phone_number = input(f'Please, input phone number for {contact_name}>> ')
    Contact.validate_phone_number(phone_number=phone_number)

    return Contact(phone_number=phone_number,
                   contact_name=contact_name,
                   date_time_creation_contact=datetime.datetime.now(),
                   validate=False)


def edit_contact(contact: Contact) -> Contact:
    contact_name = input(f'Please, input new contact name for "{contact.contact_name}">> ')
    phone_number = contact.phone_number
    new_contact = Contact(phone_number=phone_number,
                          contact_name=contact_name,
                          date_time_creation_contact=datetime.datetime.now())

    del contact
    return new_contact


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

        if cnt_rows % mark_print != 0:
            input('Output is finish. Press any key to continue...')
    else:
        print('Contact book is empty!')


def create_file_base(path_to_file_base: pathlib.Path) -> bool | None:
    with open(path_to_file_base, 'w'):
        pass
    return True


def full_download_dbase(path_to_file_base=pathlib.Path(os.getenv('HOME') + os.sep + 'contact-book.dbase')) -> tuple:
    base_dict = {}

    try:
        if not pathlib.Path(path_to_file_base).exists():
            raise FileBaseNotFound
    except FileBaseNotFound:
        if not create_file_base(path_to_file_base=path_to_file_base):
            return tuple()

    cnt_rows = 0
    mask = Contact.mask_date_time_creation()

    with open(path_to_file_base, 'r') as fb:
        len_fb = sum(1 for _ in fb)
        mark_print = get_mark_print(len_fb)  # count rows in file

    with open(path_to_file_base, 'r') as fb:
        for rec in fb:
            contact = rec.rstrip('\n').split(';')
            base_dict[contact[0]] = Contact(phone_number=contact[0],
                                            contact_name=contact[1],
                                            date_time_creation_contact=datetime.datetime.strptime(contact[2], mask),
                                            validate=False)

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
                 '2. Find contact by phone number',
                 '3. Show all contacts',
                 '4. Remove contact',
                 '5. Edit contact',
                 '6. Backup contact book',
                 '7. Save contact book to disk',
                 '8. Exit',)

    menu_text = '\n'.join(menu_text)

    print(welcome_text)

    contacts, cur_path_to_file_base = full_download_dbase()

    assert cur_path_to_file_base  # check file db

    contacts_change = False

    while True:

        print(menu_text)  # main menu

        try:
            action = int(input('Select action and press the key Enter>> '))
            if action not in (range(1, 9)):
                raise UnknownAction

            if action == 8:
                if contacts_change:
                    if not input('You have made changes. Save to disk? '
                                 '("Y" - Press any key / "N" - exit without saving)>> ').upper() == 'N':
                        full_upload_dbase(dbase_dict=contacts, path_to_file_base=cur_path_to_file_base)
                break

            while True:
                if action == 1:
                    try:
                        contact = create_contact()

                        find_obj = find_contact_by_phone(dict_contacts=contacts, phone_number=contact.phone_number)

                        if find_obj is None:
                            contacts[contact.phone_number] = contact
                            contacts_change = True
                            raise ExitInMainMenu
                        else:
                            raise ContactExistInFileDBase
                    except (NoVerifiedContactName, NoVerifiedPhoneNumber, ExitInMainMenu):
                        if input('Add another? ("Y" - Press any key / "N" - return main menu)>> ').upper() == 'N':
                            break
                    except ContactExistInFileDBase:
                        del contact
                        if input(f'Contact exist! {find_obj} {find_obj.get_str_date_time_creation_contact()} '
                                 f'Repeat another? ("Y" - Press any key / "N" - return main menu)>> '
                                 ).upper() == 'N':
                            break

                if action == 2:
                    try:
                        contact = find_contact_by_phone_phone(dict_contacts=contacts,
                                               phone_number=input('Enter phone number for find>> '))
                        if not contact:
                            raise ContactNotFound
                        else:
                            print_contacts({contact.phone_number: contact})
                            if input('Repeat find? ("Y" - Press any key / "N" - return main menu)>> ').upper() == 'N':
                                break
                    except ContactNotFound:
                        if input('Sorry, contact is not found. Repeat?'
                                 '("Y" - Press any key / "N" - return main menu)>> ').upper() == 'N':
                            break

                if action == 3:
                    print_contacts(contacts)
                    break

                if action == 4:
                    try:
                        contact = find_contact_by_phone(dict_contacts=contacts,
                                               phone_number=input('Enter phone number for remove>> '))
                        if not contact:
                            raise ContactNotFound
                        else:
                            print(f'This contact {contact} will be deleted!')
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
                    try:
                        contact = find_contact_by_phone(dict_contacts=contacts,
                                               phone_number=input('Enter phone number for edit>> '))
                        if not contact:
                            raise ContactNotFound
                        else:
                            contact = edit_contact(contact=contact)
                            contacts[contact.phone_number] = contact
                            contacts_change = True

                            if input('Repeat edit? ("Y" - Press any key / "N" - return main menu)>> ').upper() == 'N':
                                break

                    except ContactNotFound:
                        if input('Sorry, contact not found. Repeat?'
                                 '("Y" - Press any key / "N" - return main menu)>> ').upper() == 'N':
                            break

                if action == 6:
                    full_backup_dbase(dbase_dict=contacts)
                    input('Backup done...')
                    break

                if action == 7:
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
