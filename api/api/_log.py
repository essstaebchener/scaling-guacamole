from typing import Dict
from operator import itemgetter
import tabulate
import random
import copy
import logging

# TODO: create a class for logging and extend native logging instead

def log_info(data: str or Dict, field='code', _get_counts=False) -> None:
    """ Print a log of error_codes with counts (human-readable)"""

    if type(data) is str:
        LOGGER = logging.getLogger("API")
        logging.basicConfig(level=logging.DEBUG)
        LOGGER.info(data)
    elif type(data) is dict:
        # to log the generated lists, we create a deepcopy first
        # instead of using the original dict
        _data = copy.deepcopy(data)
        for key, value in _data.items():
            table_name = key  # resolved, unresolved, backlog
            dataset = get_error_counts(value, field) if _get_counts else value
            header = dataset[0].keys()
            rows = [x.values() for x in dataset]
            print("\nList : {} \n".format(table_name))
            print("="*(7+len(table_name)))
            print(tabulate.tabulate(rows, header, tablefmt='grid'))
    return


def get_error_counts(err_data: list, field='code') -> list:
    """ return list of dict['field', 'count', 'text'] or code if no field is passed"""

    # get a list of all field_values in the list
    err_codes = [d[field] for d in err_data]

    for _dict in err_data:
        _dict.pop('index', None)  # delete the index key
        if field == 'code':
            _dict.pop('operator_name', None)  # delete the operator_name key
        elif field == 'operator_name':
            _dict.pop('code', None)  # delete the code key
            _dict.pop('text', None)  # delete the text key

        _dict['count'] = err_codes.count(_dict[field])  # add in the count of occurrences of the field-values

    # get rid of non-unique error_codes
    # use tuples to check for uniqueness as tuples are hashable
    err_data = [dict(t) for t in {tuple(d.items()) for d in err_data}]
    err_data = sorted(err_data, key=itemgetter(field))  # sort the list by field

    return err_data


# test whether the code works
if __name__ == '__main__':

    # first test message string logging
    log_info("dummy message #1")

    # generate the dummy lists
    ERROR_CODES = [error_code for error_code in range(50)]
    OPERATOR_NAMES = ['OPERATOR A', 'OPERATOR B', 'OPERATOR C']
    DUMMY_RESOLVED = {
        'resolved': [{
            'index': error_idx,
            'code': random.choice(ERROR_CODES),
            'text': 'Error ABC occurred, that is `resolved`',
            'operator_name': random.choice(OPERATOR_NAMES),
        } for error_idx in range(50)]
    }

    # log error codes by operator_name and code
    log_info(DUMMY_RESOLVED, 'operator_name', True)
    log_info(DUMMY_RESOLVED, 'code', True)

    # test string again
    log_info("dummy message #2")
