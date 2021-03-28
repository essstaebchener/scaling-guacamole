from typing import Dict
from operator import itemgetter

# from table_logger import TableLogger
import tabulate
import random

ERROR_CODES = [error_code for error_code in range(50)]
DUMMY_RESOLVED = {
    'resolved': [{
        'index': error_idx,
        'code': random.choice(ERROR_CODES),
        'text': 'Error ABC occurred, that is `resolved`'
    } for error_idx in range(50)]
}


def get_error_counts(err_data: list) -> list:
    """ return list of dict['code', 'count', 'text']"""

    # get a list of all error codes in the list
    err_codes = [d['code'] for d in err_data]

    for _dict in err_data:
        _dict.pop('index', None)  # delete the index key
        _dict['count'] = err_codes.count(_dict['code'])  # add in the count of occurrences of the error_code

    # get rid of non-unique error_codes
    # use tuples to check for uniqueness as tuples are hashable
    err_data = [dict(t) for t in {tuple(d.items()) for d in err_data}]
    err_data = sorted(err_data, key=itemgetter('code'))  # sort the list by error code

    return err_data


def log_error_codes(data: Dict, _get_counts=False) -> None:
    """ Print a log of error_codes with counts (human-readable)"""

    for key, value in data.items():
        table_name = key  # resolved, unresolved, backlog
        dataset = get_error_counts(value) if _get_counts else value
        header = dataset[0].keys()
        rows = [x.values() for x in dataset]
        print("List : {} ".format(table_name))
        print("="*(7+len(table_name)))
        print(tabulate.tabulate(rows, header, tablefmt='grid'))
    return


if __name__ == '__main__':
    log_error_codes(DUMMY_RESOLVED)
