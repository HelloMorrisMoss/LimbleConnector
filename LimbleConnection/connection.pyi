from typing import List, Dict, Any, Optional, Union
import pandas as pd
from LimbleConnection.endpoint import LimbleEndpoint

class LimbleConnection(object):
    @property
    def me(self) -> MeNamespace:
        """
        Identifies the current customer. This route can be used to test that authentication to the Limble API was successful.
        
        Return data description

        Property | Description
        ----------------------
        customerName | The name of the customer that your API keys are valid for.
        customerPlan | The Limble plan the customer is currently subscribed to. The customerPlan can have one of following values:starterprofessionalbusinessenterpriselegacy - The plan the customer is currently subscribed to has been deprecated.For more information about various plans please visit the Limble website.
        """
        ...
    @property
    def assets(self) -> AssetsNamespace:
        """
        This request returns a list of Assets with top level information such as name, last edited, etc.
        
        **Note:** this endpoint supports pagination. Please refer to the [Pagination](#pagination) section for more information.
        
        Return data description

        Property | Description
        ----------------------
        meta | Requests to gather more information on an Asset such as Fields for the Asset or what Tasks are assigned to the Asset
        startedOn | The date when this Asset was started on. This property is used to help determine runtime which is used in MTBF.
        lastEdited | A UNIX timestamp of when this Asset was last edited.
        parentAssetID | The Asset that is the parent of this Asset. If the value is 0 that means this Asset does not have a parent.
        locationID | The ID of the location this asset is located at.
        hoursPerWeek | The number of hours this Asset runs per week. This is used to determine runtime which is used in MTBF. If the value is -1 then the Asset uses the Location's hoursPerWeek setting.
        workRequestPortal | The url work requestors can use to submit problems with this Asset.
        image | Array of objects that have a file name and a link you can use to download that image. All links are only valid for 15 minutes, a new call will generate a new link.
        geoLocation | The location of an asset on a Map.

        Query Parameters:
        - assets: This parameter is used to only get specific Assets. This parameter expects a comma delimited list of Asset IDs.
        - name: This is a parameter used to string search for a name or partial name of an asset this parameter expects a string with the wildcard %.
        - locations: This parameter is used to only get Assets at a specific group of Locations. This parameter accepts a comma delimited list of Location IDs.
        - start: This parameter is used to only get Assets that were last edited after the unix timestamp passed into the start parameter. For example, all Assets that were last edited after April 18th, 2018.
        - end: This parameter is used to only get Assets that were last edited *before* the unix timestamp passed into the end parameter.
        - cursor: This parameter is a cursor that selects what ID you want to start receiving results at. Without ordering, this will return results with an ID greater than the value of cursor. With ordering, this will return results starting at the next item in the order, regardless of whether its ID is greater than or lesser than the value of cursor.
        - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
        - parentAssetID: This parameter can be used to get asset(s) children using the Parent's ID. This parameter accepts a comma delimited list of Asset IDs.
        - orderBy: This parameter is used to order results by their lastEdited property instead of the default ordering by ascending assetID. CANNOT be provided alongside the cursor parameter. to paginate in this ordering, use the start or end parameters.
        - page: This parameter is used to paginate results based on the limit. Refer to Pagination section for more information.
        - geoLocation: This parameter is used to filter results that contain a geoLocation property. By default it is false and will return **all** assets with and without geoLocation property. If true, it will only return assets with a geoLocation property.
        """
        ...
    @property
    def locations(self) -> LocationsNamespace:
        """
        This request returns your Locations in Limble.
        
        **Note:** this endpoint supports pagination. Please refer to the [**Pagination**](https://desktop.postman.com/?desktopVersion=9.31.0&userId=16480856&teamId=206430) section for more information.
        
        **Note:** this endpoint supports pagination. Please refer to the [Pagination](https://desktop.postman.com/?desktopVersion=9.31.0&userId=16480856&teamId=206430) section for more information.
        
        EndFragment
        
        **Return data description**

        Property | Description
        ----------------------
        name | The name of the Location
        regionID | The ID of the region the Location is part of. A regionID of 0 means the location is not a part of any region.
        timezone | The Timezone the location is set at.List of Timezones
        weeklyOperationHours | The number of hours your Assets run at this location per week. This is used to help calculate MTBF.
        workRequestPortal | This is a URL you can use to submit Work Requests to this Location.
        geoLocation | The location of a Limble location on a Map.
        currencyCode | The ISO code for the currency at this location.

        Query Parameters:
        - locations: This parameter is used to only get locations in the list provided. This parameter accepts a comma delimited list of Location IDs.
        - name: This parameter is used to only get specific locations by name. This parameter expects a string full name of a location or partial name with the wildcard %.
        - cursor: This parameter is a cursor that selects what locationID you want to start receiving results at. e.g. passing 137 here will only get you locations with an id greater than 137.
        - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
        - regions: This parameter is used to get locations that belong to a region.
This parameter expects a regionID a location may belong to.
        - geoLocation: This parameter is used to filter results that contain a geoLocation property. By default it is false and will return **all** locations with and without geoLocation property. If true, it will only return locations with a geoLocation property.
        - page: 
        """
        ...
    @property
    def parts(self) -> PartsNamespace:
        """
        This request returns a list of Parts with top level information such as name, last edited, etc.
        
        **Note:** this endpoint supports pagination. Please refer to the [Pagination](#pagination) section for more information.
        
        Return data description

        Property | Description
        ----------------------
        number | The Part's Number. e.g. 25x25x1
        name | The Part's Name. e.g. Filter
        generalStock | How many of this Part you have in stock. Not including purchase orders.
        unitCode | The unit code displayed for the part. This represents the unit of measure assigned to the part (e.g., "kg", "lb", "each", etc.). If no unit is assigned, this field will be null.
        generalPrice | The default price of this part. Not considering purchase oder prices.
        category | The category this Part belongs to
        location | The Location of this Part. e.g. Shelf A
        minQtyStatus | Is the Part currently under the min quantity threshold. 0 = false, 1 = true.
        minQtyThreshold | The number at which reordering of this part is triggered. -1 means this feature is turned off.
        maxQtyThreshold | The number to bring the parts quantity back to. For example, if my inventory is at 4 and my maxQtyThreshold is 20 I will be reordering 16 parts to bring my inventory back up to the max quantity.
        staleThreshold | This value is how many days will need to go without a User using this Part by before this Part is considering stale.
        staleStatus | Is the Part stale or not. 0 = false, 1 = true.
        userID | The user that will receive threshold notifications and Tasks if thresholds are hit.
        team | The team that will receive threshold notifications and Tasks if thresholds are hit.
        stockOnHand | General Stock plus any unused, received PO Quantities for this part. This matches the 'Qty' value seen in the CMMS Part Management page.
        pos | Array of purchase order objects. price and quantity do not effect generalStock and generalPrice listed above.
        image | Array of objects that have a file name and a link you can use to download that image. All links are only valid for 15 minutes, a new call will generate a new link.

        Query Parameters:
        - parts: This parameter is used to only get specific Parts. This parameter accepts a comma delimited list of part IDs.
        - locations: This parameter is used to only get Parts at a specific group of Locations. This parameter accepts a comma delimited list of Location IDs.
        - name: This parameter is used to only get specific parts. This parameter expects a string either a full name of a part or a partial name with the wildcard %.
        - start: This parameter is used to only get Parts that were last edited after the unix timestamp passed into the start parameter. For example, all Parts that were last edited after April 18th, 2018.
        - end: This parameter is used to only get Parts that were last edited *before* the unix timestamp passed into the end parameter.
        - cursor: This parameter is a cursor that selects what partID you want to start receiving results at. e.g. passing 137 here will only get you parts with an id greater than 137.
        - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
        - numbers: This parameter is used to only get parts with part numbers that match the list provided. This parameter accepts a comma delimited list of Part Numbers.
        - page: This parameter is used to paginate results based on the limit. Refer to Pagination section for more information. 
        """
        ...
    @property
    def tasks(self) -> TasksNamespace:
        """
        This request gets top level information about Tasks such as completed date, assignment, assetID, etc.
        
        **Note:** this endpoint supports pagination. Please refer to the [Pagination](#pagination) section for more information.
        
        Return data description

        Property | Description
        ----------------------
        meta | This property has shortcuts to get other information related to the Task such as the Task's invoices, labor parts usage and instructions.
        name | The Task's name.
        userID | The id of the user this Task is assigned to. A Task can not be assigned to both a Team and a User at the same time.
        teamID | The id of the team this Task is assigned to. A Task can not be assigned to both a Team and a User at the same time.
        locationID | The id of the Location in which this Task belongs to.
        template | This field indicates if the task is a 'template' that spawns other tasks based on schedules or not.
        createdDate | The date this Task was created. This is a unix timestamp.
        startDate | By default this value is 0 as the startDate is usually the same as the createdDate. Sometimes a task is created such that it is scheduled to start in the future (i.e. after the createdDate). In such a case this value will be a unix timestamp indicating the actual start date of the Task.
        scheduledStart | The scheduled start date of the Task. This is a unix timestamp. A value of null means no scheduled start date is set.
        scheduledEnd | The scheduled end date of the Task. This is a unix timestamp. A value of null means no scheduled end date is set.
        due | The date this Task is due. This is a unix timestamp.
        dateCompleted | The date this Task was completed. This is a unix timestamp. A value of 0 means this Task is not completed.
        lastEdited | The date this Task was last edited. This is a unix timestamp.
        description | The decription of a task.
        completedByUser | The id of the User that completed this Task.
        lastEditedByUser | The id of the User that last edited the task.
        assetID | The id of the Asset that this Task belongs to.
        completedUserWage | The price per hour of the User's Wage at the point in time when the task was completed.
        priority | The priority of the Task.
        downtime | The amount of downtime in seconds caused by this Task.
        estimatedTime | The estimated time of the task. This is the time it takes to complete the task in minutes.
        completionNotes | Notes inputted by the user at the time of task completion.
        requestorName | The name of the person that requested this Task.
        requestorEmail | The email of the person that requested this Task.
        requestorPhone | The phone number of the person that requested this Task.
        requestTile | The title of the work request being submitted.
        requestField1 | Work request portal custom field 1.
        requestField2 | Work request portal custom field 2.
        requestField3 | Work request portal custom field 3.
        requestDropdown1 | Work request portal custom dropdown box 1.
        requestDropdown2 | Work request portal custom dropdown box 2.
        requestDropdown3 | Work request portal custom dropdown box 3.
        requestorDescription | The description of the request submitted via the Work Request portal.
        type | 1 = Preventative Maintanance (PM);2 = Unplanned Work Order (WO);4 = Planned Work Order (WO);5 = Cycle Count;6 = Work Request (WR);7 = Min Part Threshold;8 = Materials Request;
        status | 1 - Complete0 - IncompleteNote: this property indicates a task status with respect to task completion. For the custom task status refer to statusID
        statusID | The current custom status assigned to this task.Note: this indicates the current status of a task. Use GET Statuses to find the value of each statusID.
        poIDs | An array of Purchase Order IDs linked to this Task. Returns an empty array if no Purchase Orders are linked.
        associatedTaskID (deprecated) | Please refer to associatedTask meta property on GET Task Instruction for instruction type 14.
        meta1 | Task meta data. This does not show in the web application, but can be used to track items between integrated systems.
        meta2 | Task meta data. This does not show in the web application, but can be used to track items between integrated systems.
        meta3 | Task meta data. This does not show in the web application, but can be used to track items between integrated systems.
        geoLocation | The location of a task on a Map.
        customTags | An array of custom tags associated with the task.

        Query Parameters:
        - tasks: This parameter is used to only get specific Tasks. This parameter accepts a comma delimited list of task IDs.
        - assets: This parameter is used to only get Tasks that are linked to an asset. This parameter accepts a comma delimited list of asset IDs.
        - locations: This parameter is used to only get Tasks at a specific group of Locations. This parameter accepts a comma delimited list of Location IDs.
        - type: This parameter is used to only get Tasks of a specific type. This parameter accepts a comma delimited list of task types.
        - name: This is a parameter used to string search for a name or partial name of a task this parameter expects a string with the wildcard %.
        - start: This parameter is used to only get Tasks that were last edited after the unix timestamp passed into the start parameter. For example, all Tasks that were last edited after April 18th, 2018.
        - end: This parameter is used to only get Tasks that were last edited before the unix timestamp passed into the end parameter.
        - cursor: This parameter is a cursor that selects what taskID you want to start receiving results at. e.g. passing 137 here will only get you tasks with an id greater than 137.
        - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
        - page: This parameter is used to paginate results based on the limit. Refer to Pagination section for more information.
        - completedStart: This parameter is used to only get Tasks that were completed after the unix timestamp passed into this parameter. For example, all Assets that were completed after April 18th, 2018.
        - completedEnd: This parameter is used to only get Tasks that were completed before the unix timestamp passed into this parameter.
        - scheduledStart: This parameter is used as the start of a scheduled-date window. Tasks are returned when their scheduled date range overlaps this timestamp.
        - scheduledEnd: This parameter is used as the end of a scheduled-date window. Tasks are returned when their scheduled date range overlaps this timestamp.
        - orderBy: This parameter sorts based on the value you pass. Negative parameters are used to reverse sort order. This supports sorting by due, createdDate, dateCompleted, scheduledStart, scheduledEnd, and lastEdited.
        - geoLocation: This parameter is used to filter results that contain a geoLocation property. By default it is false and will return all tasks with and without geoLocation property. If true, it will only return tasks with a geoLocation property.
        - users: This parameter filters tasks by assignee user IDs. It returns tasks directly assigned to those users and tasks assigned through team/profile membership (including multi-user assignments). This parameter accepts a comma delimited list of user IDs.
        - teams: This parameter is used to only get Tasks assigned to specific teams/profiles. This parameter accepts a comma delimited list of team IDs.
        - lastEditedByUsers: This parameter is used to filter tasks by users who last edited the task.
        - status: This parameter is used to filter tasks by completed status. 1 - Complete  0 - Incomplete
        - meta1: This parameter is used to filter tasks by task meta data. This does not show in the web application, but can be used to track items between integrated systems.
        - meta2: This parameter is used to filter tasks by task meta data. This does not show in the web application, but can be used to track items between integrated systems.
        - meta3: This parameter is used to filter tasks by task meta data. This does not show in the web application, but can be used to track items between integrated systems.
        - statusIDs: This parameter is used to filter tasks by their associated statusID.
        - tag: This parameter is used to filter results that contain a certain custom tag. The tag must match exactly, i.e. "Tag" would not match "My Custom Tag". Searching for "@My Custom Tag;" is equivalent to searching for "My Custom Tag" but because custom tags are stored with an at sign ("@") at the beginning and a semicolon (";") at the end it is recommended that the param follows the same format.
        """
        ...
    @property
    def users(self) -> UsersNamespace:
        """
        This request gets information about Users such as User Login, User Email etc.
        
        Return data description

        Property | Description
        ----------------------
        username | What a User uses to login.
        wage | The hourly rate of an employee.
        active | Determines if a user can log into Limble or not.
        emailNotificationActive | Determines if a User gets Email Notifications From Limble.
        pushNotificationActive | Determines if a User gets Push Notifications From Limble.
        workdayHours | The number of hours a day this employee works.
        dateAdded | The date a user was added to Limble.  This is a unix timestamp.
        teams | What Teams a User has at specific Locations.

        Query Parameters:
        - users: This parameter expects a comma-separated list of users to get by id
        - name: This parameter is used to only get specific user by name. This parameter expects a string full name of a user or partial name with the wildcard %.
        - roles: This parameter expects a comma-separated list of users to get by roleID
        - teams: This parameter expects a comma-separated list of users to get by teamID
        - cursor: This parameter is a cursor that selects what userID you want to start receiving results at. e.g. passing 137 here will only get you tasks with an id greater than 137.
        - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
        """
        ...
    @property
    def vendors(self) -> VendorsNamespace:
        """
        This request gets information such as VendorIDs, Vendor Names, etc.
        
        This call returns a "meta" object containing URLs that can be used to get data related to a vendor.
        
        This call will also return an image array of objects that have a file name and a link you can use to download that image. All links are only valid for 15 minutes, a new call will generate a new link.
        
        **Note:** this endpoint supports pagination. Please refer to the [**Pagination**](#pagination) section for more information.

        Query Parameters:
        - vendors: This parameter is used to only get specific Vendors. This parameter expects a comma delimited list of Vendor IDs.
        - locations: This parameter is used to only get Vendors at a specific group of Locations. This parameter accepts a comma delimited list of Location IDs.
        - name: This parameter is used to only get specific vendor by name. This parameter expects a string full name of a vendor or partial name with the wildcard %.
        - start: This parameter is used to only get Vendors that were last edited after the unix timestamp passed into the start parameter. For example, all Vendors that were last edited after April 18th, 2018.
        - end: This parameter is used to only get Vendors that were last edited *before* the unix timestamp passed into the end parameter.
        - cursor: This parameter is a cursor that selects what vendorID you want to start receiving results at. e.g. passing 137 here will only get you vendors with an id greater than 137.
        - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
        - page: This parameter is used to paginate results based on the limit. Refer to Pagination section for more information.
        """
        ...
    @property
    def roles(self) -> RolesNamespace:
        """
        This request returns a list of Roles.

        Query Parameters:
        - roles: 
        - name: 
        - cursor: 
        - limit: 
        """
        ...
    @property
    def teams(self) -> TeamsNamespace:
        """
        This request returns a list of Teams.

        Query Parameters:
        - teams: This parameter expects a comma-separated list of teamIDs to filter teams by.
        - name: This parameter is used to only get specific teams by name. This parameter expects a string full name of a team or partial name with the wildcard %.
        - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
        - cursor: This parameter is a cursor that selects what teamID you want to start receiving results at. e.g. passing 137 here will only get you tasks with an id greater than 137.
        - automaticallyCreated: This parameter is used to only get specific teams by if they were automatically created by Limble or not. This parameter expects a bool true or false. Teams can get dynamically created if multiple users are assigned to the same task, for example.
        - includeRoles: This parameter is used to determine whether role-based teams (Manager, Technician, etc) are included in the response.
        """
        ...
    @property
    def purchase_orders(self) -> Purchase_ordersNamespace:
        """

        Property | Description
        ----------------------
        meta | useful links relating to this Purchase order
        poID | The unique ID of the Purchase Order.
        poNumber | The user-set Purchase Order number.
        budgetID | The unique ID of the budget associated with this Purchase Order.
        vendorID | The unique ID of the vendor associated with this Purchase Order.
        locationID | The unique ID of the location associated with this Purchase Order.
        userIDStarted | The unique ID of the user that started this Purchase Order.
        userID | The unique ID of the user this Purchase Order is currently assigned to.
        teamID | The unique ID of the team the user of this Purchase Order is currently assigned to.
        requestedByUserID | The userID of the user that request this Purchase Order. A value of 0 means this PO wasn't requested, but was manually started by the userIDStarted.
        date | The date this PO was started as a UNIX timestamp, or the date the user inputted for the Purchase Order.
        expectedDate | The date this PO is expected as a UNIX timestamp to receive items.
        billTo | The address that should receive the bill for the PO.
        shipTo | The address the PO's items should be delivered to.
        notesToVendor | Any notes sent to the vendor, possibly containing handling, packaging, or delivery instructions.
        customField1 | PO custom field, the customer chooses which custom fields are available on all POs.
        customField2 | PO custom field, the customer chooses which custom fields are available on all POs.
        customField3 | PO custom field, the customer chooses which custom fields are available on all POs.
        customField4 | PO custom field, the customer chooses which custom fields are available on all POs.
        customField5 | PO custom field, the customer chooses which custom fields are available on all POs.
        customField6 | PO custom field, the customer chooses which custom fields are available on all POs.
        poPrefix | If a PO prefix is configured, it will show up here.
        lastEdited | Last time this PO was edited as a UNIX timestamp.
        status | This is the current status of a PO. Status of PO can be as follows:0: the PO has only been setup. (Status: Setup)1-97: these are custom statuses based on the budget steps. Refer to "budgetSteps" in meta. (Status : {Name of the budgetStep it is on} )97: the PO is in the ready to receive step. This means items can be received for this PO. (Status: Ready to Receive)98 all budget steps have been completed, but not all items on the PO have been received. This means only some items or partial qty of items have been received. (Status: Partially Received)99: the PO is completed. This means all the items and their full qty on the PO have been received but not been paid for ( i.e. all the bills generated for this PO have not been marked as paid yet.) (Status: Fully Received - Pending Payment)100: the PO is closed. This means all the items on the PO have been received and have been paid for. (i.e. all the bills for this PO have been marked as paid.) (Status: Closed)
        stateDetails | JSON object containing details about the PO's current state, and available state transitions.
        poNumberDisplay | Formatted display string with leading zeros and prefix. This is the PO Number the UI will display.

        Query Parameters:
        - pos: This parameter is used to only get specific POs. This parameter expects a comma delimited list of PO IDs.
        - vendors: This parameter is used to only get specific Vendors. This parameter expects a comma delimited list of Vendor IDs.
        - locations: This parameter is used to only get POs at a specific group of Locations. This parameter accepts a comma delimited list of Location IDs.
        - numbers: This parameter is used to only get specific POs by Number. This parameter expects a comma delimited list of PO Numbers.
        - cursor: This parameter is a cursor that selects what poID you want to start receiving results at. e.g. passing 137 here will only get you PO with an id greater than 137.
        - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
        - lastEditedStart: This parameter is used to only get POs that were last edited after the unix timestamp passed into the start parameter. For example, all POs that were last edited after April 18th, 2018.
        - lastEditedEnd: This parameter is used to only get POs that were last edited *before* the unix timestamp passed in.
        - status: This parameter is used to only get POs for a specific group of status.
        - page: This parameter is used to paginate results based on the limit. Refer to Pagination section for more information.
        """
        ...
    @property
    def general_ledgers(self) -> General_ledgersNamespace:
        """
        This request returns your GLs in Limble.  
        
        Return data description

        Property | Description
        ----------------------
        glID | The GL's unique identifier.
        abbr | An abbreviation for the GL.
        name | The full name of the GL.
        locationID | Which Location this GL belongs to.
        description | An optional bit of descriptive text for the GL.
        assetID | Which Asset this GL belongs to.

        Query Parameters:
        - cursor: This parameter is a cursor that selects what glID you want to start receiving results at. e.g. passing 137 here will only get you GLs with an ID greater than 137.
        - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
        - name: This is a parameter used to string search for a name or partial name of a GL. This parameter expects a string with the wildcard %.
        - abbr: This is a parameter used to string search for an abbreviation or partial abbreviation of a GL. This parameter expects a string with the wildcard %.
        - locations: This parameter is used to only get GLs that are linked to a location. This parameter accepts a comma delimited list of location IDs.
        - gls: This parameter is used to only get specific GLs. This parameter accepts a comma delimited list of GL IDs.
        - assets: This parameter is used to only get GLs that are linked to an asset. This parameter accepts a comma delimited list of asset IDs.
        """
        ...
    @property
    def budgets(self) -> BudgetsNamespace:
        """
        This request returns your Budgets in Limble.  
        
        Return data description

        Property | Description
        ----------------------
        budgetID | The Budget's unique identifier.
        name | The full name of the Budget.
        locationID | Which Location this Budget belongs to.

        Query Parameters:
        - cursor: This parameter is a cursor that selects what budgetID you want to start receiving results at. e.g. passing 137 here will only get you budgets with an ID greater than 137.
        - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
        - name: This is a parameter used to string search for a name or partial name of a budget. This parameter expects a string with the wildcard %.
        - locations: This parameter is used to only get budgets that are linked to a location. This parameter accepts a comma delimited list of location IDs.
        - budgets: This parameter is used to only get specific budgets. This parameter accepts a comma delimited list of budget IDs.
        """
        ...
    @property
    def priorities(self) -> PrioritiesNamespace:
        """
        This request returns your priorities in Limble.  
        
        Return data description

        Property | Description
        ----------------------
        priorityID | The priority's unique identifier.
        name | The full name of the priority.
        priorityLevel | A number representing ordering or indicator of severity.
        color | A hex-color string that will be used to color tasks associated to this priority.
        isDefault | A boolean representing whether or not this is the priority that will be associated to tasks by default.

        Query Parameters:
        - priorities: 
        """
        ...
    @property
    def tags(self) -> TagsNamespace:
        """
        This request returns your tags in Limble.
        
        Return data description

        Property | Description
        ----------------------
        name | A search-string for tags.

        Query Parameters:
        - name: 
        """
        ...
    @property
    def statuses(self) -> StatusesNamespace:
        """
        This request returns your custom task statuses in Limble.
        
        Return data description

        Property | Description
        ----------------------
        statusID | A unique identifier for this status.
        name | A custom string that labels this status.
        description | An optional description that elaborates on what this status means.

        Query Parameters:
        - limit: 
        - cursor: 
        - name: 
        - statuses: 
        """
        ...
    @property
    def bills(self) -> BillsNamespace:
        """
        This request gets information such as Bill IDs, Bill Numbers, etc.
        
        This call returns a "meta" object containing URLs that can be used to get data related to the Bill.
        
        Note: this endpoint supports pagination. Please refer to the [**Pagination**](#pagination) section for more information.
        
        Return data description

        Property | Description
        ----------------------
        meta | useful links relating to this Bill
        billID | The unique ID of the Bill.
        billNumber | The bill number assigned to the Bill.
        poID | The poID of which the Bill was made.
        locationID | The unique ID of the location associated with this Bill.
        date | The date this Bill was created as a UNIX timestamp.
        status | The status of this Bill.
            The status can be as follows:
            0: The bill is setup.
            1: The bill is submitted.
            2: The bill is closed i.e. Marked as Paid
        userID | The Id of the user this Bill was assigned to.
        userIDStarted | The ID of the user this Bill was created by.
        userIDMarkPaid | The ID of the user this Bill was marked paid by.

        Query Parameters:
        - bills: This parameter is used to only get specific Bills. This parameter expects a comma delimited list of billIDs.
        - numbers: This parameter is used to only get specific Bills by Number. This parameter expects a comma delimited list of billNumbers.
        - status: This parameter is used to only get specific Bills by their status. The bill status could be 0,1 or 2

        - end: This parameter is used to only get Bills that were created before or on the unix timestamp passed into it. 
        - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
        - pos: This parameter is used to only get specific Bills by POs. This parameter expects a comma delimited list of PO IDs.
        - start: This parameter is used to only get Bills that were created after or on the unix timestamp passed into it. 
        - locations: This parameter is used to only get Bills at a specific group of Locations. This parameter accepts a comma delimited list of Location IDs.
        - cursor: This parameter is a cursor that selects what billID you want to start receiving results at. e.g. passing 130 here will only get you bills with an id greater than 130.
        - page: This parameter is used to paginate results based on the limit. Refer to Pagination section for more information.
        """
        ...
    @property
    def regions(self) -> RegionsNamespace:
        """
        This request returns your Regions in Limble.  
        
        Return data description

        Property | Description
        ----------------------
        regionID | The ID of the Region
        regionName | The name of the Region
        parentRegionID | The regionID of the parent of a region.

        Query Parameters:
        - regions: This parameter is used to only get regions in the list provided. This parameter accepts a comma delimited list of Region IDs.
        - name: This parameter is used to only get specific regions by name. This parameter expects a string- the full name of a region
 or partial name with the wildcard %.
        - cursor: This parameter is a cursor that selects what regionID you want to start receiving results at. e.g. passing 137 here will only get you regions
 with an id greater than 137.
        - limit: This parameter is a result limiter. The default is set to return no more than 100 
results at one time.
        """
        ...
    @property
    def webhooks(self) -> WebhooksNamespace:
        """
        This request returns your Webhooks configured for Limble.  
        
        Return data description

        Property | Description
        ----------------------
        webhhokID | The ID of the Webhook
        endpoint | The webhook URL.
        type | The type of webhook. Webhooks can be of type task, po, poItem.
        enabled | Determines if the webhook is enabled. 0 = Disabled 1=Enabled

        Query Parameters:
        - webhooks: This parameter is used to only get specific Webhooks. This parameter expects a comma delimited list of webhookIDs.
        - endpoint: This parameter is used for a string search by the webhook endpoint. This parameter expects a URL or partial URL of a webhook using a string with the wildcard %.
        - type: This parameter is used to only get Webhooks of a specific type. This parameter accepts a comma delimited list of webhook types.
        - enabled: This parameter is used to get Webooks which are enabled. This paramter expects 1: Enabled or 0: Disabled
        - cursor: This parameter is a cursor that selects what webhookID you want to start receiving results at. e.g. passing 10 here will only get you webhooks with an id greater than 10.
        - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
        """
        ...
    @property
    def units_of_measure(self) -> Units_of_measureNamespace: ...

class Units_of_measureNamespace(object):
    @property
    def get_units(self) -> Units_of_measureGet_unitsNamespace:
        """
        This endpoint makes an HTTP GET request to retrieve the unit of measurement (UOM) data. The response of this request is documented as a JSON schema.
        
        <p><b>Return data description</b></p>

        **Property** | **Description**
        ------------------------------
        unitCode | The identifier of this unit of measure. It is some random text for custom units (e.g. `j5VEKvW-TD8femkRe02KV`) and it is something semantic for provided units (e.g. `fluid_ounce`)
        name | The full name of a unit to make it clear what it is.
        abbreviation | The abbreviated name of a unit that is used for compact formatting such as `fl oz`. Can override the default abbreviation of a provided unit. E.g. if the default abbreviation of fluid ounce is `fl oz`, you can make it `oz.`
        defaultAbbreviation | This is always the same as abbreviation for custom units. For provided units, this never changes. If you choose to alias the abbreviation, this will show the original, and the abbreivation property will be your alias.
        category | Also known as the "physical quantity" of a unit, which tells you what exactly this is measuring. The possibilities are `volume`, `weight`, `length`, `count`. All custom units will have the category of `count`, as there is no way to setup custom conversion rates.
        isCustom | Boolean which tells you if this is a custom unit or provided unit.

        Query Parameters:
        - unitCodes: This parameter is used to only get specific units. This parameter accepts a comma delimited list of unit codes.
        - limit: This parameter is a result limiter. The default is 20 units and the max is 100.
        - page: This parameter is used to paginate results based on the limit. Refer to Pagination section for more information. 
        - nameStartsWith: Filter by units that have a name which starts with this string.
        - abbreviationStartsWith: Filter by units that have an abbreviation which starts with this string.
        """
        ...
    @property
    def create_unit(self) -> Units_of_measureCreate_unitNamespace:
        """
        The `POST /v2/uom` endpoint is used to create a new custom unit. The request should include a JSON payload with the `name` and `abbreviation` fields.
        
        ### Request Body
        
        - `name` (string): The full name of the unit.
            
        - `abbreviation` (string): A compact name of the unit.
            
        
        ### Response
        
        The full unit object of your newly created unit.
        """
        ...
    @property
    def update_unit(self) -> Units_of_measureUpdate_unitNamespace:
        """
        The HTTP PATCH request is used to update a specific unit identified by its unit code. The request should be made to the endpoint `{{protocol}}://{{server}}:{{port}}/v2/uom/:unitCode`, where `:unitCode` is the unique identifier of the unit being updated.
        
        ### Request Body
        
        The body is interpreted slightly differently, depending on whether the `unitCode` in the url is for a custom unit or a provided unit. If it is custom, then either property can be used to update the unit. If it is a provided unit, the `name` property will be ignored and only the `abbreviation` property will be used to override the defaut one. You can also use `null` to remove the override from the provided unit. If either property is `null` for a custom unit, that property will not be updated.
        
        The request should include a JSON payload with the following parameters:
        
        - `name` (string): The full name of the unit.
            
        - `abbreviation` (string): A compact name of the unit.
            
        
        ### Response
        
        The full object of the updated unit.
        """
        ...

class Units_of_measureUpdate_unitNamespace(LimbleEndpoint):
    """
    The HTTP PATCH request is used to update a specific unit identified by its unit code. The request should be made to the endpoint `{{protocol}}://{{server}}:{{port}}/v2/uom/:unitCode`, where `:unitCode` is the unique identifier of the unit being updated.
    
    ### Request Body
    
    The body is interpreted slightly differently, depending on whether the `unitCode` in the url is for a custom unit or a provided unit. If it is custom, then either property can be used to update the unit. If it is a provided unit, the `name` property will be ignored and only the `abbreviation` property will be used to override the defaut one. You can also use `null` to remove the override from the provided unit. If either property is `null` for a custom unit, that property will not be updated.
    
    The request should include a JSON payload with the following parameters:
    
    - `name` (string): The full name of the unit.
        
    - `abbreviation` (string): A compact name of the unit.
        
    
    ### Response
    
    The full object of the updated unit.
    """

class Units_of_measureCreate_unitNamespace(LimbleEndpoint):
    """
    The `POST /v2/uom` endpoint is used to create a new custom unit. The request should include a JSON payload with the `name` and `abbreviation` fields.
    
    ### Request Body
    
    - `name` (string): The full name of the unit.
        
    - `abbreviation` (string): A compact name of the unit.
        
    
    ### Response
    
    The full unit object of your newly created unit.
    """

class Units_of_measureGet_unitsNamespace(LimbleEndpoint):
    """
    This endpoint makes an HTTP GET request to retrieve the unit of measurement (UOM) data. The response of this request is documented as a JSON schema.
    
    <p><b>Return data description</b></p>

    **Property** | **Description**
    ------------------------------
    unitCode | The identifier of this unit of measure. It is some random text for custom units (e.g. `j5VEKvW-TD8femkRe02KV`) and it is something semantic for provided units (e.g. `fluid_ounce`)
    name | The full name of a unit to make it clear what it is.
    abbreviation | The abbreviated name of a unit that is used for compact formatting such as `fl oz`. Can override the default abbreviation of a provided unit. E.g. if the default abbreviation of fluid ounce is `fl oz`, you can make it `oz.`
    defaultAbbreviation | This is always the same as abbreviation for custom units. For provided units, this never changes. If you choose to alias the abbreviation, this will show the original, and the abbreivation property will be your alias.
    category | Also known as the "physical quantity" of a unit, which tells you what exactly this is measuring. The possibilities are `volume`, `weight`, `length`, `count`. All custom units will have the category of `count`, as there is no way to setup custom conversion rates.
    isCustom | Boolean which tells you if this is a custom unit or provided unit.

    Query Parameters:
    - unitCodes: This parameter is used to only get specific units. This parameter accepts a comma delimited list of unit codes.
    - limit: This parameter is a result limiter. The default is 20 units and the max is 100.
    - page: This parameter is used to paginate results based on the limit. Refer to Pagination section for more information. 
    - nameStartsWith: Filter by units that have a name which starts with this string.
    - abbreviationStartsWith: Filter by units that have an abbreviation which starts with this string.
    """

class WebhooksNamespace(LimbleEndpoint):
    """
    This request returns your Webhooks configured for Limble.  
    
    Return data description

    Property | Description
    ----------------------
    webhhokID | The ID of the Webhook
    endpoint | The webhook URL.
    type | The type of webhook. Webhooks can be of type task, po, poItem.
    enabled | Determines if the webhook is enabled. 0 = Disabled 1=Enabled

    Query Parameters:
    - webhooks: This parameter is used to only get specific Webhooks. This parameter expects a comma delimited list of webhookIDs.
    - endpoint: This parameter is used for a string search by the webhook endpoint. This parameter expects a URL or partial URL of a webhook using a string with the wildcard %.
    - type: This parameter is used to only get Webhooks of a specific type. This parameter accepts a comma delimited list of webhook types.
    - enabled: This parameter is used to get Webooks which are enabled. This paramter expects 1: Enabled or 0: Disabled
    - cursor: This parameter is a cursor that selects what webhookID you want to start receiving results at. e.g. passing 10 here will only get you webhooks with an id greater than 10.
    - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
    """
    @property
    def delete_webhook(self) -> WebhooksDelete_webhookNamespace:
        """
        This request deletes a Webhook.
        """
        ...
    @property
    def new_webhook(self) -> WebhooksNew_webhookNamespace:
        """
        This requests creates a new Webhook.

        Parameter | Type | Required? | Description
        ------------------------------------------
        endpoint | URL | Required | The webhook URL.
        type | String | Required | The type of webhook. Refer to GET webhooks for type values
        enabled | Int | Optional | Should the webhook be enabled or disabled. It is enabled(1) by default.
        """
        ...
    @property
    def update_webhook(self) -> WebhooksUpdate_webhookNamespace:
        """
        This requests updates a Webhook.

        Parameter | Type | Required? | Description
        ------------------------------------------
        endpoint | URL | Optional | The webhook URL.
        type | String | Optional | The type of webhook. Refer to GET webhooks for type values
        enabled | Int | Optional | Enable (1) or disable a webhook(0)
        """
        ...

class WebhooksUpdate_webhookNamespace(LimbleEndpoint):
    """
    This requests updates a Webhook.

    Parameter | Type | Required? | Description
    ------------------------------------------
    endpoint | URL | Optional | The webhook URL.
    type | String | Optional | The type of webhook. Refer to GET webhooks for type values
    enabled | Int | Optional | Enable (1) or disable a webhook(0)
    """

class WebhooksNew_webhookNamespace(LimbleEndpoint):
    """
    This requests creates a new Webhook.

    Parameter | Type | Required? | Description
    ------------------------------------------
    endpoint | URL | Required | The webhook URL.
    type | String | Required | The type of webhook. Refer to GET webhooks for type values
    enabled | Int | Optional | Should the webhook be enabled or disabled. It is enabled(1) by default.
    """

class WebhooksDelete_webhookNamespace(LimbleEndpoint):
    """
    This request deletes a Webhook.
    """

class RegionsNamespace(LimbleEndpoint):
    """
    This request returns your Regions in Limble.  
    
    Return data description

    Property | Description
    ----------------------
    regionID | The ID of the Region
    regionName | The name of the Region
    parentRegionID | The regionID of the parent of a region.

    Query Parameters:
    - regions: This parameter is used to only get regions in the list provided. This parameter accepts a comma delimited list of Region IDs.
    - name: This parameter is used to only get specific regions by name. This parameter expects a string- the full name of a region
 or partial name with the wildcard %.
    - cursor: This parameter is a cursor that selects what regionID you want to start receiving results at. e.g. passing 137 here will only get you regions
 with an id greater than 137.
    - limit: This parameter is a result limiter. The default is set to return no more than 100 
results at one time.
    """
    @property
    def create_region(self) -> RegionsCreate_regionNamespace:
        """
        Creates a region.
        
        Parameters:

        Parameter | In | Type | Required | Default | Description
        --------------------------------------------------------
        name | body | string | yes |  | Region name
        parentRegionID | body | integer | no | 0 | Parent region (≥ 0)

        Responses:
        - 201 Created: { regionID } with Location header.
        """
        ...
    @property
    def update_region(self) -> RegionsUpdate_regionNamespace:
        """
        Updates a region.
        
        Parameters:

        Parameter | In | Type | Required | Default | Description
        --------------------------------------------------------
        regionID | path | integer | yes |  | Region identifier
        name | body | string | no |  | New name
        parentRegionID | body | integer | no |  | New parent (≥ 1)
        """
        ...
    @property
    def delete_region(self) -> RegionsDelete_regionNamespace:
        """
        Deletes a region.
        
        Parameters:

        Parameter | In | Type | Required | Default | Description
        --------------------------------------------------------
        regionID | path | integer | yes |  | Region identifier

        Responses:
        - 200 OK: Deleted.
        - 404 Not Found: Region does not exist.
        """
        ...

class RegionsDelete_regionNamespace(LimbleEndpoint):
    """
    Deletes a region.
    
    Parameters:

    Parameter | In | Type | Required | Default | Description
    --------------------------------------------------------
    regionID | path | integer | yes |  | Region identifier

    Responses:
    - 200 OK: Deleted.
    - 404 Not Found: Region does not exist.
    """

class RegionsUpdate_regionNamespace(LimbleEndpoint):
    """
    Updates a region.
    
    Parameters:

    Parameter | In | Type | Required | Default | Description
    --------------------------------------------------------
    regionID | path | integer | yes |  | Region identifier
    name | body | string | no |  | New name
    parentRegionID | body | integer | no |  | New parent (≥ 1)
    """

class RegionsCreate_regionNamespace(LimbleEndpoint):
    """
    Creates a region.
    
    Parameters:

    Parameter | In | Type | Required | Default | Description
    --------------------------------------------------------
    name | body | string | yes |  | Region name
    parentRegionID | body | integer | no | 0 | Parent region (≥ 0)

    Responses:
    - 201 Created: { regionID } with Location header.
    """

class BillsNamespace(LimbleEndpoint):
    """
    This request gets information such as Bill IDs, Bill Numbers, etc.
    
    This call returns a "meta" object containing URLs that can be used to get data related to the Bill.
    
    Note: this endpoint supports pagination. Please refer to the [**Pagination**](#pagination) section for more information.
    
    Return data description

    Property | Description
    ----------------------
    meta | useful links relating to this Bill
    billID | The unique ID of the Bill.
    billNumber | The bill number assigned to the Bill.
    poID | The poID of which the Bill was made.
    locationID | The unique ID of the location associated with this Bill.
    date | The date this Bill was created as a UNIX timestamp.
    status | The status of this Bill.
            The status can be as follows:
            0: The bill is setup.
            1: The bill is submitted.
            2: The bill is closed i.e. Marked as Paid
    userID | The Id of the user this Bill was assigned to.
    userIDStarted | The ID of the user this Bill was created by.
    userIDMarkPaid | The ID of the user this Bill was marked paid by.

    Query Parameters:
    - bills: This parameter is used to only get specific Bills. This parameter expects a comma delimited list of billIDs.
    - numbers: This parameter is used to only get specific Bills by Number. This parameter expects a comma delimited list of billNumbers.
    - status: This parameter is used to only get specific Bills by their status. The bill status could be 0,1 or 2

    - end: This parameter is used to only get Bills that were created before or on the unix timestamp passed into it. 
    - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
    - pos: This parameter is used to only get specific Bills by POs. This parameter expects a comma delimited list of PO IDs.
    - start: This parameter is used to only get Bills that were created after or on the unix timestamp passed into it. 
    - locations: This parameter is used to only get Bills at a specific group of Locations. This parameter accepts a comma delimited list of Location IDs.
    - cursor: This parameter is a cursor that selects what billID you want to start receiving results at. e.g. passing 130 here will only get you bills with an id greater than 130.
    - page: This parameter is used to paginate results based on the limit. Refer to Pagination section for more information.
    """
    @property
    def transactions(self) -> BillsTransactionsNamespace: ...
    @property
    def comments(self) -> BillsCommentsNamespace: ...
    @property
    def new_bill(self) -> BillsNew_billNamespace:
        """
        This request creates a new Bill for a Purchase Order.

        Parameter | Type | Required? | Description
        ------------------------------------------
        poID | Int | Required | The poID for which the Bill is made.
        userID | Int | Optional | The ID of the user that this Bill will be assigned to.
        """
        ...
    @property
    def update_bill(self) -> BillsUpdate_billNamespace:
        """
        This request updates a Bill.

        Parameter | Type | Required? | Description
        ------------------------------------------
        userID | Int | Optional | The ID of the user that this Bill will be assigned to.
        status | Int | Optional | The status of this Bill.
            Refer to GET Bill to understand what values status can be. A bill status cannot be reduced once it is changed.
        """
        ...
    @property
    def delete_bill(self) -> BillsDelete_billNamespace:
        """
        This request deletes a Bill. This will also delete any Bill transactions for PO Items that were received on this Bill. The qty and price of the PO Items on the Bill will be recalculated.
        """
        ...

class BillsDelete_billNamespace(LimbleEndpoint):
    """
    This request deletes a Bill. This will also delete any Bill transactions for PO Items that were received on this Bill. The qty and price of the PO Items on the Bill will be recalculated.
    """

class BillsUpdate_billNamespace(LimbleEndpoint):
    """
    This request updates a Bill.

    Parameter | Type | Required? | Description
    ------------------------------------------
    userID | Int | Optional | The ID of the user that this Bill will be assigned to.
    status | Int | Optional | The status of this Bill.
            Refer to GET Bill to understand what values status can be. A bill status cannot be reduced once it is changed.
    """

class BillsNew_billNamespace(LimbleEndpoint):
    """
    This request creates a new Bill for a Purchase Order.

    Parameter | Type | Required? | Description
    ------------------------------------------
    poID | Int | Required | The poID for which the Bill is made.
    userID | Int | Optional | The ID of the user that this Bill will be assigned to.
    """

class BillsCommentsNamespace(object):
    @property
    def bill_comments(self) -> BillsCommentsBill_commentsNamespace:
        """
        This request gets all Bill Comments associated with a Bill.
        
        Return data description

        Property | Description
        ----------------------
        commentID | This is the commentID of comment.
        comment | The text comment that was entered by the user.
        timestamp | The date this comment was created. This is a unix timestamp.
        userID | The ID of the user that made the comment.
        commentEmailAddress | The email address of the external user that made this comment. This is only populated if the comment was made by an external user via the comment reply system.
        commentFiles | Array containing fileName and link properties.

        Query Parameters:
        - cursor: This parameter is a cursor that selects what commentID you want to start receiving results at. e.g. passing 100 here will only get you comments with an id greater than 100
        - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
        """
        ...
    @property
    def create_bill_comment(self) -> BillsCommentsCreate_bill_commentNamespace:
        """
        Adds a comment to a Bill.
        
        Parameters:

        Parameter | In | Type | Required | Default | Description
        --------------------------------------------------------
        billID | path | integer | yes |  | Bill identifier
        comment | body | string | yes |  | Comment text
        showExternalUsers | body | boolean | no | true | Visible to external users

        Responses:
        - 201 Created: Returns commentID.
        """
        ...
    @property
    def upload_bill_comment_file(self) -> BillsCommentsUpload_bill_comment_fileNamespace:
        """
        Uploads a file to a Bill comment.
        
        Parameters:

        Parameter | In | Type | Required | Default | Description
        --------------------------------------------------------
        billID | path | integer | yes |  | Bill identifier
        commentID | path | integer | yes |  | Comment identifier
        file | form-data | file | yes |  | File to upload (max 50MB). Same types as PO comment files
        """
        ...
    @property
    def delete_bill_comment_file(self) -> BillsCommentsDelete_bill_comment_fileNamespace:
        """
        Deletes a file from a Bill comment.
        
        Parameters:

        Parameter | In | Type | Required | Default | Description
        --------------------------------------------------------
        billID | path | integer | yes |  | Bill identifier
        commentID | path | integer | yes |  | Comment identifier
        filename | query | string | yes |  | Exact filename to remove

        Responses:
        - 200 OK: Deleted.
        - 404 Not Found: File not found.

        Query Parameters:
        - filename: 
        """
        ...
    @property
    def delete_bill_comment(self) -> BillsCommentsDelete_bill_commentNamespace:
        """
        Deletes a Bill comment.
        
        Parameters:

        Parameter | In | Type | Required | Default | Description
        --------------------------------------------------------
        billID | path | integer | yes |  | Bill identifier
        commentID | path | integer | yes |  | Comment identifier

        Responses:
        - 200 OK: Deleted.
        - 404 Not Found: Comment not found.
        """
        ...

class BillsCommentsDelete_bill_commentNamespace(LimbleEndpoint):
    """
    Deletes a Bill comment.
    
    Parameters:

    Parameter | In | Type | Required | Default | Description
    --------------------------------------------------------
    billID | path | integer | yes |  | Bill identifier
    commentID | path | integer | yes |  | Comment identifier

    Responses:
    - 200 OK: Deleted.
    - 404 Not Found: Comment not found.
    """

class BillsCommentsDelete_bill_comment_fileNamespace(LimbleEndpoint):
    """
    Deletes a file from a Bill comment.
    
    Parameters:

    Parameter | In | Type | Required | Default | Description
    --------------------------------------------------------
    billID | path | integer | yes |  | Bill identifier
    commentID | path | integer | yes |  | Comment identifier
    filename | query | string | yes |  | Exact filename to remove

    Responses:
    - 200 OK: Deleted.
    - 404 Not Found: File not found.

    Query Parameters:
    - filename: 
    """

class BillsCommentsUpload_bill_comment_fileNamespace(LimbleEndpoint):
    """
    Uploads a file to a Bill comment.
    
    Parameters:

    Parameter | In | Type | Required | Default | Description
    --------------------------------------------------------
    billID | path | integer | yes |  | Bill identifier
    commentID | path | integer | yes |  | Comment identifier
    file | form-data | file | yes |  | File to upload (max 50MB). Same types as PO comment files
    """

class BillsCommentsCreate_bill_commentNamespace(LimbleEndpoint):
    """
    Adds a comment to a Bill.
    
    Parameters:

    Parameter | In | Type | Required | Default | Description
    --------------------------------------------------------
    billID | path | integer | yes |  | Bill identifier
    comment | body | string | yes |  | Comment text
    showExternalUsers | body | boolean | no | true | Visible to external users

    Responses:
    - 201 Created: Returns commentID.
    """

class BillsCommentsBill_commentsNamespace(LimbleEndpoint):
    """
    This request gets all Bill Comments associated with a Bill.
    
    Return data description

    Property | Description
    ----------------------
    commentID | This is the commentID of comment.
    comment | The text comment that was entered by the user.
    timestamp | The date this comment was created. This is a unix timestamp.
    userID | The ID of the user that made the comment.
    commentEmailAddress | The email address of the external user that made this comment. This is only populated if the comment was made by an external user via the comment reply system.
    commentFiles | Array containing fileName and link properties.

    Query Parameters:
    - cursor: This parameter is a cursor that selects what commentID you want to start receiving results at. e.g. passing 100 here will only get you comments with an id greater than 100
    - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
    """

class BillsTransactionsNamespace(object):
    @property
    def add_bill_item(self) -> BillsTransactionsAdd_bill_itemNamespace:
        """
        This request creates a Bill transaction by adding a Bill Item to an unclosed Bill.

        Parameter | Type | Required? | Description
        ------------------------------------------
        poItemID | Int | Required | The ID of the item that has to be added to the Bill.
        qtyReceived | Int | Required | The item quantity received on this Bill.
        """
        ...
    @property
    def bill_transactions(self) -> BillsTransactionsBill_transactionsNamespace:
        """
        This request gets information about the transactions made for a Bill.

        Query Parameters:
        - bills: This parameter is used to only get specific Bill Transactions by billID. This parameter expects a comma delimited list of billIDs.
        - items: This parameter is used to only get specific Bill Transactions by items in a Bill. This parameter expects a comma delimited list of poItem IDs.
        - start: This parameter is used to only get Bill Transactions that were created after or on the unix timestamp passed into it. 
        - end: This parameter is used to only get Bill transactions that were created before or on the unix timestamp passed into it. 
        - transactions: This parameter is used to only get specific Bill Transactions. This parameter expects a comma delimited list of transactionIDs.
        - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
        - locations: This parameter is used to only get Bill Transactions at a specific group of Locations. This parameter accepts a comma delimited list of Location IDs.
        """
        ...
    @property
    def update_bill_transaction(self) -> BillsTransactionsUpdate_bill_transactionNamespace: ...
    @property
    def bill_transaction(self) -> BillsTransactionsBill_transactionNamespace: ...

class BillsTransactionsBill_transactionNamespace(LimbleEndpoint):
    pass

class BillsTransactionsUpdate_bill_transactionNamespace(LimbleEndpoint):
    pass

class BillsTransactionsBill_transactionsNamespace(LimbleEndpoint):
    """
    This request gets information about the transactions made for a Bill.

    Query Parameters:
    - bills: This parameter is used to only get specific Bill Transactions by billID. This parameter expects a comma delimited list of billIDs.
    - items: This parameter is used to only get specific Bill Transactions by items in a Bill. This parameter expects a comma delimited list of poItem IDs.
    - start: This parameter is used to only get Bill Transactions that were created after or on the unix timestamp passed into it. 
    - end: This parameter is used to only get Bill transactions that were created before or on the unix timestamp passed into it. 
    - transactions: This parameter is used to only get specific Bill Transactions. This parameter expects a comma delimited list of transactionIDs.
    - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
    - locations: This parameter is used to only get Bill Transactions at a specific group of Locations. This parameter accepts a comma delimited list of Location IDs.
    """

class BillsTransactionsAdd_bill_itemNamespace(LimbleEndpoint):
    """
    This request creates a Bill transaction by adding a Bill Item to an unclosed Bill.

    Parameter | Type | Required? | Description
    ------------------------------------------
    poItemID | Int | Required | The ID of the item that has to be added to the Bill.
    qtyReceived | Int | Required | The item quantity received on this Bill.
    """

class StatusesNamespace(LimbleEndpoint):
    """
    This request returns your custom task statuses in Limble.
    
    Return data description

    Property | Description
    ----------------------
    statusID | A unique identifier for this status.
    name | A custom string that labels this status.
    description | An optional description that elaborates on what this status means.

    Query Parameters:
    - limit: 
    - cursor: 
    - name: 
    - statuses: 
    """
    @property
    def create_status(self) -> StatusesCreate_statusNamespace:
        """
        Creates a new custom status for the customer account.
        
        **Request Body:**
        
        - `name` (string, required) - Status name, 1-100 characters, must be unique (case-insensitive)
            
        - `description` (string, optional) - Status description, max 65535 characters
            
        - `sortOrder` (integer, optional) - Display order, 0-99, auto-assigned if omitted
            
        
        **Response (201 Created):**
        
        - `statusID` (number) - ID of the newly created status
            
        - Location header: `/v2/statuses?statuses={statusID}`
            
        
        **Validation:**
        
        - Name must not conflict with existing statuses or defaults ("Open", "In Progress", "Complete")
            
        - Name is compared case-insensitively
        """
        ...
    @property
    def update_status(self) -> StatusesUpdate_statusNamespace:
        """
        Updates an existing custom status. Default statuses (0, 1, 2) cannot be modified.
        
        **IMPORTANT NOTE:** Changes to statuses automatically propogate to all tasks currently assigned that status.
        
        **Path Parameters:**
        
        - `statusID` (number, required) - ID of the status to update
            
        
        **Request Body (at least one field required):**
        
        - `name` (string, optional) - New status name, 1-100 characters, must be unique
            
        - `description` (string, optional) - New description, max 65535 characters
            
        - `sortOrder` (integer, optional) - New display order, 0-99
            
        
        **Validation:**
        
        - Cannot modify default statuses (IDs 0, 1, 2)
            
        - If changing name, must not conflict with existing statuses
            
        - Status must exist and belong to the customer
        """
        ...
    @property
    def delete_status(self) -> StatusesDelete_statusNamespace:
        """
        Deletes a custom status and reassigns all tasks using it. Default statuses (0, 1, 2) cannot be deleted.
        
        **IMPORTANT NOTE:** Deleting task statuses that are currently in use will result in all tasks assigned that status being reset to status 0 (open).
        
        **Path Parameters:**
        
        - `statusID` (number, required) - ID of the status to delete
            
        
        **Query Parameters:**
        
        - `replacementStatusID` (number, required) - ID of the status to assign to tasks currently using the deleted status. Can be a default status (0, 1, 2) or another custom status.
            
        
        **Validation:**
        
        - Cannot delete default statuses (IDs 0, 1, 2)
            
        - Both statusID and replacementStatusID must exist
            
        - replacementStatusID must differ from statusID
            
        - replacementStatusID must be valid for the customer

        Query Parameters:
        - replacementStatusID: ID of the status to reassign tasks to (required)
        """
        ...

class StatusesDelete_statusNamespace(LimbleEndpoint):
    """
    Deletes a custom status and reassigns all tasks using it. Default statuses (0, 1, 2) cannot be deleted.
    
    **IMPORTANT NOTE:** Deleting task statuses that are currently in use will result in all tasks assigned that status being reset to status 0 (open).
    
    **Path Parameters:**
    
    - `statusID` (number, required) - ID of the status to delete
        
    
    **Query Parameters:**
    
    - `replacementStatusID` (number, required) - ID of the status to assign to tasks currently using the deleted status. Can be a default status (0, 1, 2) or another custom status.
        
    
    **Validation:**
    
    - Cannot delete default statuses (IDs 0, 1, 2)
        
    - Both statusID and replacementStatusID must exist
        
    - replacementStatusID must differ from statusID
        
    - replacementStatusID must be valid for the customer

    Query Parameters:
    - replacementStatusID: ID of the status to reassign tasks to (required)
    """

class StatusesUpdate_statusNamespace(LimbleEndpoint):
    """
    Updates an existing custom status. Default statuses (0, 1, 2) cannot be modified.
    
    **IMPORTANT NOTE:** Changes to statuses automatically propogate to all tasks currently assigned that status.
    
    **Path Parameters:**
    
    - `statusID` (number, required) - ID of the status to update
        
    
    **Request Body (at least one field required):**
    
    - `name` (string, optional) - New status name, 1-100 characters, must be unique
        
    - `description` (string, optional) - New description, max 65535 characters
        
    - `sortOrder` (integer, optional) - New display order, 0-99
        
    
    **Validation:**
    
    - Cannot modify default statuses (IDs 0, 1, 2)
        
    - If changing name, must not conflict with existing statuses
        
    - Status must exist and belong to the customer
    """

class StatusesCreate_statusNamespace(LimbleEndpoint):
    """
    Creates a new custom status for the customer account.
    
    **Request Body:**
    
    - `name` (string, required) - Status name, 1-100 characters, must be unique (case-insensitive)
        
    - `description` (string, optional) - Status description, max 65535 characters
        
    - `sortOrder` (integer, optional) - Display order, 0-99, auto-assigned if omitted
        
    
    **Response (201 Created):**
    
    - `statusID` (number) - ID of the newly created status
        
    - Location header: `/v2/statuses?statuses={statusID}`
        
    
    **Validation:**
    
    - Name must not conflict with existing statuses or defaults ("Open", "In Progress", "Complete")
        
    - Name is compared case-insensitively
    """

class TagsNamespace(LimbleEndpoint):
    """
    This request returns your tags in Limble.
    
    Return data description

    Property | Description
    ----------------------
    name | A search-string for tags.

    Query Parameters:
    - name: 
    """
    @property
    def create_account_tag(self) -> TagsCreate_account_tagNamespace:
        """
        Creates a new account-level custom tag. The tag is normalized and validated before creation.
        
        **Request Body:**
        - `name` (string, required) - Tag name with or without leading '@', must not contain ';'
        
        **Response (200 OK):**
        - `created` (boolean) - Always true on success
        - `name` (string) - Canonical tag name without trailing ';' (e.g., `@Food Safety`)
        - `sanitizations` (array, optional) - List of normalization actions applied
        - `tags` (array) - All account tags in canonical format with trailing ';'
        
        **Normalization Rules:**
        - Semicolons ';' are rejected (not allowed in input)
        - Internal '@' characters removed, single leading '@' added
        - Backslashes removed
        - Commas converted to spaces
        - Whitespace collapsed
        - CR/LF and NBSP normalized to spaces
        - ASCII control characters removed
        
        **Error Responses:**
        - 400 Bad Request - Invalid input (contains ';' or normalizes to empty)
        - 409 Conflict - Tag already exists (case-insensitive comparison)
        """
        ...
    @property
    def rename_account_tag(self) -> TagsRename_account_tagNamespace:
        """
        Renames an account-level custom tag.  
          
        **IMPORTANT NOTE:** The change propagates to all data entities using this tag (Tasks, dashboards, notifications, etc).
        
        **Request Body:**
        
        - `oldName` (string, required) - Existing tag name (with or without '@', without trailing ';')
            
        - `newName` (string, required) - New tag name (with or without '@', without trailing ';')
            
        
        **Response (200 OK):**
        
        - `renamed` (boolean) - Always true on success
            
        - `from` (string) - Old canonical tag name without trailing ';'
            
        - `to` (string) - New canonical tag name without trailing ';'
            
        - `tags` (array) - All account tags in canonical format with trailing ';'
            
        
        **Validation:**
        
        - Old tag must exist (case-insensitive)
            
        - New tag must not exist (case-insensitive)
            
        - Semicolons not allowed in input
            
        - Both names subject to normalization rules
            
        
        **Error Responses:**
        
        - 400 Bad Request - Invalid input (contains ';' or normalizes to empty)
            
        - 404 Not Found - Old tag does not exist
            
        - 409 Conflict - New tag name already exists
        """
        ...
    @property
    def delete_account_tag(self) -> TagsDelete_account_tagNamespace:
        """
        Deletes an account-level custom tag.
        
        **IMPORTANT NOTE:** The change propagates to all data entities using this tag (Tasks, dashboards, notifications, etc).
        
        **Path Parameters:**
        
        - `tagName` (string, required) - Tag name to delete (with or without '@', without trailing ';')
            - URL encode special characters (e.g., `@Food Safety` for `@Food Safety`)
                
        
        **Response (200 OK):**
        
        - `deleted` (boolean) - Always true on success
            
        - `name` (string) - Canonical tag name that was deleted (without trailing ';')
            
        - `tags` (array) - Remaining account tags in canonical format with trailing ';'
            
        
        **Validation:**
        
        - Tag must exist (case-insensitive)
            
        - Tag name subject to normalization for matching
            
        
        **Error Responses:**
        
        - 404 Not Found - Tag does not exist
        """
        ...

class TagsDelete_account_tagNamespace(LimbleEndpoint):
    """
    Deletes an account-level custom tag.
    
    **IMPORTANT NOTE:** The change propagates to all data entities using this tag (Tasks, dashboards, notifications, etc).
    
    **Path Parameters:**
    
    - `tagName` (string, required) - Tag name to delete (with or without '@', without trailing ';')
        - URL encode special characters (e.g., `@Food Safety` for `@Food Safety`)
            
    
    **Response (200 OK):**
    
    - `deleted` (boolean) - Always true on success
        
    - `name` (string) - Canonical tag name that was deleted (without trailing ';')
        
    - `tags` (array) - Remaining account tags in canonical format with trailing ';'
        
    
    **Validation:**
    
    - Tag must exist (case-insensitive)
        
    - Tag name subject to normalization for matching
        
    
    **Error Responses:**
    
    - 404 Not Found - Tag does not exist
    """

class TagsRename_account_tagNamespace(LimbleEndpoint):
    """
    Renames an account-level custom tag.  
      
    **IMPORTANT NOTE:** The change propagates to all data entities using this tag (Tasks, dashboards, notifications, etc).
    
    **Request Body:**
    
    - `oldName` (string, required) - Existing tag name (with or without '@', without trailing ';')
        
    - `newName` (string, required) - New tag name (with or without '@', without trailing ';')
        
    
    **Response (200 OK):**
    
    - `renamed` (boolean) - Always true on success
        
    - `from` (string) - Old canonical tag name without trailing ';'
        
    - `to` (string) - New canonical tag name without trailing ';'
        
    - `tags` (array) - All account tags in canonical format with trailing ';'
        
    
    **Validation:**
    
    - Old tag must exist (case-insensitive)
        
    - New tag must not exist (case-insensitive)
        
    - Semicolons not allowed in input
        
    - Both names subject to normalization rules
        
    
    **Error Responses:**
    
    - 400 Bad Request - Invalid input (contains ';' or normalizes to empty)
        
    - 404 Not Found - Old tag does not exist
        
    - 409 Conflict - New tag name already exists
    """

class TagsCreate_account_tagNamespace(LimbleEndpoint):
    """
    Creates a new account-level custom tag. The tag is normalized and validated before creation.
    
    **Request Body:**
    - `name` (string, required) - Tag name with or without leading '@', must not contain ';'
    
    **Response (200 OK):**
    - `created` (boolean) - Always true on success
    - `name` (string) - Canonical tag name without trailing ';' (e.g., `@Food Safety`)
    - `sanitizations` (array, optional) - List of normalization actions applied
    - `tags` (array) - All account tags in canonical format with trailing ';'
    
    **Normalization Rules:**
    - Semicolons ';' are rejected (not allowed in input)
    - Internal '@' characters removed, single leading '@' added
    - Backslashes removed
    - Commas converted to spaces
    - Whitespace collapsed
    - CR/LF and NBSP normalized to spaces
    - ASCII control characters removed
    
    **Error Responses:**
    - 400 Bad Request - Invalid input (contains ';' or normalizes to empty)
    - 409 Conflict - Tag already exists (case-insensitive comparison)
    """

class PrioritiesNamespace(LimbleEndpoint):
    """
    This request returns your priorities in Limble.  
    
    Return data description

    Property | Description
    ----------------------
    priorityID | The priority's unique identifier.
    name | The full name of the priority.
    priorityLevel | A number representing ordering or indicator of severity.
    color | A hex-color string that will be used to color tasks associated to this priority.
    isDefault | A boolean representing whether or not this is the priority that will be associated to tasks by default.

    Query Parameters:
    - priorities: 
    """
    @property
    def update_priority(self) -> PrioritiesUpdate_priorityNamespace:
        """
        This request updates a Priority.
        
        **When providing priorityLevel or isDefault, calls to this endpoint may reorder or otherwise adjust** _**other**_ **priorities.**

        Parameter | Type | Required? | Description
        ------------------------------------------
        name | String | Optional | The title of this priority.
        priorityLevel | Int | Optional | What level is this priority? When moving a priority to a different priorityLevel, be mindful that this will shift other priorities' priorityLevels in order to accommodate this change. If provided, this can only be between the numbers 1 and the current highest priorityLevel.
        color | String | Optional | This is the color that will be shown on all tasks with this priority.
        isDefault | Boolean | Optional | Should this be the default priority that tasks are assigned to when a priority is not specified? When setting this to true, any other priorities whose isDefault is true will have it set to false.
        """
        ...
    @property
    def new_priority(self) -> PrioritiesNew_priorityNamespace:
        """
        This request creates a new Priority.
        
        When providing priorityLevel or isDefault, calls to this endpoint may reorder or otherwise adjust other priorities.

        Parameter | Type | Required? | Description
        ------------------------------------------
        name | String | Required | The title of this priority.
        priorityLevel | Int | Required | What level is this priority? If we're inserting a priority in the middle of the levels, priorities with a priorityLevel equal-to or greater-than the specified priorityLevel will have their priorityLevel incremented by one. This can only be between the numbers 1 and the current highest priorityLevel + 1.
        color | String | Optional | This is the color that will be shown on all tasks with this priority. Default is #429b1f
        isDefault | Boolean | Optional | Should this be the default priority that tasks are assigned to when a priority is not specified? Default is false. If isDefault is true, then any other priorities will have their isDefault set to false.
        """
        ...
    @property
    def delete_priority(self) -> PrioritiesDelete_priorityNamespace:
        """
        <p>This call simply removes a priority from Limble.</p>
        <p><strong>Things to keep in mind when using this endpoint:</strong>
        <ul>
            <li>
                Calls to this endpoint will potentially adjust other priorities' priorityLevels.
            </li>
            <li>If you delete a priority that isDefault, you will not have a default priority anymore, and that may cause issues.</li>
            <li>If you delete a priority that has tasks associated to it, those tasks will have their priority removed.</li>
        </ul></p>
        """
        ...

class PrioritiesDelete_priorityNamespace(LimbleEndpoint):
    """
    <p>This call simply removes a priority from Limble.</p>
    <p><strong>Things to keep in mind when using this endpoint:</strong>
    <ul>
        <li>
            Calls to this endpoint will potentially adjust other priorities' priorityLevels.
        </li>
        <li>If you delete a priority that isDefault, you will not have a default priority anymore, and that may cause issues.</li>
        <li>If you delete a priority that has tasks associated to it, those tasks will have their priority removed.</li>
    </ul></p>
    """

class PrioritiesNew_priorityNamespace(LimbleEndpoint):
    """
    This request creates a new Priority.
    
    When providing priorityLevel or isDefault, calls to this endpoint may reorder or otherwise adjust other priorities.

    Parameter | Type | Required? | Description
    ------------------------------------------
    name | String | Required | The title of this priority.
    priorityLevel | Int | Required | What level is this priority? If we're inserting a priority in the middle of the levels, priorities with a priorityLevel equal-to or greater-than the specified priorityLevel will have their priorityLevel incremented by one. This can only be between the numbers 1 and the current highest priorityLevel + 1.
    color | String | Optional | This is the color that will be shown on all tasks with this priority. Default is #429b1f
    isDefault | Boolean | Optional | Should this be the default priority that tasks are assigned to when a priority is not specified? Default is false. If isDefault is true, then any other priorities will have their isDefault set to false.
    """

class PrioritiesUpdate_priorityNamespace(LimbleEndpoint):
    """
    This request updates a Priority.
    
    **When providing priorityLevel or isDefault, calls to this endpoint may reorder or otherwise adjust** _**other**_ **priorities.**

    Parameter | Type | Required? | Description
    ------------------------------------------
    name | String | Optional | The title of this priority.
    priorityLevel | Int | Optional | What level is this priority? When moving a priority to a different priorityLevel, be mindful that this will shift other priorities' priorityLevels in order to accommodate this change. If provided, this can only be between the numbers 1 and the current highest priorityLevel.
    color | String | Optional | This is the color that will be shown on all tasks with this priority.
    isDefault | Boolean | Optional | Should this be the default priority that tasks are assigned to when a priority is not specified? When setting this to true, any other priorities whose isDefault is true will have it set to false.
    """

class BudgetsNamespace(LimbleEndpoint):
    """
    This request returns your Budgets in Limble.  
    
    Return data description

    Property | Description
    ----------------------
    budgetID | The Budget's unique identifier.
    name | The full name of the Budget.
    locationID | Which Location this Budget belongs to.

    Query Parameters:
    - cursor: This parameter is a cursor that selects what budgetID you want to start receiving results at. e.g. passing 137 here will only get you budgets with an ID greater than 137.
    - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
    - name: This is a parameter used to string search for a name or partial name of a budget. This parameter expects a string with the wildcard %.
    - locations: This parameter is used to only get budgets that are linked to a location. This parameter accepts a comma delimited list of location IDs.
    - budgets: This parameter is used to only get specific budgets. This parameter accepts a comma delimited list of budget IDs.
    """
    @property
    def steps(self) -> BudgetsStepsNamespace:
        """

        Query Parameters:
        - name: This is a parameter used to string search for a name or partial name of a budget. This parameter expects a string with the wildcard %.
        - steps: This parameter is used to only get specific steps. This parameter accepts a comma delimited list of step IDs.
        - budgets: This parameter is used to only get steps that are linked to a budget. This parameter accepts a comma delimited list of budget IDs.
        - locations: This parameter is used to only get steps that are linked to a budget at a specific location. This parameter accepts a comma delimited list of location IDs.
        - cursor: This parameter is a cursor that selects what stepID you want to start receiving results at. e.g. passing 137 here will only get you steps with an ID greater than 137.
        - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
        """
        ...
    @property
    def new_budget(self) -> BudgetsNew_budgetNamespace:
        """
        This request creates a new Budget.

        Parameter | Type | Required? | Description
        ------------------------------------------
        locationID | Int | Required | The ID of the location this budget will belong to.
        name | String | Required | The title of this budget.
        awaitingAllowPOEdit | Boolean | Required | When POs belonging to this budget are in the "ready to receive" state, will they be editable?
        awaitingEmailSend | Boolean | Required | When POs belonging to this budget enter the "ready to receive" state, should the assignee(s) be emailed?
        awaitingAssignmentType | Enum | Required | What type ('user' or 'team') should we interpret the awaitingAssignment value as?
        awaitingAssignment | Int or Array of Ints | Required | When POs belonging to this budget enter the "ready to receive" state, who will they be assigned to? If awaitingAssignmentType is 'team' then this cannot be an array, and may only be one number.
        prEmailSend | Boolean | Required | When PO items are received on POs that belong to this budget in the "ready to receive" or "partially received" states, should we send email notification(s)?
        prAssignmentType | Enum | Required | What type ('user' or 'team') should we interpret the prAssignment value as?
        prAssignment | Int or Array of Ints | Required | When bills are generated for PO items on POs that belong to this budget, who should the bills be assigned to? If prAssignmentType is 'team' then this cannot be an array, and may only be one number.
        defaultBudget | Object | Required | An object containing Boolean flags for global, purchaseRequests, and minPartQtyPOs. Setting any of these flags to true will set the same value for any other budgets at this location to false (we cannot have two default budgets). All properties of this object are required.
            
global: Should this be the default budget for this location?
purchaseRequests: When purchase requests are created from tasks, should this be the default budget?
minPartQtyPOs: When a PO is automatically created due to part quantity threshold, should this be the default budget?
        """
        ...
    @property
    def delete_budget(self) -> BudgetsDelete_budgetNamespace:
        """
        This request deletes a budget.
        """
        ...
    @property
    def update_budget(self) -> BudgetsUpdate_budgetNamespace:
        """
        This request updates an existing Budget.

        Parameter | Type | Required? | Description
        ------------------------------------------
        name | String | Optional | The title of this budget.
        awaitingAllowPOEdit | Boolean | Optional | When POs belonging to this budget are in the "ready to receive" state, will they be editable?
        awaitingEmailSend | Boolean | Optional | When POs belonging to this budget enter the "ready to receive" state, should the assignee(s) be emailed?
        awaitingAssignmentType | Enum | Optional | What type ('user' or 'team') should we interpret the awaitingAssignment value as? Required when awaitingAssignment is provided.
        awaitingAssignment | Int or Array of Ints | Optional | When POs belonging to this budget enter the "ready to receive" state, who will they be assigned to? If awaitingAssignmentType is 'team' then this cannot be an array, and may only be one number. Required when awaitingAssignmentType is provided.
        prEmailSend | Boolean | Optional | When PO items are received on POs that belong to this budget in the "ready to receive" or "partially received" states, should we send email notification(s)?
        prAssignmentType | Enum | Optional | What type ('user' or 'team') should we interpret the prAssignment value as? Required when prAssignment is provided.
        prAssignment | Int or Array of Ints | Optional | When bills are generated for PO items on POs that belong to this budget, who should the bills be assigned to? If prAssignmentType is 'team' then this cannot be an array, and may only be one number. Required when prAssignmentType is provided.
        defaultBudget | Object | Optional | An object containing Boolean flags for global, purchaseRequests, and minPartQtyPOs. Setting any of these flags to true will set the same value for any other budgets at this location to false (we cannot have two default budgets). All properties of this object are required when the object is provided.
            
global: Should this be the default budget for this location?
purchaseRequests: When purchase requests are created from tasks, should this be the default budget?
minPartQtyPOs: When a PO is automatically created due to part quantity threshold, should this be the default budget?
        """
        ...

class BudgetsUpdate_budgetNamespace(LimbleEndpoint):
    """
    This request updates an existing Budget.

    Parameter | Type | Required? | Description
    ------------------------------------------
    name | String | Optional | The title of this budget.
    awaitingAllowPOEdit | Boolean | Optional | When POs belonging to this budget are in the "ready to receive" state, will they be editable?
    awaitingEmailSend | Boolean | Optional | When POs belonging to this budget enter the "ready to receive" state, should the assignee(s) be emailed?
    awaitingAssignmentType | Enum | Optional | What type ('user' or 'team') should we interpret the awaitingAssignment value as? Required when awaitingAssignment is provided.
    awaitingAssignment | Int or Array of Ints | Optional | When POs belonging to this budget enter the "ready to receive" state, who will they be assigned to? If awaitingAssignmentType is 'team' then this cannot be an array, and may only be one number. Required when awaitingAssignmentType is provided.
    prEmailSend | Boolean | Optional | When PO items are received on POs that belong to this budget in the "ready to receive" or "partially received" states, should we send email notification(s)?
    prAssignmentType | Enum | Optional | What type ('user' or 'team') should we interpret the prAssignment value as? Required when prAssignment is provided.
    prAssignment | Int or Array of Ints | Optional | When bills are generated for PO items on POs that belong to this budget, who should the bills be assigned to? If prAssignmentType is 'team' then this cannot be an array, and may only be one number. Required when prAssignmentType is provided.
    defaultBudget | Object | Optional | An object containing Boolean flags for global, purchaseRequests, and minPartQtyPOs. Setting any of these flags to true will set the same value for any other budgets at this location to false (we cannot have two default budgets). All properties of this object are required when the object is provided.
            
global: Should this be the default budget for this location?
purchaseRequests: When purchase requests are created from tasks, should this be the default budget?
minPartQtyPOs: When a PO is automatically created due to part quantity threshold, should this be the default budget?
    """

class BudgetsDelete_budgetNamespace(LimbleEndpoint):
    """
    This request deletes a budget.
    """

class BudgetsNew_budgetNamespace(LimbleEndpoint):
    """
    This request creates a new Budget.

    Parameter | Type | Required? | Description
    ------------------------------------------
    locationID | Int | Required | The ID of the location this budget will belong to.
    name | String | Required | The title of this budget.
    awaitingAllowPOEdit | Boolean | Required | When POs belonging to this budget are in the "ready to receive" state, will they be editable?
    awaitingEmailSend | Boolean | Required | When POs belonging to this budget enter the "ready to receive" state, should the assignee(s) be emailed?
    awaitingAssignmentType | Enum | Required | What type ('user' or 'team') should we interpret the awaitingAssignment value as?
    awaitingAssignment | Int or Array of Ints | Required | When POs belonging to this budget enter the "ready to receive" state, who will they be assigned to? If awaitingAssignmentType is 'team' then this cannot be an array, and may only be one number.
    prEmailSend | Boolean | Required | When PO items are received on POs that belong to this budget in the "ready to receive" or "partially received" states, should we send email notification(s)?
    prAssignmentType | Enum | Required | What type ('user' or 'team') should we interpret the prAssignment value as?
    prAssignment | Int or Array of Ints | Required | When bills are generated for PO items on POs that belong to this budget, who should the bills be assigned to? If prAssignmentType is 'team' then this cannot be an array, and may only be one number.
    defaultBudget | Object | Required | An object containing Boolean flags for global, purchaseRequests, and minPartQtyPOs. Setting any of these flags to true will set the same value for any other budgets at this location to false (we cannot have two default budgets). All properties of this object are required.
            
global: Should this be the default budget for this location?
purchaseRequests: When purchase requests are created from tasks, should this be the default budget?
minPartQtyPOs: When a PO is automatically created due to part quantity threshold, should this be the default budget?
    """

class BudgetsStepsNamespace(LimbleEndpoint):
    """

    Query Parameters:
    - name: This is a parameter used to string search for a name or partial name of a budget. This parameter expects a string with the wildcard %.
    - steps: This parameter is used to only get specific steps. This parameter accepts a comma delimited list of step IDs.
    - budgets: This parameter is used to only get steps that are linked to a budget. This parameter accepts a comma delimited list of budget IDs.
    - locations: This parameter is used to only get steps that are linked to a budget at a specific location. This parameter accepts a comma delimited list of location IDs.
    - cursor: This parameter is a cursor that selects what stepID you want to start receiving results at. e.g. passing 137 here will only get you steps with an ID greater than 137.
    - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
    """
    @property
    def new_step(self) -> BudgetsStepsNew_stepNamespace:
        """
        This request creates a new Budget Step (sometimes called a PO Workflow Step).

        Parameter | Type | Required? | Description
        ------------------------------------------
        name | String | Required | The title of this budget.
        assignmentType | Enum | Required | What type ('user' or 'team') should we interpret the assignment value as?
        assignment | Int or Array of Ints | Required | When POs belonging to this step's budget enter this step, who will they be assigned to? If awaitingAssignmentType is 'team' then this cannot be an array, and may only be one number.
        emailSend | Boolean | Required | When POs of this step's budget enter this step, should we send email notification(s)?
        allowPOEdit | Boolean | Optional | When POs belonging to this step's budget are in this step, can the PO be edited?
        allowPR | Boolean | Required | When POs belonging to this step's budget are in this step, can items be received?
        """
        ...
    @property
    def delete_step(self) -> BudgetsStepsDelete_stepNamespace:
        """
        This request deletes a step from a budget.
        """
        ...
    @property
    def update_step(self) -> BudgetsStepsUpdate_stepNamespace:
        """
        This request updates a Budget Step (sometimes called a PO Workflow Step).

        Parameter | Type | Required? | Description
        ------------------------------------------
        name | String | Optional | The title of this budget.
        assignmentType | Enum | Optional | What type ('user' or 'team') should we interpret the assignment value as? This is required when the assignment property is present.
        assignment | Int or Array of Ints | Optional | When POs belonging to this step's budget enter this step, who will they be assigned to? If awaitingAssignmentType is 'team' then this cannot be an array, and may only be one number. This is required when the assignmentType property is present.
        emailSend | Boolean | Optional | When POs of this step's budget enter this step, should we send email notification(s)?
        allowPOEdit | Boolean | Optional | When POs belonging to this step's budget are in this step, can the PO be edited?
        allowPR | Boolean | Optional | When POs belonging to this step's budget are in this step, can items be received?
        order | Int | Optional | For the order of steps in this step's budget, which position should this step be in?
        """
        ...

class BudgetsStepsUpdate_stepNamespace(LimbleEndpoint):
    """
    This request updates a Budget Step (sometimes called a PO Workflow Step).

    Parameter | Type | Required? | Description
    ------------------------------------------
    name | String | Optional | The title of this budget.
    assignmentType | Enum | Optional | What type ('user' or 'team') should we interpret the assignment value as? This is required when the assignment property is present.
    assignment | Int or Array of Ints | Optional | When POs belonging to this step's budget enter this step, who will they be assigned to? If awaitingAssignmentType is 'team' then this cannot be an array, and may only be one number. This is required when the assignmentType property is present.
    emailSend | Boolean | Optional | When POs of this step's budget enter this step, should we send email notification(s)?
    allowPOEdit | Boolean | Optional | When POs belonging to this step's budget are in this step, can the PO be edited?
    allowPR | Boolean | Optional | When POs belonging to this step's budget are in this step, can items be received?
    order | Int | Optional | For the order of steps in this step's budget, which position should this step be in?
    """

class BudgetsStepsDelete_stepNamespace(LimbleEndpoint):
    """
    This request deletes a step from a budget.
    """

class BudgetsStepsNew_stepNamespace(LimbleEndpoint):
    """
    This request creates a new Budget Step (sometimes called a PO Workflow Step).

    Parameter | Type | Required? | Description
    ------------------------------------------
    name | String | Required | The title of this budget.
    assignmentType | Enum | Required | What type ('user' or 'team') should we interpret the assignment value as?
    assignment | Int or Array of Ints | Required | When POs belonging to this step's budget enter this step, who will they be assigned to? If awaitingAssignmentType is 'team' then this cannot be an array, and may only be one number.
    emailSend | Boolean | Required | When POs of this step's budget enter this step, should we send email notification(s)?
    allowPOEdit | Boolean | Optional | When POs belonging to this step's budget are in this step, can the PO be edited?
    allowPR | Boolean | Required | When POs belonging to this step's budget are in this step, can items be received?
    """

class General_ledgersNamespace(LimbleEndpoint):
    """
    This request returns your GLs in Limble.  
    
    Return data description

    Property | Description
    ----------------------
    glID | The GL's unique identifier.
    abbr | An abbreviation for the GL.
    name | The full name of the GL.
    locationID | Which Location this GL belongs to.
    description | An optional bit of descriptive text for the GL.
    assetID | Which Asset this GL belongs to.

    Query Parameters:
    - cursor: This parameter is a cursor that selects what glID you want to start receiving results at. e.g. passing 137 here will only get you GLs with an ID greater than 137.
    - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
    - name: This is a parameter used to string search for a name or partial name of a GL. This parameter expects a string with the wildcard %.
    - abbr: This is a parameter used to string search for an abbreviation or partial abbreviation of a GL. This parameter expects a string with the wildcard %.
    - locations: This parameter is used to only get GLs that are linked to a location. This parameter accepts a comma delimited list of location IDs.
    - gls: This parameter is used to only get specific GLs. This parameter accepts a comma delimited list of GL IDs.
    - assets: This parameter is used to only get GLs that are linked to an asset. This parameter accepts a comma delimited list of asset IDs.
    """
    @property
    def new_general_ledger(self) -> General_ledgersNew_general_ledgerNamespace:
        """
        This request creates a new General Ledger.

        Parameter | Type | Required? | Description
        ------------------------------------------
        locationID | Int | Required | The ID of the location this GL will be created for.
        assetID | Int | Required | The ID of the asset that this GL will be associated with.
        abbr | String | Required | An short version of this GLs name.
        name | String | Required | A full title for this GL.
        description | String | Optional | Any further needed description for this GL.
        """
        ...
    @property
    def update_general_ledger(self) -> General_ledgersUpdate_general_ledgerNamespace:
        """
        This request updates a General Ledger.

        Parameter | Type | Required? | Description
        ------------------------------------------
        assetID | Int | Optional | The ID of the asset that this GL will be associated with. Must be a valid assetID that belongs to the current GL's location.
        abbr | String | Optional | An new short version of this GLs name.
        name | String | Optional | A new title for this GL.
        description | String | Optional | Any further needed description for this GL.
        """
        ...
    @property
    def delete_general_ledger(self) -> General_ledgersDelete_general_ledgerNamespace:
        """
        This request deletes a GL. If any PO Items are associated to this GL, their glID will be set to 0.
        """
        ...

class General_ledgersDelete_general_ledgerNamespace(LimbleEndpoint):
    """
    This request deletes a GL. If any PO Items are associated to this GL, their glID will be set to 0.
    """

class General_ledgersUpdate_general_ledgerNamespace(LimbleEndpoint):
    """
    This request updates a General Ledger.

    Parameter | Type | Required? | Description
    ------------------------------------------
    assetID | Int | Optional | The ID of the asset that this GL will be associated with. Must be a valid assetID that belongs to the current GL's location.
    abbr | String | Optional | An new short version of this GLs name.
    name | String | Optional | A new title for this GL.
    description | String | Optional | Any further needed description for this GL.
    """

class General_ledgersNew_general_ledgerNamespace(LimbleEndpoint):
    """
    This request creates a new General Ledger.

    Parameter | Type | Required? | Description
    ------------------------------------------
    locationID | Int | Required | The ID of the location this GL will be created for.
    assetID | Int | Required | The ID of the asset that this GL will be associated with.
    abbr | String | Required | An short version of this GLs name.
    name | String | Required | A full title for this GL.
    description | String | Optional | Any further needed description for this GL.
    """

class Purchase_ordersNamespace(LimbleEndpoint):
    """

    Property | Description
    ----------------------
    meta | useful links relating to this Purchase order
    poID | The unique ID of the Purchase Order.
    poNumber | The user-set Purchase Order number.
    budgetID | The unique ID of the budget associated with this Purchase Order.
    vendorID | The unique ID of the vendor associated with this Purchase Order.
    locationID | The unique ID of the location associated with this Purchase Order.
    userIDStarted | The unique ID of the user that started this Purchase Order.
    userID | The unique ID of the user this Purchase Order is currently assigned to.
    teamID | The unique ID of the team the user of this Purchase Order is currently assigned to.
    requestedByUserID | The userID of the user that request this Purchase Order. A value of 0 means this PO wasn't requested, but was manually started by the userIDStarted.
    date | The date this PO was started as a UNIX timestamp, or the date the user inputted for the Purchase Order.
    expectedDate | The date this PO is expected as a UNIX timestamp to receive items.
    billTo | The address that should receive the bill for the PO.
    shipTo | The address the PO's items should be delivered to.
    notesToVendor | Any notes sent to the vendor, possibly containing handling, packaging, or delivery instructions.
    customField1 | PO custom field, the customer chooses which custom fields are available on all POs.
    customField2 | PO custom field, the customer chooses which custom fields are available on all POs.
    customField3 | PO custom field, the customer chooses which custom fields are available on all POs.
    customField4 | PO custom field, the customer chooses which custom fields are available on all POs.
    customField5 | PO custom field, the customer chooses which custom fields are available on all POs.
    customField6 | PO custom field, the customer chooses which custom fields are available on all POs.
    poPrefix | If a PO prefix is configured, it will show up here.
    lastEdited | Last time this PO was edited as a UNIX timestamp.
    status | This is the current status of a PO. Status of PO can be as follows:0: the PO has only been setup. (Status: Setup)1-97: these are custom statuses based on the budget steps. Refer to "budgetSteps" in meta. (Status : {Name of the budgetStep it is on} )97: the PO is in the ready to receive step. This means items can be received for this PO. (Status: Ready to Receive)98 all budget steps have been completed, but not all items on the PO have been received. This means only some items or partial qty of items have been received. (Status: Partially Received)99: the PO is completed. This means all the items and their full qty on the PO have been received but not been paid for ( i.e. all the bills generated for this PO have not been marked as paid yet.) (Status: Fully Received - Pending Payment)100: the PO is closed. This means all the items on the PO have been received and have been paid for. (i.e. all the bills for this PO have been marked as paid.) (Status: Closed)
    stateDetails | JSON object containing details about the PO's current state, and available state transitions.
    poNumberDisplay | Formatted display string with leading zeros and prefix. This is the PO Number the UI will display.

    Query Parameters:
    - pos: This parameter is used to only get specific POs. This parameter expects a comma delimited list of PO IDs.
    - vendors: This parameter is used to only get specific Vendors. This parameter expects a comma delimited list of Vendor IDs.
    - locations: This parameter is used to only get POs at a specific group of Locations. This parameter accepts a comma delimited list of Location IDs.
    - numbers: This parameter is used to only get specific POs by Number. This parameter expects a comma delimited list of PO Numbers.
    - cursor: This parameter is a cursor that selects what poID you want to start receiving results at. e.g. passing 137 here will only get you PO with an id greater than 137.
    - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
    - lastEditedStart: This parameter is used to only get POs that were last edited after the unix timestamp passed into the start parameter. For example, all POs that were last edited after April 18th, 2018.
    - lastEditedEnd: This parameter is used to only get POs that were last edited *before* the unix timestamp passed in.
    - status: This parameter is used to only get POs for a specific group of status.
    - page: This parameter is used to paginate results based on the limit. Refer to Pagination section for more information.
    """
    @property
    def items(self) -> Purchase_ordersItemsNamespace: ...
    @property
    def comments(self) -> Purchase_ordersCommentsNamespace: ...
    @property
    def state(self) -> Purchase_ordersStateNamespace: ...
    @property
    def new_purchase_order(self) -> Purchase_ordersNew_purchase_orderNamespace:
        """
        This request creates a new Purchase Order.

        Parameter | Type | Required? | Description
        ------------------------------------------
        locationID | Int | Required | The ID of the location this PO will be created for.
        vendorID | Int | Required | The ID of the vendor that this PO will be associated with.
        userID | Int | Required | The ID of the user that this PO will be assigned to.
        taskID | Int | Optional | The ID of the task that this PO will be associated with.
        budgetID | Int | Optional | The ID of the budget that this PO will be associated with. If not provided, this will be the location's default budget.
        date | Int | Optional | The start time of the PO -- this can be in the past or the future and will still show up in the UI. Must be a unix timestamp. If not provided, this will default to the current time.
        expectedDate | Int | Optional | The expected delivery date of this PO. Must be a unix timestamp.
        requestDescription | String | Optional | A description of the "request" for this PO.
        customField1 | String | Optional | PO custom field, the customer chooses which custom fields are available on all POs.
        customField2 | String | Optional | PO custom field, the customer chooses which custom fields are available on all POs.
        customField3 | String | Optional | PO custom field, the customer chooses which custom fields are available on all POs.
        customField4 | String | Optional | PO custom field, the customer chooses which custom fields are available on all POs.
        customField5 | String | Optional | PO custom field, the customer chooses which custom fields are available on all POs.
        customField6 | String | Optional | PO custom field, the customer chooses which custom fields are available on all POs.
        """
        ...
    @property
    def update_purchase_order(self) -> Purchase_ordersUpdate_purchase_orderNamespace:
        """
        This request updates a Purchase Order. Currently, changing the locationID that a PO belongs to is unsupported.

        Parameter | Type | Required? | Description
        ------------------------------------------
        vendorID | Int | Optional | The ID of the vendor that this PO will be associated with.
        userID | Int | Optional | The ID of the user that this PO will be assigned to.
        taskID | Int | Optional | The ID of the task that this PO will be associated with.
        budgetID | Int | Optional | The ID of the budget that this PO will be associated with. Changing budgetID when the PO is past the setup phase (state 0) is not supported.
        date | Int | Optional | The start time of the PO -- this can be in the past or the future and will still show up in the UI. Must be a unix timestamp.
        expectedDate | Int | Optional | The expected delivery date of this PO. Must be a unix timestamp.
        requestDescription | String | Optional | A description of the "request" for this PO.
        customField1 | String | Optional | PO custom field, the customer chooses which custom fields are available on all POs.
        customField2 | String | Optional | PO custom field, the customer chooses which custom fields are available on all POs.
        customField3 | String | Optional | PO custom field, the customer chooses which custom fields are available on all POs.
        customField4 | String | Optional | PO custom field, the customer chooses which custom fields are available on all POs.
        customField5 | String | Optional | PO custom field, the customer chooses which custom fields are available on all POs.
        customField6 | String | Optional | PO custom field, the customer chooses which custom fields are available on all POs.
        """
        ...
    @property
    def delete_po(self) -> Purchase_ordersDelete_poNamespace:
        """
        <p>This request deletes a PO. This will also delete any PO Items that belong to this PO, which will also remove any relationships between PO Items, Parts, and Tasks, and will clean up any history of transactions on these PO Items.</p>
        """
        ...

class Purchase_ordersDelete_poNamespace(LimbleEndpoint):
    """
    <p>This request deletes a PO. This will also delete any PO Items that belong to this PO, which will also remove any relationships between PO Items, Parts, and Tasks, and will clean up any history of transactions on these PO Items.</p>
    """

class Purchase_ordersUpdate_purchase_orderNamespace(LimbleEndpoint):
    """
    This request updates a Purchase Order. Currently, changing the locationID that a PO belongs to is unsupported.

    Parameter | Type | Required? | Description
    ------------------------------------------
    vendorID | Int | Optional | The ID of the vendor that this PO will be associated with.
    userID | Int | Optional | The ID of the user that this PO will be assigned to.
    taskID | Int | Optional | The ID of the task that this PO will be associated with.
    budgetID | Int | Optional | The ID of the budget that this PO will be associated with. Changing budgetID when the PO is past the setup phase (state 0) is not supported.
    date | Int | Optional | The start time of the PO -- this can be in the past or the future and will still show up in the UI. Must be a unix timestamp.
    expectedDate | Int | Optional | The expected delivery date of this PO. Must be a unix timestamp.
    requestDescription | String | Optional | A description of the "request" for this PO.
    customField1 | String | Optional | PO custom field, the customer chooses which custom fields are available on all POs.
    customField2 | String | Optional | PO custom field, the customer chooses which custom fields are available on all POs.
    customField3 | String | Optional | PO custom field, the customer chooses which custom fields are available on all POs.
    customField4 | String | Optional | PO custom field, the customer chooses which custom fields are available on all POs.
    customField5 | String | Optional | PO custom field, the customer chooses which custom fields are available on all POs.
    customField6 | String | Optional | PO custom field, the customer chooses which custom fields are available on all POs.
    """

class Purchase_ordersNew_purchase_orderNamespace(LimbleEndpoint):
    """
    This request creates a new Purchase Order.

    Parameter | Type | Required? | Description
    ------------------------------------------
    locationID | Int | Required | The ID of the location this PO will be created for.
    vendorID | Int | Required | The ID of the vendor that this PO will be associated with.
    userID | Int | Required | The ID of the user that this PO will be assigned to.
    taskID | Int | Optional | The ID of the task that this PO will be associated with.
    budgetID | Int | Optional | The ID of the budget that this PO will be associated with. If not provided, this will be the location's default budget.
    date | Int | Optional | The start time of the PO -- this can be in the past or the future and will still show up in the UI. Must be a unix timestamp. If not provided, this will default to the current time.
    expectedDate | Int | Optional | The expected delivery date of this PO. Must be a unix timestamp.
    requestDescription | String | Optional | A description of the "request" for this PO.
    customField1 | String | Optional | PO custom field, the customer chooses which custom fields are available on all POs.
    customField2 | String | Optional | PO custom field, the customer chooses which custom fields are available on all POs.
    customField3 | String | Optional | PO custom field, the customer chooses which custom fields are available on all POs.
    customField4 | String | Optional | PO custom field, the customer chooses which custom fields are available on all POs.
    customField5 | String | Optional | PO custom field, the customer chooses which custom fields are available on all POs.
    customField6 | String | Optional | PO custom field, the customer chooses which custom fields are available on all POs.
    """

class Purchase_ordersStateNamespace(object):
    @property
    def change_po_state(self) -> Purchase_ordersStateChange_po_stateNamespace:
        """
        Updates the state of the specified PO.  
          
        Important Note: Currently POs can only move forward one state per state change request.
        
        Parameters:
        
        | Parameter | In | Type | Required | Default | Description |
        | --- | --- | --- | --- | --- | --- |
        | poID | path | integer | yes |  | Purchase Order identifier |
        | newState | body | string | yes |  | All PO states: 0 (setup), 1–96 (custom), 97 (ready_to_receive), 98 (partially_received), 99 (fully_received), 100 (closed), 101 (disapproved). API accepts numbers, standard names, or custom_step_N |
        | reason | body | string | no |  | Optional note (max 500 chars) |
        
        Responses:
        
        - 200 OK: State changed.
            
        - 400 Bad Request: Invalid transition or failed validation.
            
        - 404 Not Found: PO not found.
            
        
        Response data:

        Property | Description
        ----------------------
        success | Boolean, if this operation was successful
        state | JSON object describing current state.
        previousState | JSON object describing previous state.
        validNextStates | JSON object with a list of possible next states.
        """
        ...
    @property
    def get_po_state_transitions(self) -> Purchase_ordersStateGet_po_state_transitionsNamespace:
        """
        Returns the list of valid next states for the specified PO.
        
        Parameters:

        Parameter | Type | Required | Default | Description
        ---------------------------------------------------
        poID | integer | yes |  | Purchase Order identifier

        Return data:  
          
        Array of JSON objects listing possible next state transitions for the selected PO.
        """
        ...

class Purchase_ordersStateGet_po_state_transitionsNamespace(LimbleEndpoint):
    """
    Returns the list of valid next states for the specified PO.
    
    Parameters:

    Parameter | Type | Required | Default | Description
    ---------------------------------------------------
    poID | integer | yes |  | Purchase Order identifier

    Return data:  
      
    Array of JSON objects listing possible next state transitions for the selected PO.
    """

class Purchase_ordersStateChange_po_stateNamespace(LimbleEndpoint):
    """
    Updates the state of the specified PO.  
      
    Important Note: Currently POs can only move forward one state per state change request.
    
    Parameters:
    
    | Parameter | In | Type | Required | Default | Description |
    | --- | --- | --- | --- | --- | --- |
    | poID | path | integer | yes |  | Purchase Order identifier |
    | newState | body | string | yes |  | All PO states: 0 (setup), 1–96 (custom), 97 (ready_to_receive), 98 (partially_received), 99 (fully_received), 100 (closed), 101 (disapproved). API accepts numbers, standard names, or custom_step_N |
    | reason | body | string | no |  | Optional note (max 500 chars) |
    
    Responses:
    
    - 200 OK: State changed.
        
    - 400 Bad Request: Invalid transition or failed validation.
        
    - 404 Not Found: PO not found.
        
    
    Response data:

    Property | Description
    ----------------------
    success | Boolean, if this operation was successful
    state | JSON object describing current state.
    previousState | JSON object describing previous state.
    validNextStates | JSON object with a list of possible next states.
    """

class Purchase_ordersCommentsNamespace(object):
    @property
    def po_comments(self) -> Purchase_ordersCommentsPo_commentsNamespace:
        """
        This request gets all PO Comments associated with a PO.
        
        Return data description

        Property | Description
        ----------------------
        commentID | This is the commentID of comment.
        comment | The text comment that was entered by the user.
        timestamp | The date this comment was created. This is a unix timestamp.
        userID | The ID of the user that made the comment.
        commentEmailAddress | The email address of the external user that made this comment. This is only populated if the comment was made by an external user via the comment reply system.
        commentFiles | Array containing fileName and link properties.

        Query Parameters:
        - cursor: This parameter is a cursor that selects what commentID you want to start receiving results at. e.g. passing 137 here will only get you comments with an id greater than 137.
        - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
        """
        ...
    @property
    def upload_po_comment_file(self) -> Purchase_ordersCommentsUpload_po_comment_fileNamespace:
        """
        Uploads a file to a PO comment.
        
        Parameters:

        Parameter | In | Type | Required | Default | Description
        --------------------------------------------------------
        poID | path | integer | yes |  | Purchase Order identifier
        commentID | path | integer | yes |  | Comment identifier
        file | form-data | file | yes |  | File to upload (max 50MB). Types: PDF, PNG, JPEG, GIF, TIFF, SVG, DOC, DOCX, XLS, XLSX, ZIP, RAR, RFC822, octet-stream
        """
        ...
    @property
    def delete_po_comment_file(self) -> Purchase_ordersCommentsDelete_po_comment_fileNamespace:
        """
        Deletes a file from a PO comment.
        
        Parameters:

        Parameter | In | Type | Required | Default | Description
        --------------------------------------------------------
        poID | path | integer | yes |  | Purchase Order identifier
        commentID | path | integer | yes |  | Comment identifier
        filename | query | string | yes |  | Exact filename to remove

        Responses:
        - 200 OK: Deleted.
        - 404 Not Found: File not found.

        Query Parameters:
        - filename: 
        """
        ...
    @property
    def create_po_comment(self) -> Purchase_ordersCommentsCreate_po_commentNamespace:
        """
        Adds a comment to the specified PO.
        
        Parameters:

        Parameter | In | Type | Required | Default | Description
        --------------------------------------------------------
        poID | path | integer | yes |  | Purchase Order identifier
        comment | body | string | yes |  | Comment text
        showExternalUsers | body | boolean | no | true | Visible to external users

        Responses:
        - 201 Created: Returns commentID.
        """
        ...
    @property
    def delete_po_comment(self) -> Purchase_ordersCommentsDelete_po_commentNamespace:
        """
        Deletes a PO comment.
        
        Parameters:

        Parameter | In | Type | Required | Default | Description
        --------------------------------------------------------
        poID | path | integer | yes |  | Purchase Order identifier
        commentID | path | integer | yes |  | Comment identifier

        Responses:
        - 200 OK: Deleted.
        - 404 Not Found: Comment not found.
        """
        ...

class Purchase_ordersCommentsDelete_po_commentNamespace(LimbleEndpoint):
    """
    Deletes a PO comment.
    
    Parameters:

    Parameter | In | Type | Required | Default | Description
    --------------------------------------------------------
    poID | path | integer | yes |  | Purchase Order identifier
    commentID | path | integer | yes |  | Comment identifier

    Responses:
    - 200 OK: Deleted.
    - 404 Not Found: Comment not found.
    """

class Purchase_ordersCommentsCreate_po_commentNamespace(LimbleEndpoint):
    """
    Adds a comment to the specified PO.
    
    Parameters:

    Parameter | In | Type | Required | Default | Description
    --------------------------------------------------------
    poID | path | integer | yes |  | Purchase Order identifier
    comment | body | string | yes |  | Comment text
    showExternalUsers | body | boolean | no | true | Visible to external users

    Responses:
    - 201 Created: Returns commentID.
    """

class Purchase_ordersCommentsDelete_po_comment_fileNamespace(LimbleEndpoint):
    """
    Deletes a file from a PO comment.
    
    Parameters:

    Parameter | In | Type | Required | Default | Description
    --------------------------------------------------------
    poID | path | integer | yes |  | Purchase Order identifier
    commentID | path | integer | yes |  | Comment identifier
    filename | query | string | yes |  | Exact filename to remove

    Responses:
    - 200 OK: Deleted.
    - 404 Not Found: File not found.

    Query Parameters:
    - filename: 
    """

class Purchase_ordersCommentsUpload_po_comment_fileNamespace(LimbleEndpoint):
    """
    Uploads a file to a PO comment.
    
    Parameters:

    Parameter | In | Type | Required | Default | Description
    --------------------------------------------------------
    poID | path | integer | yes |  | Purchase Order identifier
    commentID | path | integer | yes |  | Comment identifier
    file | form-data | file | yes |  | File to upload (max 50MB). Types: PDF, PNG, JPEG, GIF, TIFF, SVG, DOC, DOCX, XLS, XLSX, ZIP, RAR, RFC822, octet-stream
    """

class Purchase_ordersCommentsPo_commentsNamespace(LimbleEndpoint):
    """
    This request gets all PO Comments associated with a PO.
    
    Return data description

    Property | Description
    ----------------------
    commentID | This is the commentID of comment.
    comment | The text comment that was entered by the user.
    timestamp | The date this comment was created. This is a unix timestamp.
    userID | The ID of the user that made the comment.
    commentEmailAddress | The email address of the external user that made this comment. This is only populated if the comment was made by an external user via the comment reply system.
    commentFiles | Array containing fileName and link properties.

    Query Parameters:
    - cursor: This parameter is a cursor that selects what commentID you want to start receiving results at. e.g. passing 137 here will only get you comments with an id greater than 137.
    - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
    """

class Purchase_ordersItemsNamespace(object):
    @property
    def get_purchase_order_items(self) -> Purchase_ordersItemsGet_purchase_order_itemsNamespace:
        """
        This request gets information associated with PO items. Every line item on a PO is an item returned by this call.
        
        Return data description

        Property | Description
        ----------------------
        poID | The unique ID of the purchase order associated to this item.
        poItemID | The unqiue ID of this Purchase Order Item
        itemType | Which type (Part, Service, or Other) this item is.
        name | The name of the item.
        description | A more detailed description of the item.
        glID | The unique ID of the GL associated to this item.
        partID | The unique ID of the part associated to this item.
        taskID | The unique ID of the task associated to this item.
        poNumber | The user-set Purchase Order number.
        qty | The quantity purchased.
        rate | The billing rate for the item on the Purchase Order.
        tax | The tax percent rate for the item on the Purchase Order.
        discount | The discount percent rate for the item on the Purchase Order.
        shipping | The shipping rate for the item on the Purchase Order.
        qtyReceived | A number representing the total quantity that has been marked as "received" for this item.
        lastEdited | Last time this PO item was edited, this field outputs a UNIX timestamp.
        orderUnitAbbreviation | The abbreviation for the unit of measure in which the PO item was ordered. (NULL for items not assigned to a unit of measure)

        Query Parameters:
        - pos: This parameter is used to only get specific POs. This parameter expects a comma delimited list of PO IDs.
        - items: This parameter is used to only get specific PO Items by ID. This parameter expects a comma delimited list of poItem IDs.
        - numbers: This parameter is used to only get specific POs by Number. This parameter expects a comma delimited list of PO Numbers.
        - cursor: This parameter is a cursor that selects what vendorID you want to start receiving results at. e.g. passing 137 here will only get you vendors with an id greater than 137.
        - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
        - lastEditedStart: This parameter is used to only get PO items that were last edited after the unix timestamp passed into the start parameter. For example, all PO items that were last edited after April 18th, 2018.
        - lastEditedEnd: This parameter is used to only get POs items that were last edited *before* the unix timestamp passed in.
        """
        ...
    @property
    def new_purchase_order_item(self) -> Purchase_ordersItemsNew_purchase_order_itemNamespace:
        """
        This request creates a new Purchase Order Item.

        Parameter | Type | Required? | Description
        ------------------------------------------
        itemType | Int | Required | A number describing what type of PO Item this is. Valid values are: 1 (Part), 2 (Service), 4 (Other). If itemType is 1, name and taskID cannot be present and partID is required. If itemType is 2 or 4, name is required and partID cannot be present. If itemType is 2, a checklistID is required.
        name | String | Optional | A short line-item title for this PO Item.
        description | String | Optional | A more detailed description for this PO Item.
        glID | Int | Optional | The ID of the General Ledger that this PO Item will belong to.
        taskID | Int | Optional | The ID of the Task that this PO Item will belong to.
        assetID | Int | Optional | The ID of the Asset that this PO Item will belong to.
        partID | Int | Optional | The ID of the Part that this PO Item will belong to.
        quantity | Int | Optional | A number for how many items are represented in this line. If not provided, the minimum and default values are 1.
        rate | Float | Optional | A decimal (precision 4) representing the cost of one of the item(s). Default is 0.0000
        tax | Float | Optional | A decimal (precision 4) representing the amount of tax on the item(s) as a percent. Default is 0.0000
        discount | Float | Optional | A decimal (precision 4) representing the discounted cost on the item(s) as a percent. Default is 0.0000
        shipping | Float | Optional | A decimal (precision 4) representing the cost of shipping for the item(s). Default is 0.0000
        """
        ...
    @property
    def update_purchase_order_item(self) -> Purchase_ordersItemsUpdate_purchase_order_itemNamespace:
        """
        This request updates a Purchase Order Item. Considering the validation for this route is non-trivial -- keep in mind that before this update takes place, we validate the resulting PO Item, so the itemType must be valid with any existing or updated properties. For example, if you have a PO Item of itemType 1 (Part) and attempt to send a PATCH that only provides a checklistID, you will get an error back saying that this is an invalid combination.
        
        To remove an associated ID, pass in the value 0.

        Parameter | Type | Required? | Description
        ------------------------------------------
        itemType | Int | Optional | A number describing what type of PO Item this is. Valid values are: 1 (Part), 2 (Service), 4 (Other). If itemType is 1, name and taskID cannot be present and partID is required. If itemType is 2 or 4, name is required and partID cannot be present. If itemType is 2, a checklistID is required.
        name | String | Optional | A short line-item title for this PO Item.
        description | String | Optional | A more detailed description for this PO Item.
        glID | Int | Optional | The ID of the General Ledger that this PO Item will belong to.
        taskID | Int | Optional | The ID of the Task that this PO Item will belong to.
        assetID | Int | Optional | The ID of the Asset that this PO Item will belong to.
        partID | Int | Optional | The ID of the Part that this PO Item will belong to.
        quantity | Int | Optional | A number for how many items are represented in this line. If not provided, the minimum and default values are 1.
        rate | Float | Optional | A decimal (precision 4) representing the cost of one of the item(s). Default is 0.0000
        tax | Float | Optional | A decimal (precision 4) representing the amount of tax on the item(s) as a percent. Default is 0.0000
        discount | Float | Optional | A decimal (precision 4) representing the discounted cost on the item(s) as a percent. Default is 0.0000
        shipping | Float | Optional | A decimal (precision 4) representing the cost of shipping for the item(s). Default is 0.0000
        """
        ...
    @property
    def delete_po_item(self) -> Purchase_ordersItemsDelete_po_itemNamespace:
        """
        <p>This request deletes a PO Item, which will also remove any relationships between the PO Item, Parts, and Tasks, and will clean up any history of transactions on this PO Item.</p>
        """
        ...
    @property
    def receive_po_item(self) -> Purchase_ordersItemsReceive_po_itemNamespace:
        """
        This request marks a quantity of a PO item as having been received and generates a bill for the receipt of the item.
        
        
        Return data description
        
        
        
        Property
        Description
        
        
        
        
        transactionID
        The unique ID of the transaction created by this request.
        
        
        prID
        The unique ID of the PR (Bill) created by this request.

        Parameter | Type | Required? | Description
        ------------------------------------------
        quantity | Int | Required | A positive number representing the received number of items. The sum of all receipts cannot be greater than the total quantity on the PO item.For example: if a PO item has a quantity of 5, then we use this request to receive 3, that will mark 3 of the PO item as received and generate a bill for that receipt of 3 PO items. If we run the same request again to receive another 3, the total would be 6 and the request would be rejected with an error.
        """
        ...

class Purchase_ordersItemsReceive_po_itemNamespace(LimbleEndpoint):
    """
    This request marks a quantity of a PO item as having been received and generates a bill for the receipt of the item.
    
    
    Return data description
    
    
    
    Property
    Description
    
    
    
    
    transactionID
    The unique ID of the transaction created by this request.
    
    
    prID
    The unique ID of the PR (Bill) created by this request.

    Parameter | Type | Required? | Description
    ------------------------------------------
    quantity | Int | Required | A positive number representing the received number of items. The sum of all receipts cannot be greater than the total quantity on the PO item.For example: if a PO item has a quantity of 5, then we use this request to receive 3, that will mark 3 of the PO item as received and generate a bill for that receipt of 3 PO items. If we run the same request again to receive another 3, the total would be 6 and the request would be rejected with an error.
    """

class Purchase_ordersItemsDelete_po_itemNamespace(LimbleEndpoint):
    """
    <p>This request deletes a PO Item, which will also remove any relationships between the PO Item, Parts, and Tasks, and will clean up any history of transactions on this PO Item.</p>
    """

class Purchase_ordersItemsUpdate_purchase_order_itemNamespace(LimbleEndpoint):
    """
    This request updates a Purchase Order Item. Considering the validation for this route is non-trivial -- keep in mind that before this update takes place, we validate the resulting PO Item, so the itemType must be valid with any existing or updated properties. For example, if you have a PO Item of itemType 1 (Part) and attempt to send a PATCH that only provides a checklistID, you will get an error back saying that this is an invalid combination.
    
    To remove an associated ID, pass in the value 0.

    Parameter | Type | Required? | Description
    ------------------------------------------
    itemType | Int | Optional | A number describing what type of PO Item this is. Valid values are: 1 (Part), 2 (Service), 4 (Other). If itemType is 1, name and taskID cannot be present and partID is required. If itemType is 2 or 4, name is required and partID cannot be present. If itemType is 2, a checklistID is required.
    name | String | Optional | A short line-item title for this PO Item.
    description | String | Optional | A more detailed description for this PO Item.
    glID | Int | Optional | The ID of the General Ledger that this PO Item will belong to.
    taskID | Int | Optional | The ID of the Task that this PO Item will belong to.
    assetID | Int | Optional | The ID of the Asset that this PO Item will belong to.
    partID | Int | Optional | The ID of the Part that this PO Item will belong to.
    quantity | Int | Optional | A number for how many items are represented in this line. If not provided, the minimum and default values are 1.
    rate | Float | Optional | A decimal (precision 4) representing the cost of one of the item(s). Default is 0.0000
    tax | Float | Optional | A decimal (precision 4) representing the amount of tax on the item(s) as a percent. Default is 0.0000
    discount | Float | Optional | A decimal (precision 4) representing the discounted cost on the item(s) as a percent. Default is 0.0000
    shipping | Float | Optional | A decimal (precision 4) representing the cost of shipping for the item(s). Default is 0.0000
    """

class Purchase_ordersItemsNew_purchase_order_itemNamespace(LimbleEndpoint):
    """
    This request creates a new Purchase Order Item.

    Parameter | Type | Required? | Description
    ------------------------------------------
    itemType | Int | Required | A number describing what type of PO Item this is. Valid values are: 1 (Part), 2 (Service), 4 (Other). If itemType is 1, name and taskID cannot be present and partID is required. If itemType is 2 or 4, name is required and partID cannot be present. If itemType is 2, a checklistID is required.
    name | String | Optional | A short line-item title for this PO Item.
    description | String | Optional | A more detailed description for this PO Item.
    glID | Int | Optional | The ID of the General Ledger that this PO Item will belong to.
    taskID | Int | Optional | The ID of the Task that this PO Item will belong to.
    assetID | Int | Optional | The ID of the Asset that this PO Item will belong to.
    partID | Int | Optional | The ID of the Part that this PO Item will belong to.
    quantity | Int | Optional | A number for how many items are represented in this line. If not provided, the minimum and default values are 1.
    rate | Float | Optional | A decimal (precision 4) representing the cost of one of the item(s). Default is 0.0000
    tax | Float | Optional | A decimal (precision 4) representing the amount of tax on the item(s) as a percent. Default is 0.0000
    discount | Float | Optional | A decimal (precision 4) representing the discounted cost on the item(s) as a percent. Default is 0.0000
    shipping | Float | Optional | A decimal (precision 4) representing the cost of shipping for the item(s). Default is 0.0000
    """

class Purchase_ordersItemsGet_purchase_order_itemsNamespace(LimbleEndpoint):
    """
    This request gets information associated with PO items. Every line item on a PO is an item returned by this call.
    
    Return data description

    Property | Description
    ----------------------
    poID | The unique ID of the purchase order associated to this item.
    poItemID | The unqiue ID of this Purchase Order Item
    itemType | Which type (Part, Service, or Other) this item is.
    name | The name of the item.
    description | A more detailed description of the item.
    glID | The unique ID of the GL associated to this item.
    partID | The unique ID of the part associated to this item.
    taskID | The unique ID of the task associated to this item.
    poNumber | The user-set Purchase Order number.
    qty | The quantity purchased.
    rate | The billing rate for the item on the Purchase Order.
    tax | The tax percent rate for the item on the Purchase Order.
    discount | The discount percent rate for the item on the Purchase Order.
    shipping | The shipping rate for the item on the Purchase Order.
    qtyReceived | A number representing the total quantity that has been marked as "received" for this item.
    lastEdited | Last time this PO item was edited, this field outputs a UNIX timestamp.
    orderUnitAbbreviation | The abbreviation for the unit of measure in which the PO item was ordered. (NULL for items not assigned to a unit of measure)

    Query Parameters:
    - pos: This parameter is used to only get specific POs. This parameter expects a comma delimited list of PO IDs.
    - items: This parameter is used to only get specific PO Items by ID. This parameter expects a comma delimited list of poItem IDs.
    - numbers: This parameter is used to only get specific POs by Number. This parameter expects a comma delimited list of PO Numbers.
    - cursor: This parameter is a cursor that selects what vendorID you want to start receiving results at. e.g. passing 137 here will only get you vendors with an id greater than 137.
    - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
    - lastEditedStart: This parameter is used to only get PO items that were last edited after the unix timestamp passed into the start parameter. For example, all PO items that were last edited after April 18th, 2018.
    - lastEditedEnd: This parameter is used to only get POs items that were last edited *before* the unix timestamp passed in.
    """

class TeamsNamespace(LimbleEndpoint):
    """
    This request returns a list of Teams.

    Query Parameters:
    - teams: This parameter expects a comma-separated list of teamIDs to filter teams by.
    - name: This parameter is used to only get specific teams by name. This parameter expects a string full name of a team or partial name with the wildcard %.
    - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
    - cursor: This parameter is a cursor that selects what teamID you want to start receiving results at. e.g. passing 137 here will only get you tasks with an id greater than 137.
    - automaticallyCreated: This parameter is used to only get specific teams by if they were automatically created by Limble or not. This parameter expects a bool true or false. Teams can get dynamically created if multiple users are assigned to the same task, for example.
    - includeRoles: This parameter is used to determine whether role-based teams (Manager, Technician, etc) are included in the response.
    """
    @property
    def create_team(self) -> TeamsCreate_teamNamespace:
        """
        This request creates a new Team.

        Parameter | Type | Required? | Description
        ------------------------------------------
        name | String | Required | The name of the Team.
        locationID | string | Required | The locationID of the Location the Team will be available at.
        """
        ...
    @property
    def update_team(self) -> TeamsUpdate_teamNamespace:
        """
        Update a team name.

        Parameter | Type | Required? | Description
        ------------------------------------------
        name | String | Required | The name of the team.
        """
        ...
    @property
    def delete_team(self) -> TeamsDelete_teamNamespace:
        """
        This request deletes a Team. This will also remove the Team from any User it is assigned to.
        """
        ...

class TeamsDelete_teamNamespace(LimbleEndpoint):
    """
    This request deletes a Team. This will also remove the Team from any User it is assigned to.
    """

class TeamsUpdate_teamNamespace(LimbleEndpoint):
    """
    Update a team name.

    Parameter | Type | Required? | Description
    ------------------------------------------
    name | String | Required | The name of the team.
    """

class TeamsCreate_teamNamespace(LimbleEndpoint):
    """
    This request creates a new Team.

    Parameter | Type | Required? | Description
    ------------------------------------------
    name | String | Required | The name of the Team.
    locationID | string | Required | The locationID of the Location the Team will be available at.
    """

class RolesNamespace(LimbleEndpoint):
    """
    This request returns a list of Roles.

    Query Parameters:
    - roles: 
    - name: 
    - cursor: 
    - limit: 
    """
    @property
    def create_role(self) -> RolesCreate_roleNamespace:
        """
        This request creates a new Role.  Roles are used for access management in Limble. Once a Role is created you can assign permissions to that Role via the web application and then assign Users to that Role to control what that User can do in Limble.

        Parameter | Type | Required? | Description
        ------------------------------------------
        name | String | Required | The name of the role.
        """
        ...
    @property
    def update_role(self) -> RolesUpdate_roleNamespace:
        """
        This request updates a Role's name.

        Parameter | Type | Required? | Description
        ------------------------------------------
        name | String | Required | The name of the role.
        """
        ...
    @property
    def delete_role(self) -> RolesDelete_roleNamespace:
        """
        This Request deletes a Role.  This will also remove the Role from any User it is assigned to.
        """
        ...

class RolesDelete_roleNamespace(LimbleEndpoint):
    """
    This Request deletes a Role.  This will also remove the Role from any User it is assigned to.
    """

class RolesUpdate_roleNamespace(LimbleEndpoint):
    """
    This request updates a Role's name.

    Parameter | Type | Required? | Description
    ------------------------------------------
    name | String | Required | The name of the role.
    """

class RolesCreate_roleNamespace(LimbleEndpoint):
    """
    This request creates a new Role.  Roles are used for access management in Limble. Once a Role is created you can assign permissions to that Role via the web application and then assign Users to that Role to control what that User can do in Limble.

    Parameter | Type | Required? | Description
    ------------------------------------------
    name | String | Required | The name of the role.
    """

class VendorsNamespace(LimbleEndpoint):
    """
    This request gets information such as VendorIDs, Vendor Names, etc.
    
    This call returns a "meta" object containing URLs that can be used to get data related to a vendor.
    
    This call will also return an image array of objects that have a file name and a link you can use to download that image. All links are only valid for 15 minutes, a new call will generate a new link.
    
    **Note:** this endpoint supports pagination. Please refer to the [**Pagination**](#pagination) section for more information.

    Query Parameters:
    - vendors: This parameter is used to only get specific Vendors. This parameter expects a comma delimited list of Vendor IDs.
    - locations: This parameter is used to only get Vendors at a specific group of Locations. This parameter accepts a comma delimited list of Location IDs.
    - name: This parameter is used to only get specific vendor by name. This parameter expects a string full name of a vendor or partial name with the wildcard %.
    - start: This parameter is used to only get Vendors that were last edited after the unix timestamp passed into the start parameter. For example, all Vendors that were last edited after April 18th, 2018.
    - end: This parameter is used to only get Vendors that were last edited *before* the unix timestamp passed into the end parameter.
    - cursor: This parameter is a cursor that selects what vendorID you want to start receiving results at. e.g. passing 137 here will only get you vendors with an id greater than 137.
    - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
    - page: This parameter is used to paginate results based on the limit. Refer to Pagination section for more information.
    """
    @property
    def fields(self) -> VendorsFieldsNamespace: ...
    @property
    def images(self) -> VendorsImagesNamespace: ...
    @property
    def logs(self) -> VendorsLogsNamespace: ...
    @property
    def new_vendor(self) -> VendorsNew_vendorNamespace:
        """
        This request creates a new Vendor.

        Parameter | Type | Required? | Description
        ------------------------------------------
        name | String | Required | The name of the Vendor.
        locationID | string | Required | The locationID of the Location the Vendor will be at.
        email | string | Optional | The Vendor's email address.
        contact | string | Optional | The Vendor's primary contact.
        phone | string | Optional | The Vendor's phone number.
        address | string | Optional | The Vendor's address.
        """
        ...
    @property
    def update_vendor(self) -> VendorsUpdate_vendorNamespace:
        """
        This Request updates a Vendor's name, phone, email, contact, address, etc.

        Parameter | Type | Required? | Description
        ------------------------------------------
        name | String | Optional | The name of the Vendor.
        locationID | string | Required | The locationID of the Location the Vendor will be at.
        email | string | Optional | The Vendor's email address.
        contact | string | Optional | The Vendor's primary contact.
        address | string | Optional | The Vendor's address.
        phone | string | Optional | The Vendor's phone number.
        """
        ...
    @property
    def delete_vendor(self) -> VendorsDelete_vendorNamespace:
        """
        This request deletes a Vendor.
        """
        ...

class VendorsDelete_vendorNamespace(LimbleEndpoint):
    """
    This request deletes a Vendor.
    """

class VendorsUpdate_vendorNamespace(LimbleEndpoint):
    """
    This Request updates a Vendor's name, phone, email, contact, address, etc.

    Parameter | Type | Required? | Description
    ------------------------------------------
    name | String | Optional | The name of the Vendor.
    locationID | string | Required | The locationID of the Location the Vendor will be at.
    email | string | Optional | The Vendor's email address.
    contact | string | Optional | The Vendor's primary contact.
    address | string | Optional | The Vendor's address.
    phone | string | Optional | The Vendor's phone number.
    """

class VendorsNew_vendorNamespace(LimbleEndpoint):
    """
    This request creates a new Vendor.

    Parameter | Type | Required? | Description
    ------------------------------------------
    name | String | Required | The name of the Vendor.
    locationID | string | Required | The locationID of the Location the Vendor will be at.
    email | string | Optional | The Vendor's email address.
    contact | string | Optional | The Vendor's primary contact.
    phone | string | Optional | The Vendor's phone number.
    address | string | Optional | The Vendor's address.
    """

class VendorsLogsNamespace(object):
    @property
    def files(self) -> VendorsLogsFilesNamespace: ...
    @property
    def vendor_logs(self) -> VendorsLogsVendor_logsNamespace:
        """
        This request returns the manual log entries for a vendor.
        
        This request returns logs created manually by users on vendors. Logs related to tasks with vendors will not be returned.
        
        **Note:** this endpoint supports pagination. Please refer to the [**Pagination**](#pagination) section for more information.
        
        Return data description

        Property | Description
        ----------------------
        logID | The unique logID of the log.
        dateCreated | The date the log was created as a UNIX timestamp.
        vendorD | The ID of the vendor the log belongs to.
        logEntry | The log entry for the vendor.
        userID | The ID of the user that created the log.
        logFiles | An array of objects that have a fileID, fileName and a link that can used to download the files attached to the log. All links are only valid for 15 minutes, a new call will generate a new link.

        Query Parameters:
        - logs: This parameter is used to only get specific logs. This parameter accepts a comma delimited list of logIDs.
        - users: This parameter is used to only get logs created by specific users. This parameter accepts a comma delimited list of userIDs.
        - logEntry: This is a parameter used to string search for manual log entry. This parameter expects a string with the wildcard %.
        - start: This parameter is used to only get logs that were last edited after the unix timestamp passed into the start parameter. 
        - end: This parameter is used to only get logs that were last edited before the unix timestamp passed into the end parameter.
        - page: This parameter is used to paginate results based on the limit. Refer to Pagination section for more information.
        - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
        - cursor: This parameter is a cursor that selects what ID you want to start receiving results at. 
        """
        ...
    @property
    def new_vendor_log(self) -> VendorsLogsNew_vendor_logNamespace:
        """
        This creates a manual log entry for a vendor.

        Parameter | Type | Required? | Description
        ------------------------------------------
        userID | Int | Required | The ID of the user creating the log.
        logEntry | String | Required | Details of the log.
        """
        ...
    @property
    def update_vendor_log(self) -> VendorsLogsUpdate_vendor_logNamespace:
        """
        This request updates a manual log entry for a vendor.
        """
        ...
    @property
    def delete_vendor_log(self) -> VendorsLogsDelete_vendor_logNamespace:
        """
        This request deleted a manual log entry for a vendor.
        """
        ...

class VendorsLogsDelete_vendor_logNamespace(LimbleEndpoint):
    """
    This request deleted a manual log entry for a vendor.
    """

class VendorsLogsUpdate_vendor_logNamespace(LimbleEndpoint):
    """
    This request updates a manual log entry for a vendor.
    """

class VendorsLogsNew_vendor_logNamespace(LimbleEndpoint):
    """
    This creates a manual log entry for a vendor.

    Parameter | Type | Required? | Description
    ------------------------------------------
    userID | Int | Required | The ID of the user creating the log.
    logEntry | String | Required | Details of the log.
    """

class VendorsLogsVendor_logsNamespace(LimbleEndpoint):
    """
    This request returns the manual log entries for a vendor.
    
    This request returns logs created manually by users on vendors. Logs related to tasks with vendors will not be returned.
    
    **Note:** this endpoint supports pagination. Please refer to the [**Pagination**](#pagination) section for more information.
    
    Return data description

    Property | Description
    ----------------------
    logID | The unique logID of the log.
    dateCreated | The date the log was created as a UNIX timestamp.
    vendorD | The ID of the vendor the log belongs to.
    logEntry | The log entry for the vendor.
    userID | The ID of the user that created the log.
    logFiles | An array of objects that have a fileID, fileName and a link that can used to download the files attached to the log. All links are only valid for 15 minutes, a new call will generate a new link.

    Query Parameters:
    - logs: This parameter is used to only get specific logs. This parameter accepts a comma delimited list of logIDs.
    - users: This parameter is used to only get logs created by specific users. This parameter accepts a comma delimited list of userIDs.
    - logEntry: This is a parameter used to string search for manual log entry. This parameter expects a string with the wildcard %.
    - start: This parameter is used to only get logs that were last edited after the unix timestamp passed into the start parameter. 
    - end: This parameter is used to only get logs that were last edited before the unix timestamp passed into the end parameter.
    - page: This parameter is used to paginate results based on the limit. Refer to Pagination section for more information.
    - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
    - cursor: This parameter is a cursor that selects what ID you want to start receiving results at. 
    """

class VendorsLogsFilesNamespace(object):
    @property
    def delete_vendor_log_file(self) -> VendorsLogsFilesDelete_vendor_log_fileNamespace:
        """
        This requests deletes a file attached to a log.
        """
        ...
    @property
    def add_vendor_log_file(self) -> VendorsLogsFilesAdd_vendor_log_fileNamespace:
        """
        This request adds files to a log.
        
        Return data description

        Property | Description
        ----------------------
        fileID | The ID of the file attached to the log.
        """
        ...

class VendorsLogsFilesAdd_vendor_log_fileNamespace(LimbleEndpoint):
    """
    This request adds files to a log.
    
    Return data description

    Property | Description
    ----------------------
    fileID | The ID of the file attached to the log.
    """

class VendorsLogsFilesDelete_vendor_log_fileNamespace(LimbleEndpoint):
    """
    This requests deletes a file attached to a log.
    """

class VendorsImagesNamespace(object):
    @property
    def add_vendor_image(self) -> VendorsImagesAdd_vendor_imageNamespace:
        """
        This request adds the main image to a Vendor.
        """
        ...
    @property
    def delete_vendor_image(self) -> VendorsImagesDelete_vendor_imageNamespace:
        """
        This request removes the main image from a Vendor.
        """
        ...

class VendorsImagesDelete_vendor_imageNamespace(LimbleEndpoint):
    """
    This request removes the main image from a Vendor.
    """

class VendorsImagesAdd_vendor_imageNamespace(LimbleEndpoint):
    """
    This request adds the main image to a Vendor.
    """

class VendorsFieldsNamespace(object):
    @property
    def vendor_fields(self) -> VendorsFieldsVendor_fieldsNamespace:
        """
        This request gets detailed information about Vendor Fields such as contact information, contracts and any other custom set field.
        
        This request will return an array of objects that have a file name and a link you can use to download that image. All links are only valid for 15 minutes, a new call will generate a new link.
        
        **Note:** this endpoint supports pagination. Please refer to the [**Pagination**](#pagination) section for more information.

        Query Parameters:
        - fields: This parameter is used to only get specific fields by ID. This parameter expects a comma delimited list of fieldIDs.
        - name: This parameter is used to only get specific field by name. This parameter expects a string full name of a field or partial name with the wildcard %.
        - vendors: This parameter is used to only get specific Vendors. This parameter expects a comma delimited list of Vendor IDs.
        - start: This parameter is used to only get vendor fields for vendors that were last edited after the unix timestamp passed into the start parameter. For example, all Vendors that were last edited after April 18th, 2018.
        - end: This parameter is used to only get vendor fields for vendors that were last edited *before* the unix timestamp passed into the end parameter.
        - cursor: This parameter is a cursor that selects what fieldID you want to start receiving results at. e.g. passing 137 here will only get you vendor fields with an id greater than 137.
        - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
        - value: This parameter is used to only get specific field by value. This parameter expects a string full name of a field or partial name with the wildcard %.
        - page: This parameter is used to paginate results based on the limit. Refer to Pagination section for more information.
        - values: This parameter is used to get vendor fields by their valueID. This parameter expects a comma delimited list of Value IDs.
        """
        ...
    @property
    def vendor_suggested_fields(self) -> VendorsFieldsVendor_suggested_fieldsNamespace:
        """
        This request gets all possible fields a Vendor can pick from when deciding which fields it should have.

        Query Parameters:
        - fields: This parameter can be used to get a single Vendor Fields or a list of Vendor Fields in a comma-separated list.
        - name: This parameter is used to only get specific field by name. This parameter expects a string full name of a field or partial name with the wildcard %.
        - cursor: This parameter is a cursor that selects what fieldID you want to start receiving results at. e.g. passing 137 here will only get you vendor fields with an id greater than 137.
        - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
        """
        ...
    @property
    def update_vendor_field_value(self) -> VendorsFieldsUpdate_vendor_field_valueNamespace:
        """
        This request updates a Vendor's field value.

        Parameter | Type | Required? | Description
        ------------------------------------------
        value | Depends on fieldType | Required | The value that will be written to the field. "value" must correspond to the fieldType of the field. For example, if the field is a "number" fieldType, then "value" must be a number.
        """
        ...
    @property
    def attach_field_to_vendor(self) -> VendorsFieldsAttach_field_to_vendorNamespace:
        """
        This request attaches a Suggested Field to a Vendor.
        """
        ...
    @property
    def new_vendor_suggested_field(self) -> VendorsFieldsNew_vendor_suggested_fieldNamespace:
        """
        This request adds a new Field to the list of Suggested Fields that can later be attached to Vendors.

        Parameter | Type | Required? | Description
        ------------------------------------------
        locationID | Int | Required | The location ID of the Location to add the new Field to.
        name | String | Required | The name of the new Field. Some custom field names such as "Vendor Name" are not allowed and reserved for internal use. This will result in a 409 error.
        fieldType | Int | Required | The type of the new Field. You can choose from Text (1), Date (2), Pictures (3), Documents (4), Number (5), Currency (6).
        """
        ...
    @property
    def delete_vendor_field(self) -> VendorsFieldsDelete_vendor_fieldNamespace:
        """
        This request deletes a custom field attached to a Vendor.
        """
        ...

class VendorsFieldsDelete_vendor_fieldNamespace(LimbleEndpoint):
    """
    This request deletes a custom field attached to a Vendor.
    """

class VendorsFieldsNew_vendor_suggested_fieldNamespace(LimbleEndpoint):
    """
    This request adds a new Field to the list of Suggested Fields that can later be attached to Vendors.

    Parameter | Type | Required? | Description
    ------------------------------------------
    locationID | Int | Required | The location ID of the Location to add the new Field to.
    name | String | Required | The name of the new Field. Some custom field names such as "Vendor Name" are not allowed and reserved for internal use. This will result in a 409 error.
    fieldType | Int | Required | The type of the new Field. You can choose from Text (1), Date (2), Pictures (3), Documents (4), Number (5), Currency (6).
    """

class VendorsFieldsAttach_field_to_vendorNamespace(LimbleEndpoint):
    """
    This request attaches a Suggested Field to a Vendor.
    """

class VendorsFieldsUpdate_vendor_field_valueNamespace(LimbleEndpoint):
    """
    This request updates a Vendor's field value.

    Parameter | Type | Required? | Description
    ------------------------------------------
    value | Depends on fieldType | Required | The value that will be written to the field. "value" must correspond to the fieldType of the field. For example, if the field is a "number" fieldType, then "value" must be a number.
    """

class VendorsFieldsVendor_suggested_fieldsNamespace(LimbleEndpoint):
    """
    This request gets all possible fields a Vendor can pick from when deciding which fields it should have.

    Query Parameters:
    - fields: This parameter can be used to get a single Vendor Fields or a list of Vendor Fields in a comma-separated list.
    - name: This parameter is used to only get specific field by name. This parameter expects a string full name of a field or partial name with the wildcard %.
    - cursor: This parameter is a cursor that selects what fieldID you want to start receiving results at. e.g. passing 137 here will only get you vendor fields with an id greater than 137.
    - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
    """

class VendorsFieldsVendor_fieldsNamespace(LimbleEndpoint):
    """
    This request gets detailed information about Vendor Fields such as contact information, contracts and any other custom set field.
    
    This request will return an array of objects that have a file name and a link you can use to download that image. All links are only valid for 15 minutes, a new call will generate a new link.
    
    **Note:** this endpoint supports pagination. Please refer to the [**Pagination**](#pagination) section for more information.

    Query Parameters:
    - fields: This parameter is used to only get specific fields by ID. This parameter expects a comma delimited list of fieldIDs.
    - name: This parameter is used to only get specific field by name. This parameter expects a string full name of a field or partial name with the wildcard %.
    - vendors: This parameter is used to only get specific Vendors. This parameter expects a comma delimited list of Vendor IDs.
    - start: This parameter is used to only get vendor fields for vendors that were last edited after the unix timestamp passed into the start parameter. For example, all Vendors that were last edited after April 18th, 2018.
    - end: This parameter is used to only get vendor fields for vendors that were last edited *before* the unix timestamp passed into the end parameter.
    - cursor: This parameter is a cursor that selects what fieldID you want to start receiving results at. e.g. passing 137 here will only get you vendor fields with an id greater than 137.
    - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
    - value: This parameter is used to only get specific field by value. This parameter expects a string full name of a field or partial name with the wildcard %.
    - page: This parameter is used to paginate results based on the limit. Refer to Pagination section for more information.
    - values: This parameter is used to get vendor fields by their valueID. This parameter expects a comma delimited list of Value IDs.
    """

class UsersNamespace(LimbleEndpoint):
    """
    This request gets information about Users such as User Login, User Email etc.
    
    Return data description

    Property | Description
    ----------------------
    username | What a User uses to login.
    wage | The hourly rate of an employee.
    active | Determines if a user can log into Limble or not.
    emailNotificationActive | Determines if a User gets Email Notifications From Limble.
    pushNotificationActive | Determines if a User gets Push Notifications From Limble.
    workdayHours | The number of hours a day this employee works.
    dateAdded | The date a user was added to Limble.  This is a unix timestamp.
    teams | What Teams a User has at specific Locations.

    Query Parameters:
    - users: This parameter expects a comma-separated list of users to get by id
    - name: This parameter is used to only get specific user by name. This parameter expects a string full name of a user or partial name with the wildcard %.
    - roles: This parameter expects a comma-separated list of users to get by roleID
    - teams: This parameter expects a comma-separated list of users to get by teamID
    - cursor: This parameter is a cursor that selects what userID you want to start receiving results at. e.g. passing 137 here will only get you tasks with an id greater than 137.
    - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
    """
    @property
    def roles(self) -> UsersRolesNamespace: ...
    @property
    def teams(self) -> UsersTeamsNamespace: ...
    @property
    def capacity(self) -> UsersCapacityNamespace: ...
    @property
    def new_user(self) -> UsersNew_userNamespace:
        """
        This request creates a new User and emails them a welcome email with details on how to access Limble.

        Parameter | Type | Required? | Description
        ------------------------------------------
        firstName | String | Optional | The User's first name.
        lastName | String | Optional | The User's last name.
        email | string | Required | The User's email address.
        password | string | Optional | The User's password.
        locationID | Int | Required | The locationID of the Location the Role will be at.
        roleID | Int | Required | The initial Role this user will be granted. This can be changed later with the "Add Role To User" request.
        phone | string | Optional | The User's phone number.
        wage | number | Optional | The User's wage per hour.
        workDayHours | number | Optional | The User's hours per day they work.
        active | Boolean | Optional | The User's activation status.
        emailNotificationActive | Boolean | Optional | The User's email notification activation status.  Should they receive email notifications?
        pushNotificationActive | Boolean | Optional | The User's push notification activation status. Should they receive push notifications?
        """
        ...
    @property
    def update_user(self) -> UsersUpdate_userNamespace:
        """
        This request updates a User details such as first name, last name, phone number, active status and more.

        Parameter | Type | Required? | Description
        ------------------------------------------
        firstName | String | Optional | The User's first name.
        lastName | String | Optional | The User's last name.
        email | string | Optional | The User's email address.
        username | string | Optional | The User's login name.
        password | string | Optional | A new password for the User.
        phone | string | Optional | The User's phone number.
        wage | number | Optional | The User's wage per hour.
        workDayHours | number | Optional | The User's hours per day they work.
        active | Boolean | Optional | The User's activation status.
        emailNotificationActive | Boolean | Optional | The User's email notification activation status.
        pushNotificationActive | Boolean | Optional | The User's push notification activation status.
        """
        ...
    @property
    def delete_user(self) -> UsersDelete_userNamespace: ...

class UsersDelete_userNamespace(LimbleEndpoint):
    pass

class UsersUpdate_userNamespace(LimbleEndpoint):
    """
    This request updates a User details such as first name, last name, phone number, active status and more.

    Parameter | Type | Required? | Description
    ------------------------------------------
    firstName | String | Optional | The User's first name.
    lastName | String | Optional | The User's last name.
    email | string | Optional | The User's email address.
    username | string | Optional | The User's login name.
    password | string | Optional | A new password for the User.
    phone | string | Optional | The User's phone number.
    wage | number | Optional | The User's wage per hour.
    workDayHours | number | Optional | The User's hours per day they work.
    active | Boolean | Optional | The User's activation status.
    emailNotificationActive | Boolean | Optional | The User's email notification activation status.
    pushNotificationActive | Boolean | Optional | The User's push notification activation status.
    """

class UsersNew_userNamespace(LimbleEndpoint):
    """
    This request creates a new User and emails them a welcome email with details on how to access Limble.

    Parameter | Type | Required? | Description
    ------------------------------------------
    firstName | String | Optional | The User's first name.
    lastName | String | Optional | The User's last name.
    email | string | Required | The User's email address.
    password | string | Optional | The User's password.
    locationID | Int | Required | The locationID of the Location the Role will be at.
    roleID | Int | Required | The initial Role this user will be granted. This can be changed later with the "Add Role To User" request.
    phone | string | Optional | The User's phone number.
    wage | number | Optional | The User's wage per hour.
    workDayHours | number | Optional | The User's hours per day they work.
    active | Boolean | Optional | The User's activation status.
    emailNotificationActive | Boolean | Optional | The User's email notification activation status.  Should they receive email notifications?
    pushNotificationActive | Boolean | Optional | The User's push notification activation status. Should they receive push notifications?
    """

class UsersCapacityNamespace(object):
    @property
    def exceptions(self) -> UsersCapacityExceptionsNamespace: ...
    @property
    def schedules(self) -> UsersCapacitySchedulesNamespace: ...

class UsersCapacitySchedulesNamespace(object):
    @property
    def get_capacity_schedules(self) -> UsersCapacitySchedulesGet_capacity_schedulesNamespace:
        """
        Returns per-user daily capacity rows for a date range, including applied precedence details.
        
        Precedence order:
        `exception > holiday > userSchedule > profileSchedule > default`.
        
        Pagination:
        - `cursor` is a zero-based offset.
        - `limit` max is 100.
        
        Date limits:
        - `startDate` and `endDate` are required (YYYY-MM-DD).
        - Date range cannot exceed 31 days.
        
        Response notes:
        - `range` now contains only `startDate` and `endDate`.
        - `pagination` contains `cursor`, `limit`, `totalUsers`, and `nextCursor`.

        Query Parameters:
        - locations: Required comma-separated location IDs to scope users.
        - users: Optional comma-separated user IDs filter.
        - schedules: Optional comma-separated schedule IDs to narrow results to specific schedules.
        - startDate: Required start date (YYYY-MM-DD).
        - endDate: Required end date (YYYY-MM-DD), must be >= startDate and within 31 days.
        - cursor: Optional zero-based user offset for pagination.
        - limit: Optional page size (1-100).
        """
        ...
    @property
    def create_capacity_schedule(self) -> UsersCapacitySchedulesCreate_capacity_scheduleNamespace:
        """
        Creates a capacity schedule for a user or a team profile.
        
        You must provide exactly one of `userID` or `profileID` (not both).
        
        **Required fields:**
        - `scheduleName` — Name of the schedule (max 255 chars).
        - `startDate` — Start date in YYYY-MM-DD format.
        - `locationID` — The location this schedule applies to.
        - One of `userID` or `profileID`.
        
        **Optional fields:**
        - `endDate` — End date (YYYY-MM-DD). Must be >= startDate. If omitted, the schedule continues indefinitely.
        - Day capacities (`mondayCapacity` through `sundayCapacity`) — Minutes per day (0–1440).
        - Day start/end times (`mondayStartTime` through `sundayEndTime`) — HH:MM or HH:MM:SS format.
        - `rotationPatternEnabled` — Enable rotation pattern (boolean).
        - `rotationWeeksOn` / `rotationWeeksOff` — Required when rotation is enabled (1–52).
        - `scheduleNotes` — Free-text notes (max 2000 chars).
        - `priority` — Priority ranking (0–1000). Default: 0.
        - `isActive` — Whether the schedule is active (boolean). Default: true.
        
        **Capacity defaults (when not provided):**
        - Monday–Friday: **480 minutes (8 hours)**
        - Saturday–Sunday: **0 minutes**
        
        **Time defaults (when not provided):**
        - All days: **08:00–16:00**
        
        Returns `201` with the new `scheduleID` and a `Location` header.
        """
        ...

class UsersCapacitySchedulesCreate_capacity_scheduleNamespace(LimbleEndpoint):
    """
    Creates a capacity schedule for a user or a team profile.
    
    You must provide exactly one of `userID` or `profileID` (not both).
    
    **Required fields:**
    - `scheduleName` — Name of the schedule (max 255 chars).
    - `startDate` — Start date in YYYY-MM-DD format.
    - `locationID` — The location this schedule applies to.
    - One of `userID` or `profileID`.
    
    **Optional fields:**
    - `endDate` — End date (YYYY-MM-DD). Must be >= startDate. If omitted, the schedule continues indefinitely.
    - Day capacities (`mondayCapacity` through `sundayCapacity`) — Minutes per day (0–1440).
    - Day start/end times (`mondayStartTime` through `sundayEndTime`) — HH:MM or HH:MM:SS format.
    - `rotationPatternEnabled` — Enable rotation pattern (boolean).
    - `rotationWeeksOn` / `rotationWeeksOff` — Required when rotation is enabled (1–52).
    - `scheduleNotes` — Free-text notes (max 2000 chars).
    - `priority` — Priority ranking (0–1000). Default: 0.
    - `isActive` — Whether the schedule is active (boolean). Default: true.
    
    **Capacity defaults (when not provided):**
    - Monday–Friday: **480 minutes (8 hours)**
    - Saturday–Sunday: **0 minutes**
    
    **Time defaults (when not provided):**
    - All days: **08:00–16:00**
    
    Returns `201` with the new `scheduleID` and a `Location` header.
    """

class UsersCapacitySchedulesGet_capacity_schedulesNamespace(LimbleEndpoint):
    """
    Returns per-user daily capacity rows for a date range, including applied precedence details.
    
    Precedence order:
    `exception > holiday > userSchedule > profileSchedule > default`.
    
    Pagination:
    - `cursor` is a zero-based offset.
    - `limit` max is 100.
    
    Date limits:
    - `startDate` and `endDate` are required (YYYY-MM-DD).
    - Date range cannot exceed 31 days.
    
    Response notes:
    - `range` now contains only `startDate` and `endDate`.
    - `pagination` contains `cursor`, `limit`, `totalUsers`, and `nextCursor`.

    Query Parameters:
    - locations: Required comma-separated location IDs to scope users.
    - users: Optional comma-separated user IDs filter.
    - schedules: Optional comma-separated schedule IDs to narrow results to specific schedules.
    - startDate: Required start date (YYYY-MM-DD).
    - endDate: Required end date (YYYY-MM-DD), must be >= startDate and within 31 days.
    - cursor: Optional zero-based user offset for pagination.
    - limit: Optional page size (1-100).
    """

class UsersCapacityExceptionsNamespace(object):
    @property
    def get_capacity_exceptions_by_user(self) -> UsersCapacityExceptionsGet_capacity_exceptions_by_userNamespace:
        """
        Gets capacity exception records for a specific user.
        
        `capacityMinutes` is the user's available capacity **per day** for each date in the exception range.
        
        Query behavior:
        - `locations` scopes by user location membership.
        - `startDate`/`endDate` filter by date overlap (YYYY-MM-DD).
        - `cursor`/`limit` paginate results.
        
        Response fields include:
        `exceptionID`, `userID`, `createdByUserID`, `exceptionStartDate`, `exceptionEndDate`, `capacityMinutes`, `hoursPerDay`, `minutesPerDay`, `exceptionTitle`, `exceptionNotes`.

        Query Parameters:
        - locations: Required comma-separated location IDs used to scope the user access context.
        - startDate: Optional lower date bound (YYYY-MM-DD) for overlap filtering.
        - endDate: Optional upper date bound (YYYY-MM-DD) for overlap filtering. Must be >= startDate when both are present.
        - cursor: Optional ID cursor for keyset pagination.
        - limit: Optional max rows per page.
        """
        ...
    @property
    def get_capacity_exceptions_by_location(self) -> UsersCapacityExceptionsGet_capacity_exceptions_by_locationNamespace:
        """
        Gets capacity exception records across users for the requested locations.
        
        `capacityMinutes` is the user's available capacity **per day** for each date in the exception range.
        
        Query behavior:
        - `locations` is required.
        - `users` optionally narrows results to specific users.
        - `startDate`/`endDate` filter by date overlap (YYYY-MM-DD).
        - `cursor`/`limit` paginate results.
        
        Response fields include:
        `exceptionID`, `userID`, `createdByUserID`, `exceptionStartDate`, `exceptionEndDate`, `capacityMinutes`, `hoursPerDay`, `minutesPerDay`, `exceptionTitle`, `exceptionNotes`.

        Query Parameters:
        - locations: Required comma-separated location IDs.
        - users: Optional comma-separated user IDs filter.
        - startDate: Optional lower date bound (YYYY-MM-DD) for overlap filtering.
        - endDate: Optional upper date bound (YYYY-MM-DD) for overlap filtering. Must be >= startDate when both are present.
        - cursor: Optional ID cursor for keyset pagination.
        - limit: Optional max rows per page.
        """
        ...
    @property
    def new_capacity_exception(self) -> UsersCapacityExceptionsNew_capacity_exceptionNamespace:
        """
        Creates a capacity exception for a user.
        
        `capacityMinutes` means the user's available work capacity **per day** for each day in the exception date/range. It is **not** the total duration of the exception range.
        
        Examples:
        
        - `capacityMinutes: 0` => unavailable that day (or each day in the range).
            
        - `capacityMinutes: 480` => 8 hours available per day.
            
        
        You can provide either:
        
        - `capacityMinutes` directly, or
            
        - `hoursPerDay` + `minutesPerDay` (equivalent input).
        """
        ...
    @property
    def delete_capacity_exception(self) -> UsersCapacityExceptionsDelete_capacity_exceptionNamespace:
        """
        Deletes a capacity exception for a user.
        """
        ...
    @property
    def update_capacity_exception(self) -> UsersCapacityExceptionsUpdate_capacity_exceptionNamespace:
        """
        This request updates an existing capacity exception and returns the updated resource.
        
        `capacityMinutes` means the user's available capacity **per day** for each day in the exception date/range. It is **not** the total duration of the exception range.
        
        Examples:
        - `capacityMinutes: 0` => unavailable that day (or each day in the range).
        - `capacityMinutes: 480` => 8 hours available per day.
        
        Return data description
        
        Property	Description
        exceptionID	Unique ID for the capacity exception record.
        userID	The user the exception applies to.
        createdByUserID	The user who created the exception.
        exceptionStartDate	The first date the exception applies (YYYY-MM-DD).
        exceptionEndDate	The last date the exception applies (YYYY-MM-DD). Null when the exception is only for one day.
        capacityMinutes	Allowed capacity in minutes **per day** for the exception date/range.
        hoursPerDay	Derived whole-hour portion of capacityMinutes.
        minutesPerDay	Derived minute remainder after hoursPerDay.
        exceptionTitle	Optional short title for the exception.
        exceptionNotes	Optional notes/details for the exception.
        """
        ...

class UsersCapacityExceptionsUpdate_capacity_exceptionNamespace(LimbleEndpoint):
    """
    This request updates an existing capacity exception and returns the updated resource.
    
    `capacityMinutes` means the user's available capacity **per day** for each day in the exception date/range. It is **not** the total duration of the exception range.
    
    Examples:
    - `capacityMinutes: 0` => unavailable that day (or each day in the range).
    - `capacityMinutes: 480` => 8 hours available per day.
    
    Return data description
    
    Property	Description
    exceptionID	Unique ID for the capacity exception record.
    userID	The user the exception applies to.
    createdByUserID	The user who created the exception.
    exceptionStartDate	The first date the exception applies (YYYY-MM-DD).
    exceptionEndDate	The last date the exception applies (YYYY-MM-DD). Null when the exception is only for one day.
    capacityMinutes	Allowed capacity in minutes **per day** for the exception date/range.
    hoursPerDay	Derived whole-hour portion of capacityMinutes.
    minutesPerDay	Derived minute remainder after hoursPerDay.
    exceptionTitle	Optional short title for the exception.
    exceptionNotes	Optional notes/details for the exception.
    """

class UsersCapacityExceptionsDelete_capacity_exceptionNamespace(LimbleEndpoint):
    """
    Deletes a capacity exception for a user.
    """

class UsersCapacityExceptionsNew_capacity_exceptionNamespace(LimbleEndpoint):
    """
    Creates a capacity exception for a user.
    
    `capacityMinutes` means the user's available work capacity **per day** for each day in the exception date/range. It is **not** the total duration of the exception range.
    
    Examples:
    
    - `capacityMinutes: 0` => unavailable that day (or each day in the range).
        
    - `capacityMinutes: 480` => 8 hours available per day.
        
    
    You can provide either:
    
    - `capacityMinutes` directly, or
        
    - `hoursPerDay` + `minutesPerDay` (equivalent input).
    """

class UsersCapacityExceptionsGet_capacity_exceptions_by_locationNamespace(LimbleEndpoint):
    """
    Gets capacity exception records across users for the requested locations.
    
    `capacityMinutes` is the user's available capacity **per day** for each date in the exception range.
    
    Query behavior:
    - `locations` is required.
    - `users` optionally narrows results to specific users.
    - `startDate`/`endDate` filter by date overlap (YYYY-MM-DD).
    - `cursor`/`limit` paginate results.
    
    Response fields include:
    `exceptionID`, `userID`, `createdByUserID`, `exceptionStartDate`, `exceptionEndDate`, `capacityMinutes`, `hoursPerDay`, `minutesPerDay`, `exceptionTitle`, `exceptionNotes`.

    Query Parameters:
    - locations: Required comma-separated location IDs.
    - users: Optional comma-separated user IDs filter.
    - startDate: Optional lower date bound (YYYY-MM-DD) for overlap filtering.
    - endDate: Optional upper date bound (YYYY-MM-DD) for overlap filtering. Must be >= startDate when both are present.
    - cursor: Optional ID cursor for keyset pagination.
    - limit: Optional max rows per page.
    """

class UsersCapacityExceptionsGet_capacity_exceptions_by_userNamespace(LimbleEndpoint):
    """
    Gets capacity exception records for a specific user.
    
    `capacityMinutes` is the user's available capacity **per day** for each date in the exception range.
    
    Query behavior:
    - `locations` scopes by user location membership.
    - `startDate`/`endDate` filter by date overlap (YYYY-MM-DD).
    - `cursor`/`limit` paginate results.
    
    Response fields include:
    `exceptionID`, `userID`, `createdByUserID`, `exceptionStartDate`, `exceptionEndDate`, `capacityMinutes`, `hoursPerDay`, `minutesPerDay`, `exceptionTitle`, `exceptionNotes`.

    Query Parameters:
    - locations: Required comma-separated location IDs used to scope the user access context.
    - startDate: Optional lower date bound (YYYY-MM-DD) for overlap filtering.
    - endDate: Optional upper date bound (YYYY-MM-DD) for overlap filtering. Must be >= startDate when both are present.
    - cursor: Optional ID cursor for keyset pagination.
    - limit: Optional max rows per page.
    """

class UsersTeamsNamespace(object):
    @property
    def get_user_teams(self) -> UsersTeamsGet_user_teamsNamespace:
        """
        This request gets all of the Teams a User has and what Location they have that Team at.

        Query Parameters:
        - teams: This parameter expects a comma-separated list of teamIDs to filter teams by
        - locations: This parameter expects a comma-separated list of locationIDs to filter teams by
        - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
        - cursor: This parameter is a cursor that selects what teamID you want to start receiving results at. e.g. passing 137 here will only get you tasks with an id greater than 137.
        - name: This parameter is used to only get specific team by name. This parameter expects a string full name of a user or partial name with the wildcard %.
        """
        ...
    @property
    def add_user_to_team(self) -> UsersTeamsAdd_user_to_teamNamespace:
        """
        This request adds a User to a Team.
        """
        ...
    @property
    def remove_team_from_user(self) -> UsersTeamsRemove_team_from_userNamespace:
        """
        This request removes a Team from a User.
        """
        ...

class UsersTeamsRemove_team_from_userNamespace(LimbleEndpoint):
    """
    This request removes a Team from a User.
    """

class UsersTeamsAdd_user_to_teamNamespace(LimbleEndpoint):
    """
    This request adds a User to a Team.
    """

class UsersTeamsGet_user_teamsNamespace(LimbleEndpoint):
    """
    This request gets all of the Teams a User has and what Location they have that Team at.

    Query Parameters:
    - teams: This parameter expects a comma-separated list of teamIDs to filter teams by
    - locations: This parameter expects a comma-separated list of locationIDs to filter teams by
    - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
    - cursor: This parameter is a cursor that selects what teamID you want to start receiving results at. e.g. passing 137 here will only get you tasks with an id greater than 137.
    - name: This parameter is used to only get specific team by name. This parameter expects a string full name of a user or partial name with the wildcard %.
    """

class UsersRolesNamespace(object):
    @property
    def get_user_roles(self) -> UsersRolesGet_user_rolesNamespace:
        """
        This request gets all of the Roles a User has and what Location they have that Role at.

        Query Parameters:
        - roles: This parameter expects a comma-separated list of roleIDs to filter teams by
        - locations: This parameter expects a comma-separated list of locationIDs to filter roles by
        - name: This parameter is used to only get specific role by name. This parameter expects a string full name of a user or partial name with the wildcard %.
        - cursor: This parameter is a cursor that selects what teamID you want to start receiving results at. e.g. passing 137 here will only get you tasks with an id greater than 137.
        - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
        """
        ...
    @property
    def add_user_to_role(self) -> UsersRolesAdd_user_to_roleNamespace:
        """
        This request adds a User to a Role.
        """
        ...
    @property
    def remove_role_from_user(self) -> UsersRolesRemove_role_from_userNamespace:
        """
        This request removes a Role from a User.
        """
        ...

class UsersRolesRemove_role_from_userNamespace(LimbleEndpoint):
    """
    This request removes a Role from a User.
    """

class UsersRolesAdd_user_to_roleNamespace(LimbleEndpoint):
    """
    This request adds a User to a Role.
    """

class UsersRolesGet_user_rolesNamespace(LimbleEndpoint):
    """
    This request gets all of the Roles a User has and what Location they have that Role at.

    Query Parameters:
    - roles: This parameter expects a comma-separated list of roleIDs to filter teams by
    - locations: This parameter expects a comma-separated list of locationIDs to filter roles by
    - name: This parameter is used to only get specific role by name. This parameter expects a string full name of a user or partial name with the wildcard %.
    - cursor: This parameter is a cursor that selects what teamID you want to start receiving results at. e.g. passing 137 here will only get you tasks with an id greater than 137.
    - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
    """

class TasksNamespace(LimbleEndpoint):
    """
    This request gets top level information about Tasks such as completed date, assignment, assetID, etc.
    
    **Note:** this endpoint supports pagination. Please refer to the [Pagination](#pagination) section for more information.
    
    Return data description

    Property | Description
    ----------------------
    meta | This property has shortcuts to get other information related to the Task such as the Task's invoices, labor parts usage and instructions.
    name | The Task's name.
    userID | The id of the user this Task is assigned to. A Task can not be assigned to both a Team and a User at the same time.
    teamID | The id of the team this Task is assigned to. A Task can not be assigned to both a Team and a User at the same time.
    locationID | The id of the Location in which this Task belongs to.
    template | This field indicates if the task is a 'template' that spawns other tasks based on schedules or not.
    createdDate | The date this Task was created. This is a unix timestamp.
    startDate | By default this value is 0 as the startDate is usually the same as the createdDate. Sometimes a task is created such that it is scheduled to start in the future (i.e. after the createdDate). In such a case this value will be a unix timestamp indicating the actual start date of the Task.
    scheduledStart | The scheduled start date of the Task. This is a unix timestamp. A value of null means no scheduled start date is set.
    scheduledEnd | The scheduled end date of the Task. This is a unix timestamp. A value of null means no scheduled end date is set.
    due | The date this Task is due. This is a unix timestamp.
    dateCompleted | The date this Task was completed. This is a unix timestamp. A value of 0 means this Task is not completed.
    lastEdited | The date this Task was last edited. This is a unix timestamp.
    description | The decription of a task.
    completedByUser | The id of the User that completed this Task.
    lastEditedByUser | The id of the User that last edited the task.
    assetID | The id of the Asset that this Task belongs to.
    completedUserWage | The price per hour of the User's Wage at the point in time when the task was completed.
    priority | The priority of the Task.
    downtime | The amount of downtime in seconds caused by this Task.
    estimatedTime | The estimated time of the task. This is the time it takes to complete the task in minutes.
    completionNotes | Notes inputted by the user at the time of task completion.
    requestorName | The name of the person that requested this Task.
    requestorEmail | The email of the person that requested this Task.
    requestorPhone | The phone number of the person that requested this Task.
    requestTile | The title of the work request being submitted.
    requestField1 | Work request portal custom field 1.
    requestField2 | Work request portal custom field 2.
    requestField3 | Work request portal custom field 3.
    requestDropdown1 | Work request portal custom dropdown box 1.
    requestDropdown2 | Work request portal custom dropdown box 2.
    requestDropdown3 | Work request portal custom dropdown box 3.
    requestorDescription | The description of the request submitted via the Work Request portal.
    type | 1 = Preventative Maintanance (PM);2 = Unplanned Work Order (WO);4 = Planned Work Order (WO);5 = Cycle Count;6 = Work Request (WR);7 = Min Part Threshold;8 = Materials Request;
    status | 1 - Complete0 - IncompleteNote: this property indicates a task status with respect to task completion. For the custom task status refer to statusID
    statusID | The current custom status assigned to this task.Note: this indicates the current status of a task. Use GET Statuses to find the value of each statusID.
    poIDs | An array of Purchase Order IDs linked to this Task. Returns an empty array if no Purchase Orders are linked.
    associatedTaskID (deprecated) | Please refer to associatedTask meta property on GET Task Instruction for instruction type 14.
    meta1 | Task meta data. This does not show in the web application, but can be used to track items between integrated systems.
    meta2 | Task meta data. This does not show in the web application, but can be used to track items between integrated systems.
    meta3 | Task meta data. This does not show in the web application, but can be used to track items between integrated systems.
    geoLocation | The location of a task on a Map.
    customTags | An array of custom tags associated with the task.

    Query Parameters:
    - tasks: This parameter is used to only get specific Tasks. This parameter accepts a comma delimited list of task IDs.
    - assets: This parameter is used to only get Tasks that are linked to an asset. This parameter accepts a comma delimited list of asset IDs.
    - locations: This parameter is used to only get Tasks at a specific group of Locations. This parameter accepts a comma delimited list of Location IDs.
    - type: This parameter is used to only get Tasks of a specific type. This parameter accepts a comma delimited list of task types.
    - name: This is a parameter used to string search for a name or partial name of a task this parameter expects a string with the wildcard %.
    - start: This parameter is used to only get Tasks that were last edited after the unix timestamp passed into the start parameter. For example, all Tasks that were last edited after April 18th, 2018.
    - end: This parameter is used to only get Tasks that were last edited before the unix timestamp passed into the end parameter.
    - cursor: This parameter is a cursor that selects what taskID you want to start receiving results at. e.g. passing 137 here will only get you tasks with an id greater than 137.
    - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
    - page: This parameter is used to paginate results based on the limit. Refer to Pagination section for more information.
    - completedStart: This parameter is used to only get Tasks that were completed after the unix timestamp passed into this parameter. For example, all Assets that were completed after April 18th, 2018.
    - completedEnd: This parameter is used to only get Tasks that were completed before the unix timestamp passed into this parameter.
    - scheduledStart: This parameter is used as the start of a scheduled-date window. Tasks are returned when their scheduled date range overlaps this timestamp.
    - scheduledEnd: This parameter is used as the end of a scheduled-date window. Tasks are returned when their scheduled date range overlaps this timestamp.
    - orderBy: This parameter sorts based on the value you pass. Negative parameters are used to reverse sort order. This supports sorting by due, createdDate, dateCompleted, scheduledStart, scheduledEnd, and lastEdited.
    - geoLocation: This parameter is used to filter results that contain a geoLocation property. By default it is false and will return all tasks with and without geoLocation property. If true, it will only return tasks with a geoLocation property.
    - users: This parameter filters tasks by assignee user IDs. It returns tasks directly assigned to those users and tasks assigned through team/profile membership (including multi-user assignments). This parameter accepts a comma delimited list of user IDs.
    - teams: This parameter is used to only get Tasks assigned to specific teams/profiles. This parameter accepts a comma delimited list of team IDs.
    - lastEditedByUsers: This parameter is used to filter tasks by users who last edited the task.
    - status: This parameter is used to filter tasks by completed status. 1 - Complete  0 - Incomplete
    - meta1: This parameter is used to filter tasks by task meta data. This does not show in the web application, but can be used to track items between integrated systems.
    - meta2: This parameter is used to filter tasks by task meta data. This does not show in the web application, but can be used to track items between integrated systems.
    - meta3: This parameter is used to filter tasks by task meta data. This does not show in the web application, but can be used to track items between integrated systems.
    - statusIDs: This parameter is used to filter tasks by their associated statusID.
    - tag: This parameter is used to filter results that contain a certain custom tag. The tag must match exactly, i.e. "Tag" would not match "My Custom Tag". Searching for "@My Custom Tag;" is equivalent to searching for "My Custom Tag" but because custom tags are stored with an at sign ("@") at the beginning and a semicolon (";") at the end it is recommended that the param follows the same format.
    """
    @property
    def invoices(self) -> TasksInvoicesNamespace:
        """
        This request gets all Invoices associated with Tasks.

        Query Parameters:
        - invoices: This parameter is used to only get specific invoices or invoices. This parameter accepts a comma delimited list of invoice IDs.
        - tasks: This parameter is used to only get invoices on a task or tasks. This parameter accepts a comma delimited list of task IDs.
        - start: This parameter is used to only get invoices that were logged after the unix timestamp passed into the start parameter. For example, all Invoices that were last edited after April 18th, 2018.
        - end: This parameter is used to only get invoices that were logged *before* the unix timestamp passed into the end parameter.
        - cursor: This parameter is a cursor that selects what invoiceID you want to start receiving results at. e.g. passing 137 here will only get you tasks with an id greater than 137.
        - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
        """
        ...
    @property
    def instructions(self) -> TasksInstructionsNamespace: ...
    @property
    def images(self) -> TasksImagesNamespace: ...
    @property
    def labor(self) -> TasksLaborNamespace: ...
    @property
    def parts(self) -> TasksPartsNamespace: ...
    @property
    def comments(self) -> TasksCommentsNamespace: ...
    @property
    def tags(self) -> TasksTagsNamespace:
        """
        This request gets all Custom Tags associated with a Task.
        
        <p><b>Return data description</b></p>

        Property | Description
        ----------------------
        tags | An array of custom tags associated with the task.
        """
        ...
    @property
    def work_request_submissions(self) -> TasksWork_request_submissionsNamespace: ...
    @property
    def new_task(self) -> TasksNew_taskNamespace:
        """
        This request will create an empty Task, assign to a User or Team, etc.

        Parameter | Type | Required? | Description
        ------------------------------------------
        name | String | Required | The name of the Task.
        locationID | Int | Required | The id of the Location this Task is assigned to. Must be the Location's unique ID number.
        due | Int | Required | The time at which the Task is due. Must be a unix timestamp.
        type | Int | Required | The type of Task according to this legend:1 = Preventative Maintanance (PM).2 = Unplanned Work Order (WO);4 = Planned Work Order (WO);6 = Work Request (WR).Task types not listed here are not currently supported.If you would like another Task type to be supported, please contact us.A taskType of 6 prevents the user from assigning a batchID.
        description | string | Optional | A brief description about the Task.
        assetID | Int | Optional | The Asset that the Task will be attached to, if any. Must be the unique ID number of the Asset. Omitting this parameter or setting it to zero will not attach the Task to an asset.
        assignment | Int | Optional. Required if 'assignmentType' is used. | The User or Team to which the Task will be assigned. Must be a User or Team that exists at the specified Location. Must be the unique ID number of the user or Team. If this parameter is set, the assignmentType parameter must also be set.
        templateID | Int | Optional | The taskID of the task you wish to utilize as a template when posting a new Task. Using this will duplicate all steps in the Template to the newly created task. Templates can be easily viewed and built in Limble's web application.
        assignmentType | Enum | Optional. Required if 'assignment' is used. | Specifies whether this Task will be assigned to a 'user', 'team' or 'multi'. If this parameter is set, the assignment parameter must also be set.
        priority | Int | Optional | Specifies the priority of the Task. Must correspond to a 'priorityLevel' (See GET Priorities) configured in your Limble account.
        estimatedTime | Int | Optional | Updates the estimated time of the task. This is the time it takes to complete the task in minutes.
        scheduledStart | Int | Optional | The scheduled start date of the task. Must be a unix timestamp. Must be 0 or greater.
        scheduledEnd | Int | Optional | The scheduled end date of the task. Must be a unix timestamp. Must be 0 or greater. If both scheduledStart and scheduledEnd are provided, scheduledEnd must be greater than scheduledStart.
        requestName | string | Optional | Specifies the name of the Work Requestor.
        requestEmail | string | Optional | Specifies the email address of the Work Requestor.
        requestPhone | string | Optional | Specifies the phone number of the Work Requestor.
        requestDescription | string | Optional | Specifies the description of the problem submitted by the Work Requestor.
        meta1 | string | Optional | Task meta data. This does not show in the web application, but can be used to track items between integrated systems.
        meta2 | string | Optional | Task meta data. This does not show in the web application, but can be used to track items between integrated systems.
        meta3 | string | Optional | Task meta data. This does not show in the web application, but can be used to track items between integrated systems.
        geoLocation | geoJSON | Optional | The geoJSON Feature object that can be used to locate a task on a Map.
        multiUsers | array | Optional. Required if assignmentType = multi | Array list of users a task is being assigned to.

        Query Parameters:
        - name: 
        - locationID: 
        - due: 
        - type: 
        - templateID: 
        """
        ...
    @property
    def update_task(self) -> TasksUpdate_taskNamespace:
        """
        This request updates the top level information of a Task.

        Parameter | Type | Required? | Description
        ------------------------------------------
        name | String | Optional | The name of the task.
        locationID | Int | Optional | The location to which the task is assigned. Must be the location's unique ID number.
        due | Int | Optional | The time at which the task is due for completion. Must be a unix timestamp.
        type | Int | Optional | The type of task according to this legend:1 = Preventative Maintanance (PM).2 = Unplanned Work Order (WO);4 = Planned Work Order (WO);6 = Work Request (WR).Only these type of tasks can be changed from one task type to another.
        description | string | Optional | A brief description about the task.
        asset | Int | Optional | The asset that the task will be attached to, if any. Must be the unique ID number of the asset. Omitting this parameter or setting it to zero will not attach the task to any asset.
        assignment | Int | Optional. Required if 'assignmentType' is used. | The user or team to which the task will be assigned. Must be a user or team that exists at the specified location. Must be the unique ID number of the user or team. If this parameter is set, the assignmentType parameter must also be set.
        assignmentType | Enum | Optional. Required if 'assignment' is used. | Specifies whether this task will be assigned to a 'user', 'team' or 'multi'. If this parameter is set, the assignment parameter must also be set.
        priority | Int | Optional | Specifies the priority of the task. Must be between 0 and 6 inclusive: 0 = lowest priority, 5 = highest priority, 6 = "On Hold".
        estimatedTime | Int | Optional | Updates the estimated time of the task. This is the time it takes to complete the task in minutes.
        scheduledStart | Int | Optional | The scheduled start date of the task. Must be a unix timestamp. Must be 0 or greater.
        scheduledEnd | Int | Optional | The scheduled end date of the task. Must be a unix timestamp. Must be 0 or greater. If both scheduledStart and scheduledEnd are provided, scheduledEnd must be greater than scheduledStart.
        requestName | string | Optional | Specifies the name of the work requestor.
        requestEmail | string | Optional | Specifies the email address of the work requestor.
        requestPhone | string | Optional | Specifies the phone number of the work requestor.
        requestDescription | string | Optional | Specifies the description set by the work requestor.
        status | int | Optional | 1 - Closes a task.0 - Opens a task.If this parameter is set to 1, the assignment and assignmentType parameters must also be set.
        meta1 | string | Optional | Task meta data. This does not show in the web application, but can be used to track items between integrated systems.
        meta2 | string | Optional | Task meta data. This does not show in the web application, but can be used to track items between integrated systems.
        meta3 | string | Optional | Task meta data. This does not show in the web application, but can be used to track items between integrated systems.
        geoLocation | geoJSON | Optional | The geoJSON Feature object that can be used to locate a task on a Map. To remove geoLocation from a Task pass an empty object ({}).
        statusID | int | Optional | Update the custom status of the task. Cannot update custom status to 1 (Open) or 2 (Complete).
        multiUsers | array | Optional. Required if assignmentType = multi | Array list of users a task is being assigned to.
        """
        ...
    @property
    def delete_task(self) -> TasksDelete_taskNamespace: ...

class TasksDelete_taskNamespace(LimbleEndpoint):
    pass

class TasksUpdate_taskNamespace(LimbleEndpoint):
    """
    This request updates the top level information of a Task.

    Parameter | Type | Required? | Description
    ------------------------------------------
    name | String | Optional | The name of the task.
    locationID | Int | Optional | The location to which the task is assigned. Must be the location's unique ID number.
    due | Int | Optional | The time at which the task is due for completion. Must be a unix timestamp.
    type | Int | Optional | The type of task according to this legend:1 = Preventative Maintanance (PM).2 = Unplanned Work Order (WO);4 = Planned Work Order (WO);6 = Work Request (WR).Only these type of tasks can be changed from one task type to another.
    description | string | Optional | A brief description about the task.
    asset | Int | Optional | The asset that the task will be attached to, if any. Must be the unique ID number of the asset. Omitting this parameter or setting it to zero will not attach the task to any asset.
    assignment | Int | Optional. Required if 'assignmentType' is used. | The user or team to which the task will be assigned. Must be a user or team that exists at the specified location. Must be the unique ID number of the user or team. If this parameter is set, the assignmentType parameter must also be set.
    assignmentType | Enum | Optional. Required if 'assignment' is used. | Specifies whether this task will be assigned to a 'user', 'team' or 'multi'. If this parameter is set, the assignment parameter must also be set.
    priority | Int | Optional | Specifies the priority of the task. Must be between 0 and 6 inclusive: 0 = lowest priority, 5 = highest priority, 6 = "On Hold".
    estimatedTime | Int | Optional | Updates the estimated time of the task. This is the time it takes to complete the task in minutes.
    scheduledStart | Int | Optional | The scheduled start date of the task. Must be a unix timestamp. Must be 0 or greater.
    scheduledEnd | Int | Optional | The scheduled end date of the task. Must be a unix timestamp. Must be 0 or greater. If both scheduledStart and scheduledEnd are provided, scheduledEnd must be greater than scheduledStart.
    requestName | string | Optional | Specifies the name of the work requestor.
    requestEmail | string | Optional | Specifies the email address of the work requestor.
    requestPhone | string | Optional | Specifies the phone number of the work requestor.
    requestDescription | string | Optional | Specifies the description set by the work requestor.
    status | int | Optional | 1 - Closes a task.0 - Opens a task.If this parameter is set to 1, the assignment and assignmentType parameters must also be set.
    meta1 | string | Optional | Task meta data. This does not show in the web application, but can be used to track items between integrated systems.
    meta2 | string | Optional | Task meta data. This does not show in the web application, but can be used to track items between integrated systems.
    meta3 | string | Optional | Task meta data. This does not show in the web application, but can be used to track items between integrated systems.
    geoLocation | geoJSON | Optional | The geoJSON Feature object that can be used to locate a task on a Map. To remove geoLocation from a Task pass an empty object ({}).
    statusID | int | Optional | Update the custom status of the task. Cannot update custom status to 1 (Open) or 2 (Complete).
    multiUsers | array | Optional. Required if assignmentType = multi | Array list of users a task is being assigned to.
    """

class TasksNew_taskNamespace(LimbleEndpoint):
    """
    This request will create an empty Task, assign to a User or Team, etc.

    Parameter | Type | Required? | Description
    ------------------------------------------
    name | String | Required | The name of the Task.
    locationID | Int | Required | The id of the Location this Task is assigned to. Must be the Location's unique ID number.
    due | Int | Required | The time at which the Task is due. Must be a unix timestamp.
    type | Int | Required | The type of Task according to this legend:1 = Preventative Maintanance (PM).2 = Unplanned Work Order (WO);4 = Planned Work Order (WO);6 = Work Request (WR).Task types not listed here are not currently supported.If you would like another Task type to be supported, please contact us.A taskType of 6 prevents the user from assigning a batchID.
    description | string | Optional | A brief description about the Task.
    assetID | Int | Optional | The Asset that the Task will be attached to, if any. Must be the unique ID number of the Asset. Omitting this parameter or setting it to zero will not attach the Task to an asset.
    assignment | Int | Optional. Required if 'assignmentType' is used. | The User or Team to which the Task will be assigned. Must be a User or Team that exists at the specified Location. Must be the unique ID number of the user or Team. If this parameter is set, the assignmentType parameter must also be set.
    templateID | Int | Optional | The taskID of the task you wish to utilize as a template when posting a new Task. Using this will duplicate all steps in the Template to the newly created task. Templates can be easily viewed and built in Limble's web application.
    assignmentType | Enum | Optional. Required if 'assignment' is used. | Specifies whether this Task will be assigned to a 'user', 'team' or 'multi'. If this parameter is set, the assignment parameter must also be set.
    priority | Int | Optional | Specifies the priority of the Task. Must correspond to a 'priorityLevel' (See GET Priorities) configured in your Limble account.
    estimatedTime | Int | Optional | Updates the estimated time of the task. This is the time it takes to complete the task in minutes.
    scheduledStart | Int | Optional | The scheduled start date of the task. Must be a unix timestamp. Must be 0 or greater.
    scheduledEnd | Int | Optional | The scheduled end date of the task. Must be a unix timestamp. Must be 0 or greater. If both scheduledStart and scheduledEnd are provided, scheduledEnd must be greater than scheduledStart.
    requestName | string | Optional | Specifies the name of the Work Requestor.
    requestEmail | string | Optional | Specifies the email address of the Work Requestor.
    requestPhone | string | Optional | Specifies the phone number of the Work Requestor.
    requestDescription | string | Optional | Specifies the description of the problem submitted by the Work Requestor.
    meta1 | string | Optional | Task meta data. This does not show in the web application, but can be used to track items between integrated systems.
    meta2 | string | Optional | Task meta data. This does not show in the web application, but can be used to track items between integrated systems.
    meta3 | string | Optional | Task meta data. This does not show in the web application, but can be used to track items between integrated systems.
    geoLocation | geoJSON | Optional | The geoJSON Feature object that can be used to locate a task on a Map.
    multiUsers | array | Optional. Required if assignmentType = multi | Array list of users a task is being assigned to.

    Query Parameters:
    - name: 
    - locationID: 
    - due: 
    - type: 
    - templateID: 
    """

class TasksWork_request_submissionsNamespace(object):
    @property
    def list_wr_submissions(self) -> TasksWork_request_submissionsList_wr_submissionsNamespace:
        """
        Lists WR submissions
        
        Return data description:

        **Property** | **Description**
        ------------------------------
        workRequestSubmissionId | The unique identifier of the work request submission.
        status | Pending, Approved or Rejected.
        createdByUserId | The unique identifier of the user who created the work request submission.
        createdAt | The date the work request submission was created. The timestamp is in the following format: YYYY-MM-DD (2025-07-02) HH:MM:SS (21:36:31)
        updatedAt | The date the work request submission was last updated. The timestamp is in the following format: YYYY-MM-DD (2025-07-02) HH:MM:SS (21:36:31)
        deletedAt | The date the work request submission was deleted. The timestamp is in the following format: YYYY-MM-DD (2025-07-02) HH:MM:SS (21:36:31) Will be NULL if the submission is not deleted.
        reviewedByUserId | The unique identifier of the user who reviewed the submission.
        reviewedAt | The date the work request submission was reviewed. The timestamp is in the following format: YYYY-MM-DD (2025-07-02) HH:MM:SS (21:36:31) Will be NULL if the submission has not yet been reviewed
        reviewedReason | The predefined reason the work request was declined.
        additionalNotes | Any additional notes the person who declined the submission wishes to leave.
        locationId | The unique identifier of the location the submission belongs to.
        assetId | The unique identifier of the asset associated with the submission.
        priorityId | The unique identifier of the priority of the submission.
        dueDateUnit | The unit of measure used to communicate when the task will be due. Can be “days” or “hours”.
        requestInformation | The information filled out in the Work Request Portal. Includes any of the following fields in JSON format. customerCode requesterName requesterEmail requesterPhone timeUnix customTag customFieldOne customFieldTwo customFieldThree customFieldOneTitle customFieldTwoTitle customFieldThreeTitle customFieldDropdownAnswerOne customFieldDropdownAnswerTwo customFieldDropdownAnswerThree customDropdownTitleOne customDropdownTitleTwo customDropdownTitleThree customDropdownOptionsOne customDropdownOptionsTwo customDropdownOptionsThree geoLocation
        customerID | The unique identifier of the customer account.
        requestTitle | The title of the submission.
        assignedToProfileId | The Limble profile the submission is assigned to. This is used to determine what team or individual is assigned to review the submission.
        requestDescription | The description of the problem filled out in the Work Request Portal.
        checklistID | The unique identifier of the task generated from the submission when it is approved. Will be NULL if submission status is declined or pending.
        requesterName | The name of the person who submitted the work request submission.

        Query Parameters:
        - orderBy: This parameter is used to order results by their createdAt, status, requestTitle, workRequestSubmissionID, and location property instead of the default ordering. each property can be flipped reverse by putting a minus before the property e.g. "-createdAt".
        - search: Free-text search
        - locationIDs: This parameter is used to only get work requests at a specific group of Locations. This parameter accepts a comma delimited list of Location IDs.
        - statuses: CSV of statuses
        - limit: Max rows
        - columns: CSV of field names (letters only); forwarded upstream as array
        - createdDateStart: ISO 8601 start
        - createdDateEnd: ISO 8601 end (≥ start)
        - workRequestIDs: CSV of WR IDs
        - page: Page-based pagination (mutually exclusive with cursor)
        - cursor: Cursor for pagination (forbidden with page)
        """
        ...

class TasksWork_request_submissionsList_wr_submissionsNamespace(LimbleEndpoint):
    """
    Lists WR submissions
    
    Return data description:

    **Property** | **Description**
    ------------------------------
    workRequestSubmissionId | The unique identifier of the work request submission.
    status | Pending, Approved or Rejected.
    createdByUserId | The unique identifier of the user who created the work request submission.
    createdAt | The date the work request submission was created. The timestamp is in the following format: YYYY-MM-DD (2025-07-02) HH:MM:SS (21:36:31)
    updatedAt | The date the work request submission was last updated. The timestamp is in the following format: YYYY-MM-DD (2025-07-02) HH:MM:SS (21:36:31)
    deletedAt | The date the work request submission was deleted. The timestamp is in the following format: YYYY-MM-DD (2025-07-02) HH:MM:SS (21:36:31) Will be NULL if the submission is not deleted.
    reviewedByUserId | The unique identifier of the user who reviewed the submission.
    reviewedAt | The date the work request submission was reviewed. The timestamp is in the following format: YYYY-MM-DD (2025-07-02) HH:MM:SS (21:36:31) Will be NULL if the submission has not yet been reviewed
    reviewedReason | The predefined reason the work request was declined.
    additionalNotes | Any additional notes the person who declined the submission wishes to leave.
    locationId | The unique identifier of the location the submission belongs to.
    assetId | The unique identifier of the asset associated with the submission.
    priorityId | The unique identifier of the priority of the submission.
    dueDateUnit | The unit of measure used to communicate when the task will be due. Can be “days” or “hours”.
    requestInformation | The information filled out in the Work Request Portal. Includes any of the following fields in JSON format. customerCode requesterName requesterEmail requesterPhone timeUnix customTag customFieldOne customFieldTwo customFieldThree customFieldOneTitle customFieldTwoTitle customFieldThreeTitle customFieldDropdownAnswerOne customFieldDropdownAnswerTwo customFieldDropdownAnswerThree customDropdownTitleOne customDropdownTitleTwo customDropdownTitleThree customDropdownOptionsOne customDropdownOptionsTwo customDropdownOptionsThree geoLocation
    customerID | The unique identifier of the customer account.
    requestTitle | The title of the submission.
    assignedToProfileId | The Limble profile the submission is assigned to. This is used to determine what team or individual is assigned to review the submission.
    requestDescription | The description of the problem filled out in the Work Request Portal.
    checklistID | The unique identifier of the task generated from the submission when it is approved. Will be NULL if submission status is declined or pending.
    requesterName | The name of the person who submitted the work request submission.

    Query Parameters:
    - orderBy: This parameter is used to order results by their createdAt, status, requestTitle, workRequestSubmissionID, and location property instead of the default ordering. each property can be flipped reverse by putting a minus before the property e.g. "-createdAt".
    - search: Free-text search
    - locationIDs: This parameter is used to only get work requests at a specific group of Locations. This parameter accepts a comma delimited list of Location IDs.
    - statuses: CSV of statuses
    - limit: Max rows
    - columns: CSV of field names (letters only); forwarded upstream as array
    - createdDateStart: ISO 8601 start
    - createdDateEnd: ISO 8601 end (≥ start)
    - workRequestIDs: CSV of WR IDs
    - page: Page-based pagination (mutually exclusive with cursor)
    - cursor: Cursor for pagination (forbidden with page)
    """

class TasksTagsNamespace(LimbleEndpoint):
    """
    This request gets all Custom Tags associated with a Task.
    
    <p><b>Return data description</b></p>

    Property | Description
    ----------------------
    tags | An array of custom tags associated with the task.
    """
    @property
    def put_apply_task_tags(self) -> TasksTagsPut_apply_task_tagsNamespace:
        """
        Applies one or more existing custom tags to a task. Tags must already exist at the account level (see POST /v2/tags to create new tags).
        
        Body:
        - tags: string[] — List of tags, or
        - tag: string — Single tag.
        
        Success Response (200):
        - created: true
        - name?: string — Present when a single tag was added; canonical without trailing ';'.
        - sanitizations?: string[] — Applied normalizations.
        - note?: string — Present when input had multiple '@' characters.
        - tags: string[] — Updated canonical tags with trailing ';'.
        
        Conflicts (409):
        - Single: { created: false, message: 'Tag already exists', name, tags }
        - Multiple: { created: false, message: 'No new tags to add', tags }
        
        Errors:
        - 404: { created: false, message, invalidTag(s), tags, availableTags } — Tag(s) don't exist at account level.
        - 400: { added: [], message: string } — Invalid input (semicolons, empty tags, etc.).
        
        Notes:
        - Tags MUST exist in the account's tag definitions before they can be applied to tasks.
        - Validation is case-insensitive (e.g., '@urgent' matches '@Urgent').
        - Semicolons in input are rejected.
        - The availableTags field in 404 responses shows which tags can be used.
        """
        ...
    @property
    def delete_remove_task_tag(self) -> TasksTagsDelete_remove_task_tagNamespace:
        """
        Removes a single custom tag from a task.
        
        Path:
        - tag: string — Tag to remove; may be raw or canonical; server normalizes.
        
        Success Response (200):
        - deleted: true
        - name: string — Canonical tag (includes trailing ';').
        - tags: string[] — Updated canonical tags.
        
        Errors:
        - 404: { message: 'Tag not found' }
        - 400: { removed: null, message: string } — Invalid input.
        """
        ...

class TasksTagsDelete_remove_task_tagNamespace(LimbleEndpoint):
    """
    Removes a single custom tag from a task.
    
    Path:
    - tag: string — Tag to remove; may be raw or canonical; server normalizes.
    
    Success Response (200):
    - deleted: true
    - name: string — Canonical tag (includes trailing ';').
    - tags: string[] — Updated canonical tags.
    
    Errors:
    - 404: { message: 'Tag not found' }
    - 400: { removed: null, message: string } — Invalid input.
    """

class TasksTagsPut_apply_task_tagsNamespace(LimbleEndpoint):
    """
    Applies one or more existing custom tags to a task. Tags must already exist at the account level (see POST /v2/tags to create new tags).
    
    Body:
    - tags: string[] — List of tags, or
    - tag: string — Single tag.
    
    Success Response (200):
    - created: true
    - name?: string — Present when a single tag was added; canonical without trailing ';'.
    - sanitizations?: string[] — Applied normalizations.
    - note?: string — Present when input had multiple '@' characters.
    - tags: string[] — Updated canonical tags with trailing ';'.
    
    Conflicts (409):
    - Single: { created: false, message: 'Tag already exists', name, tags }
    - Multiple: { created: false, message: 'No new tags to add', tags }
    
    Errors:
    - 404: { created: false, message, invalidTag(s), tags, availableTags } — Tag(s) don't exist at account level.
    - 400: { added: [], message: string } — Invalid input (semicolons, empty tags, etc.).
    
    Notes:
    - Tags MUST exist in the account's tag definitions before they can be applied to tasks.
    - Validation is case-insensitive (e.g., '@urgent' matches '@Urgent').
    - Semicolons in input are rejected.
    - The availableTags field in 404 responses shows which tags can be used.
    """

class TasksCommentsNamespace(object):
    @property
    def task_comments(self) -> TasksCommentsTask_commentsNamespace:
        """
        This request gets all Task Comments associated with a Task.
        
        Return data description

        Property | Description
        ----------------------
        commentID | This is the commentID of comment.
        comment | The text comment that was entered by the user.
        timestamp | The date this comment was created. This is a unix timestamp.
        userID | The ID of the user that made the comment.
        commentEmailAddress | The email address of the external user that made this comment. This is only populated if the comment was made by an external user via the comment reply system.
        showExternalUsers | The comment can be seen by external users or not.default value : true
        commentFiles | Array of objects that have a file name and a link you can use to download that file. All links are only valid for 15 minutes, a new call will generate a new link.

        Query Parameters:
        - cursor: This parameter is a cursor that selects what commentID you want to start receiving results at. e.g. passing 137 here will only get you parts with an id greater than 137.
        - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
        """
        ...
    @property
    def add_task_comments(self) -> TasksCommentsAdd_task_commentsNamespace:
        """
        This request adds a comment to a task.

        Parameter | Type | Required? | Description
        ------------------------------------------
        comment | String | Required | The comment to be added.
        showExternalUsers | Boolean | Optional | This will show the comment to external users. The default value is true.
        """
        ...

class TasksCommentsAdd_task_commentsNamespace(LimbleEndpoint):
    """
    This request adds a comment to a task.

    Parameter | Type | Required? | Description
    ------------------------------------------
    comment | String | Required | The comment to be added.
    showExternalUsers | Boolean | Optional | This will show the comment to external users. The default value is true.
    """

class TasksCommentsTask_commentsNamespace(LimbleEndpoint):
    """
    This request gets all Task Comments associated with a Task.
    
    Return data description

    Property | Description
    ----------------------
    commentID | This is the commentID of comment.
    comment | The text comment that was entered by the user.
    timestamp | The date this comment was created. This is a unix timestamp.
    userID | The ID of the user that made the comment.
    commentEmailAddress | The email address of the external user that made this comment. This is only populated if the comment was made by an external user via the comment reply system.
    showExternalUsers | The comment can be seen by external users or not.default value : true
    commentFiles | Array of objects that have a file name and a link you can use to download that file. All links are only valid for 15 minutes, a new call will generate a new link.

    Query Parameters:
    - cursor: This parameter is a cursor that selects what commentID you want to start receiving results at. e.g. passing 137 here will only get you parts with an id greater than 137.
    - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
    """

class TasksPartsNamespace(object):
    @property
    def get_attached_parts(self) -> TasksPartsGet_attached_partsNamespace:
        """
        Gets parts attached to a task.
        
        This request gets parts associated with a task.  A single Task can have multiple parts associated with it.
        
        Return data description

        Property | Description
        ----------------------
        partID | The partID of the part associated to this task.
        quantity | The quantity of this part associated to this task.
        usedPrice | The price of the part at the time of use.
        partName | The name of the part.
        poItemID | The unique ID of the PO item associated with this record.
        """
        ...
    @property
    def get_all_attached_parts(self) -> TasksPartsGet_all_attached_partsNamespace:
        """
        Gets parts attached to all tasks.
        
        This request gets parts associated with any task.  A single Task can have multiple parts associated with it.
        
        Return data description

        Property | Description
        ----------------------
        relationID | The identifier that associates parts to tasks.
        partID | The partID of the part associated to this task.
        taskID | The taskID this part is assoicated with.
        quantity | The quantity of this part associated to this task.
        lastEdited | The unix timestamp date of the last time this record was edited.
        usedPrice | The price of the part at the time of use.
        partName | The name of the part.
        poItemID | The unique ID of the PO item associated with this record.

        Query Parameters:
        - tasks: This parameter is used to get parts attached to a list of tasks. This parameter accepts a comma delimited list of task IDs.
        - parts: This parameter is used to get only certain. This parameter accepts a comma delimited list of task IDs.
        - cursor: This parameter is a cursor that selects what id you want to start receiving results at. e.g. passing 137 here will only get you assets with an id greater than 137.
        - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
        """
        ...
    @property
    def attach_part_to_task(self) -> TasksPartsAttach_part_to_taskNamespace:
        """
        This request associates a part to a task.
        """
        ...
    @property
    def delete_part_from_task(self) -> TasksPartsDelete_part_from_taskNamespace:
        """
        This request deletes a part from a task.
        """
        ...

class TasksPartsDelete_part_from_taskNamespace(LimbleEndpoint):
    """
    This request deletes a part from a task.
    """

class TasksPartsAttach_part_to_taskNamespace(LimbleEndpoint):
    """
    This request associates a part to a task.
    """

class TasksPartsGet_all_attached_partsNamespace(LimbleEndpoint):
    """
    Gets parts attached to all tasks.
    
    This request gets parts associated with any task.  A single Task can have multiple parts associated with it.
    
    Return data description

    Property | Description
    ----------------------
    relationID | The identifier that associates parts to tasks.
    partID | The partID of the part associated to this task.
    taskID | The taskID this part is assoicated with.
    quantity | The quantity of this part associated to this task.
    lastEdited | The unix timestamp date of the last time this record was edited.
    usedPrice | The price of the part at the time of use.
    partName | The name of the part.
    poItemID | The unique ID of the PO item associated with this record.

    Query Parameters:
    - tasks: This parameter is used to get parts attached to a list of tasks. This parameter accepts a comma delimited list of task IDs.
    - parts: This parameter is used to get only certain. This parameter accepts a comma delimited list of task IDs.
    - cursor: This parameter is a cursor that selects what id you want to start receiving results at. e.g. passing 137 here will only get you assets with an id greater than 137.
    - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
    """

class TasksPartsGet_attached_partsNamespace(LimbleEndpoint):
    """
    Gets parts attached to a task.
    
    This request gets parts associated with a task.  A single Task can have multiple parts associated with it.
    
    Return data description

    Property | Description
    ----------------------
    partID | The partID of the part associated to this task.
    quantity | The quantity of this part associated to this task.
    usedPrice | The price of the part at the time of use.
    partName | The name of the part.
    poItemID | The unique ID of the PO item associated with this record.
    """

class TasksLaborNamespace(object):
    @property
    def task_labor(self) -> TasksLaborTask_laborNamespace:
        """
        This request gets the labor (time spent) on a Task. A single Task can have multiple times logged onto it.
        
        Return data description

        Property | Description
        ----------------------
        meta | This property contains shortcuts to other requests that can be used to get more information regarding the Task the labor was logged on and the user who logged the time.
        taskID | The Task ID associated with this labor entry.
        timeSpent | The amount of time measure in seconds.
        userWage | The wage per hour.
        description | A description of the labor entry.
        dateLogged | The date that this time was logged on the Task.
        billableTime | The amount of time that is billable for this Task.
        billableRate | The rate at which this labor entry is billed at.
        categoryID | The labor category this entry is associated with.
        taskName | The name of the task associated with this labor entry.
        taskPriorityID | The Priority ID of the task this labor entry is associated with.
        taskPriorityLevel | The Priority value of the task this labor entry is associated with.

        Query Parameters:
        - tasks: This parameter is used to only get specific Tasks. This parameter accepts a comma delimited list of task IDs.
        - users: This parameter is used to only get labor records for a specific user or set of users in a comma delimited list.
        - start: This parameter is used to only get labor that was logged after the unix timestamp passed into the start parameter. For example, all Assets that were last edited after April 18th, 2018.
        - end: This parameter is used to only get labor that was logged *before* the unix timestamp passed into the end parameter.
        - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
        - cursor: This parameter is a cursor that selects what taskID you want to start receiving results at. e.g. passing 137 here will only get you tasks with an id greater than 137.
        - locations: This parameter is used to retrieve labor entries for particular locations. This parameter accepts a comma delimited list of location IDs.
        - orderBy: This parameter is used to order results by their dateLogged property instead of the default ordering. CANNOT be provided alongside the cursor parameter. to paginate in this ordering, use the start or end parameters.
        """
        ...
    @property
    def get_labor_categories(self) -> TasksLaborGet_labor_categoriesNamespace:
        """
        This request gets the labor categories.
        
        Return data description

        Property | Description
        ----------------------
        categoryID | The unique ID for this billing category.
        categoryName | The name of this billing category.
        categoryRate | The rate per hour of this billing category.

        Query Parameters:
        - name: This is a parameter used to string search for a name or partial name of a category this parameter expects a string with the wildcard %.
        - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
        - cursor: This parameter is a cursor that selects what taskID you want to start receiving results at. e.g. passing 137 here will only get you tasks with an id greater than 137.
        """
        ...

class TasksLaborGet_labor_categoriesNamespace(LimbleEndpoint):
    """
    This request gets the labor categories.
    
    Return data description

    Property | Description
    ----------------------
    categoryID | The unique ID for this billing category.
    categoryName | The name of this billing category.
    categoryRate | The rate per hour of this billing category.

    Query Parameters:
    - name: This is a parameter used to string search for a name or partial name of a category this parameter expects a string with the wildcard %.
    - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
    - cursor: This parameter is a cursor that selects what taskID you want to start receiving results at. e.g. passing 137 here will only get you tasks with an id greater than 137.
    """

class TasksLaborTask_laborNamespace(LimbleEndpoint):
    """
    This request gets the labor (time spent) on a Task. A single Task can have multiple times logged onto it.
    
    Return data description

    Property | Description
    ----------------------
    meta | This property contains shortcuts to other requests that can be used to get more information regarding the Task the labor was logged on and the user who logged the time.
    taskID | The Task ID associated with this labor entry.
    timeSpent | The amount of time measure in seconds.
    userWage | The wage per hour.
    description | A description of the labor entry.
    dateLogged | The date that this time was logged on the Task.
    billableTime | The amount of time that is billable for this Task.
    billableRate | The rate at which this labor entry is billed at.
    categoryID | The labor category this entry is associated with.
    taskName | The name of the task associated with this labor entry.
    taskPriorityID | The Priority ID of the task this labor entry is associated with.
    taskPriorityLevel | The Priority value of the task this labor entry is associated with.

    Query Parameters:
    - tasks: This parameter is used to only get specific Tasks. This parameter accepts a comma delimited list of task IDs.
    - users: This parameter is used to only get labor records for a specific user or set of users in a comma delimited list.
    - start: This parameter is used to only get labor that was logged after the unix timestamp passed into the start parameter. For example, all Assets that were last edited after April 18th, 2018.
    - end: This parameter is used to only get labor that was logged *before* the unix timestamp passed into the end parameter.
    - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
    - cursor: This parameter is a cursor that selects what taskID you want to start receiving results at. e.g. passing 137 here will only get you tasks with an id greater than 137.
    - locations: This parameter is used to retrieve labor entries for particular locations. This parameter accepts a comma delimited list of location IDs.
    - orderBy: This parameter is used to order results by their dateLogged property instead of the default ordering. CANNOT be provided alongside the cursor parameter. to paginate in this ordering, use the start or end parameters.
    """

class TasksImagesNamespace(object):
    @property
    def task_instruction_image(self) -> TasksImagesTask_instruction_imageNamespace:
        """
        This request adds instructional images to an Instruction.
        
        Return data description

        Property | Description
        ----------------------
        filename | The name of the file after being uploaded to Limble.
        """
        ...
    @property
    def delete_task_instruction_image(self) -> TasksImagesDelete_task_instruction_imageNamespace:
        """
        This request removes an instructional image from an Instruction.

        Query Parameters:
        - filename: The name of the instruction file that needs to be deleted. This is an optional parameter. If not given, **all** the files attached to an instruction will be deleted.
        """
        ...
    @property
    def upload_task_main_image(self) -> TasksImagesUpload_task_main_imageNamespace:
        """
        Uploads a main image to a task.
        
        Parameters:

        Parameter | In | Type | Required | Default | Description
        --------------------------------------------------------
        taskID | path | integer | yes |  | Task identifier
        image | form-data | file | yes |  | Image file (≤ 50MB). Types: JPEG, PNG, JPG, GIF
        """
        ...
    @property
    def delete_task_main_image(self) -> TasksImagesDelete_task_main_imageNamespace:
        """
        Deletes the task's main image.
        
        Parameters:

        Parameter | In | Type | Required | Default | Description
        --------------------------------------------------------
        taskID | path | integer | yes |  | Task identifier

        Responses:
        - 200 OK: Image cleared.
        - 404 Not Found: No image exists for this task.
        """
        ...

class TasksImagesDelete_task_main_imageNamespace(LimbleEndpoint):
    """
    Deletes the task's main image.
    
    Parameters:

    Parameter | In | Type | Required | Default | Description
    --------------------------------------------------------
    taskID | path | integer | yes |  | Task identifier

    Responses:
    - 200 OK: Image cleared.
    - 404 Not Found: No image exists for this task.
    """

class TasksImagesUpload_task_main_imageNamespace(LimbleEndpoint):
    """
    Uploads a main image to a task.
    
    Parameters:

    Parameter | In | Type | Required | Default | Description
    --------------------------------------------------------
    taskID | path | integer | yes |  | Task identifier
    image | form-data | file | yes |  | Image file (≤ 50MB). Types: JPEG, PNG, JPG, GIF
    """

class TasksImagesDelete_task_instruction_imageNamespace(LimbleEndpoint):
    """
    This request removes an instructional image from an Instruction.

    Query Parameters:
    - filename: The name of the instruction file that needs to be deleted. This is an optional parameter. If not given, **all** the files attached to an instruction will be deleted.
    """

class TasksImagesTask_instruction_imageNamespace(LimbleEndpoint):
    """
    This request adds instructional images to an Instruction.
    
    Return data description

    Property | Description
    ----------------------
    filename | The name of the file after being uploaded to Limble.
    """

class TasksInstructionsNamespace(object):
    @property
    def options(self) -> TasksInstructionsOptionsNamespace: ...
    @property
    def task_instructions(self) -> TasksInstructionsTask_instructionsNamespace:
        """
        This request gets all Task Instructions associated with a Task.
        
        **Note:** this endpoint supports pagination. Please refer to the [Pagination](#pagination) section for more information.
        
        Return data description

        Property | Description
        ----------------------
        parentInstructionID | This is the instructionID of the Instruction's parent. If this value is 0 then this Instruction does not have a parent.
        instruction | The text that guides a User on what to do on this Instruction.
        type | The type of the Instruction. See the request Post New Task Instruction to see a list of possible types and their meaning.
        instructionFiles | Array of objects that have a file name and a link you can use to download that file. All links are only valid for 15 minutes, a new call will generate a new link.
        options | Array of objects that have an itemOptionID, itemOptionOrder, and itemOptionText.
        response | This field is the "response" of an instruction i.e. what a user filled out when doing this instruction. The return value changes based on the instruction type:1 Check Box - true/false2 Radio List - if no option is selected, this will be 0. If an option is selected, this will be a number that maps to the itemOptionID of one of the members of the options array.3 Text Box - string4 Dropdown Box - if no option is selected, this will be 0. If an option is selected, this will be a number that maps to the itemOptionID of one of the members of the options array.5 Date Picker - unix time stamp7 Label - labels will never have a user response9 File or Picture Attachment - Array of objects that have a file name and a link you can use to download that image. All links are only valid for 15 minutes, a new call will generate a new link.10 Assign PM - not supported yet.13 Number - integer14 Start WO - not supported yet.15 Capture Signature - Array of objects that have a file name and a link you can use to download that image. All links are only valid for 15 minutes, a new call will generate a new link.16 Request Approval - Array of objects that have a file name and a link you can use to download that image. All links are only valid for 15 minutes, a new call will generate a new link.
        meta | This property is useful to get more information related to the Task Instructions. Different instruction types may have different properties in the meta section.Instruction Type:14 Start WO - If this instruction is completed on the task, the meta property would have an "associatedTask" property on it. The associatedTask gives the route for the task created by this instruction. For example, if task 2 was created by a "Start WO" instruction on task 1. In GET Task Instruction for task 1, this instruction would have a meta associatedTask property pointing to task 2.

        Query Parameters:
        - limit: 
        - page: 
        - cursor: This parameter is a cursor that selects what partID you want to start receiving results at. e.g. passing 137 here will only get you parts with an id greater than 137.
        """
        ...
    @property
    def new_task_instruction(self) -> TasksInstructionsNew_task_instructionNamespace:
        """
        This request will create a new Instruction for a Task.

        Parameter | Type | Required? | Description
        ------------------------------------------
        type | Int | Required | The type of each checklist item.
				1 = Check Box;
 2 = Option List;
				3 = Text Box;
4 = Dropdown List;
				5 = Date Picker;
				7 = Label;
				9 = File or Picture Attachment;
				11 = Deadline Date Picker;
				13 = Number;
				14 = Start WO;
				15 = Capture Signature.
				Item types not listed here are not currently supported.  If you would like another item type to be supported, please contact us at product@limblecmms.com.
        instruction | string | Required | The text that guides a User on what to do on this Instruction.
        parentInstructionID | Int | Required | If this is set this Instruction is a 'child' or sub-instruction. This value is the id of the Instruction's parent.  A value of 0 means it does not have a parent.
        parentInstructionOptionID | Int | Optional | If type is set to 2,4 and a parentInstructionID of an existing option/dropdown list is set then the parentInstructionOptionID needs to be set as the ID of the option for which a child option/dropdown list needs to be added.
        """
        ...
    @property
    def update_task_instruction(self) -> TasksInstructionsUpdate_task_instructionNamespace:
        """
        This request updates an Task Instruction.

        Parameter | Type | Required? | Description
        ------------------------------------------
        instruction | string | Optional | The text that guides a User on what to do on this Instruction.
        parentInstructionID | Int | Optional | If this is set this Instruction is a 'child' or sub-instruction. This value of parentInstructionID is the id of the Instruction's parent.  A value of 0 means this Instruction does not have a parent Instruction.
        """
        ...
    @property
    def delete_task_instruction(self) -> TasksInstructionsDelete_task_instructionNamespace:
        """
        This request removes a Task Instruction from a Task.
        """
        ...
    @property
    def batch_task_instructions(self) -> TasksInstructionsBatch_task_instructionsNamespace:
        """
        Retrieves instructions across multiple tasks, by taskID.
        
        Return data description

        Property | Description
        ----------------------
        parentInstructionID | This is the instructionID of the Instruction's parent. If this value is 0 then this Instruction does not have a parent.
        instruction | The text that guides a User on what to do on this Instruction.
        type | The type of the Instruction. See the request Post New Task Instruction to see a list of possible types and their meaning.
        instructionFiles | Array of objects that have a file name and a link you can use to download that file. All links are only valid for 15 minutes, a new call will generate a new link.
        options | Array of objects that have an itemOptionID, itemOptionOrder, and itemOptionText.
        response | This field is the "response" of an instruction i.e. what a user filled out when doing this instruction. The return value changes based on the instruction type:1 Check Box - true/false2 Radio List - if no option is selected, this will be 0. If an option is selected, this will be a number that maps to the itemOptionID of one of the members of the options array.3 Text Box - string4 Dropdown Box - if no option is selected, this will be 0. If an option is selected, this will be a number that maps to the itemOptionID of one of the members of the options array.5 Date Picker - unix time stamp7 Label - labels will never have a user response9 File or Picture Attachment - Array of objects that have a file name and a link you can use to download that image. All links are only valid for 15 minutes, a new call will generate a new link.10 Assign PM - not supported yet.13 Number - integer14 Start WO - not supported yet.15 Capture Signature - Array of objects that have a file name and a link you can use to download that image. All links are only valid for 15 minutes, a new call will generate a new link.16 Request Approval - Array of objects that have a file name and a link you can use to download that image. All links are only valid for 15 minutes, a new call will generate a new link.
        meta | This property is useful to get more information related to the Task Instructions. Different instruction types may have different properties in the meta section.Instruction Type:14 Start WO - If this instruction is completed on the task, the meta property would have an "associatedTask" property on it. The associatedTask gives the route for the task created by this instruction. For example, if task 2 was created by a "Start WO" instruction on task 1. In GET Task Instruction for task 1, this instruction would have a meta associatedTask property pointing to task 2.

        Query Parameters:
        - tasks: CSV of task IDs 
        - limit: Page size (1..1000)
        - page: Page-based pagination (mutually exclusive with cursor)
        """
        ...
    @property
    def get_task_instruction_by_id(self) -> TasksInstructionsGet_task_instruction_by_idNamespace:
        """
        This request retrieves a single Task Instruction by its instructionID.
        
        **Path Parameters:**
        - `instructionID` (required): The ID of the instruction to retrieve
        
        **Return data description:**
        
        Returns a single instruction object with the following properties:

        Property | Description
        ----------------------
        instructionID | The unique identifier for this instruction
        taskID | The ID of the task this instruction belongs to
        parentInstructionID | This is the instructionID of the Instruction's parent. If this value is 0 then this Instruction does not have a parent.
        instruction | The text that guides a User on what to do on this Instruction.
        type | The type of the Instruction. See the request Post New Task Instruction to see a list of possible types and their meaning.
        instructionFiles | Array of objects that have a file name and a link you can use to download that file. All links are only valid for 15 minutes, a new call will generate a new link.
        response | This field is the 'response' of an instruction i.e. what a user filled out when completing this instruction.

        **Error Responses:**
        - 404: Instruction not found
        """
        ...

class TasksInstructionsGet_task_instruction_by_idNamespace(LimbleEndpoint):
    """
    This request retrieves a single Task Instruction by its instructionID.
    
    **Path Parameters:**
    - `instructionID` (required): The ID of the instruction to retrieve
    
    **Return data description:**
    
    Returns a single instruction object with the following properties:

    Property | Description
    ----------------------
    instructionID | The unique identifier for this instruction
    taskID | The ID of the task this instruction belongs to
    parentInstructionID | This is the instructionID of the Instruction's parent. If this value is 0 then this Instruction does not have a parent.
    instruction | The text that guides a User on what to do on this Instruction.
    type | The type of the Instruction. See the request Post New Task Instruction to see a list of possible types and their meaning.
    instructionFiles | Array of objects that have a file name and a link you can use to download that file. All links are only valid for 15 minutes, a new call will generate a new link.
    response | This field is the 'response' of an instruction i.e. what a user filled out when completing this instruction.

    **Error Responses:**
    - 404: Instruction not found
    """

class TasksInstructionsBatch_task_instructionsNamespace(LimbleEndpoint):
    """
    Retrieves instructions across multiple tasks, by taskID.
    
    Return data description

    Property | Description
    ----------------------
    parentInstructionID | This is the instructionID of the Instruction's parent. If this value is 0 then this Instruction does not have a parent.
    instruction | The text that guides a User on what to do on this Instruction.
    type | The type of the Instruction. See the request Post New Task Instruction to see a list of possible types and their meaning.
    instructionFiles | Array of objects that have a file name and a link you can use to download that file. All links are only valid for 15 minutes, a new call will generate a new link.
    options | Array of objects that have an itemOptionID, itemOptionOrder, and itemOptionText.
    response | This field is the "response" of an instruction i.e. what a user filled out when doing this instruction. The return value changes based on the instruction type:1 Check Box - true/false2 Radio List - if no option is selected, this will be 0. If an option is selected, this will be a number that maps to the itemOptionID of one of the members of the options array.3 Text Box - string4 Dropdown Box - if no option is selected, this will be 0. If an option is selected, this will be a number that maps to the itemOptionID of one of the members of the options array.5 Date Picker - unix time stamp7 Label - labels will never have a user response9 File or Picture Attachment - Array of objects that have a file name and a link you can use to download that image. All links are only valid for 15 minutes, a new call will generate a new link.10 Assign PM - not supported yet.13 Number - integer14 Start WO - not supported yet.15 Capture Signature - Array of objects that have a file name and a link you can use to download that image. All links are only valid for 15 minutes, a new call will generate a new link.16 Request Approval - Array of objects that have a file name and a link you can use to download that image. All links are only valid for 15 minutes, a new call will generate a new link.
    meta | This property is useful to get more information related to the Task Instructions. Different instruction types may have different properties in the meta section.Instruction Type:14 Start WO - If this instruction is completed on the task, the meta property would have an "associatedTask" property on it. The associatedTask gives the route for the task created by this instruction. For example, if task 2 was created by a "Start WO" instruction on task 1. In GET Task Instruction for task 1, this instruction would have a meta associatedTask property pointing to task 2.

    Query Parameters:
    - tasks: CSV of task IDs 
    - limit: Page size (1..1000)
    - page: Page-based pagination (mutually exclusive with cursor)
    """

class TasksInstructionsDelete_task_instructionNamespace(LimbleEndpoint):
    """
    This request removes a Task Instruction from a Task.
    """

class TasksInstructionsUpdate_task_instructionNamespace(LimbleEndpoint):
    """
    This request updates an Task Instruction.

    Parameter | Type | Required? | Description
    ------------------------------------------
    instruction | string | Optional | The text that guides a User on what to do on this Instruction.
    parentInstructionID | Int | Optional | If this is set this Instruction is a 'child' or sub-instruction. This value of parentInstructionID is the id of the Instruction's parent.  A value of 0 means this Instruction does not have a parent Instruction.
    """

class TasksInstructionsNew_task_instructionNamespace(LimbleEndpoint):
    """
    This request will create a new Instruction for a Task.

    Parameter | Type | Required? | Description
    ------------------------------------------
    type | Int | Required | The type of each checklist item.
				1 = Check Box;
 2 = Option List;
				3 = Text Box;
4 = Dropdown List;
				5 = Date Picker;
				7 = Label;
				9 = File or Picture Attachment;
				11 = Deadline Date Picker;
				13 = Number;
				14 = Start WO;
				15 = Capture Signature.
				Item types not listed here are not currently supported.  If you would like another item type to be supported, please contact us at product@limblecmms.com.
    instruction | string | Required | The text that guides a User on what to do on this Instruction.
    parentInstructionID | Int | Required | If this is set this Instruction is a 'child' or sub-instruction. This value is the id of the Instruction's parent.  A value of 0 means it does not have a parent.
    parentInstructionOptionID | Int | Optional | If type is set to 2,4 and a parentInstructionID of an existing option/dropdown list is set then the parentInstructionOptionID needs to be set as the ID of the option for which a child option/dropdown list needs to be added.
    """

class TasksInstructionsTask_instructionsNamespace(LimbleEndpoint):
    """
    This request gets all Task Instructions associated with a Task.
    
    **Note:** this endpoint supports pagination. Please refer to the [Pagination](#pagination) section for more information.
    
    Return data description

    Property | Description
    ----------------------
    parentInstructionID | This is the instructionID of the Instruction's parent. If this value is 0 then this Instruction does not have a parent.
    instruction | The text that guides a User on what to do on this Instruction.
    type | The type of the Instruction. See the request Post New Task Instruction to see a list of possible types and their meaning.
    instructionFiles | Array of objects that have a file name and a link you can use to download that file. All links are only valid for 15 minutes, a new call will generate a new link.
    options | Array of objects that have an itemOptionID, itemOptionOrder, and itemOptionText.
    response | This field is the "response" of an instruction i.e. what a user filled out when doing this instruction. The return value changes based on the instruction type:1 Check Box - true/false2 Radio List - if no option is selected, this will be 0. If an option is selected, this will be a number that maps to the itemOptionID of one of the members of the options array.3 Text Box - string4 Dropdown Box - if no option is selected, this will be 0. If an option is selected, this will be a number that maps to the itemOptionID of one of the members of the options array.5 Date Picker - unix time stamp7 Label - labels will never have a user response9 File or Picture Attachment - Array of objects that have a file name and a link you can use to download that image. All links are only valid for 15 minutes, a new call will generate a new link.10 Assign PM - not supported yet.13 Number - integer14 Start WO - not supported yet.15 Capture Signature - Array of objects that have a file name and a link you can use to download that image. All links are only valid for 15 minutes, a new call will generate a new link.16 Request Approval - Array of objects that have a file name and a link you can use to download that image. All links are only valid for 15 minutes, a new call will generate a new link.
    meta | This property is useful to get more information related to the Task Instructions. Different instruction types may have different properties in the meta section.Instruction Type:14 Start WO - If this instruction is completed on the task, the meta property would have an "associatedTask" property on it. The associatedTask gives the route for the task created by this instruction. For example, if task 2 was created by a "Start WO" instruction on task 1. In GET Task Instruction for task 1, this instruction would have a meta associatedTask property pointing to task 2.

    Query Parameters:
    - limit: 
    - page: 
    - cursor: This parameter is a cursor that selects what partID you want to start receiving results at. e.g. passing 137 here will only get you parts with an id greater than 137.
    """

class TasksInstructionsOptionsNamespace(object):
    @property
    def instruction_options(self) -> TasksInstructionsOptionsInstruction_optionsNamespace:
        """
        This request gets all the Options for an Instruction Option or Dropdown list associated with a Task.
        """
        ...
    @property
    def new_instruction_option(self) -> TasksInstructionsOptionsNew_instruction_optionNamespace:
        """
        This request will create a new Option for a Dropdown or Option instruction of a task.

        Parameter | Type | Required? | Description
        ------------------------------------------
        instruction | string | Required | The text that guides the User for selecting the option. | instructionOptionOrder | Int | Optional | If this is set the option is created at that position of the list. This value cannot be greater than the total number of option present in the list. If not set the option is added to the end of the list.
        instruction | string | Required | The text that guides the User for selecting the option.
        instructionOptionOrder | Int | Optional | If this is set the option is created at that position of the list. This value cannot be greater than the total number of option present in the list. If not set the option is added to the end of the list.
        """
        ...
    @property
    def delete_instruction_option(self) -> TasksInstructionsOptionsDelete_instruction_optionNamespace:
        """
        This request will delete an option from a Dropdown or Option instruction.
        """
        ...
    @property
    def update_instruction_option(self) -> TasksInstructionsOptionsUpdate_instruction_optionNamespace: ...

class TasksInstructionsOptionsUpdate_instruction_optionNamespace(LimbleEndpoint):
    pass

class TasksInstructionsOptionsDelete_instruction_optionNamespace(LimbleEndpoint):
    """
    This request will delete an option from a Dropdown or Option instruction.
    """

class TasksInstructionsOptionsNew_instruction_optionNamespace(LimbleEndpoint):
    """
    This request will create a new Option for a Dropdown or Option instruction of a task.

    Parameter | Type | Required? | Description
    ------------------------------------------
    instruction | string | Required | The text that guides the User for selecting the option. | instructionOptionOrder | Int | Optional | If this is set the option is created at that position of the list. This value cannot be greater than the total number of option present in the list. If not set the option is added to the end of the list.
    instruction | string | Required | The text that guides the User for selecting the option.
    instructionOptionOrder | Int | Optional | If this is set the option is created at that position of the list. This value cannot be greater than the total number of option present in the list. If not set the option is added to the end of the list.
    """

class TasksInstructionsOptionsInstruction_optionsNamespace(LimbleEndpoint):
    """
    This request gets all the Options for an Instruction Option or Dropdown list associated with a Task.
    """

class TasksInvoicesNamespace(LimbleEndpoint):
    """
    This request gets all Invoices associated with Tasks.

    Query Parameters:
    - invoices: This parameter is used to only get specific invoices or invoices. This parameter accepts a comma delimited list of invoice IDs.
    - tasks: This parameter is used to only get invoices on a task or tasks. This parameter accepts a comma delimited list of task IDs.
    - start: This parameter is used to only get invoices that were logged after the unix timestamp passed into the start parameter. For example, all Invoices that were last edited after April 18th, 2018.
    - end: This parameter is used to only get invoices that were logged *before* the unix timestamp passed into the end parameter.
    - cursor: This parameter is a cursor that selects what invoiceID you want to start receiving results at. e.g. passing 137 here will only get you tasks with an id greater than 137.
    - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
    """
    @property
    def files(self) -> TasksInvoicesFilesNamespace: ...
    @property
    def attach_an_invoice_to_task(self) -> TasksInvoicesAttach_an_invoice_to_taskNamespace:
        """
        StartFragment
        
        .expect('Content-Type', /json/);
        
        EndFragment
        """
        ...
    @property
    def delete_invoice_from_task(self) -> TasksInvoicesDelete_invoice_from_taskNamespace:
        """
        This request will remove an invoice from an **open** Task (i.e. task status=0).
        """
        ...
    @property
    def update_an_invoice(self) -> TasksInvoicesUpdate_an_invoiceNamespace:
        """
        This request will update an invoice attached to an **open** Task (i.e. task status=0).

        Parameter | Type | Required? | Description
        ------------------------------------------
        cost | Float | Required | The cost on the invoice.
        description | String | Required | Brief description for the invoice.
        """
        ...

class TasksInvoicesUpdate_an_invoiceNamespace(LimbleEndpoint):
    """
    This request will update an invoice attached to an **open** Task (i.e. task status=0).

    Parameter | Type | Required? | Description
    ------------------------------------------
    cost | Float | Required | The cost on the invoice.
    description | String | Required | Brief description for the invoice.
    """

class TasksInvoicesDelete_invoice_from_taskNamespace(LimbleEndpoint):
    """
    This request will remove an invoice from an **open** Task (i.e. task status=0).
    """

class TasksInvoicesAttach_an_invoice_to_taskNamespace(LimbleEndpoint):
    """
    StartFragment
    
    .expect('Content-Type', /json/);
    
    EndFragment
    """

class TasksInvoicesFilesNamespace(object):
    @property
    def attach_a_file_to_an_invoice(self) -> TasksInvoicesFilesAttach_a_file_to_an_invoiceNamespace:
        """
        This request will attach a text or image file to an invoice on an **open** Task (i.e. task status=0).
        """
        ...
    @property
    def delete_file_from_invoice(self) -> TasksInvoicesFilesDelete_file_from_invoiceNamespace:
        """
        This request removes a file attached to an invoice on an open Task (i.e. task status = 0).
        """
        ...

class TasksInvoicesFilesDelete_file_from_invoiceNamespace(LimbleEndpoint):
    """
    This request removes a file attached to an invoice on an open Task (i.e. task status = 0).
    """

class TasksInvoicesFilesAttach_a_file_to_an_invoiceNamespace(LimbleEndpoint):
    """
    This request will attach a text or image file to an invoice on an **open** Task (i.e. task status=0).
    """

class PartsNamespace(LimbleEndpoint):
    """
    This request returns a list of Parts with top level information such as name, last edited, etc.
    
    **Note:** this endpoint supports pagination. Please refer to the [Pagination](#pagination) section for more information.
    
    Return data description

    Property | Description
    ----------------------
    number | The Part's Number. e.g. 25x25x1
    name | The Part's Name. e.g. Filter
    generalStock | How many of this Part you have in stock. Not including purchase orders.
    unitCode | The unit code displayed for the part. This represents the unit of measure assigned to the part (e.g., "kg", "lb", "each", etc.). If no unit is assigned, this field will be null.
    generalPrice | The default price of this part. Not considering purchase oder prices.
    category | The category this Part belongs to
    location | The Location of this Part. e.g. Shelf A
    minQtyStatus | Is the Part currently under the min quantity threshold. 0 = false, 1 = true.
    minQtyThreshold | The number at which reordering of this part is triggered. -1 means this feature is turned off.
    maxQtyThreshold | The number to bring the parts quantity back to. For example, if my inventory is at 4 and my maxQtyThreshold is 20 I will be reordering 16 parts to bring my inventory back up to the max quantity.
    staleThreshold | This value is how many days will need to go without a User using this Part by before this Part is considering stale.
    staleStatus | Is the Part stale or not. 0 = false, 1 = true.
    userID | The user that will receive threshold notifications and Tasks if thresholds are hit.
    team | The team that will receive threshold notifications and Tasks if thresholds are hit.
    stockOnHand | General Stock plus any unused, received PO Quantities for this part. This matches the 'Qty' value seen in the CMMS Part Management page.
    pos | Array of purchase order objects. price and quantity do not effect generalStock and generalPrice listed above.
    image | Array of objects that have a file name and a link you can use to download that image. All links are only valid for 15 minutes, a new call will generate a new link.

    Query Parameters:
    - parts: This parameter is used to only get specific Parts. This parameter accepts a comma delimited list of part IDs.
    - locations: This parameter is used to only get Parts at a specific group of Locations. This parameter accepts a comma delimited list of Location IDs.
    - name: This parameter is used to only get specific parts. This parameter expects a string either a full name of a part or a partial name with the wildcard %.
    - start: This parameter is used to only get Parts that were last edited after the unix timestamp passed into the start parameter. For example, all Parts that were last edited after April 18th, 2018.
    - end: This parameter is used to only get Parts that were last edited *before* the unix timestamp passed into the end parameter.
    - cursor: This parameter is a cursor that selects what partID you want to start receiving results at. e.g. passing 137 here will only get you parts with an id greater than 137.
    - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
    - numbers: This parameter is used to only get parts with part numbers that match the list provided. This parameter accepts a comma delimited list of Part Numbers.
    - page: This parameter is used to paginate results based on the limit. Refer to Pagination section for more information. 
    """
    @property
    def images(self) -> PartsImagesNamespace: ...
    @property
    def categories(self) -> PartsCategoriesNamespace:
        """

        Query Parameters:
        - categories: This parameter is used to only get specific part categories. This parameter accepts a comma delimited list of categoryIDs.
        - name: This parameter is used to string search part categories names either partial or full name with the wildcard %.
        """
        ...
    @property
    def fields(self) -> PartsFieldsNamespace: ...
    @property
    def logs(self) -> PartsLogsNamespace: ...
    @property
    def purchasables(self) -> PartsPurchasablesNamespace:
        """
        This endpoint makes an HTTP GET request to retrieve a part's purchasable data. The response of this request is documented as a JSON schema.
        
        <p><b>Return data description</b></p>

        **Property** | **Description**
        ------------------------------
        partID | The ID of the part the purchasable belongs to.
        name | The name of the purchasable.
        size | The size of the purchasable.
        orderUnitCode | The unit that describes how this purchasable is ordered. E.g. "by the box", or "by the foot".
        sizeUnitCode | The unit that qualifies the size value. E.g. this tells you whether this purchasable is 10 liters, or cans, or feet, etc.

        Query Parameters:
        - page: This parameter is used to paginate results based on the limit. Refer to Pagination section for more information.
        - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
        - nameStartsWith: Filter purchasables that have a name which starts with this string.
        """
        ...
    @property
    def vendor_associations(self) -> PartsVendor_associationsNamespace: ...
    @property
    def create_part(self) -> PartsCreate_partNamespace:
        """
        This request adds new Parts to inventory list.

        Parameter | Type | Required? | Description
        ------------------------------------------
        locationID | Int | Required | The location of the Part to be updated. Must be the Location's unique ID number.
        name | String | Required | The new name of the Part.
        number | String | Optional | The new number of the Part.
        generalStock | number | Optional | How many of this Part are now in stock. Not including purchase orders
        generalPrice | number | Optional | The new price of the Part. Not considering purchase order prices.
        unitCode | String | Optional | The unit code to assign to the part. If the unit code is not found, the request will return a 404 error.
        supplier | String | Optional | The new supplier of the Part.
        location | String | Optional | The new location of the Part (i.e. bin).
        categoryID | int | Optional | The category this part is in. (i.e. Electronics).
        staleThreshold | Int | Optional | The Stale Threshold setting allows you to set how many days need to go by without a Work Order or Task using this Part. For example, if the Stale Threshold is set at 30 and a Part does not get used by a Work Order or Task within 30 days, then the Part clock indicator will change color to red. If you wish to turn off this feature, assign a value of -1.
        minQtyThreshold | Int | Optional | The Minimum Part Qty Threshold setting allows you to set a limit on how low you want this Part's qty to get. For example, if a Part Qty is lower than the Part Qty Threshold, a Task will be assigned to the Manager of the location to order new Parts. If you wish to turn off this feature, assign a value of -1.
        maxQtyThreshold | Int | Optional | The Max Part Quantity Threshold number is used to determine what level you would like to bring your stock back to when you need to reorder a part. For example if I have 4 parts and my Maximum Part Qty Threshold is set to 20, I will have a task letting me know to order 16 more parts. If you wish to disable this feature please have a value of -1 entered.
        minQtyStatus | Boolean | Optional | This indicates if you are understocked or not.
        staleStatus | Boolean | Optional | This indicates if the part has gone stale or not. This value cannot be changed by regular user interaction it is change automatically by limble.
        assignment | Int | Optional. Required if 'assignmentType' is used. | The user or team to which the task will be assigned.Must be a user or team that exists at the specified location. Must be the unique ID number of the user or team. If this parameter is set, the assignmentType parameter must also be set.
        assignmentType | Enum | Optional. Required if 'assignment' is used. | Specifies wether this task will be assigned to a 'user' or a 'team'. Those two strings are the only accepted input. If this parameter is set, the assignment parameter must also be set.
        """
        ...
    @property
    def update_part(self) -> PartsUpdate_partNamespace:
        """
        This request updates an Part's information such as a Part's quantity.

        Parameter | Type | Required? | Description
        ------------------------------------------
        locationID | Int | Required | The location of the Part to be updated. Must be the Location's unique ID number.
        name | String | Optional | The new name of the Part.
        number | String | Optional | The new number of the Part.
        generalStock | number | Optional | How many of this Part are now in stock. Not including purchase orders.
        generalPrice | number | Optional | The new price of the Part. Not considering purchase order prices.
        unitCode | String | Optional | Update the part's unit by providing a unit code. If the unit code is not found, the request will return a 404 error. The unit of measure cannot be changed if the part has purchasables associated with it or is referenced in open purchase orders - in these cases, the request will return a 400 error.
        supplier | String | Optional | The new supplier of the Part.
        location | String | Optional | The new location of the Part (i.e. bin).
        categoryID | int | Optional | The category this part is in. (i.e. Electronics).
        staleThreshold | Int | Optional | The Stale Threshold setting allows you to set how many days need to go by without a Work Order or Task using this Part. For example, if the Stale Threshold is set at 30 and a Part does not get used by a Work Order or Task within 30 days, then the Part clock indicator will change color to red. If you wish to turn off this feature, assign a value of -1.
        minQtyThreshold | Int | Optional | The Minimum Part Qty Threshold setting allows you to set a limit on how low you want this Part's qty to get. For example, if a Part Qty is lower than the Part Qty Threshold, a Task will be assigned to the Manager of the location to order new Parts. If you wish to turn off this feature, assign a value of -1.
        maxQtyThreshold | Int | Optional | The Max Part Quantity Threshold number is used to determine what level you would like to bring your stock back to when you need to reorder a part. For example if I have 4 parts and my Maximum Part Qty Threshold is set to 20, I will have a task letting me know to order 16 more parts. If you wish to disable this feature please have a value of -1 entered.
        minQtyStatus | Boolean | Optional | This indicates if you are understocked or not.
        staleStatus | Boolean | Optional | This indicates if the part has gone stale or not. This value cannot be changed by regular user interaction it is change automatically by limble.
        assignment | Int | Optional. Required if 'assignmentType' is used. | The user or team to which the task will be assigned.Must be a user or team that exists at the specified location. Must be the unique ID number of the user or team. If this parameter is set, the assignmentType parameter must also be set.
        assignmentType | Enum | Optional. Required if 'assignment' is used. | Specifies wether this task will be assigned to a 'user' or a 'team'. Those two strings are the only accepted input. If this parameter is set, the assignment parameter must also be set.
        """
        ...
    @property
    def delete_part(self) -> PartsDelete_partNamespace:
        """
        This request removes a Part from your inventory list.
        """
        ...
    @property
    def parts_usage(self) -> PartsParts_usageNamespace:
        """
        This request gets your Parts usage log.
        
        Return data description

        Property | Description
        ----------------------
        meta | A call which can be used to quickly look up the Task that this part's usage was recorded on.
        name | The name of the part used.
        taskID | The associated Task where this part was used.
        usedCount | The number of parts that were used.
        usedPrice | The price per 1 part.
        usedOn | The date when the part was used.  This is a unix timestamp.
        poItemID | The unique ID of the PO item associated with this usage record.

        Query Parameters:
        - parts: This parameter is used to only get specific Parts. This parameter accepts a comma delimited list of part IDs.
        - tasks: This parameter is used to only get Parts at a specific group of Tasks. This parameter accepts a comma delimited list of Task IDs.
        - start: This parameter is used to only get Parts that were last edited after the unix timestamp passed into the start parameter. For example, all Assets that were last edited after April 18th, 2018.
        - end: This parameter is used to only get Parts that were last edited *before* the unix timestamp passed into the end parameter.
        - name: This parameter is used to string search part names either partial or full name with the wildcard %.
        - cursor: This parameter is a cursor that selects what partID you want to start receiving results at. e.g. passing 137 here will only get you part usage records with an id greater than 137.
        - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
        """
        ...

class PartsParts_usageNamespace(LimbleEndpoint):
    """
    This request gets your Parts usage log.
    
    Return data description

    Property | Description
    ----------------------
    meta | A call which can be used to quickly look up the Task that this part's usage was recorded on.
    name | The name of the part used.
    taskID | The associated Task where this part was used.
    usedCount | The number of parts that were used.
    usedPrice | The price per 1 part.
    usedOn | The date when the part was used.  This is a unix timestamp.
    poItemID | The unique ID of the PO item associated with this usage record.

    Query Parameters:
    - parts: This parameter is used to only get specific Parts. This parameter accepts a comma delimited list of part IDs.
    - tasks: This parameter is used to only get Parts at a specific group of Tasks. This parameter accepts a comma delimited list of Task IDs.
    - start: This parameter is used to only get Parts that were last edited after the unix timestamp passed into the start parameter. For example, all Assets that were last edited after April 18th, 2018.
    - end: This parameter is used to only get Parts that were last edited *before* the unix timestamp passed into the end parameter.
    - name: This parameter is used to string search part names either partial or full name with the wildcard %.
    - cursor: This parameter is a cursor that selects what partID you want to start receiving results at. e.g. passing 137 here will only get you part usage records with an id greater than 137.
    - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
    """

class PartsDelete_partNamespace(LimbleEndpoint):
    """
    This request removes a Part from your inventory list.
    """

class PartsUpdate_partNamespace(LimbleEndpoint):
    """
    This request updates an Part's information such as a Part's quantity.

    Parameter | Type | Required? | Description
    ------------------------------------------
    locationID | Int | Required | The location of the Part to be updated. Must be the Location's unique ID number.
    name | String | Optional | The new name of the Part.
    number | String | Optional | The new number of the Part.
    generalStock | number | Optional | How many of this Part are now in stock. Not including purchase orders.
    generalPrice | number | Optional | The new price of the Part. Not considering purchase order prices.
    unitCode | String | Optional | Update the part's unit by providing a unit code. If the unit code is not found, the request will return a 404 error. The unit of measure cannot be changed if the part has purchasables associated with it or is referenced in open purchase orders - in these cases, the request will return a 400 error.
    supplier | String | Optional | The new supplier of the Part.
    location | String | Optional | The new location of the Part (i.e. bin).
    categoryID | int | Optional | The category this part is in. (i.e. Electronics).
    staleThreshold | Int | Optional | The Stale Threshold setting allows you to set how many days need to go by without a Work Order or Task using this Part. For example, if the Stale Threshold is set at 30 and a Part does not get used by a Work Order or Task within 30 days, then the Part clock indicator will change color to red. If you wish to turn off this feature, assign a value of -1.
    minQtyThreshold | Int | Optional | The Minimum Part Qty Threshold setting allows you to set a limit on how low you want this Part's qty to get. For example, if a Part Qty is lower than the Part Qty Threshold, a Task will be assigned to the Manager of the location to order new Parts. If you wish to turn off this feature, assign a value of -1.
    maxQtyThreshold | Int | Optional | The Max Part Quantity Threshold number is used to determine what level you would like to bring your stock back to when you need to reorder a part. For example if I have 4 parts and my Maximum Part Qty Threshold is set to 20, I will have a task letting me know to order 16 more parts. If you wish to disable this feature please have a value of -1 entered.
    minQtyStatus | Boolean | Optional | This indicates if you are understocked or not.
    staleStatus | Boolean | Optional | This indicates if the part has gone stale or not. This value cannot be changed by regular user interaction it is change automatically by limble.
    assignment | Int | Optional. Required if 'assignmentType' is used. | The user or team to which the task will be assigned.Must be a user or team that exists at the specified location. Must be the unique ID number of the user or team. If this parameter is set, the assignmentType parameter must also be set.
    assignmentType | Enum | Optional. Required if 'assignment' is used. | Specifies wether this task will be assigned to a 'user' or a 'team'. Those two strings are the only accepted input. If this parameter is set, the assignment parameter must also be set.
    """

class PartsCreate_partNamespace(LimbleEndpoint):
    """
    This request adds new Parts to inventory list.

    Parameter | Type | Required? | Description
    ------------------------------------------
    locationID | Int | Required | The location of the Part to be updated. Must be the Location's unique ID number.
    name | String | Required | The new name of the Part.
    number | String | Optional | The new number of the Part.
    generalStock | number | Optional | How many of this Part are now in stock. Not including purchase orders
    generalPrice | number | Optional | The new price of the Part. Not considering purchase order prices.
    unitCode | String | Optional | The unit code to assign to the part. If the unit code is not found, the request will return a 404 error.
    supplier | String | Optional | The new supplier of the Part.
    location | String | Optional | The new location of the Part (i.e. bin).
    categoryID | int | Optional | The category this part is in. (i.e. Electronics).
    staleThreshold | Int | Optional | The Stale Threshold setting allows you to set how many days need to go by without a Work Order or Task using this Part. For example, if the Stale Threshold is set at 30 and a Part does not get used by a Work Order or Task within 30 days, then the Part clock indicator will change color to red. If you wish to turn off this feature, assign a value of -1.
    minQtyThreshold | Int | Optional | The Minimum Part Qty Threshold setting allows you to set a limit on how low you want this Part's qty to get. For example, if a Part Qty is lower than the Part Qty Threshold, a Task will be assigned to the Manager of the location to order new Parts. If you wish to turn off this feature, assign a value of -1.
    maxQtyThreshold | Int | Optional | The Max Part Quantity Threshold number is used to determine what level you would like to bring your stock back to when you need to reorder a part. For example if I have 4 parts and my Maximum Part Qty Threshold is set to 20, I will have a task letting me know to order 16 more parts. If you wish to disable this feature please have a value of -1 entered.
    minQtyStatus | Boolean | Optional | This indicates if you are understocked or not.
    staleStatus | Boolean | Optional | This indicates if the part has gone stale or not. This value cannot be changed by regular user interaction it is change automatically by limble.
    assignment | Int | Optional. Required if 'assignmentType' is used. | The user or team to which the task will be assigned.Must be a user or team that exists at the specified location. Must be the unique ID number of the user or team. If this parameter is set, the assignmentType parameter must also be set.
    assignmentType | Enum | Optional. Required if 'assignment' is used. | Specifies wether this task will be assigned to a 'user' or a 'team'. Those two strings are the only accepted input. If this parameter is set, the assignment parameter must also be set.
    """

class PartsVendor_associationsNamespace(object):
    @property
    def get_part_vendor_associations(self) -> PartsVendor_associationsGet_part_vendor_associationsNamespace:
        """
        Returns a paginated list of vendor-part associations for the customer.
        
        **Note:** this endpoint supports both cursor-based and page-based pagination. Please refer to the [**Pagination**](#pagination) section for more information.
        
        Return data description

        Property | Description
        ----------------------
        relationID | The unique ID of this vendor-part association.
        partID | The ID of the associated part.
        vendorID | The ID of the associated vendor.
        vendorPartNumber | The vendor's part number for this part, if provided.
        partPrice | The vendor's price for this part, if provided.
        createdAt | Unix timestamp of when this association was created.
        updatedAt | Unix timestamp of when this association was last updated.
        partName | The name of the associated part.
        number | The part's internal part number.
        locationID | The ID of the location this part belongs to.
        vendorName | The name of the associated vendor.

        Query Parameters:
        - parts: This parameter is used to only get associations for specific parts. This parameter accepts a comma delimited list of part IDs.
        - vendors: This parameter is used to only get associations for specific vendors. This parameter accepts a comma delimited list of vendor IDs.
        - vendorPartNumber: This parameter is used to search for associations by vendor part number. This parameter expects a string with the wildcard % for partial matching.
        - vendorName: This parameter is used to search for associations by vendor name. This parameter expects a string with the wildcard % for partial matching.
        - start: This parameter is used to only get associations that were last updated after the unix timestamp passed into the start parameter.
        - end: This parameter is used to only get associations that were last updated before the unix timestamp passed into the end parameter.
        - cursor: This parameter is a cursor that selects what relationID you want to start receiving results at. This will return results with a relationID greater than the value of cursor.
        - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time. The maximum is 1000.
        - orderBy: This parameter is used to order results. Accepted values: relationID, -relationID, createdAt, -createdAt, updatedAt, -updatedAt, partName, -partName, vendorName, -vendorName. Prefix with - for descending order.
        - page: This parameter is used to paginate results based on the limit. Refer to Pagination section for more information.
        """
        ...
    @property
    def delete_part_vendor_association(self) -> PartsVendor_associationsDelete_part_vendor_associationNamespace:
        """
        Deletes a vendor-part association by its `relationID`. Only manually created associations (associationType: `manual`) can be deleted through this endpoint.
        
        Returns `204 No Content` on success. Returns `404 Not Found` if the association does not exist or does not belong to your account.
        """
        ...
    @property
    def create_part_vendor_association(self) -> PartsVendor_associationsCreate_part_vendor_associationNamespace:
        """
        Creates a manual vendor-part association.
        
        The part and vendor must both exist and the vendor must be at the same location as the part. If an association between the given part and vendor already exists, a `409 Conflict` is returned.
        
        **Required fields:**
        - `partID` — The ID of the part.
        - `vendorID` — The ID of the vendor.
        
        Returns `201 Created` with the new `relationID` and a `Location` header pointing to the association.
        """
        ...

class PartsVendor_associationsCreate_part_vendor_associationNamespace(LimbleEndpoint):
    """
    Creates a manual vendor-part association.
    
    The part and vendor must both exist and the vendor must be at the same location as the part. If an association between the given part and vendor already exists, a `409 Conflict` is returned.
    
    **Required fields:**
    - `partID` — The ID of the part.
    - `vendorID` — The ID of the vendor.
    
    Returns `201 Created` with the new `relationID` and a `Location` header pointing to the association.
    """

class PartsVendor_associationsDelete_part_vendor_associationNamespace(LimbleEndpoint):
    """
    Deletes a vendor-part association by its `relationID`. Only manually created associations (associationType: `manual`) can be deleted through this endpoint.
    
    Returns `204 No Content` on success. Returns `404 Not Found` if the association does not exist or does not belong to your account.
    """

class PartsVendor_associationsGet_part_vendor_associationsNamespace(LimbleEndpoint):
    """
    Returns a paginated list of vendor-part associations for the customer.
    
    **Note:** this endpoint supports both cursor-based and page-based pagination. Please refer to the [**Pagination**](#pagination) section for more information.
    
    Return data description

    Property | Description
    ----------------------
    relationID | The unique ID of this vendor-part association.
    partID | The ID of the associated part.
    vendorID | The ID of the associated vendor.
    vendorPartNumber | The vendor's part number for this part, if provided.
    partPrice | The vendor's price for this part, if provided.
    createdAt | Unix timestamp of when this association was created.
    updatedAt | Unix timestamp of when this association was last updated.
    partName | The name of the associated part.
    number | The part's internal part number.
    locationID | The ID of the location this part belongs to.
    vendorName | The name of the associated vendor.

    Query Parameters:
    - parts: This parameter is used to only get associations for specific parts. This parameter accepts a comma delimited list of part IDs.
    - vendors: This parameter is used to only get associations for specific vendors. This parameter accepts a comma delimited list of vendor IDs.
    - vendorPartNumber: This parameter is used to search for associations by vendor part number. This parameter expects a string with the wildcard % for partial matching.
    - vendorName: This parameter is used to search for associations by vendor name. This parameter expects a string with the wildcard % for partial matching.
    - start: This parameter is used to only get associations that were last updated after the unix timestamp passed into the start parameter.
    - end: This parameter is used to only get associations that were last updated before the unix timestamp passed into the end parameter.
    - cursor: This parameter is a cursor that selects what relationID you want to start receiving results at. This will return results with a relationID greater than the value of cursor.
    - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time. The maximum is 1000.
    - orderBy: This parameter is used to order results. Accepted values: relationID, -relationID, createdAt, -createdAt, updatedAt, -updatedAt, partName, -partName, vendorName, -vendorName. Prefix with - for descending order.
    - page: This parameter is used to paginate results based on the limit. Refer to Pagination section for more information.
    """

class PartsPurchasablesNamespace(LimbleEndpoint):
    """
    This endpoint makes an HTTP GET request to retrieve a part's purchasable data. The response of this request is documented as a JSON schema.
    
    <p><b>Return data description</b></p>

    **Property** | **Description**
    ------------------------------
    partID | The ID of the part the purchasable belongs to.
    name | The name of the purchasable.
    size | The size of the purchasable.
    orderUnitCode | The unit that describes how this purchasable is ordered. E.g. "by the box", or "by the foot".
    sizeUnitCode | The unit that qualifies the size value. E.g. this tells you whether this purchasable is 10 liters, or cans, or feet, etc.

    Query Parameters:
    - page: This parameter is used to paginate results based on the limit. Refer to Pagination section for more information.
    - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
    - nameStartsWith: Filter purchasables that have a name which starts with this string.
    """

class PartsLogsNamespace(object):
    @property
    def part_logs(self) -> PartsLogsPart_logsNamespace:
        """
        This request returns the log entries for a part.
        
        **Note:** this endpoint supports pagination. Please refer to the [Pagination](#pagination) section for more information.
        
        Return data description

        Property | Description
        ----------------------
        logID | The unique logID of the log.
        dateCreated | The date the log was created as a UNIX timestamp.
        partID | The partID the log belongs to.
        sourceID | The sourceID of the source of the log. The sourceID can be as follows:1: Part name was changed.2: Part Number was changed.3: Parts were added/removed.4: Manual log entry.5: Parts were used on a Task.6: Part Price was changed.7: Stale threshold was manually changed.8: Part Qty threshold was manually changed.11: Part Qty threshold status was changed.13: Part Location was changed.14: Part Vendor was changed.15: Part Image was changed.18: Parts were received on a Bill.19: Part Maximum Part Qty was manually changed.20: Some of a PO Item Received Qty was used during manual Part Qty adjustment
        logEntry | The log entry for the part.
        userID | The ID of the user that created the log.
        associatedID | The ID of the item associated with this log, if any. Current examples include:sourceID: 5, associatedID type: TasksourceID: 18, associatedID type: BillsourceID: 20, associatedID type: Bill

        Query Parameters:
        - logs: This parameter is used to only get specific logs. This parameter accepts a comma delimited list of logIDs.
        - sources: This parameter is used to only get logs for a specific sourceID. This parameter accepts a comma delimited list of sourceIDs.
        - users: This parameter is used to only get logs created by specific users. This parameter accepts a comma delimited list of userIDs.
        - logEntry: This is a parameter used to string search for manual log entry (sourceID: 4). This parameter expects a string with the wildcard %.
        - start: This parameter is used to only get logs that were last edited after the unix timestamp passed into the start parameter. 
        - end: This parameter is used to only get logs that were last edited before the unix timestamp passed into the end parameter.
        - page: This parameter is used to paginate results based on the limit. Refer to Pagination section for more information.
        - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
        - cursor: This parameter is a cursor that selects what ID you want to start receiving results at. 
        """
        ...
    @property
    def new_part_log(self) -> PartsLogsNew_part_logNamespace:
        """
        This request creates a manual log entry for a part.
        
        This request adds a new Field to the list of Suggested Fields that can later be attached to Parts.

        Parameter | Type | Required? | Description
        ------------------------------------------
        userID | Int | Required | The ID of the user creating the log.
        logEntry | String | Required | Details of the log.
        """
        ...
    @property
    def update_part_log(self) -> PartsLogsUpdate_part_logNamespace:
        """
        This requests updates a manual log entry. Only logs with a sourceID=4 can be updated.
        """
        ...
    @property
    def delete_part_log(self) -> PartsLogsDelete_part_logNamespace:
        """
        This request deletes manual log entries (sourceID=4).
        """
        ...
    @property
    def all_part_logs(self) -> PartsLogsAll_part_logsNamespace:
        """
        This request returns all part logs across your Limble account.
        
        **Note:** this endpoint supports pagination. Please refer to the [Pagination](#pagination) section for more information.
        
        Return data description

        Property | Description
        ----------------------
        logID | The unique logID of the log.
        dateCreated | The date the log was created as a UNIX timestamp.
        partID | The partID the log belongs to.
        sourceID | The sourceID of the source of the log. The sourceID can be as follows:1: Part name was changed.2: Part Number was changed.3: Parts were added/removed.4: Manual log entry.5: Parts were used on a Task.6: Part Price was changed.7: Stale threshold was manually changed.8: Part Qty threshold was manually changed.11: Part Qty threshold status was changed.13: Part Location was changed.14: Part Vendor was changed.15: Part Image was changed.18: Parts were received on a Bill.19: Part Maximum Part Qty was manually changed.20. Some of a PO Item Received Qty was used during manual Part Qty adjustment
        logEntry | The log entry for the part.
        userID | The ID of the user that created the log.
        associatedID | The ID of the item associated with this log, if any. Current examples include:sourceID: 5, associatedID type: TasksourceID: 18, associatedID type: BillsourceID: 20, associatedID type: Bill

        Query Parameters:
        - logs: 
        - sources: 
        - users: 
        - logEntry: 
        - start: 
        - end: 
        - page: 
        - parts: 
        - limit: 
        - cursor: 
        """
        ...

class PartsLogsAll_part_logsNamespace(LimbleEndpoint):
    """
    This request returns all part logs across your Limble account.
    
    **Note:** this endpoint supports pagination. Please refer to the [Pagination](#pagination) section for more information.
    
    Return data description

    Property | Description
    ----------------------
    logID | The unique logID of the log.
    dateCreated | The date the log was created as a UNIX timestamp.
    partID | The partID the log belongs to.
    sourceID | The sourceID of the source of the log. The sourceID can be as follows:1: Part name was changed.2: Part Number was changed.3: Parts were added/removed.4: Manual log entry.5: Parts were used on a Task.6: Part Price was changed.7: Stale threshold was manually changed.8: Part Qty threshold was manually changed.11: Part Qty threshold status was changed.13: Part Location was changed.14: Part Vendor was changed.15: Part Image was changed.18: Parts were received on a Bill.19: Part Maximum Part Qty was manually changed.20. Some of a PO Item Received Qty was used during manual Part Qty adjustment
    logEntry | The log entry for the part.
    userID | The ID of the user that created the log.
    associatedID | The ID of the item associated with this log, if any. Current examples include:sourceID: 5, associatedID type: TasksourceID: 18, associatedID type: BillsourceID: 20, associatedID type: Bill

    Query Parameters:
    - logs: 
    - sources: 
    - users: 
    - logEntry: 
    - start: 
    - end: 
    - page: 
    - parts: 
    - limit: 
    - cursor: 
    """

class PartsLogsDelete_part_logNamespace(LimbleEndpoint):
    """
    This request deletes manual log entries (sourceID=4).
    """

class PartsLogsUpdate_part_logNamespace(LimbleEndpoint):
    """
    This requests updates a manual log entry. Only logs with a sourceID=4 can be updated.
    """

class PartsLogsNew_part_logNamespace(LimbleEndpoint):
    """
    This request creates a manual log entry for a part.
    
    This request adds a new Field to the list of Suggested Fields that can later be attached to Parts.

    Parameter | Type | Required? | Description
    ------------------------------------------
    userID | Int | Required | The ID of the user creating the log.
    logEntry | String | Required | Details of the log.
    """

class PartsLogsPart_logsNamespace(LimbleEndpoint):
    """
    This request returns the log entries for a part.
    
    **Note:** this endpoint supports pagination. Please refer to the [Pagination](#pagination) section for more information.
    
    Return data description

    Property | Description
    ----------------------
    logID | The unique logID of the log.
    dateCreated | The date the log was created as a UNIX timestamp.
    partID | The partID the log belongs to.
    sourceID | The sourceID of the source of the log. The sourceID can be as follows:1: Part name was changed.2: Part Number was changed.3: Parts were added/removed.4: Manual log entry.5: Parts were used on a Task.6: Part Price was changed.7: Stale threshold was manually changed.8: Part Qty threshold was manually changed.11: Part Qty threshold status was changed.13: Part Location was changed.14: Part Vendor was changed.15: Part Image was changed.18: Parts were received on a Bill.19: Part Maximum Part Qty was manually changed.20: Some of a PO Item Received Qty was used during manual Part Qty adjustment
    logEntry | The log entry for the part.
    userID | The ID of the user that created the log.
    associatedID | The ID of the item associated with this log, if any. Current examples include:sourceID: 5, associatedID type: TasksourceID: 18, associatedID type: BillsourceID: 20, associatedID type: Bill

    Query Parameters:
    - logs: This parameter is used to only get specific logs. This parameter accepts a comma delimited list of logIDs.
    - sources: This parameter is used to only get logs for a specific sourceID. This parameter accepts a comma delimited list of sourceIDs.
    - users: This parameter is used to only get logs created by specific users. This parameter accepts a comma delimited list of userIDs.
    - logEntry: This is a parameter used to string search for manual log entry (sourceID: 4). This parameter expects a string with the wildcard %.
    - start: This parameter is used to only get logs that were last edited after the unix timestamp passed into the start parameter. 
    - end: This parameter is used to only get logs that were last edited before the unix timestamp passed into the end parameter.
    - page: This parameter is used to paginate results based on the limit. Refer to Pagination section for more information.
    - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
    - cursor: This parameter is a cursor that selects what ID you want to start receiving results at. 
    """

class PartsFieldsNamespace(object):
    @property
    def part_fields(self) -> PartsFieldsPart_fieldsNamespace:
        """
        This request gets detailed information about custom set Part Fields.
        
        This request will return an array of objects that have a file name and a link you can use to download that image. All links are only valid for 15 minutes, a new call will generate a new link.
        
        **Note:** this endpoint supports pagination. Please refer to the [**Pagination**](#pagination) section for more information.

        Query Parameters:
        - fields: This parameter is used to only get specific fields by ID. This parameter expects a comma delimited list of fieldIDs.
        - name: This parameter is used to only get specific field by name. This parameter expects a string full name of a field or partial name with the wildcard %.
        - parts: This parameter is used to only get part fields for a specific Part. This parameter expects a partID.
        - start: This parameter is used to only get part fields for parts that were last edited after the unix timestamp passed into the start parameter.
        - end: This parameter is used to only get parts fields for part fields that were last edited *before* the unix timestamp passed into the end parameter.
        - cursor: This parameter is a cursor that selects what fieldID you want to start receiving results at. e.g. passing 137 here will only get you vendor fields with an id greater than 137.
        - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
        - value: This parameter is used to only get specific field by value. This parameter expects a string full name of a field or partial name with the wildcard %.
        - locations: This parameter is used to paginate results based on the limit. Refer to Pagination section for more information.
        - values: This parameter is used to get part fields by their valueID. This parameter expects a comma delimited list of Value IDs.
        - page: 
        """
        ...
    @property
    def part_suggested_fields(self) -> PartsFieldsPart_suggested_fieldsNamespace:
        """
        This request gets all possible fields a Part can pick from when deciding which fields it should have.

        Query Parameters:
        - fields: This parameter can be used to get a single Part Fields or a list of Part Fields in a comma-separated list.
        - name: This parameter is used to only get specific field by name. This parameter expects a string full name of a field or partial name with the wildcard %.
        - cursor: This parameter is a cursor that selects what fieldID you want to start receiving results at. e.g. passing 137 here will only get you vendor fields with an id greater than 137.
        - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
        """
        ...
    @property
    def update_part_field_value(self) -> PartsFieldsUpdate_part_field_valueNamespace:
        """
        This request updates a Part's field value.

        Parameter | Type | Required? | Description
        ------------------------------------------
        value | Depends on fieldType | Required | The value that will be written to the field. "value" must correspond to the fieldType of the field. For example, if the field is a "number" fieldType, then "value" must be a number.
        """
        ...
    @property
    def attach_field_to_part(self) -> PartsFieldsAttach_field_to_partNamespace:
        """
        This request attaches a Suggested Field to a Part.
        """
        ...
    @property
    def new_part_suggested_field(self) -> PartsFieldsNew_part_suggested_fieldNamespace:
        """
        This request adds a new Field to the list of Suggested Fields that can later be attached to Parts.

        Parameter | Type | Required? | Description
        ------------------------------------------
        locationID | Int | Required | The location ID of the Location to add the new Field to.
        name | String | Required | The name of the new Field. Some custom field names such as "Part Name" are not allowed and reserved for internal use. This will result in a 409 error.
        fieldType | Int | Required | The type of the new Field. You can choose from Text (1), Date (2), Pictures (3), Documents (4), Number (5), Currency (6).
        """
        ...
    @property
    def delete_part_field(self) -> PartsFieldsDelete_part_fieldNamespace:
        """
        This request deletes a custom field attached to a Part.
        """
        ...

class PartsFieldsDelete_part_fieldNamespace(LimbleEndpoint):
    """
    This request deletes a custom field attached to a Part.
    """

class PartsFieldsNew_part_suggested_fieldNamespace(LimbleEndpoint):
    """
    This request adds a new Field to the list of Suggested Fields that can later be attached to Parts.

    Parameter | Type | Required? | Description
    ------------------------------------------
    locationID | Int | Required | The location ID of the Location to add the new Field to.
    name | String | Required | The name of the new Field. Some custom field names such as "Part Name" are not allowed and reserved for internal use. This will result in a 409 error.
    fieldType | Int | Required | The type of the new Field. You can choose from Text (1), Date (2), Pictures (3), Documents (4), Number (5), Currency (6).
    """

class PartsFieldsAttach_field_to_partNamespace(LimbleEndpoint):
    """
    This request attaches a Suggested Field to a Part.
    """

class PartsFieldsUpdate_part_field_valueNamespace(LimbleEndpoint):
    """
    This request updates a Part's field value.

    Parameter | Type | Required? | Description
    ------------------------------------------
    value | Depends on fieldType | Required | The value that will be written to the field. "value" must correspond to the fieldType of the field. For example, if the field is a "number" fieldType, then "value" must be a number.
    """

class PartsFieldsPart_suggested_fieldsNamespace(LimbleEndpoint):
    """
    This request gets all possible fields a Part can pick from when deciding which fields it should have.

    Query Parameters:
    - fields: This parameter can be used to get a single Part Fields or a list of Part Fields in a comma-separated list.
    - name: This parameter is used to only get specific field by name. This parameter expects a string full name of a field or partial name with the wildcard %.
    - cursor: This parameter is a cursor that selects what fieldID you want to start receiving results at. e.g. passing 137 here will only get you vendor fields with an id greater than 137.
    - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
    """

class PartsFieldsPart_fieldsNamespace(LimbleEndpoint):
    """
    This request gets detailed information about custom set Part Fields.
    
    This request will return an array of objects that have a file name and a link you can use to download that image. All links are only valid for 15 minutes, a new call will generate a new link.
    
    **Note:** this endpoint supports pagination. Please refer to the [**Pagination**](#pagination) section for more information.

    Query Parameters:
    - fields: This parameter is used to only get specific fields by ID. This parameter expects a comma delimited list of fieldIDs.
    - name: This parameter is used to only get specific field by name. This parameter expects a string full name of a field or partial name with the wildcard %.
    - parts: This parameter is used to only get part fields for a specific Part. This parameter expects a partID.
    - start: This parameter is used to only get part fields for parts that were last edited after the unix timestamp passed into the start parameter.
    - end: This parameter is used to only get parts fields for part fields that were last edited *before* the unix timestamp passed into the end parameter.
    - cursor: This parameter is a cursor that selects what fieldID you want to start receiving results at. e.g. passing 137 here will only get you vendor fields with an id greater than 137.
    - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
    - value: This parameter is used to only get specific field by value. This parameter expects a string full name of a field or partial name with the wildcard %.
    - locations: This parameter is used to paginate results based on the limit. Refer to Pagination section for more information.
    - values: This parameter is used to get part fields by their valueID. This parameter expects a comma delimited list of Value IDs.
    - page: 
    """

class PartsCategoriesNamespace(LimbleEndpoint):
    """

    Query Parameters:
    - categories: This parameter is used to only get specific part categories. This parameter accepts a comma delimited list of categoryIDs.
    - name: This parameter is used to string search part categories names either partial or full name with the wildcard %.
    """
    @property
    def create_part_category(self) -> PartsCategoriesCreate_part_categoryNamespace:
        """
        Creates a part category to help you organize your parts.

        Parameter | Type | Required? | Description
        ------------------------------------------
        name | string | Required | The name of your new part category (i.e. "Lawn Mower Parts")
        """
        ...
    @property
    def update_part_category(self) -> PartsCategoriesUpdate_part_categoryNamespace:
        """
        This request updates a Part Category's name.

        Parameter | Type | Required? | Description
        ------------------------------------------
        name | string | Required | The name of your new part category (i.e. "Filters")
        """
        ...
    @property
    def delete_part_category(self) -> PartsCategoriesDelete_part_categoryNamespace:
        """
        This request will remove the Part Category from all Parts and from possible Categories.
        """
        ...

class PartsCategoriesDelete_part_categoryNamespace(LimbleEndpoint):
    """
    This request will remove the Part Category from all Parts and from possible Categories.
    """

class PartsCategoriesUpdate_part_categoryNamespace(LimbleEndpoint):
    """
    This request updates a Part Category's name.

    Parameter | Type | Required? | Description
    ------------------------------------------
    name | string | Required | The name of your new part category (i.e. "Filters")
    """

class PartsCategoriesCreate_part_categoryNamespace(LimbleEndpoint):
    """
    Creates a part category to help you organize your parts.

    Parameter | Type | Required? | Description
    ------------------------------------------
    name | string | Required | The name of your new part category (i.e. "Lawn Mower Parts")
    """

class PartsImagesNamespace(object):
    @property
    def add_part_image(self) -> PartsImagesAdd_part_imageNamespace:
        """
        This request adds the main image for a Part.
        """
        ...
    @property
    def delete_part_image(self) -> PartsImagesDelete_part_imageNamespace:
        """
        This request removes the main image from a Part.
        """
        ...

class PartsImagesDelete_part_imageNamespace(LimbleEndpoint):
    """
    This request removes the main image from a Part.
    """

class PartsImagesAdd_part_imageNamespace(LimbleEndpoint):
    """
    This request adds the main image for a Part.
    """

class LocationsNamespace(LimbleEndpoint):
    """
    This request returns your Locations in Limble.
    
    **Note:** this endpoint supports pagination. Please refer to the [**Pagination**](https://desktop.postman.com/?desktopVersion=9.31.0&userId=16480856&teamId=206430) section for more information.
    
    **Note:** this endpoint supports pagination. Please refer to the [Pagination](https://desktop.postman.com/?desktopVersion=9.31.0&userId=16480856&teamId=206430) section for more information.
    
    EndFragment
    
    **Return data description**

    Property | Description
    ----------------------
    name | The name of the Location
    regionID | The ID of the region the Location is part of. A regionID of 0 means the location is not a part of any region.
    timezone | The Timezone the location is set at.List of Timezones
    weeklyOperationHours | The number of hours your Assets run at this location per week. This is used to help calculate MTBF.
    workRequestPortal | This is a URL you can use to submit Work Requests to this Location.
    geoLocation | The location of a Limble location on a Map.
    currencyCode | The ISO code for the currency at this location.

    Query Parameters:
    - locations: This parameter is used to only get locations in the list provided. This parameter accepts a comma delimited list of Location IDs.
    - name: This parameter is used to only get specific locations by name. This parameter expects a string full name of a location or partial name with the wildcard %.
    - cursor: This parameter is a cursor that selects what locationID you want to start receiving results at. e.g. passing 137 here will only get you locations with an id greater than 137.
    - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
    - regions: This parameter is used to get locations that belong to a region.
This parameter expects a regionID a location may belong to.
    - geoLocation: This parameter is used to filter results that contain a geoLocation property. By default it is false and will return **all** locations with and without geoLocation property. If true, it will only return locations with a geoLocation property.
    - page: 
    """
    @property
    def new_location(self) -> LocationsNew_locationNamespace:
        """
        This request creates a new Location.
        
        **Body parameter descriptions**

        Parameter | Type | Required? | Description
        ------------------------------------------
        name | String | Required | The new name of the Location.
        timezone | string | Required | The timezone this location resides in. This accepts a standard tz database name, see here.
        phone | string | Required | The phone number associated with this location.
        weeklyOperationHours | Int | Optional | The hours per week this location operates.
        address | string | Optional | The physical address of this location.
        address2 | string | Optional | The physical address of this location.
        geoLocation | geoJSON | Optional | The geoJSON Feature object that can be used to locate a Limble location on a Map.
        extraNotificationsEmail | string | Optional | Include an email address to receive notifications for the location.
        currencyCode | string | Optional | The ISO code for the currency at this location. For example: "USD".
        """
        ...
    @property
    def update_location(self) -> LocationsUpdate_locationNamespace:
        """
        This request updates a Location.
        
        **Body parameter descriptions**

        Parameter | Type | Required? | Description
        ------------------------------------------
        name | String | Optional | The new name of the Location.
        timezone | string | Optional | The timezone this location resides in. This accepts a standard tz database name, see here.
        phone | string | Optional | The phone number associated with this location.
        weeklyOperationHours | Int | Optional | The number of hours your Assets run at this location per week. This is used to help calculate MTBF.
        address | string | Optional | The physical address of this location.
        address2 | string | Optional | The physical address of this location.
        geoLocation | geoJSON | Optional | The geoJSON Feature object that can be used to locate a Limble location on a Map.To remove geoLocation from a Limble Location pass an empty object ( {}).
        currencyCode | string | Optional | The ISO code for the currency at this location. For example: "USD".
        """
        ...
    @property
    def delete_location(self) -> LocationsDelete_locationNamespace:
        """
        This request removes a Location from your Limble account.  This will also remove everything else at this locaiton including Assets, Parts, Tasks, etc.  Be VERY careful using this call.
        """
        ...

class LocationsDelete_locationNamespace(LimbleEndpoint):
    """
    This request removes a Location from your Limble account.  This will also remove everything else at this locaiton including Assets, Parts, Tasks, etc.  Be VERY careful using this call.
    """

class LocationsUpdate_locationNamespace(LimbleEndpoint):
    """
    This request updates a Location.
    
    **Body parameter descriptions**

    Parameter | Type | Required? | Description
    ------------------------------------------
    name | String | Optional | The new name of the Location.
    timezone | string | Optional | The timezone this location resides in. This accepts a standard tz database name, see here.
    phone | string | Optional | The phone number associated with this location.
    weeklyOperationHours | Int | Optional | The number of hours your Assets run at this location per week. This is used to help calculate MTBF.
    address | string | Optional | The physical address of this location.
    address2 | string | Optional | The physical address of this location.
    geoLocation | geoJSON | Optional | The geoJSON Feature object that can be used to locate a Limble location on a Map.To remove geoLocation from a Limble Location pass an empty object ( {}).
    currencyCode | string | Optional | The ISO code for the currency at this location. For example: "USD".
    """

class LocationsNew_locationNamespace(LimbleEndpoint):
    """
    This request creates a new Location.
    
    **Body parameter descriptions**

    Parameter | Type | Required? | Description
    ------------------------------------------
    name | String | Required | The new name of the Location.
    timezone | string | Required | The timezone this location resides in. This accepts a standard tz database name, see here.
    phone | string | Required | The phone number associated with this location.
    weeklyOperationHours | Int | Optional | The hours per week this location operates.
    address | string | Optional | The physical address of this location.
    address2 | string | Optional | The physical address of this location.
    geoLocation | geoJSON | Optional | The geoJSON Feature object that can be used to locate a Limble location on a Map.
    extraNotificationsEmail | string | Optional | Include an email address to receive notifications for the location.
    currencyCode | string | Optional | The ISO code for the currency at this location. For example: "USD".
    """

class AssetsNamespace(LimbleEndpoint):
    """
    This request returns a list of Assets with top level information such as name, last edited, etc.
    
    **Note:** this endpoint supports pagination. Please refer to the [Pagination](#pagination) section for more information.
    
    Return data description

    Property | Description
    ----------------------
    meta | Requests to gather more information on an Asset such as Fields for the Asset or what Tasks are assigned to the Asset
    startedOn | The date when this Asset was started on. This property is used to help determine runtime which is used in MTBF.
    lastEdited | A UNIX timestamp of when this Asset was last edited.
    parentAssetID | The Asset that is the parent of this Asset. If the value is 0 that means this Asset does not have a parent.
    locationID | The ID of the location this asset is located at.
    hoursPerWeek | The number of hours this Asset runs per week. This is used to determine runtime which is used in MTBF. If the value is -1 then the Asset uses the Location's hoursPerWeek setting.
    workRequestPortal | The url work requestors can use to submit problems with this Asset.
    image | Array of objects that have a file name and a link you can use to download that image. All links are only valid for 15 minutes, a new call will generate a new link.
    geoLocation | The location of an asset on a Map.

    Query Parameters:
    - assets: This parameter is used to only get specific Assets. This parameter expects a comma delimited list of Asset IDs.
    - name: This is a parameter used to string search for a name or partial name of an asset this parameter expects a string with the wildcard %.
    - locations: This parameter is used to only get Assets at a specific group of Locations. This parameter accepts a comma delimited list of Location IDs.
    - start: This parameter is used to only get Assets that were last edited after the unix timestamp passed into the start parameter. For example, all Assets that were last edited after April 18th, 2018.
    - end: This parameter is used to only get Assets that were last edited *before* the unix timestamp passed into the end parameter.
    - cursor: This parameter is a cursor that selects what ID you want to start receiving results at. Without ordering, this will return results with an ID greater than the value of cursor. With ordering, this will return results starting at the next item in the order, regardless of whether its ID is greater than or lesser than the value of cursor.
    - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
    - parentAssetID: This parameter can be used to get asset(s) children using the Parent's ID. This parameter accepts a comma delimited list of Asset IDs.
    - orderBy: This parameter is used to order results by their lastEdited property instead of the default ordering by ascending assetID. CANNOT be provided alongside the cursor parameter. to paginate in this ordering, use the start or end parameters.
    - page: This parameter is used to paginate results based on the limit. Refer to Pagination section for more information.
    - geoLocation: This parameter is used to filter results that contain a geoLocation property. By default it is false and will return **all** assets with and without geoLocation property. If true, it will only return assets with a geoLocation property.
    """
    @property
    def image(self) -> AssetsImageNamespace: ...
    @property
    def fields(self) -> AssetsFieldsNamespace:
        """
        Asset fields are a way to add custom information onto your assets.  For example you may want to fields such as Make, Model, Meter Readings, Manuals, Pictures, Contracts etc.
        """
        ...
    @property
    def logs(self) -> AssetsLogsNamespace: ...
    @property
    def batch(self) -> AssetsBatchNamespace: ...
    @property
    def parts(self) -> AssetsPartsNamespace: ...
    @property
    def new_asset(self) -> AssetsNew_assetNamespace:
        """
        This request creates a new blank Asset.

        Parameter | Type | Required? | Description
        ------------------------------------------
        name | String | Required | The new name of the Asset.
        hoursPerWeek | Integer | Optional | The new hours of operation per week for this Asset. Use -1 to disable this feature.
        parentAssetID | Int | Optional | The asset's parent. This makes it so assets can be nested in the web application.
        locationID | Int | Required | The ID of the location this asset is located at.
        geoLocation | geoJSON | Optional | The geoJSON Feature object that can be used to locate an asset on a Map.
        """
        ...
    @property
    def patch_asset(self) -> AssetsPatch_assetNamespace:
        """
        This request updates an Asset's top level information. See Update Asset Field Value to update an Asset Field's value.

        Parameter | Type | Required? | Description
        ------------------------------------------
        name | String | Optional | The new name of the Asset.
        hoursPerWeek | Integer | Optional | The new hours of operation per week for this Asset. Use -1 to disable this feature and have it default to the Locations hours of operation.
        parentAssetID | Int | Optional | The asset's parent. This must be another asset ID and is used to display an Asset hierarchy. You can not have assets be their own ancestor.
        startedOn | Int | Optional | The new date this Asset was created. Must be a unixtimestamp.
        geoLocation | geoJSON | Optional | The geoJSON Feature object that can be used to locate an asset on a Map. To remove geoLocation from an Asset pass an empty object ( {}).
        """
        ...
    @property
    def delete_asset(self) -> AssetsDelete_assetNamespace:
        """
        This request removes an Asset from your Limble account.
        """
        ...
    @property
    def move_asset_to_another_location(self) -> AssetsMove_asset_to_another_locationNamespace:
        """
        This request moves an existing asset from it's current location to another location. An parent asset that has one or more children assets cannot be moved.
        
        A child asset can be moved and will be created as a top level asset in the other location.

        Parameter | Type | Required? | Description
        ------------------------------------------
        locationID | Int | Required | The locationID of the location the asset needs to be moved to.
        transferParts | boolean | Optional | A boolean representing whether parts associated with the asset should be moved to the location as well.Defaults to true.
        """
        ...

class AssetsMove_asset_to_another_locationNamespace(LimbleEndpoint):
    """
    This request moves an existing asset from it's current location to another location. An parent asset that has one or more children assets cannot be moved.
    
    A child asset can be moved and will be created as a top level asset in the other location.

    Parameter | Type | Required? | Description
    ------------------------------------------
    locationID | Int | Required | The locationID of the location the asset needs to be moved to.
    transferParts | boolean | Optional | A boolean representing whether parts associated with the asset should be moved to the location as well.Defaults to true.
    """

class AssetsDelete_assetNamespace(LimbleEndpoint):
    """
    This request removes an Asset from your Limble account.
    """

class AssetsPatch_assetNamespace(LimbleEndpoint):
    """
    This request updates an Asset's top level information. See Update Asset Field Value to update an Asset Field's value.

    Parameter | Type | Required? | Description
    ------------------------------------------
    name | String | Optional | The new name of the Asset.
    hoursPerWeek | Integer | Optional | The new hours of operation per week for this Asset. Use -1 to disable this feature and have it default to the Locations hours of operation.
    parentAssetID | Int | Optional | The asset's parent. This must be another asset ID and is used to display an Asset hierarchy. You can not have assets be their own ancestor.
    startedOn | Int | Optional | The new date this Asset was created. Must be a unixtimestamp.
    geoLocation | geoJSON | Optional | The geoJSON Feature object that can be used to locate an asset on a Map. To remove geoLocation from an Asset pass an empty object ( {}).
    """

class AssetsNew_assetNamespace(LimbleEndpoint):
    """
    This request creates a new blank Asset.

    Parameter | Type | Required? | Description
    ------------------------------------------
    name | String | Required | The new name of the Asset.
    hoursPerWeek | Integer | Optional | The new hours of operation per week for this Asset. Use -1 to disable this feature.
    parentAssetID | Int | Optional | The asset's parent. This makes it so assets can be nested in the web application.
    locationID | Int | Required | The ID of the location this asset is located at.
    geoLocation | geoJSON | Optional | The geoJSON Feature object that can be used to locate an asset on a Map.
    """

class AssetsPartsNamespace(object):
    @property
    def asset_parts(self) -> AssetsPartsAsset_partsNamespace:
        """
        This request returns a list of Part Asset Relations with top level information such as part, asset, qty, last edited, etc.
        
        **Note:** this endpoint supports pagination. Please refer to the [Pagination](#pagination) section for more information.
        
        Return data description

        Property | Description
        ----------------------
        relationID | The Relations ID. e.g. 1
        partID | The ID of the Part in this Relation
        assetID | The ID of the Asset in this Relation
        qty | The qty of the Part related to this Asset
        createdAt | The unix timestamp at which this Relation was created
        lastEdited | The unix timestamp at which this Relation last saw a change
        associationType | The method used to create this Relation. At this time, only "manual" is supported

        Query Parameters:
        - assets: This parameter is used to only get specific Assets. This parameter expects a comma delimited list of Asset IDs.
        - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
        - page: This parameter is used to paginate results based on the limit. Refer to Pagination section for more information.
        - cursor: This parameter is a cursor that selects what ID you want to start receiving results at. Without ordering, this will return results with an ID greater than the value of cursor. With ordering, this will return results starting at the next item in the order, regardless of whether its ID is greater than or lesser than the value of cursor.
        - parts: This parameter is used to only get specific Parts. This parameter accepts a comma delimited list of part IDs.
        - relations: This parameter is used to only get specific relations. This parameter expects a comma delimited list of relation IDs.
        - start: This parameter is used to only get relations that were last edited after the unix timestamp passed into the start parameter. For example, all relations that were last edited after April 18th, 2018.
        - end: This parameter is used to only get relations that were last edited *before* the unix timestamp passed into the end parameter.
        """
        ...

class AssetsPartsAsset_partsNamespace(LimbleEndpoint):
    """
    This request returns a list of Part Asset Relations with top level information such as part, asset, qty, last edited, etc.
    
    **Note:** this endpoint supports pagination. Please refer to the [Pagination](#pagination) section for more information.
    
    Return data description

    Property | Description
    ----------------------
    relationID | The Relations ID. e.g. 1
    partID | The ID of the Part in this Relation
    assetID | The ID of the Asset in this Relation
    qty | The qty of the Part related to this Asset
    createdAt | The unix timestamp at which this Relation was created
    lastEdited | The unix timestamp at which this Relation last saw a change
    associationType | The method used to create this Relation. At this time, only "manual" is supported

    Query Parameters:
    - assets: This parameter is used to only get specific Assets. This parameter expects a comma delimited list of Asset IDs.
    - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
    - page: This parameter is used to paginate results based on the limit. Refer to Pagination section for more information.
    - cursor: This parameter is a cursor that selects what ID you want to start receiving results at. Without ordering, this will return results with an ID greater than the value of cursor. With ordering, this will return results starting at the next item in the order, regardless of whether its ID is greater than or lesser than the value of cursor.
    - parts: This parameter is used to only get specific Parts. This parameter accepts a comma delimited list of part IDs.
    - relations: This parameter is used to only get specific relations. This parameter expects a comma delimited list of relation IDs.
    - start: This parameter is used to only get relations that were last edited after the unix timestamp passed into the start parameter. For example, all relations that were last edited after April 18th, 2018.
    - end: This parameter is used to only get relations that were last edited *before* the unix timestamp passed into the end parameter.
    """

class AssetsBatchNamespace(object):
    @property
    def batch_update_asset_fields(self) -> AssetsBatchBatch_update_asset_fieldsNamespace:
        """
        This request will update multiple asset fields values at a time. The request expects an array of asset fields values. The array needs to have atleast two asset field values and atmost 100 asset field values. The request expects an array made up of asset field values that need to be updated. Only asset fields values of type Text (1), Date (2), Number (5) and Currency (6) can be updated using this request.
        
        The response returns `{ sucess:true }` if all field values are updated successfully. The response returns `{ sucess: false }` and an `updates` array that gives details of which field values were updated and the `reason` for field values that were not updated successfully. Please refer to the examples for more information.

        Parameter | Type | Required? | Description
        ------------------------------------------
        valueID | Integer | Required | The valueID of the asset field value
        value | Based on the type of value | Required | The value that needs to be updated
        """
        ...

class AssetsBatchBatch_update_asset_fieldsNamespace(LimbleEndpoint):
    """
    This request will update multiple asset fields values at a time. The request expects an array of asset fields values. The array needs to have atleast two asset field values and atmost 100 asset field values. The request expects an array made up of asset field values that need to be updated. Only asset fields values of type Text (1), Date (2), Number (5) and Currency (6) can be updated using this request.
    
    The response returns `{ sucess:true }` if all field values are updated successfully. The response returns `{ sucess: false }` and an `updates` array that gives details of which field values were updated and the `reason` for field values that were not updated successfully. Please refer to the examples for more information.

    Parameter | Type | Required? | Description
    ------------------------------------------
    valueID | Integer | Required | The valueID of the asset field value
    value | Based on the type of value | Required | The value that needs to be updated
    """

class AssetsLogsNamespace(object):
    @property
    def files(self) -> AssetsLogsFilesNamespace: ...
    @property
    def asset_logs(self) -> AssetsLogsAsset_logsNamespace:
        """
        This request returns logs created manually by users and automatically created (where userID=0) by certain actions taken on the asset. Logs related to tasks completed on an Asset will not be returned.
        
        **Note:** this endpoint supports pagination. Please refer to the [**Pagination**](#pagination) section for more information.
        
        Return data description

        Property | Description
        ----------------------
        logID | The unique logID of the log.
        dateCreated | The date the log was created as a UNIX timestamp.
        assetD | The ID of the asset the log belongs to.
        logEntry | The log entry for the asset.
        userID | The ID of the user that created the log.
        logFiles | An array of objects that have a fileID, fileName and a link that can used to download the files attached to the log. All links are only valid for 15 minutes, a new call will generate a new link.

        Query Parameters:
        - logs: This parameter is used to only get specific logs. This parameter accepts a comma delimited list of logIDs.
        - users: This parameter is used to only get logs created by specific users. This parameter accepts a comma delimited list of userIDs.
        - logEntry: This is a parameter used to string search for manual log entry. This parameter expects a string with the wildcard %.
        - start: This parameter is used to only get logs that were last edited after the unix timestamp passed into the start parameter. 
        - end: This parameter is used to only get logs that were last edited before the unix timestamp passed into the end parameter.
        - page: This parameter is used to paginate results based on the limit. Refer to Pagination section for more information.
        - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
        - cursor: This parameter is a cursor that selects what ID you want to start receiving results at. 
        """
        ...
    @property
    def new_asset_log(self) -> AssetsLogsNew_asset_logNamespace:
        """
        This requests creates a manual log entry for an asset.

        Parameter | Type | Required? | Description
        ------------------------------------------
        userID | Int | Optional | The ID of the user creating the log. If userID is not given a log entry with userID=0 will be created.
        logEntry | String | Required | Details of the log.
        """
        ...
    @property
    def update_asset_log(self) -> AssetsLogsUpdate_asset_logNamespace:
        """
        This requests updates a manual log entry for an asset.
        """
        ...
    @property
    def delete_asset_log(self) -> AssetsLogsDelete_asset_logNamespace:
        """
        This requests deletes a manual log entry for an asset.
        """
        ...

class AssetsLogsDelete_asset_logNamespace(LimbleEndpoint):
    """
    This requests deletes a manual log entry for an asset.
    """

class AssetsLogsUpdate_asset_logNamespace(LimbleEndpoint):
    """
    This requests updates a manual log entry for an asset.
    """

class AssetsLogsNew_asset_logNamespace(LimbleEndpoint):
    """
    This requests creates a manual log entry for an asset.

    Parameter | Type | Required? | Description
    ------------------------------------------
    userID | Int | Optional | The ID of the user creating the log. If userID is not given a log entry with userID=0 will be created.
    logEntry | String | Required | Details of the log.
    """

class AssetsLogsAsset_logsNamespace(LimbleEndpoint):
    """
    This request returns logs created manually by users and automatically created (where userID=0) by certain actions taken on the asset. Logs related to tasks completed on an Asset will not be returned.
    
    **Note:** this endpoint supports pagination. Please refer to the [**Pagination**](#pagination) section for more information.
    
    Return data description

    Property | Description
    ----------------------
    logID | The unique logID of the log.
    dateCreated | The date the log was created as a UNIX timestamp.
    assetD | The ID of the asset the log belongs to.
    logEntry | The log entry for the asset.
    userID | The ID of the user that created the log.
    logFiles | An array of objects that have a fileID, fileName and a link that can used to download the files attached to the log. All links are only valid for 15 minutes, a new call will generate a new link.

    Query Parameters:
    - logs: This parameter is used to only get specific logs. This parameter accepts a comma delimited list of logIDs.
    - users: This parameter is used to only get logs created by specific users. This parameter accepts a comma delimited list of userIDs.
    - logEntry: This is a parameter used to string search for manual log entry. This parameter expects a string with the wildcard %.
    - start: This parameter is used to only get logs that were last edited after the unix timestamp passed into the start parameter. 
    - end: This parameter is used to only get logs that were last edited before the unix timestamp passed into the end parameter.
    - page: This parameter is used to paginate results based on the limit. Refer to Pagination section for more information.
    - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
    - cursor: This parameter is a cursor that selects what ID you want to start receiving results at. 
    """

class AssetsLogsFilesNamespace(object):
    @property
    def delete_asset_log_file(self) -> AssetsLogsFilesDelete_asset_log_fileNamespace:
        """
        This requests deletes a file attached to a log.
        """
        ...
    @property
    def add_asset_log_file(self) -> AssetsLogsFilesAdd_asset_log_fileNamespace:
        """
        This request adds files to a log.
        
        Return data description

        Property | Description
        ----------------------
        fileID | The ID of the file attached to the log.
        """
        ...

class AssetsLogsFilesAdd_asset_log_fileNamespace(LimbleEndpoint):
    """
    This request adds files to a log.
    
    Return data description

    Property | Description
    ----------------------
    fileID | The ID of the file attached to the log.
    """

class AssetsLogsFilesDelete_asset_log_fileNamespace(LimbleEndpoint):
    """
    This requests deletes a file attached to a log.
    """

class AssetsFieldsNamespace(object):
    """
    Asset fields are a way to add custom information onto your assets.  For example you may want to fields such as Make, Model, Meter Readings, Manuals, Pictures, Contracts etc.
    """
    @property
    def asset_fields(self) -> AssetsFieldsAsset_fieldsNamespace:
        """
        This request gets detailed information about asset fields such as Make, Model and any other custom field.
        
        This call also returns "files" which is an array of objects that have a file name and a link you can use to download that file. All links are only valid for 15 minutes, a new call will generate a new link.
        
        **Note:** this endpoint supports pagination. Please refer to the [**Pagination**](#pagination) section for more information.

        Query Parameters:
        - name: This parameter is used to only get specific field by name. This parameter expects a string full name of a field or partial name with the wildcard %.
        - fields: This parameter can be used to get a single Asset Fields or a list of Asset Fields in a comma-separated list.
        - start: This parameter is used to only get Asset Fields for Assets that were last edited after the unix timestamp passed into the start parameter. For example, all Assets that were last edited after April 18th, 2018.
        - end: This parameter is used to only get Asset Fields for Assets that were last edited *before* the unix timestamp passed into the end parameter.
        - cursor: This parameter is a cursor that selects what id you want to start receiving results at. e.g. passing 137 here will only get you asset fields with an id greater than 137.
        - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
        - locations: This parameter can be used to get a group of asset fields in a location in a comma-separated list.
        - value: This parameter is used to only get specific field by value. This parameter expects a string full name of a field or partial name with the wildcard %.
        - assetName: This parameter is used to only get specific fields by asset name. This parameter expects a string full name of a field or partial name with the wildcard %.
        - fieldType[0]: This parameter is used to only get specific fields by type. This parameter expects an array of strings "Text, Date, Pictures, Documents, Number, Currency, Dropdown"
        - fieldType[1]: This parameter is used to only get specific fields by type. This parameter expects an array of strings "Text, Date, Pictures, Documents, Number, Currency, Dropdown"
        - page: This parameter is used to paginate results based on the limit. Refer to Pagination section for more information.
        - values: This parameter is used to get asset fields by their valueID. This parameter expects a comma delimited list of Value IDs.
        - assets: This parameter can be used to get a group of asset fields for a specific set of asset ids in a comma-separated list.
        """
        ...
    @property
    def asset_suggested_fields(self) -> AssetsFieldsAsset_suggested_fieldsNamespace:
        """
        This request gets all possible fields an Asset can pick from when deciding which fields it should have.  
        
        To understand this concept, let's pretend you have the following assets:  
        
        Your first Asset (a Truck) has the fields Make, Model, and VIN.  
        
        Your second Asset (a HVAC) has the fields Make, Model, and Serial Number.  
        
        This would mean there are 4 suggested fields that exist:  Make, Model, VIN and Serial Number.  If I added a third new asset I could pick from any of the 4 suggested fields.
        
        Suggested fields are the full list of possible fields that can be added to assets at that location.

        Query Parameters:
        - fields: This parameter can be used to get a single Asset Fields or a list of Asset Fields in a comma-separated list.
        - name: This parameter is used to only get specific field by name. This parameter expects a string full name of a field or partial name with the wildcard %.
        - cursor: This parameter is a cursor that selects what id you want to start receiving results at. e.g. passing 137 here will only get you asset fields with an id greater than 137.
        - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
        - locations: This parameter is used to only get fields at a specific group of Locations. This parameter accepts a comma delimited list of Location IDs.
        """
        ...
    @property
    def asset_field_history(self) -> AssetsFieldsAsset_field_historyNamespace:
        """
        Any time an Asset's field is changed an entry is inserted into a history.  
        
        This request allows you to pull that information so you can see trends over time.

        Query Parameters:
        - assets: This parameter can be used to get a single Asset or a list of Assets in a comma-separated list.
        - fields: This parameter can be used to get a single Asset Fields or a list of Asset Fields in a comma-separated list.
        - start: This parameter is used to only get Asset Fields for Assets that were last edited after the unix timestamp passed into the start parameter. For example, all Assets that were last edited after April 18th, 2018.
        - end: This parameter is used to only get Asset Fields for Assets that were last edited *before* the unix timestamp passed into the end parameter.
        - limit: This parameter is a cursor that selects what id you want to start receiving results at. e.g. passing 137 here will only get you asset fields with an id greater than 137.
        - cursor: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
        """
        ...
    @property
    def new_asset_suggested_field(self) -> AssetsFieldsNew_asset_suggested_fieldNamespace:
        """
        This request creates a new Suggested Field.
        
        Suggested Fields are the full list of possible Fields that can be added to Assets at that Location.

        Parameter | Type | Required? | Description
        ------------------------------------------
        locationID | Int | Required | The location ID of the Asset to add the new Field to.
        name | String | Required | The name of the new Field. Some custom field names such as "Asset" are not allowed and reserved for internal use. This will result in a 409 error.
        fieldType | Int | Required | The type of the new Field. You can choose from Text (1), Date (2), Pictures (3), Documents (4), Number (5),
				Currency (6).
        """
        ...
    @property
    def update_asset_field_value(self) -> AssetsFieldsUpdate_asset_field_valueNamespace:
        """
        This request updates the value of a Field that is attached to an Asset.

        Parameter | Type | Required? | Description
        ------------------------------------------
        value | Varies depending on the Field's type | Required | The value that will be written to the field, overwriting the previous value and creating an entry in the field history.  "value" must correspond to the fieldType of the field. For example, if the field is a "number" fieldType, then "value" must be a number.

        Query Parameters:
        - : 
        """
        ...
    @property
    def attach_field_to_asset(self) -> AssetsFieldsAttach_field_to_assetNamespace:
        """
        This request attaches a Suggested Field to an Asset. The field and asset must belong to the same location.
        
        For example, let's say I have an Asset called Truck - 001.  This Truck doesn't have any Fields attached to it, but I want to track its Make so I can set that this Truck is a Dodge.  This is the request I would use to attach the Make Field to the Truck and then I would use the Update Asset Field Value request to set it to Dodge.

        Parameter | Type | Required? | Description
        ------------------------------------------
        locationID | Int | Required | The ID of the Location the Asset exists at.
        fieldID | Int | Required | The ID of the existing Field to add to the Asset.
        """
        ...
    @property
    def delete_asset_field(self) -> AssetsFieldsDelete_asset_fieldNamespace:
        """
        This request deletes a field attached to an Asset.
        """
        ...

class AssetsFieldsDelete_asset_fieldNamespace(LimbleEndpoint):
    """
    This request deletes a field attached to an Asset.
    """

class AssetsFieldsAttach_field_to_assetNamespace(LimbleEndpoint):
    """
    This request attaches a Suggested Field to an Asset. The field and asset must belong to the same location.
    
    For example, let's say I have an Asset called Truck - 001.  This Truck doesn't have any Fields attached to it, but I want to track its Make so I can set that this Truck is a Dodge.  This is the request I would use to attach the Make Field to the Truck and then I would use the Update Asset Field Value request to set it to Dodge.

    Parameter | Type | Required? | Description
    ------------------------------------------
    locationID | Int | Required | The ID of the Location the Asset exists at.
    fieldID | Int | Required | The ID of the existing Field to add to the Asset.
    """

class AssetsFieldsUpdate_asset_field_valueNamespace(LimbleEndpoint):
    """
    This request updates the value of a Field that is attached to an Asset.

    Parameter | Type | Required? | Description
    ------------------------------------------
    value | Varies depending on the Field's type | Required | The value that will be written to the field, overwriting the previous value and creating an entry in the field history.  "value" must correspond to the fieldType of the field. For example, if the field is a "number" fieldType, then "value" must be a number.

    Query Parameters:
    - : 
    """

class AssetsFieldsNew_asset_suggested_fieldNamespace(LimbleEndpoint):
    """
    This request creates a new Suggested Field.
    
    Suggested Fields are the full list of possible Fields that can be added to Assets at that Location.

    Parameter | Type | Required? | Description
    ------------------------------------------
    locationID | Int | Required | The location ID of the Asset to add the new Field to.
    name | String | Required | The name of the new Field. Some custom field names such as "Asset" are not allowed and reserved for internal use. This will result in a 409 error.
    fieldType | Int | Required | The type of the new Field. You can choose from Text (1), Date (2), Pictures (3), Documents (4), Number (5),
				Currency (6).
    """

class AssetsFieldsAsset_field_historyNamespace(LimbleEndpoint):
    """
    Any time an Asset's field is changed an entry is inserted into a history.  
    
    This request allows you to pull that information so you can see trends over time.

    Query Parameters:
    - assets: This parameter can be used to get a single Asset or a list of Assets in a comma-separated list.
    - fields: This parameter can be used to get a single Asset Fields or a list of Asset Fields in a comma-separated list.
    - start: This parameter is used to only get Asset Fields for Assets that were last edited after the unix timestamp passed into the start parameter. For example, all Assets that were last edited after April 18th, 2018.
    - end: This parameter is used to only get Asset Fields for Assets that were last edited *before* the unix timestamp passed into the end parameter.
    - limit: This parameter is a cursor that selects what id you want to start receiving results at. e.g. passing 137 here will only get you asset fields with an id greater than 137.
    - cursor: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
    """

class AssetsFieldsAsset_suggested_fieldsNamespace(LimbleEndpoint):
    """
    This request gets all possible fields an Asset can pick from when deciding which fields it should have.  
    
    To understand this concept, let's pretend you have the following assets:  
    
    Your first Asset (a Truck) has the fields Make, Model, and VIN.  
    
    Your second Asset (a HVAC) has the fields Make, Model, and Serial Number.  
    
    This would mean there are 4 suggested fields that exist:  Make, Model, VIN and Serial Number.  If I added a third new asset I could pick from any of the 4 suggested fields.
    
    Suggested fields are the full list of possible fields that can be added to assets at that location.

    Query Parameters:
    - fields: This parameter can be used to get a single Asset Fields or a list of Asset Fields in a comma-separated list.
    - name: This parameter is used to only get specific field by name. This parameter expects a string full name of a field or partial name with the wildcard %.
    - cursor: This parameter is a cursor that selects what id you want to start receiving results at. e.g. passing 137 here will only get you asset fields with an id greater than 137.
    - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
    - locations: This parameter is used to only get fields at a specific group of Locations. This parameter accepts a comma delimited list of Location IDs.
    """

class AssetsFieldsAsset_fieldsNamespace(LimbleEndpoint):
    """
    This request gets detailed information about asset fields such as Make, Model and any other custom field.
    
    This call also returns "files" which is an array of objects that have a file name and a link you can use to download that file. All links are only valid for 15 minutes, a new call will generate a new link.
    
    **Note:** this endpoint supports pagination. Please refer to the [**Pagination**](#pagination) section for more information.

    Query Parameters:
    - name: This parameter is used to only get specific field by name. This parameter expects a string full name of a field or partial name with the wildcard %.
    - fields: This parameter can be used to get a single Asset Fields or a list of Asset Fields in a comma-separated list.
    - start: This parameter is used to only get Asset Fields for Assets that were last edited after the unix timestamp passed into the start parameter. For example, all Assets that were last edited after April 18th, 2018.
    - end: This parameter is used to only get Asset Fields for Assets that were last edited *before* the unix timestamp passed into the end parameter.
    - cursor: This parameter is a cursor that selects what id you want to start receiving results at. e.g. passing 137 here will only get you asset fields with an id greater than 137.
    - limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.
    - locations: This parameter can be used to get a group of asset fields in a location in a comma-separated list.
    - value: This parameter is used to only get specific field by value. This parameter expects a string full name of a field or partial name with the wildcard %.
    - assetName: This parameter is used to only get specific fields by asset name. This parameter expects a string full name of a field or partial name with the wildcard %.
    - fieldType[0]: This parameter is used to only get specific fields by type. This parameter expects an array of strings "Text, Date, Pictures, Documents, Number, Currency, Dropdown"
    - fieldType[1]: This parameter is used to only get specific fields by type. This parameter expects an array of strings "Text, Date, Pictures, Documents, Number, Currency, Dropdown"
    - page: This parameter is used to paginate results based on the limit. Refer to Pagination section for more information.
    - values: This parameter is used to get asset fields by their valueID. This parameter expects a comma delimited list of Value IDs.
    - assets: This parameter can be used to get a group of asset fields for a specific set of asset ids in a comma-separated list.
    """

class AssetsImageNamespace(object):
    @property
    def add_asset_main_image(self) -> AssetsImageAdd_asset_main_imageNamespace:
        """
        Each asset can have one main image associated with it.  This request allows you to set that image.
        """
        ...
    @property
    def delete_asset_main_image(self) -> AssetsImageDelete_asset_main_imageNamespace:
        """
        This request removes the main image from the asset.
        """
        ...

class AssetsImageDelete_asset_main_imageNamespace(LimbleEndpoint):
    """
    This request removes the main image from the asset.
    """

class AssetsImageAdd_asset_main_imageNamespace(LimbleEndpoint):
    """
    Each asset can have one main image associated with it.  This request allows you to set that image.
    """

class MeNamespace(LimbleEndpoint):
    """
    Identifies the current customer. This route can be used to test that authentication to the Limble API was successful.
    
    Return data description

    Property | Description
    ----------------------
    customerName | The name of the customer that your API keys are valid for.
    customerPlan | The Limble plan the customer is currently subscribed to. The customerPlan can have one of following values:starterprofessionalbusinessenterpriselegacy - The plan the customer is currently subscribed to has been deprecated.For more information about various plans please visit the Limble website.
    """
