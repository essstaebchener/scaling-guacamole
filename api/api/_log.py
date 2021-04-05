"""Module for logging messages or list passed. Uses tabulate to print in a more human-readable form"""

from typing import Dict
from operator import itemgetter
import tabulate
import random
import copy
import logging


# TODO: create a class for logging and extend native logging instead


def log_info(data=None, logger='API', get_counts=False, field_name='code') -> None:
    """
    Print a log of error_codes with counts (human-readable)
    accepts strings or dicts as datasets (`data`)
    if dict is passed, first key is assumed to be table-name
    ---
    INPUTS:
        data : data to be logged, can be string or dict #TODO: extend this, using Dict for type-check
        logger : logger name, 'API' by default
        get_counts : if values need to be tabulated by counts of a column
        field_name : if counts are needed, then by which field, 'code' by default
    """
    _log_str = ""

    if data is None or data == "":
        _log_str = "log_info() called with empty 'data' param: "
        _log_str += "log_info(data, logger_name, field_name, _get_counts)"
    else:
        if type(data) is str:
            _log_str = data
        elif type(data) is dict:
            # to log the message or generated lists, we use a deepcopy
            # instead of using the original data
            _data = copy.deepcopy(data)
            header = ""
            rows = ""
            for key, value in _data.items():
                table_name = key  # resolved, unresolved, backlog
                dataset = get_error_counts(value, field_name) if get_counts else value
                if type(dataset) is list:
                    # if passed table is a list of dicts
                    header = dataset[0].keys()
                    rows = [x.values() for x in dataset]
                    _log_str += "\nList : {} \n".format(table_name)
                    _log_str += "=" * (7 + len(table_name)) + "\n"
                    _log_str += tabulate.tabulate(rows, header, tablefmt='grid')
                elif type(dataset) is dict:
                    # if passed table is a dict of dicts
                    header = dataset.keys()
                    rows = [v for k, v in dataset.items()]

    str_logger = logging.getLogger(logger)
    logging.basicConfig(level=logging.INFO)
    str_logger.info(_log_str)
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
    log_info("dummy message #1", logger='Test')

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
    log_info(DUMMY_RESOLVED, field_name='operator_name', get_counts=True)
    log_info(DUMMY_RESOLVED, field_name='code', get_counts=True)

    # test string again
    log_info("dummy message #2", logger='Test')
