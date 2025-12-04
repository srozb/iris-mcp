# [Helpers ](#module-dfir_iris_client.helper.analysis_status)

*class* dfir\_iris\_client.helper.analysis\_status. AnalysisStatusHelper ( *session* ) [](#dfir_iris_client.helper.analysis_status.AnalysisStatusHelper)

Handles the analysis status methods

get\_analysis\_status (

*analysis\_status\_id : int* ) → [ApiResponse](#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.helper.analysis_status.AnalysisStatusHelper.get_analysis_status)

Returns an analysis status from its ID

Parameters :

**analysis\_status\_id** - Status ID to lookup

Returns :

ApiResponse object

list\_analysis\_status\_types ( ) →

[ApiResponse](#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.helper.analysis_status.AnalysisStatusHelper.list_analysis_status_types)

Returns a list of all analysis statuses

Args:

Returns :

APIResponse object

lookup\_analysis\_status\_name (

*analysis\_status\_name : str* ) → int | None [](#dfir_iris_client.helper.analysis_status.AnalysisStatusHelper.lookup_analysis_status_name)

Returns an analysis status ID from its name otherwise None

Parameters :

**analysis\_status\_name** - str:

Returns :

Union[int, None] - analysis status ID matching provided analysis status name or None if not found

*class* dfir\_iris\_client.helper.assets\_type. AssetTypeHelper ( *session* ) [](#dfir_iris_client.helper.assets_type.AssetTypeHelper)

Handles the assets type methods

get\_asset\_type (

*asset\_type\_id : int* ) → [ApiResponse](#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.helper.assets_type.AssetTypeHelper.get_asset_type)

Returns an asset type data from its id

Parameters :

**asset\_type\_id** - ID of asset type to fetch

Returns :

ApiResponse

list\_asset\_types ( ) →

[ApiResponse](#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.helper.assets_type.AssetTypeHelper.list_asset_types)

Returns a list of all assets types available

Args:

Returns :

APIResponse object

lookup\_asset\_type\_name (

*asset\_type\_name : str* ) → int | None [](#dfir_iris_client.helper.assets_type.AssetTypeHelper.lookup_asset_type_name)

Returns an asset type ID from its name otherwise None

Raise :

Exception if server data is invalid

Parameters :

**asset\_type\_name** - Name of the asset type to lookup

Returns :

Asset type ID matching provided asset type name

Return type :

Union[int, None]

*class* dfir\_iris\_client.helper.authorization. CaseAccessLevel ( *value* ) [](#dfir_iris_client.helper.authorization.CaseAccessLevel)

An enumeration.

*class* dfir\_iris\_client.helper.authorization. Permissions ( *value* ) [](#dfir_iris_client.helper.authorization.Permissions)

An enumeration.

*class* dfir\_iris\_client.helper.case\_classifications. CaseClassificationsHelper ( *session* ) [](#dfir_iris_client.helper.case_classifications.CaseClassificationsHelper)

Handles the case classifications methods

get\_case\_classification (

*case\_classification\_id : int* ) → [ApiResponse](#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.helper.case_classifications.CaseClassificationsHelper.get_case_classification)

Returns a case classification from its ID

Parameters :

**case\_classification\_id** - Case classification ID

Returns :

APIResponse object

list\_case\_classifications ( ) →

[ApiResponse](#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.helper.case_classifications.CaseClassificationsHelper.list_case_classifications)

Returns a list of all case classifications

Args:

Returns :

APIResponse object

lookup\_case\_classification\_name (

*case\_classification\_name : str* ) → None | int [](#dfir_iris_client.helper.case_classifications.CaseClassificationsHelper.lookup_case_classification_name)

Returns a case\_classification\_name from its name otherwise None

Parameters :

**case\_classification\_name** - Case classification name to lookup

Returns :

case\_classification\_name matching provided case classification name otherwise none

Defines standard colors of events used in the GUI.

While custom color can be used, it's recommended to use the same

to keep consistency.

*class* dfir\_iris\_client.helper.compromise\_status. CompromiseStatusHelper ( *session* ) [](#dfir_iris_client.helper.compromise_status.CompromiseStatusHelper)

Handles the compromise status methods

list\_compromise\_status\_types ( )

[](#dfir_iris_client.helper.compromise_status.CompromiseStatusHelper.list_compromise_status_types)

Returns a list of all compromise statuses

lookup\_compromise\_status\_name (

*compromise\_status\_name : str* ) → int | None [](#dfir_iris_client.helper.compromise_status.CompromiseStatusHelper.lookup_compromise_status_name)

Returns a compromise status ID from its name otherwise None

Parameters :

**compromise\_status\_name** - str:

Returns :

Union[int, None] - compromise status ID matching provided analysis status name or None if not found

*class* dfir\_iris\_client.helper.errors. IrisStatus ( *message = None* , *data = None* , *uri = None* , *is\_error = False* ) [](#dfir_iris_client.helper.errors.IrisStatus)

Defines a custom status class, used by the abstraction layer

to communicate about API and operations feedbacks

Args:

Returns:

is\_error ( ) → bool

[](#dfir_iris_client.helper.errors.IrisStatus.is_error)

Simply return true if status is an error

Args:

Returns :

bool

is\_success ( ) → bool

[](#dfir_iris_client.helper.errors.IrisStatus.is_success)

Simply return true if status is a success

Returns :

True if status is a success

Args:

Returns :

bool

set\_error ( ) → None

[](#dfir_iris_client.helper.errors.IrisStatus.set_error)

Force the status to error

Args:

Returns :

None

set\_success ( ) → None

[](#dfir_iris_client.helper.errors.IrisStatus.set_success)

Force the status to success

Args:

Returns :

None

*class* dfir\_iris\_client.helper.errors. IrisStatusError ( *message = None* , *data = None* , *uri = None* ) [](#dfir_iris_client.helper.errors.IrisStatusError)

Overlay of IrisStatus, defining a base error status

*class* dfir\_iris\_client.helper.errors. IrisStatusSuccess ( *message = None* , *data = None* , *uri = None* ) [](#dfir_iris_client.helper.errors.IrisStatusSuccess)

Overlay of IrisStatus, defining a base success status

*class* dfir\_iris\_client.helper.events\_categories. EventCategoryHelper ( *session* ) [](#dfir_iris_client.helper.events_categories.EventCategoryHelper)

Handles the event category methods

get\_event\_category (

*event\_category\_id : int* ) → [ApiResponse](#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.helper.events_categories.EventCategoryHelper.get_event_category)

Returns an event category from its ID

Parameters :

**event\_category\_id** - Event category to lookup

Returns :

ApiResponse object

list\_events\_categories ( ) →

[ApiResponse](#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.helper.events_categories.EventCategoryHelper.list_events_categories)

Returns a list of all events categories available

Args:

Returns :

ApiResponse object

lookup\_event\_category\_name (

*event\_category : str* ) → None | int [](#dfir_iris_client.helper.events_categories.EventCategoryHelper.lookup_event_category_name)

Returns an event category ID from its name otherwise None

Parameters :

**event\_category** - Name of the event to lookup

Returns :

Event category ID matching provided event\_category name

Return type :

Union[None, int]

*class* dfir\_iris\_client.helper.ioc\_types. IocTypeHelper ( *session* ) [](#dfir_iris_client.helper.ioc_types.IocTypeHelper)

Handles the IOC types methods

get\_ioc\_type (

*ioc\_type\_id : int* ) → [ApiResponse](#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.helper.ioc_types.IocTypeHelper.get_ioc_type)

Returns an ioc type from its ID

Parameters :

**ioc\_type\_id** - Type ID to lookup

Returns :

ApiResponse object

list\_ioc\_types ( ) →

[ApiResponse](#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.helper.ioc_types.IocTypeHelper.list_ioc_types)

Returns a list of all ioc types

Args:

Returns :

APIResponse object

lookup\_ioc\_type\_name (

*ioc\_type\_name : str* ) → None | int [](#dfir_iris_client.helper.ioc_types.IocTypeHelper.lookup_ioc_type_name)

Returns an ioc\_type\_name from its name otherwise None

Parameters :

**ioc\_type\_name** - IOC type name to lookup

Returns :

ioc\_type\_name matching provided ioc type name otherwise none

Defines standard template types

*class* dfir\_iris\_client.helper.report\_template\_types. ReportTemplateLanguage ( *value* ) [](#dfir_iris_client.helper.report_template_types.ReportTemplateLanguage)

An enumeration.

*class* dfir\_iris\_client.helper.report\_template\_types. ReportTemplateType ( *value* ) [](#dfir_iris_client.helper.report_template_types.ReportTemplateType)

An enumeration.

*class* dfir\_iris\_client.helper.task\_status. TaskStatusHelper ( *session* ) [](#dfir_iris_client.helper.task_status.TaskStatusHelper)

Handles the analysis status methods

get\_task\_status (

*task\_status\_id : int* ) → [ApiResponse](#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.helper.task_status.TaskStatusHelper.get_task_status)

Returns a task status from its ID

Parameters :

**task\_status\_id** - int: Task ID to lookup

Returns :

ApiResponse object

list\_task\_status\_types ( ) →

[ApiResponse](#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.helper.task_status.TaskStatusHelper.list_task_status_types)

Returns a list of all tasks statuses

Args:

Returns :

ApiResponse

lookup\_task\_status\_name (

*task\_status\_name : str* ) → int | None [](#dfir_iris_client.helper.task_status.TaskStatusHelper.lookup_task_status_name)

Returns a task status ID from its name otherwise None

Parameters :

**task\_status\_name** - str: Task name to lookup

Returns :

Union[int, None] - task status ID matching provided task status name

*class* dfir\_iris\_client.helper.tlps. TlpHelper ( *session* ) [](#dfir_iris_client.helper.tlps.TlpHelper)

Handles the TLP methods

get\_tlp (

*tlp\_id : int* ) → [ApiResponse](#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.helper.tlps.TlpHelper.get_tlp)

Returns a tlp from its ID

Parameters :

**tlp\_id** - TLP ID to lookup

Returns :

ApiResponse object

list\_tlps ( ) →

[ApiResponse](#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.helper.tlps.TlpHelper.list_tlps)

Returns a list of all tlps available

Args:

Returns :

ApiResponse object

lookup\_tlp\_name (

*tlp\_name : str* ) → int | None [](#dfir_iris_client.helper.tlps.TlpHelper.lookup_tlp_name)

Returns a tlp ID from its name otherwise None

Returns :

tlp ID matching provided tlp name or None

Parameters :

**tlp\_name** - str: Name of the TLP

Returns :

Union[int, None]

*class* dfir\_iris\_client.helper.utils. ApiResponse ( *response : str | None = None* , *uri : str | None = None* ) [](#dfir_iris_client.helper.utils.ApiResponse)

Handles API returns and error. It parses the standard API returns and build an

standard ApiResponse object.

is\_error ( )

[](#dfir_iris_client.helper.utils.ApiResponse.is_error)

Returns :

Bool - True if return is error

is\_success ( )

[](#dfir_iris_client.helper.utils.ApiResponse.is_success)

Returns :

Bool - True if return is success

dfir\_iris\_client.helper.utils. ClientApiData (

*message = None* , *data = None* , *status = None* ) [](#dfir_iris_client.helper.utils.ClientApiData)

Parameters :

- **message** - (Default value = None)
- **data** - (Default value = None)
- **status** - (Default value = None)

Returns:

dfir\_iris\_client.helper.utils. ClientApiError (

*error = None* , *msg = None* ) [](#dfir_iris_client.helper.utils.ClientApiError)

Parameters :

- **error** - (Default value = None)
- **msg** - (Default value = None)

Returns:

dfir\_iris\_client.helper.utils. assert\_api\_resp (

*api\_response :* [*ApiResponse*](#dfir_iris_client.helper.utils.ApiResponse) , *soft\_fail = True* ) → [IrisStatus](#dfir_iris_client.helper.errors.IrisStatus) [](#dfir_iris_client.helper.utils.assert_api_resp)

Convert an ApiResponse to an IrisStatus for the overlay

Parameters :

- **api\_response** - ApiResponse: Object to assert
- **soft\_fail** - Set to false to raise exception (Default value = True)

Returns:

dfir\_iris\_client.helper.utils. get\_data\_from\_resp (

*api\_response :* [*ApiResponse*](#dfir_iris_client.helper.utils.ApiResponse) ) [](#dfir_iris_client.helper.utils.get_data_from_resp)

Returns the data of an ApiResponse object

Parameters :

**api\_response** - ApiResponse:

Returns:

dfir\_iris\_client.helper.utils. get\_iris\_session ( )

[](#dfir_iris_client.helper.utils.get_iris_session)

Return the global variable client session

Args:

Returns :

ClientSession

dfir\_iris\_client.helper.utils. map\_object (

*obj* , *data\_obj : dict* , *obj\_type = None* , *strict = False* ) → [IrisStatus](#dfir_iris_client.helper.errors.IrisStatus) [](#dfir_iris_client.helper.utils.map_object)

Map a Python IrisObject with a known Iris API return. The mapping is done

thanks to objects\_def. Each field is attributed to an attribute of the

provided obj.

The methods takes advantage of iris\_abj\_attribute and iris\_dynamic\_attribute to

preprocess data if needed.

Parameters :

- **obj** - Object where attributes need to be set
- **obj\_type** - Force the object type. Unused (Default value = None)
- **data\_obj** - Dict describing the data to set
- **strict** - Set to true to fail if an attribute is missing (Default value = False)

Returns :

IrisStatus

dfir\_iris\_client.helper.utils. parse\_api\_data (

*data : dict* , *path : list | str* , *strict = True* ) → any [](#dfir_iris_client.helper.utils.parse_api_data)

Parses the data field of an API response. Path describes a path to fetch a specific value in data.

If strict is set, an exception is raised, otherwise None is returned.

Parameters :

- **data** - Dict from the API response
- **path** - Value to get from within data
- **strict** - Set to true to fails if path is not found in data (default)

Returns :

ApiResponse