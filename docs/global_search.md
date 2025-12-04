# [Global search ](#module-dfir_iris_client.global_search)

dfir\_iris\_client.global\_search. global\_search\_ioc (

*session :* [*ClientSession*](session.html#dfir_iris_client.session.ClientSession) , *search\_term : str* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.global_search.global_search_ioc)

Searches an IOC across all investigation

Parameters :

- **session** - Client Session to use for request
- **search\_term** - Search term to search for IOC

Returns :

ApiResponse object

dfir\_iris\_client.global\_search. global\_search\_notes (

*session :* [*ClientSession*](session.html#dfir_iris_client.session.ClientSession) , *search\_term : str* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.global_search.global_search_notes)

Searches in note contents across all investigation

Parameters :

- **session** - Client Session to use for request
- **search\_term** - Search term to search for notes

Returns :

ApiResponse object