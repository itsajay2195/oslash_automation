""" METHOD CONSTANTS """
POST = "POST"
PATCH = "PATCH"
GET = "GET"
DELETE = "DELETE"
PUT = "PUT"

""" URL CONSTANTS """
base_url = "https://appsync-api.oslash.com/graphql"

""" ERROR CONSTANTS """
AUTH_ERROR = "UnauthorizedException"
AUTH_ERROR_MESSAGE = 'Valid authorization header not provided.'
SL_DOES_NOT_EXIST = 'Shortcut does not exist'

""" QUERY CONSTANTS """
getShortLink = {
    "query": "query GetShortcut($sk: String!) {\n  getShortcut(sk: $sk) {\n    creator\n    creatorDetails {"
             "\n      pk\n      sk\n      profileImageUrl\n      fName\n      lName\n      createdAt\n      "
             "email\n    }\n    description\n    pk\n    shortlink\n    sk\n    url\n    uid\n    "
             "sharedWith\n    createdAt\n    thisMonthAnalytics {\n      dates {\n        date\n        "
             "dateValue\n      }\n    }\n    lastMonthAnalytics {\n  dates {\n  date\n  dateValue\n  }\n  "
             "}\n  _version\n  }\n}\n", "variables": {"sk": "LINK#o/food-api"}}

getAllShortLinks = {
    "query": "query QueryShortcuts($query: String!, $suggestions: Boolean, $filter: ShortcutQueryInput, "
             "$limit: Int, $offset: Int, $sort: ShortcutQuerySort) {\n  queryShortcuts(query: $query, "
             "suggestions: $suggestions, filter: $filter, limit: $limit, offset: $offset, sort: $sort) "
             "{\n    items {\n           sk\n      uid\n      creator\n      creatorDetails {\n        "
             "pk\n        sk\n        profileImageUrl\n        fName\n        lName\n      }\n          "
             "  description\n      shortlink\n      url\n      \n      \n                  createdAt\n  "
             "    _version\n    }\n    total\n    nextOffset\n  }\n}\n", "variables": {"limit": 15,
                                                                                       "query": "",
                                                                                       "filter": {
                                                                                           "isPublic": True},
                                                                                       "sort": {}}}

createShortLink = {"query": "mutation CreateShortcut($input: CreateShortcutInput!) {\n  createShortcut(input: $input) {"
                            "\n    description\n    pk\n    shortlink\n    sk\n    url\n    uid\n    collectionId\n    "
                            "creator\n    collection {\n      uid\n      name\n      shortlink\n    }\n  }\n}\n",
                   "variables": {"input": {"shortlink": "o/enigma", "description": "test ",
                                           "url": "https://en.wikipedia.org/wiki/Enigma_machine", "_version": 0}}}


deleteShortLink ={"query":"mutation DeleteShortcut($input: DeleteShortcutInput!, $pk: String!, $sk: String!, "
                          "$uid: String!) {\n  deleteShortcut(input: $input, pk: $pk, sk: $sk, uid: $uid) {\n    pk\n "
                          "   shortlink\n    sk\n    uid\n    createdAt\n    _version\n  }\n}\n","variables":{
    "input":{"_version":0},"pk":"ORG#c359e997-48d8-49aa-a353-589d2bc057cb","sk":"LINK#o/okjkkjh",
    "uid":"6511fb4c-603d-4b42-b5bc-2e57dfec5a05"}}