from bitrix24 import *
import pprint

bx24 = Bitrix24('https://metodika.bitrix24.ru/rest/6/rxx2cwnjenyj56s3/')
pp = pprint.PrettyPrinter(indent=4)


def phoneisorcreate(phone):
    the = bx24.callMethod('crm.contact.list',
                          order={'STAGE_ID': 'ASC'},
                          filter={'PHONE': phone},
                          select=['ID'])
    # pp.pprint(the)
    if not the:
        iss = False

    else:
        iss = True
    return iss, the


def dealsfromcontact(phone):
    iss, the = phoneisorcreate(phone)
    if iss:
        thedeals = bx24.callMethod('crm.deal.list', filter={'CONTACT_ID': the[0]['ID'], 'CLOSED': 'N'}, order={'STAGE_ID': 'ASC'})
        # pp.pprint(thedeals)
        return thedeals
    else:
        return None

# def bitrixincome(phone):
#     iss, the = phoneis(phone)
#     if iss:
#     pass

# pp.pprint(dealsfromcontact('995557947579'))