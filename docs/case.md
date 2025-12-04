# [Case ](#module-dfir_iris_client.case)

*class* dfir\_iris\_client.case. Case ( *session :* [*ClientSession*](session.html#dfir_iris_client.session.ClientSession) , *case\_id : int | None = None* ) [](#dfir_iris_client.case.Case)

Handles the case methods

add\_asset (

*name : str* , *asset\_type : str | int* , *analysis\_status : str | int* , *compromise\_status : str | int | None = None* , *tags : List [ str ] | None = None* , *description : str | None = None* , *domain : str | None = None* , *ip : str | None = None* , *additional\_info : str | None = None* , *ioc\_links : List [ int ] | None = None* , *custom\_attributes : dict | None = None* , *cid : int | None = None* , *** kwargs* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.add_asset)

Adds an asset to the target case id.

If they are strings, asset\_types and analysis\_status are lookup-ed up before the addition request is issued.

Both can be either a name or an ID. For performances prefer an ID as they're used directly in the request

without prior lookup.

Custom\_attributes is an undefined structure when the call is made. This method does not

allow to push a new attribute structure. The submitted structure must follow the one defined

by administrators in the UI otherwise it is ignored.

Parameters :

- **name** - Name of the asset to add
- **asset\_type** - Name or ID of the asset type
- **description** - Description of the asset
- **compromise\_status** - Compromise status of the asset
- **domain** - Domain of the asset
- **ip** - IP of the asset
- **additional\_info** - Additional information,
- **analysis\_status** - Status of the analysis
- **tags** - List of tags
- **ioc\_links** - List of IOC to link to this asset
- **custom\_attributes** - Custom attributes of the asset
- **kwargs** - Additional arguments to pass to the API
- **cid** - int - Case ID

Returns :

APIResponse

add\_asset\_comment (

*asset\_id : int* , *comment : str* , *cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.add_asset_comment)

Adds a comment to an asset.

Parameters :

- **asset\_id** - int - Asset ID
- **comment** - str - Comment
- **cid** - int - Case ID

Returns :

APIResponse object

add\_case (

*case\_name : str* , *case\_description : str* , *case\_customer : str | int* , *case\_classification : str | int* , *soc\_id : str* , *custom\_attributes : dict | None = None* , *create\_customer = False* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.add_case)

Creates a new case. If create\_customer is set to true and the customer doesn't exist,

it is created. Otherwise an error is returned.

Custom\_attributes is an undefined structure when the call is made. This method does not

allow to push a new attribute structure. The submitted structure must follow the one defined

by administrators in the UI otherwise it is ignored.

Parameters :

- **case\_name** - case\_name
- **case\_classification** - Classification of the case
- **case\_description** - Description of the case
- **case\_customer** - Name or ID of the customer
- **soc\_id** - SOC Number
- **custom\_attributes** - Custom attributes of the case
- **create\_customer** - Set to true to create the customer is doesn't exists. (Default value = False)

Returns :

ApiResponse object

add\_ds\_file (

*parent\_id : int* , *file\_stream : BinaryIO* , *filename : str* , *file\_description : str* , *file\_is\_ioc : bool = False* , *file\_is\_evidence : bool = False* , *file\_password : str | None = None* , *file\_tags : list [ str ] | None = None* , *cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.add_ds_file)

Adds a file to the Datastore.

Parameters :

- **file\_stream** - BinaryIO - File stream to upload
- **filename** - str - File name
- **file\_description** - str - File description
- **file\_is\_ioc** - bool - Is the file an IOC
- **file\_is\_evidence** - bool - Is the file an evidence
- **parent\_id** - int - Parent ID
- **file\_password** - str - File password
- **file\_tags** - str - File tags
- **cid** - int - Case ID

Returns :

APIResponse object

add\_ds\_folder (

*parent\_id : int* , *folder\_name : str* , *cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.add_ds_folder)

Adds a folder to the Datastore.

Parameters :

- **parent\_id** - int - Parent ID
- **folder\_name** - str - Folder name
- **cid** - int - Case ID

Returns :

APIResponse object

add\_event (

*title : str* , *date\_time : datetime* , *content : str | None = None* , *raw\_content : str | None = None* , *source : str | None = None* , *linked\_assets : list | None = None* , *linked\_iocs : list | None = None* , *category : str | int | None = None* , *tags : list | None = None* , *color : str | None = None* , *display\_in\_graph : bool | None = None* , *display\_in\_summary : bool | None = None* , *custom\_attributes : str | None = None* , *timezone\_string : str | None = None* , *sync\_ioc\_with\_assets : bool = False* , *cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.add_event)

Adds a new event to the timeline.

If it is a string, category is lookup-ed up before the addition request is issued.

it can be either a name or an ID. For performances prefer an ID as it is used directly in the request

without prior lookup.

Custom\_attributes is an undefined structure when the call is made. This method does not

allow to push a new attribute structure. The submitted structure must follow the one defined

by administrators in the UI otherwise it is ignored.

Parameters :

- **title** - Title of the event
- **date\_time** - Datetime of the event, including timezone
- **content** - Content of the event (displayed in timeline on GUI)
- **raw\_content** - Raw content of the event (displayed in detailed event on GUI)
- **source** - Source of the event
- **linked\_assets** - List of assets to link with this event
- **linked\_iocs** - List of IOCs to link with this event
- **category** - Category of the event (MITRE [ATT @ CK](mailto:ATT%40CK) )
- **color** - Left border of the event in the timeline
- **display\_in\_graph** - Set to true to display in graph page - Default to true
- **display\_in\_summary** - Set to true to display in Summary - Default to false
- **tags** - A list of strings to add as tags
- **custom\_attributes** - Custom attributes of the event
- **timezone\_string** - Timezone in format +XX:XX or -XX:XX. If none, +00:00 is used
- **sync\_ioc\_with\_assets** - Set to true to sync the IOC with the assets
- **cid** - Case ID

Returns :

APIResponse object

add\_event\_comment (

*event\_id : int* , *comment : str* , *cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.add_event_comment)

Adds a comment to an event.

Parameters :

- **event\_id** - int - Event ID
- **comment** - str - Comment
- **cid** - int - Case ID

Returns :

APIResponse object

add\_evidence (

*filename : str* , *file\_size : int* , *description : str | None = None* , *file\_hash : str | None = None* , *custom\_attributes : dict | None = None* , *cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.add_evidence)

Adds a new evidence to the target case.

Custom\_attributes is an undefined structure when the call is made. This method does not

allow to push a new attribute structure. The submitted structure must follow the one defined

by administrators in the UI otherwise it is ignored.

Parameters :

- **filename** - name of the evidence
- **file\_size** - Size of the file
- **description** - Description of the evidence
- **file\_hash** - hash of the evidence
- **custom\_attributes** - Custom attributes of the evidences
- **cid** - Case ID

Returns :

APIResponse object

add\_evidence\_comment (

*evidence\_id : int* , *comment : str* , *cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.add_evidence_comment)

Adds a comment to an evidence.

Parameters :

- **evidence\_id** - int - Evidence ID
- **comment** - str - Comment
- **cid** - int - Case ID

Returns :

APIResponse object

add\_global\_task (

*title : str* , *status : str | int* , *assignee : str | int* , *description : str | None = None* , *tags : list | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.add_global_task)

Adds a new task.

If set as strings, status and assignee are lookup-ed up before the addition request is issued.

Both can be either a name or an ID. For performances prefer an ID as it is used directly in the request

without prior lookup.

Parameters :

- **title** - Title of the task
- **description** - Description of the task
- **assignee** - Assignee ID or username
- **tags** - Tags of the task
- **status** - String or status ID, need to be a valid status

Returns :

APIResponse object

add\_ioc (

*value : str* , *ioc\_type : str | int* , *description : str | None = None* , *ioc\_tlp : str | int | None = None* , *ioc\_tags : list | None = None* , *custom\_attributes : dict | None = None* , *cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.add_ioc)

Adds an ioc to the target case id.

If they are strings, ioc\_tlp and ioc\_type are lookup-ed up before the addition request is issued.

Both can be either a name or an ID. For performances prefer an ID as they're used directly in the request

without prior lookup.

Custom\_attributes is an undefined structure when the call is made. This method does not

allow to push a new attribute structure. The submitted structure must follow the one defined

by administrators in the UI otherwise it is ignored.

Parameters :

- **value** - Value of the IOC
- **ioc\_type** - Type of IOC, either name or type ID
- **description** - Optional - Description of the IOC
- **ioc\_tlp** - TLP name or tlp ID. Default is orange
- **ioc\_tags** - List of tags to add
- **custom\_attributes** - Custom attributes of the ioc
- **cid** - Case ID

Returns :

APIResponse

add\_ioc\_comment (

*ioc\_id : int* , *comment : str* , *cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.add_ioc_comment)

Adds a comment to an ioc.

Parameters :

- **ioc\_id** - int - IOC ID
- **comment** - str - Comment
- **cid** - int - Case ID

Returns :

APIResponse object

add\_note (

*note\_title : str* , *note\_content : str* , *group\_id : int* , *custom\_attributes : dict | None = None* , *cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.add_note)

Creates a new note. Case ID and group note ID need to match the case in which the note is stored.

Custom\_attributes is an undefined structure when the call is made. This method does not

allow to push a new attribute structure. The submitted structure must follow the one defined

by administrators in the UI otherwise it is ignored.

Parameters :

- **cid** - Case ID
- **note\_title** - Title of the note
- **note\_content** - Content of the note
- **group\_id** - Target group to attach the note to
- **custom\_attributes** - Custom attributes of the note

Returns :

APIResponse object

add\_note\_comment (

*note\_id : int* , *comment : str* , *cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.add_note_comment)

Adds a comment to a note.

Parameters :

- **note\_id** - int - Note ID
- **comment** - str - Comment
- **cid** - int - Case ID

Returns :

APIResponse object

add\_notes\_group (

*group\_title : str | None = None* , *cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.add_notes_group)

Creates a new notes group in the target cid case.

Group\_title can be an existing group, there is no uniqueness.

Parameters :

- **cid** - Case ID
- **group\_title** - Name of the group to add

Returns :

APIResponse object

add\_task (

*title : str* , *status : str | int* , *assignees : List [ str | int ]* , *description : str | None = None* , *tags : list | None = None* , *custom\_attributes : dict | None = None* , *cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.add_task)

Adds a new task to the target case.

If they are strings, status and assignee are lookup-ed up before the addition request is issued.

Both can be either a name or an ID. For performances prefer an ID as they're used directly in the request

without prior lookup.

Custom\_attributes is an undefined structure when the call is made. This method does not

allow to push a new attribute structure. The submitted structure must follow the one defined

by administrators in the UI otherwise it is ignored.

Parameters :

- **title** - Title of the task
- **description** - Description of the task
- **assignees** - List of assignees ID or username
- **cid** - Case ID
- **tags** - Tags of the task
- **status** - String or status ID, need to be a valid status
- **custom\_attributes** - Custom attributes of the task

Returns :

APIResponse object

add\_task\_comment (

*task\_id : int* , *comment : str* , *cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.add_task_comment)

Adds a comment to a task.

Parameters :

- **task\_id** - int - Task ID
- **comment** - str - Comment
- **cid** - int - Case ID

Returns :

APIResponse object

add\_task\_log (

*message : str* , *cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.add_task_log)

Adds a new task log that will appear under activities

Parameters :

- **message** - Message to log
- **cid** - Case ID

Returns :

ApiResponse

asset\_exists (

*asset\_id : int* , *cid : int | None = None* ) → bool [](#dfir_iris_client.case.Case.asset_exists)

Returns true if asset\_id exists in the context of the current case or cid.

This method is an overlay of get\_asset and thus not performant.

Parameters :

- **asset\_id** - Asset to lookup
- **cid** - Case ID

Returns :

True if exists else false

case\_id\_exists (

*cid : int* ) → bool [](#dfir_iris_client.case.Case.case_id_exists)

Checks if a case id is valid by probing the summary endpoint.

This method returns true if the probe was successful. If False is returned

it might not indicate the case doesn't exist but might be the result of a request malfunction

(server down, invalid API token, etc).

Parameters :

**cid** - Case ID to check

Returns :

True if case ID exists otherwise false

close\_case (

*case\_id : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.close_case)

Closes a case based on its ID

Parameters :

**case\_id** - Case ID to close

Returns :

ApiResponse

delete\_asset (

*asset\_id : int* , *cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.delete_asset)

Deletes an asset identified by asset\_id. CID must match the case in which the asset is stored.

Parameters :

- **asset\_id** - ID of the asset to delete
- **cid** - Case ID

Returns :

APIResponse object

delete\_asset\_comment (

*asset\_id : int* , *comment\_id : int* , *cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.delete_asset_comment)

Deletes a comment of an asset.

Parameters :

- **asset\_id** - int - Asset ID
- **comment\_id** - int - Comment ID
- **cid** - int - Case ID

Returns :

APIResponse object

delete\_case (

*cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.delete_case)

Deletes a case based on its ID. All objects associated to the case are deleted. This includes :

- assets,
- iocs that are only referenced in this case
- notes
- summary
- events
- evidences
- tasklogs

Parameters :

**cid** - Case to delete

Returns :

ApiResponse

delete\_ds\_file (

*file\_id : int* , *cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.delete_ds_file)

Deletes a file from the Datastore.

Parameters :

- **file\_id** - int - File ID
- **cid** - int - Case ID

Returns :

APIResponse object

delete\_ds\_folder (

*folder\_id : int* , *cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.delete_ds_folder)

Deletes a folder from the Datastore.

Parameters :

- **folder\_id** - int - Folder ID
- **cid** - int - Case ID

Returns :

APIResponse object

delete\_event (

*event\_id : int* , *cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.delete_event)

Deletes an event from its ID. CID must match the case in which the event is stored

Parameters :

- **event\_id** - Event to delete
- **cid** - Case ID

Returns :

APIResponse object

delete\_event\_comment (

*event\_id : int* , *comment\_id : int* , *cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.delete_event_comment)

Deletes a comment of an event.

Parameters :

- **event\_id** - int - Event ID
- **comment\_id** - int - Comment ID
- **cid** - int - Case ID

Returns :

APIResponse object

delete\_evidence (

*evidence\_id : int* , *cid : int | None = None* ) [](#dfir_iris_client.case.Case.delete_evidence)

Deletes an evidence from its ID. evidence\_id needs to be an existing evidence in the target case.

Parameters :

- **evidence\_id** - int - Evidence to delete
- **cid** - int - Case ID

Returns :

APIResponse object

delete\_evidence\_comment (

*evidence\_id : int* , *comment\_id : int* , *cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.delete_evidence_comment)

Deletes a comment of an evidence.

Parameters :

- **evidence\_id** - int - Evidence ID
- **comment\_id** - int - Comment ID
- **cid** - int - Case ID

Returns :

APIResponse object

delete\_global\_task (

*task\_id : int* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.delete_global_task)

Deletes a global task from its ID. task\_id needs to be an existing task in the database.

Parameters :

**task\_id** - int - Task to delete

Returns :

APIResponse object

delete\_ioc (

*ioc\_id : int* , *cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.delete_ioc)

Deletes an IOC from its ID. CID must match the case in which the ioc is stored.

Parameters :

- **ioc\_id** - ID of the ioc
- **cid** - Case ID

Returns :

APIResponse object

delete\_ioc\_comment (

*ioc\_id : int* , *comment\_id : int* , *cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.delete_ioc_comment)

Deletes a comment of an ioc.

Parameters :

- **ioc\_id** - int - IOC ID
- **comment\_id** - int - Comment ID
- **cid** - int - Case ID

Returns :

APIResponse object

delete\_note (

*note\_id : int* , *cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.delete_note)

Deletes a note. note\_id needs to be a valid existing note in the target case.

Parameters :

- **cid** - Case ID
- **note\_id** - Name of the note to delete

Returns :

APIResponse object

delete\_note\_comment (

*note\_id : int* , *comment\_id : int* , *cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.delete_note_comment)

Deletes a comment of a note.

Parameters :

- **note\_id** - int - Note ID
- **comment\_id** - int - Comment ID
- **cid** - int - Case ID

Returns :

APIResponse object

delete\_notes\_group (

*group\_id : int* , *cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.delete_notes_group)

Deletes a notes group. All notes in the target groups are deleted ! There is not way to get the notes back.

Case ID needs to match the case where the group is stored.

Parameters :

- **cid** - Case ID
- **group\_id** - ID of the group

Returns :

APIResponse object

delete\_task (

*task\_id : int* , *cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.delete_task)

Deletes a task from its ID. CID must match the case in which the task is stored.

Parameters :

- **task\_id** - Task to delete
- **cid** - Case ID

Returns :

APIResponse object

delete\_task\_comment (

*task\_id : int* , *comment\_id : int* , *cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.delete_task_comment)

Deletes a comment of a task.

Parameters :

- **task\_id** - int - Task ID
- **comment\_id** - int - Comment ID
- **cid** - int - Case ID

Returns :

APIResponse object

download\_activity\_report (

*report\_id : int* , *cid : int | None = None* ) → Response [](#dfir_iris_client.case.Case.download_activity_report)

Download an activity report.

Parameters :

- **report\_id** - int - ID of the template report
- **cid** - int - Case ID

Returns :

Flask Response object

download\_ds\_file (

*file\_id : int* , *cid : int | None = None* ) → Response [](#dfir_iris_client.case.Case.download_ds_file)

Downloads a file from the Datastore.

Parameters :

- **file\_id** - int - File ID
- **cid** - int - Case ID

Returns :

APIResponse object

download\_investigation\_report (

*report\_id : int* , *cid : int | None = None* ) → Response [](#dfir_iris_client.case.Case.download_investigation_report)

Download an investigation report.

Parameters :

- **report\_id** - int - ID of the template report
- **cid** - int - Case ID

Returns :

Flask Response object

filter\_events (

*filter\_str : dict | None = None* , *cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.filter_events)

Returns a list of events from the timeline, filtered with the same query types used in

the UI.

Parameters :

- **filter\_str** - Filter the timeline as in the UI
- **cid** - Case ID

Returns :

APIResponse object

get\_asset (

*asset\_id : int* , *cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.get_asset)

Returns an asset information from its ID.

Parameters :

- **asset\_id** - ID of the asset to fetch
- **cid** - Case ID

Returns :

APIResponse object

get\_case (

*cid : int* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.get_case)

Gets an existing case from its ID

Parameters :

**cid** - CaseID to fetch

Returns :

ApiResponse object

get\_ds\_file\_info (

*file\_id : int* , *cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.get_ds_file_info)

Returns information from file of the Datastore.

Parameters :

- **file\_id** - int - File ID
- **cid** - int - Case ID

Returns :

APIResponse object

get\_event (

*event\_id : int* , *cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.get_event)

Returns an event from the timeline

Parameters :

- **event\_id** - ID of the event to fetch
- **cid** - Case ID

Returns :

APIResponse object

get\_evidence (

*evidence\_id : int* , *cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.get_evidence)

Returns an evidence from its ID. evidence\_id needs to be an existing evidence in the target case.

Parameters :

- **evidence\_id** - Evidence ID to lookup
- **cid** - Case ID

Returns :

APIResponse object

get\_global\_task (

*task\_id : int* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.get_global_task)

Returns a global task from its ID.

Parameters :

**task\_id** - Task ID to lookup

Returns :

APIResponse object

get\_ioc (

*ioc\_id : int* , *cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.get_ioc)

Returns an IOC.  ioc\_id needs to be an existing ioc in the provided case ID.

Parameters :

- **ioc\_id** - IOC ID
- **cid** - Case ID

Returns :

APIResponse object

get\_note (

*note\_id : int* , *cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.get_note)

Fetches a note. note\_id needs to be a valid existing note in the target case.

Parameters :

- **cid** - Case ID
- **note\_id** - ID of the note to fetch

Returns :

APIResponse object

get\_notes\_group (

*group\_id : int* , *cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.get_notes_group)

Returns a notes group based on its ID. The group ID needs to match the CID where it is stored.

Parameters :

- **group\_id** - Group ID to fetch
- **cid** - Case ID (Default value = None)

Returns :

APIResponse object

get\_summary (

*cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.get_summary)

Returns the summary of the specified case id.

Parameters :

**cid** - Case ID (Default value = None)

Returns :

APIResponse object

get\_task (

*task\_id : int* , *cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.get_task)

Returns a task from its ID. task\_id needs to be a valid task in the target case.

Parameters :

- **task\_id** - Task ID to lookup
- **cid** - Case ID

Returns :

APIResponse object

list\_asset\_comments (

*asset\_id : int* , *cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.list_asset_comments)

List comments of an asset.

Parameters :

- **asset\_id** - int - Asset ID
- **cid** - int - Case ID

Returns :

APIResponse object

list\_assets (

*cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.list_assets)

Returns a list of all assets of the target case.

Parameters :

**cid** - int - Case ID

Returns :

APIResponse

list\_cases ( ) →

[ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.list_cases)

Returns a list of all the cases

Returns :

ApiResponse

Args:

Returns:

list\_ds\_tree (

*cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.list_ds_tree)

Returns the tree of the Datastore

Parameters :

**cid** - Case ID

Returns :

APIResponse object

list\_event\_comments (

*event\_id : int* , *cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.list_event_comments)

List comments of an event.

Parameters :

- **event\_id** - int - Event ID
- **cid** - int - Case ID

Returns :

APIResponse object

list\_events (

*filter\_by\_asset : int = 0* , *cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.list_events)

Returns a list of events from the timeline. filter\_by\_asset can be used to return only the events

linked to a specific asset. In case the asset doesn't exist, an empty timeline is returned.

Parameters :

- **filter\_by\_asset** - Select the timeline of a specific asset by setting an existing asset ID
- **cid** - Case ID

Returns :

APIResponse object

list\_evidence\_comments (

*evidence\_id : int* , *cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.list_evidence_comments)

List comments of an evidence.

Parameters :

- **evidence\_id** - int - Evidence ID
- **cid** - int - Case ID

Returns :

APIResponse object

list\_evidences (

*cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.list_evidences)

Returns a list of evidences.

Parameters :

**cid** - Case ID

Returns :

ApiResponse object

list\_global\_tasks ( ) →

[ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.list_global_tasks)

Args:

Returns :

return: ApiResponse object

list\_ioc\_comments (

*ioc\_id : int* , *cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.list_ioc_comments)

List comments of an ioc.

Parameters :

- **ioc\_id** - int - IOC ID
- **cid** - int - Case ID

Returns :

APIResponse object

list\_iocs (

*cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.list_iocs)

Returns a list of all iocs of the target case.

Parameters :

**cid** - Case ID

Returns :

APIResponse

list\_note\_comments (

*note\_id : int* , *cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.list_note_comments)

List comments of a note.

Parameters :

- **note\_id** - int - Note ID
- **cid** - int - Case ID

Returns :

APIResponse object

list\_notes\_groups (

*cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.list_notes_groups)

Returns a list of notes groups of the target cid case

Parameters :

**cid** - Case ID (Default value = None)

Returns :

APIResponse object

list\_task\_comments (

*task\_id : int* , *cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.list_task_comments)

List comments of a task.

Parameters :

- **task\_id** - int - Task ID
- **cid** - int - Case ID

Returns :

APIResponse object

list\_tasks (

*cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.list_tasks)

Returns a list of tasks linked to the provided case.

Parameters :

**cid** - Case ID

Returns :

ApiResponse object

move\_ds\_file (

*file\_id : int* , *parent\_id : int* , *cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.move_ds_file)

Moves a file from a folder to another.

Parameters :

- **file\_id** - int - File ID
- **parent\_id** - int - New parent ID
- **cid** - int - Case ID

Returns :

APIResponse object

move\_ds\_folder (

*folder\_id : int* , *parent\_id : int* , *cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.move_ds_folder)

Moves a folder from a folder to another.

Parameters :

- **folder\_id** - int - Folder ID
- **parent\_id** - int - New parent ID
- **cid** - int - Case ID

Returns :

APIResponse object

rename\_ds\_folder (

*folder\_id : int* , *new\_name : str* , *cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.rename_ds_folder)

Renames a folder in the Datastore.

Parameters :

- **folder\_id** - int - Folder ID
- **new\_name** - str - New name
- **cid** - int - Case ID

Returns :

APIResponse object

reopen\_case (

*case\_id : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.reopen_case)

Reopens a case based on its ID

Parameters :

**case\_id** - Case ID to open

Returns :

ApiResponse

search\_notes (

*search\_term : str* , *cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.search_notes)

Searches in notes. Case ID and group note ID need to match the case in which the notes are stored.

Only the titles and notes ID of the matching notes are return, not the actual content.

Use % for wildcard.

Parameters :

- **cid** - int - Case ID
- **search\_term** - str - Term to search in notes

Returns :

APIResponse object

set\_case\_outcome\_status (

*outcome\_status : str | int* , *case\_id : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.set_case_outcome_status)

Sets the outcome status of a case

Parameters :

- **case\_id** - ID of the case to update
- **outcome\_status** - Outcome status to set

Returns :

ApiResponse object

set\_cid (

*cid : int* ) → bool [](#dfir_iris_client.case.Case.set_cid)

Sets the current cid for the Case instance.

It can be override be setting the cid of each method though not recommended to keep consistency.

Parameters :

**cid** - Case ID

Returns :

Always true

set\_summary (

*summary\_content : str | None = None* , *cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.set_summary)

Sets the summary of the specified case id.

!!! warning

This completely replace the current content of the summary. Any co-worker working on the summary

will receive an overwrite order from the server. The order is immediately received by web socket. This method

should probably be only used when setting a new case.

Parameters :

- **summary\_content** - Content of the summary to push. This will completely replace the current content (Default value = None)
- **cid** - Case ID (Default value = None)

Returns :

APIResponse object

trigger\_manual\_hook (

*hook\_ui\_name : str* , *module\_name : str* , *targets : list* , *target\_type : str* , *cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.trigger_manual_hook)

Triggers a module hook call. These can only be used with manual hooks. The request is sent to the target

module and processed asynchronously. The server replies immediately after queuing the task. Success feedback

from this endpoint does not implies the hook processing was successful.

Parameters :

- **hook\_ui\_name** - Hook name, as defined by the module on the UI
- **module\_name** - Module associated with the hook name
- **targets** - List of IDs of objects to be processed
- **target\_type** - Target type of targets
- **cid** - Case ID

Returns :

ApiResponse object

update\_asset (

*asset\_id : int* , *name : str | None = None* , *asset\_type : str | int | None = None* , *tags : List [ str ] | None = None* , *analysis\_status : str | int | None = None* , *description : str | None = None* , *domain : str | None = None* , *ip : str | None = None* , *additional\_info : str | None = None* , *ioc\_links : List [ int ] | None = None* , *compromise\_status : str | int | None = None* , *custom\_attributes : dict | None = None* , *cid : int | None = None* , *no\_sync = False* , *** kwargs* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.update_asset)

Updates an asset. asset\_id needs to be an existing asset in the target case cid.

If they are strings, asset\_types and analysis\_status are lookup-ed up before the addition request is issued.

Both can be either a name or an ID. For performances prefer an ID as they're used directly in the request

without prior lookup.

Custom\_attributes is an undefined structure when the call is made. This method does not

allow to push a new attribute structure. The submitted structure must follow the one defined

by administrators in the UI otherwise it is ignored.

Parameters :

- **asset\_id** - ID of the asset to update
- **name** - Name of the asset
- **asset\_type** - Name or ID of the asset type
- **tags** - List of tags
- **description** - Description of the asset
- **domain** - Domain of the asset
- **ip** - IP of the asset
- **additional\_info** - Additional information,
- **analysis\_status** - Status of the analysis
- **ioc\_links** - List of IOC to link to this asset
- **compromise\_status** - Status of the compromise
- **custom\_attributes** - Custom attributes of the asset
- **cid** - Case ID

Returns :

APIResponse

update\_asset\_comment (

*asset\_id : int* , *comment\_id : int* , *comment : str* , *cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.update_asset_comment)

Updates a comment of an asset.

Parameters :

- **asset\_id** - int - Asset ID
- **comment\_id** - int - Comment ID
- **comment** - str - Comment
- **cid** - int - Case ID

Returns :

APIResponse object

update\_case (

*case\_id : int | None = None* , *case\_name : str | None = None* , *case\_description : str | None = None* , *case\_classification : str | int | None = None* , *case\_owner : str | int | None = None* , *soc\_id : str | None = None* , *case\_tags : List [ str ] | None = None* , *custom\_attributes : dict | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.update_case)

Updates an existing case. If create\_customer is set to true and the customer doesn't exist,

it is created. Otherwise, an error is returned.

Custom\_attributes is an undefined structure when the call is made. This method does not

allow to push a new attribute structure. The submitted structure must follow the one defined

by administrators in the UI otherwise it is ignored.

If a value is not provided, it is not updated.

Parameters :

- **case\_id** - ID of the case to update
- **case\_name** - case\_name
- **case\_description** - Description of the case
- **case\_classification** - Classification of the case
- **case\_tags** - List of tags to add to the case
- **case\_owner** - Name or ID of the owner
- **soc\_id** - SOC Number
- **custom\_attributes** - Custom attributes of the case

Returns :

ApiResponse object

update\_ds\_file (

*file\_id : int* , *file\_name : str | None = None* , *file\_description : str | None = None* , *file\_is\_ioc : bool = False* , *file\_is\_evidence : bool = False* , *file\_password : str | None = None* , *file\_tags : list [ str ] | None = None* , *cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.update_ds_file)

Updates a file in the Datastore.

Parameters :

- **file\_id** - int - File ID
- **file\_name** - str - File name
- **file\_description** - str - File description
- **file\_is\_ioc** - bool - Is the file an IOC
- **file\_is\_evidence** - bool - Is the file an evidence
- **file\_password** - str - File password
- **file\_tags** - str - File tags
- **cid** - int - Case ID

Returns :

APIResponse object

update\_event (

*event\_id : int* , *title : str | None = None* , *date\_time : datetime | None = None* , *content : str | None = None* , *raw\_content : str | None = None* , *source : str | None = None* , *linked\_assets : list | None = None* , *linked\_iocs : list | None = None* , *category : str | int | None = None* , *tags : list | None = None* , *color : str | None = None* , *display\_in\_graph : bool | None = None* , *display\_in\_summary : bool | None = None* , *custom\_attributes : dict | None = None* , *cid : int | None = None* , *timezone\_string : str | None = None* , *sync\_ioc\_with\_assets : bool = False* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.update_event)

Updates an event of the timeline. event\_id needs to be an existing event in the target case.

If it is a string, category is lookup-ed up before the addition request is issued.

it can be either a name or an ID. For performances prefer an ID as it is used directly in the request

without prior lookup.

Custom\_attributes is an undefined structure when the call is made. This method does not

allow to push a new attribute structure. The submitted structure must follow the one defined

by administrators in the UI otherwise it is ignored.

Parameters :

- **event\_id** - Event ID to update
- **title** - Title of the event
- **date\_time** - Datetime of the event, including timezone
- **content** - Content of the event (displayed in timeline on GUI)
- **raw\_content** - Raw content of the event (displayed in detailed event on GUI)
- **source** - Source of the event
- **linked\_assets** - List of assets to link with this event
- **linked\_iocs** - List of IOCs to link with this event
- **category** - Category of the event (MITRE [ATT @ CK](mailto:ATT%40CK) )
- **color** - Left border of the event in the timeline
- **display\_in\_graph** - Set to true to display in graph page - Default to true
- **display\_in\_summary** - Set to true to display in Summary - Default to false
- **tags** - A list of strings to add as tags
- **custom\_attributes** - Custom attributes of the event
- **timezone\_string** - Timezone in format +XX:XX or -XX:XX. If none, +00:00 is used
- **sync\_ioc\_with\_assets** - Set to true to sync the IOC with the assets
- **cid** - Case ID

Returns :

APIResponse object

update\_event\_comment (

*event\_id : int* , *comment\_id : int* , *comment : str* , *cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.update_event_comment)

Updates a comment of an event.

Parameters :

- **event\_id** - int - Event ID
- **comment\_id** - int - Comment ID
- **comment** - str - Comment
- **cid** - int - Case ID

Returns :

APIResponse object

update\_evidence (

*evidence\_id : int* , *filename : str | None = None* , *file\_size : int | None = None* , *description : str | None = None* , *file\_hash : str | None = None* , *custom\_attributes : dict | None = None* , *cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.update_evidence)

Updates an evidence of the matching case. evidence\_id needs to be an existing evidence in the target case.

Custom\_attributes is an undefined structure when the call is made. This method does not

allow to push a new attribute structure. The submitted structure must follow the one defined

by administrators in the UI otherwise it is ignored.

Parameters :

- **evidence\_id** - ID of the evidence
- **filename** - name of the evidence
- **file\_size** - Size of the file
- **description** - Description of the evidence
- **file\_hash** - hash of the evidence
- **custom\_attributes** - custom attributes of the evidences
- **cid** - Case ID

Returns :

APIResponse object

update\_evidence\_comment (

*evidence\_id : int* , *comment\_id : int* , *comment : str* , *cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.update_evidence_comment)

Updates a comment of an evidence.

Parameters :

- **evidence\_id** - int - Evidence ID
- **comment\_id** - int - Comment ID
- **comment** - str - Comment
- **cid** - int - Case ID

Returns :

APIResponse object

update\_global\_task (

*task\_id : int* , *title : str | None = None* , *status : str | int | None = None* , *assignee : str | int | None = None* , *description : str | None = None* , *tags : list | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.update_global_task)

Updates a task. task\_id needs to be an existing task in the database.

If they are strings, status and assignee are lookup-ed up before the addition request is issued.

Both can be either a name or an ID. For performances prefer an ID as they're used directly in the request

without prior lookup.

Parameters :

- **task\_id** - ID of the task to update
- **title** - Title of the task
- **description** - Description of the task
- **assignee** - Assignee ID or assignee username
- **tags** - Tags of the task
- **status** - String status, need to be a valid status

Returns :

APIResponse object

update\_ioc (

*ioc\_id : int* , *value : str | None = None* , *ioc\_type : str | int | None = None* , *description : str | None = None* , *ioc\_tlp : str | int | None = None* , *ioc\_tags : list | None = None* , *custom\_attributes : dict | None = None* , *cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.update_ioc)

Updates an existing IOC. ioc\_id needs to be an existing ioc in the provided case ID.

If they are strings, ioc\_tlp and ioc\_type are lookup-ed up before the addition request is issued.

Both can be either a name or an ID. For performances prefer an ID as they're used directly in the request

without prior lookup.

Custom\_attributes is an undefined structure when the call is made. This method does not

allow to push a new attribute structure. The submitted structure must follow the one defined

by administrators in the UI otherwise it is ignored.

Parameters :

- **ioc\_id** - IOC ID to update
- **value** - Value of the IOC
- **ioc\_type** - Type of IOC, either name or type ID
- **description** - Description of the IOC
- **ioc\_tlp** - TLP name or tlp ID. Default is orange
- **ioc\_tags** - List of tags to add,
- **custom\_attributes** - Custom attributes of the IOC
- **cid** - Case ID

Returns :

APIResponse object

update\_ioc\_comment (

*ioc\_id : int* , *comment\_id : int* , *comment : str* , *cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.update_ioc_comment)

Updates a comment of an ioc.

Parameters :

- **ioc\_id** - int - IOC ID
- **comment\_id** - int - Comment ID
- **comment** - str - Comment
- **cid** - int - Case ID

Returns :

APIResponse object

update\_note (

*note\_id : int* , *note\_title : str | None = None* , *note\_content : str | None = None* , *custom\_attributes : dict | None = None* , *cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.update_note)

Updates a note. note\_id needs to be a valid existing note in the target case.

Only the content of the set fields is replaced.

Custom\_attributes is an undefined structure when the call is made. This method does not

allow to push a new attribute structure. The submitted structure must follow the one defined

by administrators in the UI otherwise it is ignored.

Parameters :

- **cid** - Case ID
- **note\_id** - Name of the note to update
- **note\_content** - Content of the note
- **note\_title** - Title of the note
- **custom\_attributes** - Custom attributes of the note

Returns :

APIResponse object

update\_note\_comment (

*note\_id : int* , *comment\_id : int* , *comment : str* , *cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.update_note_comment)

Updates a comment of a note.

Parameters :

- **note\_id** - int - Note ID
- **comment\_id** - int - Comment ID
- **comment** - str - Comment
- **cid** - int - Case ID

Returns :

APIResponse object

update\_notes\_group (

*group\_id : int* , *group\_title : str* , *cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.update_notes_group)

Updates a notes group in the target cid case. group\_id need to be an existing group in the target case. group\_title can be an existing group, there is no uniqueness.

Parameters :

- **cid** - Case ID
- **group\_id** - Group ID to update
- **group\_title** - Name of the group

Returns :

APIResponse object

update\_task (

*task\_id : int* , *title : str | None = None* , *status : str | int | None = None* , *assignees : List [ str | int ] | None = None* , *description : str | None = None* , *tags : list | None = None* , *custom\_attributes : dict | None = None* , *cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.update_task)

Updates a task. task\_id needs to be a valid task in the target case.

If they are strings, status and assignee are lookup-ed up before the addition request is issued.

Both can be either a name or an ID. For performances prefer an ID as they're used directly in the request

without prior lookup.

Custom\_attributes is an undefined structure when the call is made. This method does not

allow to push a new attribute structure. The submitted structure must follow the one defined

by administrators in the UI otherwise it is ignored.

Parameters :

- **task\_id** - ID of the task to update
- **title** - Title of the task
- **description** - Description of the task
- **assignees** - List of assignee ID or assignee username
- **cid** - Case ID
- **tags** - Tags of the task
- **status** - String status, need to be a valid status
- **custom\_attributes** - Custom attributes of the task

Returns :

APIResponse object

update\_task\_comment (

*task\_id : int* , *comment\_id : int* , *comment : str* , *cid : int | None = None* ) → [ApiResponse](helpers.html#dfir_iris_client.helper.utils.ApiResponse) [](#dfir_iris_client.case.Case.update_task_comment)

Updates a comment of a task.

Parameters :

- **task\_id** - int - Task ID
- **comment\_id** - int - Comment ID
- **comment** - str - Comment
- **cid** - int - Case ID

Returns :

APIResponse object