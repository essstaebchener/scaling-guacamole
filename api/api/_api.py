"""Module to setup fastapi API to expose API to the outside world."""
import random
from collections import Counter
from typing import Any, Dict

from fastapi import FastAPI, HTTPException
import uvicorn
from _log import log_info as log

ERROR_CODES = [error_code for error_code in range(50)]
OPERATOR_NAMES = ['OPERATOR A', 'OPERATOR B', 'OPERATOR C']
app = FastAPI()


def _generate_lists() -> Dict[str, Any]:
    """Generate resolved, unresolved and backlog lists."""
    log('Generating resolved, unresolved and backlog lists.', logger='API')
    error_lists = {
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

    log(error_lists, field_name='code', get_counts=True)
    log(error_lists, field_name='operator_name', get_counts=True)
    return error_lists


@app.get("/")
async def root():
    """" Test whether end-point setup works """
    return {"message": "Hello World"}

@app.get("/get_lists")
def get_lists() -> Dict[str, Any]:
    """Return resolved, unresolved and backlog lists."""
    return _generate_lists()


@app.get("/get_list_intersection_counts")
def get_list_intersection_counts() -> Dict[str, int]:
    """Return the error intersection counts between a set of resolved, unresolved and backlog lists -
        intersection_counts: Dict[str, int]
    """
    # Generate the three lists required for this calculation
    error_lists = _generate_lists()

    resolved, unresolved, backlog = error_lists['resolved'], error_lists['unresolved'], error_lists['backlog']

    # create three lists for error_codes of each type
    resolved_codes = [d['code'] for d in resolved]
    unresolved_codes = [d['code'] for d in unresolved]
    backlog_codes = [d['code'] for d in backlog]

    # Calculate how many errors with *the same error code* are shared between the possible pairs of lists.
    log('Generating the intersection counts between a set of resolved, unresolved and backlog lists.', logger='API')
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
    _error_lists = _generate_lists()

    try:
        err_list = _error_lists[list_type]
    except KeyError:
        raise HTTPException(status_code=404, detail="list_type not found")

    err_codes = [d['code'] for d in err_list]
    err_dict = Counter(err_codes)
    return {
        list_type: err_dict,
    }


def run(host: str, port: int) -> None:
    """Run the code challenge API."""
    uvicorn.run(app, host=host, port=port)
