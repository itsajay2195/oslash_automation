import requests
import time
import random


def request_method(method, url, headers=None, params=None, json=None, _print=True):
    """ Constructs and sends a :class:`Request <Request>
    :param method: GET, POST, PATCH, DELETE, PUT
    :param url: required API endpoint. "staff/" or "tickets/"
    :param headers: to be passed if need to use a specific auth_token
    :param params: params to be passed as dict
    :param json: query in json
    :return: response in Json
    """

    # data is None condition is to handle 500 error due to data=None passed to certain endpoints.
    response = requests.request(method, url, json=json, headers=headers, params=params)
    if _print:
        print(response.content)
    return response


def success_assertion(msg='assert OK'):
    print(msg)
    return True


def return_error_details_if_error(response_code, url, data):
    if response_code not in [200, 201, 202, 204]:
        print(url)
        if data is not None:
            print(data)


# https://en.wikipedia.org/wiki/Enigma_machine

def operations(i, limit=15, sk=None, sl=None, des=None, url=None, pk=None, uid=None):
    switcher = {
        'get_SL': {
            "query": "query GetShortcut($sk: String!) {\n  getShortcut(sk: $sk) {\n    creator\n    creatorDetails {"
                     "\n      pk\n      sk\n      profileImageUrl\n      fName\n      lName\n      createdAt\n      "
                     "email\n    }\n    description\n    pk\n    shortlink\n    sk\n    url\n    uid\n    "
                     "sharedWith\n    createdAt\n    thisMonthAnalytics {\n      dates {\n        date\n        "
                     "dateValue\n      }\n    }\n    lastMonthAnalytics {\n  dates {\n  date\n  dateValue\n  }\n  "
                     "}\n  _version\n  }\n}\n", "variables": {"sk": "LINK#o/" + str(sk)}},
        'get_All': {
            "query": "query QueryShortcuts($query: String!, $suggestions: Boolean, $filter: ShortcutQueryInput, "
                     "$limit: Int, $offset: Int, $sort: ShortcutQuerySort) {\n  queryShortcuts(query: $query, "
                     "suggestions: $suggestions, filter: $filter, limit: $limit, offset: $offset, sort: $sort) "
                     "{\n    items {\n           sk\n      uid\n      creator\n      creatorDetails {\n        "
                     "pk\n        sk\n        profileImageUrl\n        fName\n        lName\n      }\n          "
                     "  description\n      shortlink\n      url\n      \n      \n                  createdAt\n  "
                     "    _version\n    }\n    total\n    nextOffset\n  }\n}\n", "variables": {"limit": limit,
                                                                                               "query": "",
                                                                                               "filter": {
                                                                                                   "isPublic": True},
                                                                                               "sort": {}}},

        'create': {"query": "mutation CreateShortcut($input: CreateShortcutInput!) {\n  createShortcut(input: $input) {"
                            "\n    description\n    pk\n    shortlink\n    sk\n    url\n    uid\n    collectionId\n    "
                            "creator\n    collection {\n      uid\n      name\n      shortlink\n    }\n  }\n}\n",
                   "variables": {"input": {"shortlink": "o/" + str(sl), "description": str(des),
                                           "url": str(url), "_version": 0}}},

        'delete': {"query": "mutation DeleteShortcut($input: DeleteShortcutInput!, $pk: String!, $sk: String!, "
                            "$uid: String!) {\n  deleteShortcut(input: $input, pk: $pk, sk: $sk, uid: $uid) {\n    "
                            "pk\n "
                            "   shortlink\n    sk\n    uid\n    createdAt\n    _version\n  }\n}\n", "variables": {
            "input": {"_version": 0}, "pk": str(pk), "sk": "LINK#o/" + str(sk),
            "uid": str(uid)}},

        'edit': {
            "query": "mutation UpdateShortcutV2($input: UpdateShortcutInput!, $pk: String!, $sk: String!, "
                     "$uid: String!) {\n  updateShortcutV2(input: $input, pk: $pk, sk: $sk, uid: $uid) {\n    "
                     "creator\n        description\n    pk\n    shortlink\n    sk\n    url\n    uid\n    "
                     "collectionId\n    collection {\n      name\n      shortlink\n      pk\n      sk\n      uid\n    "
                     "  createdAt\n      _version\n    }\n    sharedWith\n    sharedGroups {\n      pk\n      sk\n    "
                     "  group {\n        sk\n        members\n        uId\n        uid\n        groupName\n        "
                     "groupSlug\n      }\n    }\n    sharedMembers {\n      pk\n      sk\n      member {\n        "
                     "pk\n        profileImageUrl\n        sk\n        uid\n        createdAt\n        email\n        "
                     "fName\n        lName\n        _version\n      }\n    }\n    createdAt\n    thisMonthAnalytics {"
                     "\n      dates {\n        date\n        dateValue\n      }\n    }\n    lastMonthAnalytics {\n    "
                     "  dates {\n        date\n        dateValue\n      }\n    }\n    _version\n  }\n}\n",
            "variables": {"input": {"description": str(des), "shortlink": "o/"+str(sl),
                                    "url": str(url), "_version": 1},
                          "pk": str(pk), "sk": "LINK#o/"+str(sk),
                          "uid": str(uid)}}
    }
    return switcher.get(i, "Invalid")


def unique_id():
    time_stamp = time.strftime('%d%H%M%S')
    rand_int = random.randint(0, 1000)
    _unique_id = (time_stamp + str(rand_int))
    return _unique_id

# {"query":"query GetCollectionShortcutDetails($sk: String!, $shortlinkSk: String!) {\n  getCollectionShortcutDetails(sk: $sk, shortlinkSk: $shortlinkSk) {\n    creator\n    creatorDetails {\n      pk\n      sk\n      profileImageUrl\n      fName\n      lName\n      createdAt\n      email\n    }\n    description\n    pk\n    shortlink\n    sk\n    url\n    uid\n    collectionId\n    createdAt\n    thisMonthAnalytics {\n      dates {\n        date\n        dateValue\n      }\n    }\n    lastMonthAnalytics {\n      dates {\n        date\n        dateValue\n      }\n    }\n    _version\n  }\n}\n","variables":{"shortlinkSk":"LINK#fggg","sk":"COLLECTION#o/my"}}
