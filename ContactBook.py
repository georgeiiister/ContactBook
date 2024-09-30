import datetime
import os
import pathlib
import json


def get_tuning_value(tuning_name: str) -> (str, int):
    """function for getting tuning parameters for application"""
    tuning_dict: dict = dict(sep_in_dbase=';',
                             welcome_text='Welcome to you contact book!',
                             num_of_lines=10,
                             mark_print=100,
                             path_to_dbase=os.path.expanduser('~'),
                             path_to_dir='contact_book',
                             name_log='contact-book.log')

    if tuning_name == 'path_to_dbase':
        path_to_dir = f'{tuning_dict[tuning_name]}{os.sep}{tuning_dict["path_to_dir"]}'
        if not os.path.exists(path_to_dir):
            os.mkdir(path_to_dir)

        return path_to_dir

    return tuning_dict[tuning_name]


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

class DirBaseNotCreated(ExceptionContactBook):
    pass


class FileLogNotFound(ExceptionContactBook):
    pass


class FileLogNotCreated(ExceptionContactBook):
    pass


class ContactExistInFileDBase(ExceptionContactBook):
    pass


class Contact(object):
    __count_objects = 0
    __mask_date_time_creation = '%d.%m.%Y %H:%M:%S'

    @classmethod
    def mask_date_time_creation(cls) -> str:
        """This method return validate mask for date and time of object Contact"""
        return cls.__mask_date_time_creation

    @classmethod
    def count(cls) -> int:
        return cls.__count_objects

    def __del__(self):
        Contact.__count_objects -= 1

    @classmethod
    def validate_contact_name(cls,
                              contact_name: str,
                              raise_error=True) -> bool:
        """This function for validate contact name"""
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

            phone_number_without_plus = phone_number[1:] if phone_number.startswith('+') else phone_number

            import string
            if tuple(filter(lambda i: not (i in string.digits), phone_number_without_plus)):
                raise NoVerifiedPhoneNumberOnOnlyDigits
            return True

        except (NoVerifiedPhoneNumber, NoVerifiedPhoneNumberOnOnlyDigits, NonePhoneNumber):
            if raise_error:
                print(f'Sorry, you phone number not valid {phone_number}')
                raise
            else:
                return False

    __slots__ = ('__phone_number',
                 '__contact_name',
                 '__date_time_creation_contact',
                 '__count',)

    def __init__(self,
                 phone_number: str,
                 contact_name: str,
                 date_time_creation_contact=datetime.datetime.now(),
                 validate=True):

        if validate:
            Contact.validate_contact_name(contact_name=contact_name)
            Contact.validate_phone_number(phone_number=phone_number)

        self.__phone_number = phone_number
        self.__contact_name = contact_name
        self.__date_time_creation_contact = date_time_creation_contact
        self.__count = 0

        Contact.__count_objects += 1

    def __str__(self):
        return f'{self.__contact_name} {self.__phone_number}'

    def __repr__(self):
        return (f'Contact(contact_name={self.contact_name}, phone_number={self.phone_number}, '
                f'date_time_creation_contact={self.date_time_creation_contact})')

    def __del__(self):
        Contact.__count_objects -= 1

    def __eq__(self, other):
        return self.phone_number == other.phone_number

    @property
    def contact_name(self):
        return self.__contact_name

    @property
    def phone_number(self):
        return self.__phone_number

    @property
    def date_time_creation_contact(self) -> datetime.datetime:
        return self.__date_time_creation_contact

    @property
    def str_date_time_creation_contact(self) -> str:
        return self.date_time_creation_contact.strftime(Contact.mask_date_time_creation())

    @property
    def format_to_dbase(self) -> str:
        return (f'{self.phone_number};{self.contact_name};'
                f'{self.str_date_time_creation_contact}')

    @property
    def dict(self) -> dict:
        return {self.phone_number: {'phone_number': self.phone_number,
                                    'contact_name': self.contact_name,
                                    'date_time_creation_contact': self.str_date_time_creation_contact
                                    }
                }

    @property
    def tuple(self) -> tuple:
        return tuple(self.dict[self.phone_number].items())

    def __iter__(self):
        return self

    def __next__(self):
        contact = self.tuple

        if self.__count >= len(contact):
            raise StopIteration
        else:
            contact_item = contact[self.__count]
            self.__count += 1
            return contact_item

    @property
    def dict_with_object(self) -> dict:
        return {self.phone_number: self}


class ContactMr(Contact):
    @classmethod
    def title(cls):
        return 'Mr'

    def __init__(self,
                 phone_number: str,
                 contact_name: str,
                 date_time_creation_contact: datetime.datetime,
                 validate):
        super().__init__(phone_number=phone_number,
                         contact_name=contact_name,
                         date_time_creation_contact=date_time_creation_contact,
                         validate=validate
                         )


class ContactMs(Contact):
    @classmethod
    def title(cls):
        return 'Ms'

    def __init__(self,
                 phone_number: str,
                 contact_name: str,
                 date_time_creation_contact: datetime.datetime,
                 validate):
        super().__init__(phone_number=phone_number,
                         contact_name=contact_name,
                         date_time_creation_contact=date_time_creation_contact,
                         validate=validate
                         )


def get_eq(val1: str, val2: str):
    """case-insensitive search"""
    result = True if val1.lower() == val2.lower() else False

    if not result:
        eq_sym = {'ё': 'е',
                  't': 'т',
                  'e': 'е',
                  'k': 'к',
                  'a': 'а',
                  'm': 'м',
                  'b': 'в',
                  'c': 'с',
                  'h': 'н',
                  'p': 'р',
                  'o': 'о'}

        if ''.join([eq_sym.get(i, i) for i in val1.lower()]) == ''.join([eq_sym.get(i, i) for i in val2.lower()]):
            result = True

    return result


def sorted_dict_contacts(dict_contacts: dict) -> list:
    list_contacts = sorted(dict_contacts.items(), key=lambda i: i[1].contact_name)
    return list_contacts


def obj2json(obj):
    try:
        return json.dumps(obj, indent=4, sort_keys=True)
    except TypeError:
        return str(obj)


def decorator_time_lost(func):
    def wrapper(*args, **kwargs):
        path_to_file_log = pathlib.Path(get_tuning_value('path_to_dbase') + os.sep + get_tuning_value('name_log'))
        try:
            if not pathlib.Path(path_to_file_log).exists():
                raise FileLogNotFound
        except FileLogNotFound:
            if not create_file_log(path_to_file_log=path_to_file_log):
                raise FileLogNotCreated

        with open(path_to_file_log, 'a') as fl:
            fl.write(f'start function: {func.__name__}'
                     f'{datetime.datetime.now().strftime(Contact.mask_date_time_creation())}\n')
            ret = func(*args, **kwargs)
            fl.write(f'stop function {func.__name__}'
                     f'{datetime.datetime.now().strftime(Contact.mask_date_time_creation())}\n')

        return ret

    return wrapper


def decorator_args_kwargs(func):
    def wrapper(*args, **kwargs):
        path_to_file_log = pathlib.Path(get_tuning_value('path_to_dbase') + os.sep + get_tuning_value('name_log'))

        if path_to_file_log is not None:
            try:
                if not pathlib.Path(path_to_file_log).exists():
                    raise FileLogNotFound
            except FileLogNotFound:
                if not create_file_log(path_to_file_log=path_to_file_log):
                    raise FileLogNotCreated

            with open(path_to_file_log, 'a') as fl:
                sep = get_tuning_value('sep_in_dbase')
                fl.write(f'args: {sep.join(list(args))}\n')

                list_kwargs = [str(i) + ':' + str(j) for i, j in kwargs.items()]
                fl.write(f'kwargs: {sep.join(list_kwargs)}\n')
        else:
            print(*args, sep='\n')
            print(*kwargs, sep='\n')
        result = func(*args, **kwargs)

        if path_to_file_log is not None:
            with open(path_to_file_log, 'a') as fl:
                fl.write(f'result: {str(result)}\n')

        return result

    return wrapper


@decorator_args_kwargs
def find_contact_by_phone(dict_contacts: dict,
                          phone_number: str) -> None | Contact:
    return dict_contacts.get(phone_number)


def find_contact_by_name(dict_contacts: dict,
                         contact_name: str) -> tuple:
    contacts = ()
    for obj in dict_contacts.values():
        if obj.contact_name.upper().find(contact_name.upper()) >= 0:
            contacts += (obj,)
    return contacts


@decorator_time_lost
def find_contact_by_name_(names_dict: dict,
                          dict_contacts: dict,
                          contact_name: str) -> tuple:
    contacts = names_dict.get(contact_name.upper())

    if contacts is None:
        contacts = find_contact_by_name(dict_contacts=dict_contacts,
                                        contact_name=contact_name)
    return contacts


def create_contact() -> Contact:
    contact_name = input('Please, input contact name>> ')
    Contact.validate_contact_name(contact_name=contact_name)

    phone_number = input(f'Please, input phone number for {contact_name}>> ')
    Contact.validate_phone_number(phone_number=phone_number)

    return Contact(phone_number=phone_number,
                   contact_name=contact_name,
                   validate=False)


def edit_contact(contact: Contact) -> Contact:
    contact_name = input(f'Please, input new contact name for "{contact.contact_name}">> ')
    phone_number = contact.phone_number
    new_contact = Contact(phone_number=phone_number,
                          contact_name=contact_name)

    del contact
    return new_contact


def get_mark_print(len_obj: int, num_of_lines: int = get_tuning_value('num_of_lines')) -> int:
    if len_obj <= num_of_lines:
        mark_print: int = get_tuning_value('mark_print')
    else:
        mark_print = num_of_lines

    return 1 if mark_print == 0 else mark_print


def print_contacts(dict_contacts: dict) -> None:
    cnt_rows: int = 0
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


def create_file_base(path_to_file_dbase: pathlib.Path) -> bool | None:
    with open(path_to_file_dbase, 'w'):
        pass
    return True


def create_file_log(path_to_file_log: pathlib.Path) -> bool | None:
    with open(path_to_file_log, 'w'):
        pass
    return True


def full_download_dbase(path_to_file_dbase=pathlib.Path(get_tuning_value('path_to_dbase')
                                                        + os.sep + 'contact-book.dbase'),
                        mark_print=None) -> tuple:
    base_dict: dict = {}

    try:
        if not pathlib.Path(path_to_file_dbase).exists():
            raise FileBaseNotFound
    except FileBaseNotFound:
        if not create_file_base(path_to_file_dbase=path_to_file_dbase):
            return tuple()

    cnt_rows: int = 0
    mask = Contact.mask_date_time_creation()

    with open(path_to_file_dbase, 'r') as fb:
        len_fb = sum(1 for _ in fb)
        if mark_print is None:
            mark_print = get_mark_print(len_fb)  # count rows in file

    with open(path_to_file_dbase, 'r') as fb:
        for rec in fb:
            contact = rec.rstrip('\n').split(get_tuning_value('sep_in_dbase'))  # it's tuning
            base_dict[contact[0]] = Contact(phone_number=contact[0],
                                            contact_name=contact[1],
                                            date_time_creation_contact=datetime.datetime.strptime(contact[2], mask),
                                            validate=False)

            cnt_rows += 1
            if (len_fb // mark_print) >= 2 and cnt_rows % mark_print == 0:
                print(f'download {cnt_rows} rows')

    if cnt_rows > 0:
        print(f'total download {cnt_rows} rows')

    return base_dict, path_to_file_dbase


def create_cash_names(dict_contacts: dict) -> dict:
    names_dict: dict = {}

    for contact in dict_contacts.values():
        part_of_contact_name = ''
        for i in contact.contact_name:
            part_of_contact_name += i.upper()
            if names_dict.get(part_of_contact_name):
                names_dict[part_of_contact_name] = names_dict[part_of_contact_name] + (contact,)
            else:
                names_dict[part_of_contact_name] = (contact,)
    return names_dict


# @decorator_args_kwargs
def full_upload_dbase(dbase_dict: dict,
                      path_to_file_dbase: pathlib.Path,
                      mark_print=None) -> None:
    try:
        if not pathlib.Path(path_to_file_dbase).exists():
            raise FileBaseNotFound
    except FileBaseNotFound:
        if not create_file_base(path_to_file_dbase=path_to_file_dbase):
            raise FileBaseNotCreated

    cnt_rows: int = 0
    len_dbase_dict: int = len(dbase_dict)

    if mark_print is None:
        mark_print = get_mark_print(len_obj=len_dbase_dict)

    with open(path_to_file_dbase, 'w') as fb:
        for _, contact in dbase_dict.items():
            fb.write(f'{contact.format_to_dbase}\n')
            cnt_rows += 1
            if (len_dbase_dict // mark_print) >= 2 and cnt_rows % mark_print == 0:
                print(f'upload {cnt_rows} rows...')

    if cnt_rows > 0:
        print(f'total upload {cnt_rows} rows...')


def full_backup_dbase(dbase_dict: dict,
                      path_to_file_dbase=pathlib.Path(get_tuning_value('path_to_dbase')
                                                      + os.sep + 'contact-book.backup'),
                      mark_print=None) -> pathlib.Path:
    try:
        if not pathlib.Path(path_to_file_dbase).exists():
            raise FileBaseNotFound
    except FileBaseNotFound:
        if not create_file_base(path_to_file_dbase=path_to_file_dbase):
            raise FileBaseNotCreated

    dict2json = {}

    cnt_rows = 0
    len_dbase_dict = len(dbase_dict)
    if mark_print is None:
        mark_print = get_mark_print(len_obj=len_dbase_dict)

    for _, contact in dbase_dict.items():
        dict2json = {**dict2json, **contact.dict}
        cnt_rows += 1
        if (len_dbase_dict // mark_print) >= 2 and cnt_rows % mark_print == 0:
            print(f'prepared {cnt_rows} rows...')

    if cnt_rows > 0:
        print(f'total prepared {cnt_rows} rows...')

    with open(path_to_file_dbase, 'w') as fb:
        json.dump(dict2json, fb, indent=4)

    return path_to_file_dbase


def main():
    welcome_text = get_tuning_value('welcome_text')  # it's tuning

    menu_text = ('Select on action (enter number) and press key Enter:',
                 '1. Add contact',
                 '2. Find contact',
                 '3. Show all contacts',
                 '4. Remove contact',
                 '5. Edit contact',
                 '6. Backup contact book',
                 '7. Save contact book to disk',
                 '8. Exit',)

    menu_text = '\n'.join(menu_text)

    print(welcome_text)

    contacts, cur_path_to_file_dbase = full_download_dbase()
    names = {}

    assert cur_path_to_file_dbase  # check file db

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
                        full_upload_dbase(dbase_dict=contacts, path_to_file_dbase=cur_path_to_file_dbase)
                break

            while True:
                if action == 1:
                    try:
                        contact = create_contact()

                        find_contact = find_contact_by_phone(dict_contacts=contacts,
                                                             phone_number=contact.phone_number)

                        if find_contact is None:
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
                        if input(f'Contact exist!'
                                 f'Repeat another? ("Y" - Press any key / "N" - return main menu)>> '
                                 ).upper() == 'N':
                            break

                if action == 2:
                    try:
                        search_type = int(input('1 - find by phone, 2 - find by contact name>> '))

                        if search_type not in range(1, 3):
                            raise UnknownAction

                        match search_type:
                            case 1:
                                contact = (find_contact_by_phone(dict_contacts=contacts,
                                                                 phone_number=input('Enter phone for search>> ')),)
                            case 2:
                                if not names:
                                    names = create_cash_names(dict_contacts=contacts)

                                contact = find_contact_by_name_(names_dict=names,
                                                                dict_contacts=contacts,
                                                                contact_name=input('Enter name for search>> '))
                            case _:
                                contact = None

                        if contact is None:
                            raise ContactNotFound
                        else:
                            contact = {i.phone_number: i for i in contact}
                            print_contacts(contact)

                            if input('Repeat find? ("Y" - Press any key / "N" - return main menu)>> ').upper() == 'N':
                                break
                    except ContactNotFound:
                        if input('Sorry, contact is not found. Repeat?'
                                 '("Y" - Press any key / "N" - return main menu)>> ').upper() == 'N':
                            break

                    except (UnknownAction, ValueError):
                        if input('Sorry, you select unknown action. Repeat?'
                                 '("Y" - Press any key / "N" - return main menu)>> ').upper() == 'N':
                            break

                if action == 3:
                    print_contacts(contacts)
                    break

                if action == 4:
                    try:
                        contact = find_contact_by_phone(dict_contacts=contacts,
                                                        phone_number=input('Enter phone number for remove>> '))
                        if contact is None:
                            raise ContactNotFound
                        else:
                            print(f'This contact {str(contact)} will be deleted!')
                            del contacts[contact.phone_number]
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
                        if contact is None:
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
                    path_to_file = full_backup_dbase(dbase_dict=contacts)
                    input(f'Backup done... create file: {path_to_file}')
                    break

                if action == 7:
                    if contacts_change:
                        full_upload_dbase(dbase_dict=contacts,
                                          path_to_file_dbase=cur_path_to_file_dbase
                                          )
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
