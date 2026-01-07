# [Session ](#module-dfir_iris_client.session)

dfir\_iris\_client.session. API\_VERSION

*= '2.0.0'* [](#dfir_iris_client.session.API_VERSION)

client\_session

Defines a global session, accessible by all classes. client\_session is of type ClientSession.

*class* dfir\_iris\_client.session. ClientSession ( *apikey = None* , *host = None* , *agent = 'iris-client'* , *ssl\_verify = True* , *proxy = None* , *timeout = 120* ) [](#dfir_iris_client.session.ClientSession)

Represents a client that can interacts with Iris. It is basic wrapper handling authentication and the requests

to the server.

Args:

Returns:

pi\_get (

*uri : str* , *cid : int | None = None* , *no\_wrap : bool = False* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) | Response [](#dfir_iris_client.session.ClientSession.pi_get)

Adds the CID information needed by the server when issuing GET requests

and then issue the request itself.

Parameters :

- **uri** - URI endpoint to request
- **no\_wrap** - Do not wrap the response in ApiResponse object
- **cid** - Target case ID

Returns :

ApiResponse or Response object

pi\_post (

*uri : str* , *data : dict | None = None* , *cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.session.ClientSession.pi_post)

Issues a POSt request with the provided data. Simple wrapper around \_pi\_request

Parameters :

- **uri** - URI endpoint to request
- **data** - data to be posted. Expect a dict
- **cid** - Target case ID

Returns :

ApiResponse object

pi\_post\_files (

*uri : str* , *files : dict | None = None* , *data : dict | None = None* , *cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.session.ClientSession.pi_post_files)

Issues a POST request in multipart with the provided data.

Parameters :

- **uri** - URI endpoint to request
- **files** - data to be posted. Expect a dict
- **data** - data to be posted. Expect a dict
- **cid** - Target case ID

Returns :

ApiResponse object

preload\_base\_objects ( ) → None

[](#dfir_iris_client.session.ClientSession.preload_base_objects)

Preload the base objects most commonly used. This simply init the BaseObjects

class, which in turns requests and build all the most common objects such as

AnalysisStatus, EventCategory, EventType, etc.

For future use only

Args:

Returns:

dfir\_iris\_client.session. log

*= &lt;Logger dfir\_iris\_client.session (WARNING)&gt;* [](#dfir_iris_client.session.log)

API\_VERSION

The API version is not directly correlated with Iris version.

Server has an endpoint /api/versions which should returns the API compatible versions

it can handles.