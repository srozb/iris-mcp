# [Administration ](#module-dfir_iris_client.admin)

*class* dfir\_iris\_client.admin. AdminHelper ( *session* ) [](#dfir_iris_client.admin.AdminHelper)

Handles administrative tasks

add\_asset\_type (

*name : str* , *description : str* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.admin.AdminHelper.add_asset_type)

Add a new Asset Type.

Parameters :

- **name** - Name of the Asset type
- **description** - Description of the Asset type

Returns :

ApiResponse

add\_case\_classification (

*name : str* , *name\_expanded : str* , *description : str* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.admin.AdminHelper.add_case_classification)

Add a new Case Classification.

Parameters :

- **name** - Name of the Case Classification
- **name\_expanded** - Expanded name of the Case Classification
- **description** - Description of the Case Classification

Returns :

ApiResponse

add\_customer (

*customer\_name : str* ) [](#dfir_iris_client.admin.AdminHelper.add_customer)

Creates a new customer. A new customer can be added if:

- customer\_name is unique

Parameters :

**customer\_name** - Name of the customer to add.

Returns :

ApiResponse object

add\_group (

*group\_name : str* , *group\_description : str* , *group\_permissions : List [* [*Permissions*](helpers.html#dfir_iris_client.helper.authorization.Permissions) *]* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.admin.AdminHelper.add_group)

Add a new group with permissions. Cases access and members can be set later on with set\_group\_access and set\_group\_members methods. Permissions must be a list of known

permissions from the Permission enum.

Parameters :

- **group\_name** - Name of the group
- **group\_description** - Description of the group
- **group\_permissions** - List of permission from Permission enum

Returns :

ApiResponse object

add\_ioc\_type (

*name : str* , *description : str* , *taxonomy : str | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.admin.AdminHelper.add_ioc_type)

Add a new IOC Type.

Parameters :

- **name** - Name of the IOC type
- **description** - Description of the IOC type
- **taxonomy** - Taxonomy of the IOC Type

Returns :

ApiResponse

add\_report\_template (

*template\_name : str* , *template\_description : str* , *template\_type :* [*ReportTemplateType*](helpers.html#dfir_iris_client.helper.report_template_types.ReportTemplateType) , *template\_name\_format : str* , *template\_language :* [*ReportTemplateLanguage*](helpers.html#dfir_iris_client.helper.report_template_types.ReportTemplateLanguage) , *template\_stream : BinaryIO* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.admin.AdminHelper.add_report_template)

Add a new report template. template\_type must be a ReportTemplateType enum.

Parameters :

- **template\_name** - Name of the template
- **template\_description** - Description of the template
- **template\_type** - ReportTemplateType enum
- **template\_language** - ReportTemplateLanguage enum
- **template\_name\_format** - Name format of the template
- **template\_stream** - Template data
- **cid** - Case ID

Returns :

ApiResponse object

add\_user (

*login : str* , *name : str* , *password : str* , *email : str* , *** kwargs* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.admin.AdminHelper.add_user)

Adds a new user. A new user can be successfully added if

- login is unique
- email is unique
- password meets the requirements of IRIS

!!! tip "Requires server administrator rights"

Parameters :

- **login** - Username (login name) of the user to add
- **name** - Full name of the user
- **password** - Password of the user
- **email** - Email of the user

Returns :

ApiResponse

deactivate\_user (

*user: [&lt;class 'int'&gt;* , *&lt;class 'str'&gt;] = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.admin.AdminHelper.deactivate_user)

Deactivate a user from its user ID or login. Disabled users can't log in interactively nor user their API keys.

They do not appear in proposed user lists.

Parameters :

**user** - User ID or login to deactivate

Returns :

ApiResponse object

delete\_asset\_type (

*asset\_type\_id : int* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.admin.AdminHelper.delete_asset_type)

Delete an existing asset type by its ID.

Parameters :

**asset\_type\_id** - Asset type to delete

Returns :

ApiResponse

delete\_case\_classification (

*case\_classification\_id : int* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.admin.AdminHelper.delete_case_classification)

Delete an existing Case Classification by its ID.

Parameters :

**case\_classification\_id** - Case Classification to delete

Returns :

ApiResponse

delete\_customer (

*customer : str | int* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.admin.AdminHelper.delete_customer)

Deletes a customer from its ID or name.

Parameters :

**customer** - Customer name or customer ID

Returns :

ApiResponse object

delete\_group (

*group : str | int* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.admin.AdminHelper.delete_group)

Delete a group by its ID or name.

Parameters :

**group** - Group ID or group name

Returns :

ApiResponse object

delete\_ioc\_type (

*ioc\_type\_id : int* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.admin.AdminHelper.delete_ioc_type)

Delete an existing IOC Type by its ID.

Parameters :

**ioc\_type\_id** - IOC type to delete

Returns :

ApiResponse

delete\_report\_template (

*template\_id : int* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.admin.AdminHelper.delete_report_template)

Delete a report template by its ID.

Parameters :

**template\_id** - Template ID

Returns :

ApiResponse object

delete\_user (

*user: [&lt;class 'int'&gt;, &lt;class 'str'&gt;], **kwargs* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.admin.AdminHelper.delete_user)

Deletes a user based on its login. A user can only be deleted if it does not have any

activities in IRIS. This is to maintain coherence in the database. The user needs to be

deactivated first.

!!! tip "Requires administrative rights"

Parameters :

**user** - Username or user ID of the user to delete

Returns :

ApiResponse

delete\_user\_by\_id (

*user\_id : int* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.admin.AdminHelper.delete_user_by_id)

Delete a user based on its ID. A user can only be deleted if it does not have any

activities in IRIS. This is to maintain coherence in the database.

Parameters :

**user\_id** - UserID of the user to delete

Returns :

ApiResponse

get\_group (

*group : str | int* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.admin.AdminHelper.get_group)

Get a group by its ID or name.

Parameters :

**group** - Group ID or group name

Returns :

ApiResponse object

get\_user (

*user : int | str* , *** kwargs* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.admin.AdminHelper.get_user)

Return a user data

Parameters :

**user** - User ID or login of the user to get

Returns :

ApiResponse object

get\_user\_cases\_access\_trace (

*user : int | str* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.admin.AdminHelper.get_user_cases_access_trace)

Get the trace of the cases access of a user.

Parameters :

**user** - User ID or login to update

Returns :

ApiResponse

has\_permission (

*permission :* [*Permissions*](helpers.html#dfir_iris_client.helper.authorization.Permissions) ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.admin.AdminHelper.has_permission)

Returns true if the user has the given permissions

Parameters :

**permission** - Permission to check

Returns :

ApiResponse

is\_user\_admin ( ) → bool

[](#dfir_iris_client.admin.AdminHelper.is_user_admin)

Deprecated in IRIS v1.5.0. Use the new has\_permission(&lt;permission&gt;) method.

Returns True if the calling user is administrator

Args:

Returns :

Bool - true if the calling is administrator

list\_groups ( ) →

[ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.admin.AdminHelper.list_groups)

List all groups.

Returns :

ApiResponse object

lookup\_group (

*group\_name : str* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.admin.AdminHelper.lookup_group)

Lookup a group by its name.

Parameters :

**group\_name** - Group name

Returns :

ApiResponse object

recompute\_all\_users\_cases\_access ( ) →

[ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.admin.AdminHelper.recompute_all_users_cases_access)

Recompute the cases access of all users.

Returns :

ApiResponse object

recompute\_user\_cases\_access (

*user : int | str* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.admin.AdminHelper.recompute_user_cases_access)

Recompute the cases access of a user.

Parameters :

**user** - User ID or login to update

Returns :

ApiResponse

update\_asset\_type (

*asset\_type\_id : int* , *name : str | None = None* , *description : str | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.admin.AdminHelper.update_asset_type)

Updates an Asset type. asset\_type\_id needs to be a valid existing AssetType ID.

Parameters :

- **asset\_type\_id** - Asset type to update
- **name** - Name of the IOC type
- **description** - Description of the IOC type

Returns :

ApiResponse

update\_case\_classification (

*classification\_id : int* , *name : str | None = None* , *name\_expanded : str | None = None* , *description : str | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.admin.AdminHelper.update_case_classification)

Updates a Case Classification. case\_classification\_id needs to be a valid existing CaseClassification ID.

Parameters :

- **classification\_id** - Case Classification to update
- **name** - Name of the Case Classification
- **name\_expanded** - Expanded name of the Case Classification
- **description** - Description of the Case Classification

Returns :

ApiResponse

update\_customer (

*customer\_id : int* , *customer\_name : str* ) [](#dfir_iris_client.admin.AdminHelper.update_customer)

Updates an existing customer. A customer can be updated if :

- customer\_id is a know customer ID in IRIS
- customer\_name is unique

Parameters :

- **customer\_id** - ID of the customer to update
- **customer\_name** - Customer name

Returns :

ApiResponse object

update\_group (

*group : str | int* , *group\_name : str | None = None* , *group\_description : str | None = None* , *group\_permissions : List [* [*Permissions*](helpers.html#dfir_iris_client.helper.authorization.Permissions) *] | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.admin.AdminHelper.update_group)

Update a group. Cases access and members can be with set\_group\_access and set\_group\_members methods. Permissions must be a list of known

permissions from the Permission enum.

Parameters :

- **group** - Group ID or group name
- **group\_name** - Name of the group
- **group\_description** - Description of the group
- **group\_permissions** - List of permission from Permission enum

Returns :

ApiResponse object

update\_group\_cases\_access (

*group : str | int* , *cases\_list : List [ int ]* , *access\_level :* [*CaseAccessLevel*](helpers.html#dfir_iris_client.helper.authorization.CaseAccessLevel) , *auto\_follow : bool = False* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.admin.AdminHelper.update_group_cases_access)

Update the cases access of a group. Cases access must be a list of case IDs. access\_level must be

a CaseAccessLevel enum.

If auto\_follow is True, the cases will be automatically added to the group when they are created.

Parameters :

- **group** - Group ID or group name
- **cases\_list** - List of case IDs
- **access\_level** - CaseAccessLevel enum
- **auto\_follow** - Set to true to auto follow cases new cases

Returns :

ApiResponse object

update\_group\_members (

*group : str | int* , *members : List [ int ]* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.admin.AdminHelper.update_group_members)

Update the members of a group. Members must be a list of user IDs.

Parameters :

- **group** - Group ID or group name
- **members** - List of user IDs

Returns :

ApiResponse object

update\_ioc\_type (

*ioc\_type\_id : int* , *name : str | None = None* , *description : str | None = None* , *taxonomy : str | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.admin.AdminHelper.update_ioc_type)

Updates an IOC type. ioc\_type\_id needs to be a valid existing IocType ID.

Parameters :

- **ioc\_type\_id** - IOC type to update
- **name** - Name of the IOC type
- **description** - Description of the IOC type
- **taxonomy** - Taxonomy of the IOC Type

Returns :

ApiResponse

update\_user (

*user : int | str* , *login : str | None = None* , *name : str | None = None* , *password : str | None = None* , *email : str | None = None* , *** kwargs* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.admin.AdminHelper.update_user)

Updates a user. The user can be updated if :

- login is unique
- email is unique
- password meets the requirements of IRIS

Only set the parameters that needs to be updated.

Parameters :

- **user** - User ID or login to update
- **login** - Login of the user
- **name** - Full name of the user
- **password** - Password of the user
- **email** - Email of the user

Returns :

ApiResponse

update\_user\_cases\_access (

*user : int | str* , *cases\_list : List [ int ]* , *access\_level :* [*CaseAccessLevel*](helpers.html#dfir_iris_client.helper.authorization.CaseAccessLevel) ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.admin.AdminHelper.update_user_cases_access)

Updates the cases that a user can access.

Parameters :

- **user** - User ID or login to update
- **cases\_list** - List of case IDs
- **access\_level** - Access level to set for the user

Returns :

ApiResponse