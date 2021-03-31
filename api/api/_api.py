"""Module to setup fastapi API to expose API to the outside world."""
import logging
import random
from collections import Counter
from typing import Any, Dict

from fastapi import FastAPI
import uvicorn
from  _log import log_error_codes as log

ERROR_CODES = [error_code for error_code in range(50)]
OPERATOR_NAMES = ['OPERATOR A', 'OPERATOR B', 'OPERATOR C']
app = FastAPI()


def _generate_lists() -> Dict[str, Any]:
    """Generate resolved, unresolved and backlog lists."""
    return {
        'resolved': [{
            'index': error_idx,
            'code': random.choice(ERROR_CODES),
            'text': 'Error ABC occurred, that is `resolved`',
            'operator_name': random.choice(OPERATOR_NAMES),
        } for error_idx in range(50)],
        'unresolved': [{
            'index': error_idx,
            'code': random.choice(ERROR_CODES),
            'text': 'Error DEF occurred, that is `unresolved`',
            'operator_name': random.choice(OPERATOR_NAMES),
        } for error_idx in range(50, 100)],
        'backlog': [{
            'index': error_idx,
            'code': random.choice(ERROR_CODES),
            'text': 'Error XYZ occurred, that is in the `backlog`',
            'operator_name': random.choice(OPERATOR_NAMES),
        } for error_idx in range(100, 150)]
    }


@app.get("/get_lists")
def get_lists() -> Dict[str, Any]:
    """Return resolved, unresolved and backlog lists."""
    LOGGER.info('Generating resolved, unresolved, and backlog lists.')
    return _generate_lists()


@app.get("/get_list_intersection_counts")
def get_list_intersection_counts() -> Dict[str, int]:
    """Return the error intersection counts between a set of resolved, unresolved and backlog lists -
        intersection_counts: Dict[str, int]
    """
    # Generate the three lists required for this calculation
    LOGGER.info('Generating the intersection counts between a set of resolved, unresolved and backlog lists.')
    error_lists = _generate_lists()
    log_text = log(error_lists, True)
    print(log_text)

    resolved, unresolved, backlog = error_lists['resolved'], error_lists['unresolved'], error_lists['backlog']

    resolved_codes = [d['code'] for d in resolved]
    unresolved_codes = [d['code'] for d in unresolved]
    backlog_codes = [d['code'] for d in backlog]

    all_codes = resolved_codes + unresolved_codes + backlog_codes
    new_counter_dict = Counter(all_codes)
    LOGGER.info(" all codes counts = {}".format(Counter(new_counter_dict)))

    LOGGER.info(" resolved codes counts = {}".format(Counter(resolved_codes)))
    LOGGER.info(" unresolved_count = {}".format(Counter(unresolved_codes)))
    LOGGER.info(" backlog_count = {}".format(Counter(backlog_codes)))

    # Calculate how many errors with *the same error code* are shared between the possible pairs of lists.
    resolved_unresolved_codes = set(resolved_codes).intersection(set(unresolved_codes))
    resolved_backlog_codes = set(resolved_codes).intersection(set(backlog_codes))
    unresolved_backlog_codes = set(unresolved_codes).intersection(set(backlog_codes))

    # Then return a Dict of intersection counts
    return {
        'resolved_unresolved': len(resolved_unresolved_codes),
        'resolved_backlog': len(resolved_backlog_codes),
        'unresolved_backlog': len(unresolved_backlog_codes),
    }


@app.get("/get_error_resolved_count")
def get_error_resolved_count(error_code: int) -> Dict[str, int]:
    """ Return the num of times a certain error.code was resolved
        throws HTTPException, if error_code not found
    """
    # TODO: should we instead return count = 0 if err_code not found?

    # Generate the three lists required for this calculation
    error_lists = _generate_lists()

    resolved = error_lists['resolved']
    resolved_codes = [d['code'] for d in resolved]
    if error_code not in resolved_codes:
        raise HTTPException(status_code=404, detail="error_code not found")

    return {
        'resolved': resolved_codes.count(error_code),
    }


@app.get("/get_error_all_counts")
def get_error_resolved_all_counts(list_type='resolved') -> Dict[str, Dict]:
    """ Return the num of times each error.code occurred on the list_type selected
        list_type : 'resolved', 'unresolved', or 'backlog' (default: 'resolved')
        throws HTTPException (404), if list_type is not found
     """
    # Generate the three lists required for this calculation
    LOGGER.info('Generating resolved, unresolved and backlog lists.')
    error_lists = _generate_lists()

    resolved = error_lists['resolved']
    resolved_codes = [d['code'] for d in resolved]
    # print(*resolved_codes)
    resolved_dict = Counter(resolved_codes)

    return {
        'resolved': resolved_dict,
    }


@app.get("/get_error_resolved_count")
def get_error_resolved_count(error_code: int) -> Dict[str, int]:
    """ Return the num of times a certain error.code was resolved """
    # Generate the three lists required for this calculation
    error_lists = _generate_lists()

    resolved = error_lists['resolved']
    resolved_codes = [d['code'] for d in resolved]
    # print(*resolved_codes)
    resolved_count = resolved_codes.count(error_code)
    return {
        'resolved': resolved_count,
    }


def run(host: str, port: int) -> None:
    """Run the code challenge API."""
    uvicorn.run(app, host=host, port=port)
