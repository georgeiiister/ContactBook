from main import *
import random
import string


def create_dummy_contacts() -> tuple:
    max_contacts: int = 100_000
    max_contacts_for_search = 10
    contacts_index = (random.choice(range(max_contacts_for_search)) for i in range(max_contacts_for_search))

    _ = tuple(Contact(phone_number=f'+{random.choice(string.digits)}'
                                   f'{random.choice(string.digits)}'
                                   f'{random.choice(string.digits)}'
                                   f'{random.choice(string.digits)}'
                                   f'{random.choice(string.digits)}'
                                   f'{random.choice(string.digits)}'
                                   f'{random.choice(string.digits)}'
                                   f'{random.choice(string.digits)}'
                                   f'{random.choice(string.digits)}'
                      , contact_name=((f'{random.choice(string.ascii_letters)}'
                                       f'{random.choice(string.ascii_letters)}'
                                       f'{random.choice(string.ascii_letters)}'
                                       * 3) + str(i) + ' ' +
                                      (f'{random.choice(string.ascii_letters)}'
                                       f'{random.choice(string.ascii_letters)}'
                                       f'{random.choice(string.ascii_letters)}'
                                       * 3) + str(i)
                                      )
                      )
              for i in range(max_contacts))

    return {contact.phone_number: contact for contact in _}, {_[i].phone_number: _[i] for i in contacts_index}


def create_dummy_dbase():
    max_num_file: int = 10_000
    mark_print: int = 100_000
    path_to_file_dbase = os.path.expanduser('~') + os.sep + f'contact-book{random.randint(0, max_num_file)}.tst'

    contacts_, contacts_search_ = create_dummy_contacts()

    # send to file dummy contacts_
    full_upload_dbase(dbase_dict=contacts_,
                      path_to_file_dbase=path_to_file_dbase,
                      mark_print=mark_print
                      )
    return contacts_search_, path_to_file_dbase


def create_dummy() -> tuple:
    mark_print: int = 100_000
    contacts_search_, path_to_file_dbase = create_dummy_dbase()

    (base_dict, path_to_file_dbase) = full_download_dbase(path_to_file_dbase=path_to_file_dbase,
                                                          mark_print=mark_print
                                                          )

    return base_dict, path_to_file_dbase, contacts_search_


def create_dummy_cash_names(dict_contacts: dict) -> dict:
    print('start create cash contact for search...')
    time_start = datetime.datetime.now()

    names_dict_ = create_cash_names(dict_contacts=dict_contacts)

    time_stop = datetime.datetime.now()
    print(f'begin: {time_start}', f'stop: {time_stop}', f'cost:{time_stop - time_start}', sep='\n')

    return names_dict_


def search_contact_in_dummy(names_dict_: dict, dict_contacts: dict, contacts_search_: dict) -> tuple:
    result_search = ()
    for _, contact in contacts_search_.items():
        result_search += find_contact_by_name_(names_dict=names_dict_,
                                               dict_contacts=dict_contacts,
                                               contact_name=contact.contact_name[:int(len(contact.contact_name)/3)])

    return result_search


#contacts, path_to_file, contacts_search = create_dummy()

#names_dict = create_dummy_cash_names(dict_contacts=contacts)

'''search_contact = search_contact_in_dummy(names_dict_=names_dict,
                                         dict_contacts=contacts,
                                         contacts_search_=contacts_search
                                         )'''


