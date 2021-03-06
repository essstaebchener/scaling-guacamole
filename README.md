# Coding challenge

Welcome to this fullstack coding challenge. This Readme will guide you through it. It will first present a high level full picture of the project and then scope your task.

In order to run the code that already exists for the frontend and the api, please check out the `api/README.md` and the `frontend/README.md`.

Please do not modify the `Makefile`. In the end you may run `make -j2` to verify that we can validate your solution. This command should start both the API and the frontend automatically and run through with no problems. If your environment does not support `make`, starting both services by manually is usually enough.

## High Level Description

Our company wants to write a checking tool for internal JSONs that store data. These JSONs are checked, everytime our checking system finds an error, it generates a JSON error object like:

```json
{
    "index": SOME_NUMERIC_INDEX,
    "code": SOME_NUMERIC_ERROR_CODE,
    "text": SOME_TEXT_DESCRIPTION
}
```

We then wrote an API that will get all errors generated so far, separated by their status. A human operator has to be able to see and understand these errors in order to fix them in the original data. Our company strives to reduce errors to almost zero by providing a flawless UI/UX for operators to check errors and resolve them.

## Challenge task
Some other developer already wrote an API that delivers errors sorted into the 3 available categories: resolved, unresolved, backlog. Another developer has already started on the frontend, but he only did the bare minimum.
The tasks are split across the frontend and the api, the main focus lies on data manipulation and UI/UX implementation.


To access the api endpoints, call from the frontend on:
* http://localhost:8000/get_lists : to generate (get) lists of the 3 types
* http://localhost:8000/get_list_intersection_counts : to get the error intersection counts between a set of resolved, unresolved and backlog lists
* http://localhost:8000/get_error_resolved_count/error_code= : the num of times a certain error.code was resolved
* http://localhost:8000//get_error_all_counts : the num of times each error.code occurred on the list_type selected

Check http://localhost:8000/docs for Swagger API documentation.
Presently only the first end-point is used on the frontend: error_lists are generated from get_lists 


Completed tasks are checked. Additional stretch-goal tasks are also listed with the rest. 
Functions have basic documentation about code.
Additional TO-DOs are listed afterwards.

_backend_

-   [x] write a logging functionality, that counts how many requests for errors are received (you can store these numbers in memory, no persistent storage required)
    - [x] added _log.py module to do logging of count and messages
-   [x] implement the code of the `get_list_intersection_counts` function endpoint. You can find it in `_api.py`.

-   [x] add the `operator_name` as a parameter to the request that is sent from the `frontend` to the `api` to get the error lists. Then log how many times a certain operator requested data (you can store these numbers in memory, no persistent storage required).
    - [x] added `operator_name` with random values in the generated lists
-   [x] add a new functionality: The operator can send all errors that are currently marked as `resolved` to the `api`, the `api` prints out how many times a certain `error.code` was resolved
    - added api end-point `get_error_resolved_count(error_code: int)`
-  [x] added api end-point `get_error_all_counts()` to return error counts of all lists

  
_Notes_:- TODO:
- [ ] create a class for logging and extend native logging instead
  - [ ] add logging into file functionality
- [ ] add unit-testing
- [ ] Front-end  

_frontend_

-   [ ] Write a UI that allows the operator to:
  -   [x] have an "nice" overview of all errors, it should show `unresolved`, then `resolved` and then `backlog` errors
  -   [x] see the `text` and `code` of each error
  -   [ ] resolve each individual `unresolved` error by clicking an individual button
  -   [ ] unresolve each individual `resolved` error (e.g., when an error was set to `resolved` by mistake) by clicking an individual button
  -   [ ] move an individual backlog error to the bottom of the `unresolved` list of displayed errors, by clicking an individual button
  -   [ ] undo his last action. E.g., if he resolved an unresolved error, an `undo` functionality enables him to move it back into the unresolved list of errors. This should work between all lists for _ only the last_ action of a user


This is the absolute minimum our operators and their managers need, in order to resolve errors effectively. If you still have time/if you're still willing, you may start on the `version two` - this will enable our operators to resolve errors _effectively_ (frontend version two) and us to check the system for systematic errors (api version two).

_frontend version two_

-   [ ] make the UI/UX better
  -   [ ] shadows,
  -   [ ] click, hover animations (e.g. changing to a darker shade of said color)
  -   [ ] notifications
  -   [ ] mobile layout
  -   [ ] ...
-   [ ] make the undo functionality better
  -   [ ] the user should be able to undo _all_ of his actions
  -   [ ] when a user clicks undo, the item that switches lists should be in the same position as before (e.g., if the user resolved an error that was in the middle of the list at position 4, it should also re-appear at position 4 if he undoes this action)

## Screenshots

Some screenshots to get you started/so that you know, that you're on the right path.

[frontend output](./screenshots/start_frontend_output.png) shows the raw, initial frontend that the previous developer left for you.

[terminal output](./screenshots/start_terminal_output.png) show the raw terminal output, that you will see once you ran all the correct commands to get the frontend and api started.
