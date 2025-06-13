from LimbleConnection.LimbleEndpoint import LimbleEndpoint


class Users_Teams:
    """This request gets information about Users such as User Login, User Email etc.

    Parameters:

teams: This parameter expects a comma-separated list of teamIDs to filter teams by.

locations: This parameter expects a comma-separated list of locationIDs to filter teams by

limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.

cursor: This parameter is a cursor that selects what teamID you want to start receiving results at. e.g. passing 137 here will only get you tasks with an id greater than 137.

name: This parameter is used to only get specific team by name. This parameter expects a string full name of a user or partial name with the wildcard %.

    Return data description

    Property:                     Description
    --------------------------------------------------------------------------------------------
    username:                     What a User uses to login.
    wage:                         The hourly rate of an employee.
    active:                       Determines if a user can log into Limble or not.
    emailNotificationActive:      Determines if a User gets Email Notifications From Limble.
    pushNotificationActive:       Determines if a User gets Push Notifications From Limble.
    workdayHours:                 The number of hours a day this employee works.
    dateAdded:                    The date a user was added to Limble. This is a unix timestamp.
    teams:                        What Teams a User has at specific Locations.
    """


class Users(LimbleEndpoint):
    """LimbleEndpoint for user data.

Get Request params:
=======================

users: This parameter expects a comma-separated list of users to get by id

name: This parameter is used to only get specific user by name. This parameter expects a string full name of a user or partial name with the wildcard %.

roles: This parameter expects a comma-separated list of users to get by roleID

teams: This parameter expects a comma-separated list of users to get by teamID

cursor: This parameter is a cursor that selects what userID you want to start receiving results at. e.g. passing 137 here will only get you tasks with an id greater than 137.

limit: This parameter is a result limiter. The default is set to return no more than 100 results at one time.



Return data description
=======================
Property:                     Description

username:                     What a User uses to login.

wage:                         The hourly rate of an employee.

active:                       Determines if a user can log into Limble or not.

emailNotificationActive:      Determines if a User gets Email Notifications From Limble.

pushNotificationActive:       Determines if a User gets Push Notifications From Limble.

workdayHours:                 The number of hours a day this employee works.

dateAdded:                    The date a user was added to Limble. This is a unix timestamp.

teams:                        What Teams a User has at specific Locations.
"""

    teams = Users_Teams


# class other:
#     """This request gets information about Users such as User Login, User Email etc.
#
# Property:                     Description
# username:                     What a User uses to login.
# wage:                         The hourly rate of an employee.
# active:                       Determines if a user can log into Limble or not.
# emailNotificationActive:      Determines if a User gets Email Notifications From Limble.
# pushNotificationActive:       Determines if a User gets Push Notifications From Limble.
# workdayHours:                 The number of hours a day this employee works.
# dateAdded:                    The date a user was added to Limble. This is a unix timestamp.
# teams:                        What Teams a User has at specific Locations.
# """
#
#
#
# """
#         User Properties
#     ===============
#
#     +--------------------------+--------------------------------------------------------------+
#     | Property                 | Description                                                  |
#     +==========================+==============================================================+
#     | username                 | What a User uses to login.                                   |
#     +--------------------------+--------------------------------------------------------------+
#     | wage                     | The hourly rate of an employee.                              |
#     +--------------------------+--------------------------------------------------------------+
#     | active                   | Determines if a user can log into Limble or not.             |
#     +--------------------------+--------------------------------------------------------------+
#     | emailNotificationActive  | Determines if a User gets Email Notifications From Limble.   |
#     +--------------------------+--------------------------------------------------------------+
#     | pushNotificationActive   | Determines if a User gets Push Notifications From Limble.    |
#     +--------------------------+--------------------------------------------------------------+
#     | workdayHours             | The number of hours a day this employee works.               |
#     +--------------------------+--------------------------------------------------------------+
#     | dateAdded                | The date a user was added to Limble. This is a unix timestamp.|
#     +--------------------------+--------------------------------------------------------------+
#     | teams                    | What Teams a User has at specific Locations.                 |
#     +--------------------------+--------------------------------------------------------------+
#
#
# #
# # '''
# # Property:                     Description
# # username:                     What a User uses to login.
# # wage:                         The hourly rate of an employee.
# # active:                       Determines if a user can log into Limble or not.
# # emailNotificationActive:      Determines if a User gets Email Notifications From Limble.
# # pushNotificationActive:       Determines if a User gets Push Notifications From Limble.
# # workdayHours:                 The number of hours a day this employee works.
# # dateAdded:                    The date a user was added to Limble. This is a unix timestamp.
# # teams:                        What Teams a User has at specific Locations.
# # '''


def clean_docs(intext):
    # todo: finish this up
    line_count = 0
    params = {}
    def_bits = []
    for line in intext.splitlines():
        print(f'{line_count=}')
        stripped = line.strip()
        if len(stripped):
            if any([line_count == 0, line_count == 2]):
                print(f'{line_count=}: {stripped}')
                def_bits.append(stripped)

            if len(def_bits) == 2:
                params[def_bits[0]] = def_bits[1]
                def_bits = []
                line_count = 0
            else:
                line_count += 1
    print(params)


if __name__ == '__main__':
    pass
