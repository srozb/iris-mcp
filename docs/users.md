# [Users ](#module-dfir_iris_client.users)

*class* dfir\_iris\_client.users. User ( *session* ) [](#dfir_iris_client.users.User)

Handles the users type methods

get\_user (

*user : int | str* , *** kwargs* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.users.User.get_user)

Return a user data

Parameters :

**user** - User ID or login of the user to get

Returns :

ApiResponse object

list\_users ( ) →

[ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.users.User.list_users)

Returns a list of the users with a restricted view so it can be called by unprivileged users.

Args:

Returns :

ApiResponse object

lookup\_username (

*username : str* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.users.User.lookup_username)

Returns a user ID corresponding to the username, else None

Parameters :

**username** - Username to lookup

Returns :

ApiResponse

user\_exists (

*user : str | int* ) → bool [](#dfir_iris_client.users.User.user_exists)

Returns True if the user (login) exists, else false. User ID can also be looked up.

Parameters :

**user** - Login or user ID to lookup

Returns :

True if exists else false