from main import *
import random
import string


def dummy_contacts_dict() -> dict:
    max_contacts: int = 1000_000

    _ = tuple(Contact(phone_number=f'+{random.choice(string.digits)}'
                                   f'{random.choice(string.digits)}'
                                   f'{random.choice(string.digits)}'
                                   f'{random.choice(string.digits)}'
                                   f'{random.choice(string.digits)}'
                                   f'{random.choice(string.digits)}'
                                   f'{random.choice(string.digits)}'
                                   f'{random.choice(string.digits)}'
                                   f'{random.choice(string.digits)}'
                      , contact_name=((f'{random.choice(string.ascii_letters)}' * 10) + str(i))[:15]
                      )
              for i in range(max_contacts))

    return {contact.phone_number: contact for contact in _}


def tst_full_upload_dbase() -> None:
    max_num_file: int = 10_000
    mark_print: int = 10_000

    full_upload_dbase(dbase_dict=dummy_contacts_dict(),
                      path_to_file_base=pathlib.Path(
                          os.getenv('HOME') + os.sep + f'contact-book{random.randint(0, max_num_file)}.tst'),
                      mark_print=mark_print
                      )