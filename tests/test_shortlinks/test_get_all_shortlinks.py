from tests.common.common_methods import *
from tests.common.constants import *
from tests.common.global_fixtures import *
import os


class TestGetShorLinks:
    header = os.environ['TOKEN']

    def test_retrieve_all_available_sl_should_yield_http_200(self):

        # print("ENV variabel is ", $ENV_NAME)
        # creating shortlinks as desired
        sls = []
        pks = []
        uids = []
        count = 1
        for shortlink_creation in range(0, count):
            data = shorlink_creation_payload()
            create_response = request_method(POST, url=base_url,
                                             headers={
                                                 "Authorization": self.header},
                                             json=operations('create', sl=data['sl'],
                                                             des=data['des'],
                                                             url=data['url'])
                                             ).json()
            sls.append(data['sl'])
            pks.append(create_response['data']['createShortcut']['pk'])
            uids.append(create_response['data']['createShortcut']['uid'])

        # retrieve the above created SLS and validate the details
        retrieve_response = request_method(POST, url=base_url,
                                           headers={
                                               "Authorization": self.header},
                                           json=operations('get_All', limit=20)
                                           )

        # deleting the above created SLS
        for shortlink_deletion in range(0, count):
            request_method(POST, url=base_url, headers={"Authorization": self.header},
                           json=operations('delete', sk=sls[shortlink_deletion], pk=pks[shortlink_deletion],
                                           uid=uids[shortlink_deletion]))

        assert retrieve_response.status_code == 200 and success_assertion("data retrieval success")
        assert retrieve_response.json()['data']['queryShortcuts']['total'] == count and success_assertion(
            "total available shortlinks count is valid")

    def test_retrieve_short_link_yield_200(self):
        # create a shortlink and verify the details of the same
        sl = "ajaytestautomation11"
        des = "test automation using python requests"
        url = "https://en.wikipedgia.org/wiki/Enigma_machine"

        create_sl_response = request_method(POST, url=base_url,
                                            headers={
                                                "Authorization": self.header},
                                            json=operations('create', sl=sl, des=des, url=url)
                                            )

        # retrieve above created shortlink and validate the same
        retrieve_sl_response = request_method(POST, url=base_url,
                                              headers={
                                                  "Authorization": self.header},
                                              json=operations('get_SL', sk=sl)
                                              )
        retrieve_sl_response_json = retrieve_sl_response.json()
        # deleting the above created SL
        pk = retrieve_sl_response_json['data']['getShortcut']['pk']
        uid = retrieve_sl_response_json['data']['getShortcut']['uid']
        del_res = request_method(POST, url=base_url, headers={"Authorization": self.header},
                                 json=operations('delete', sk=sl, pk=pk, uid=uid))

        assert retrieve_sl_response.status_code == 200 and success_assertion("short link retrieval success")
        assert retrieve_sl_response_json['data']['getShortcut']['shortlink'] == "o/" + sl and success_assertion(
            "appropriate short link retrieved")
        assert retrieve_sl_response_json['data']['getShortcut']['url'] == url and success_assertion(
            "appropriate short link url ")

    def test_retrieve_invalid_short_link_yield_404(self):
        retrieve_response = request_method(POST, url=base_url,
                                           headers={
                                               "Authorization": self.header},
                                           json=operations('get_SL', sk='ok323')
                                           )

        assert retrieve_response.json()['errors'][0]['message'] == SL_DOES_NOT_EXIST and \
               success_assertion("appropriate validation message")
        assert retrieve_response.status_code == 404 and success_assertion("short link retrieval success"), \
            'Inappropriate status code'

    def test_retrieve_short_link_with_invalid_token_should_yield_401(self):
        retrieve_response = request_method(POST, url=base_url,
                                           headers={
                                               "Authorization": 'invalid'},
                                           json=operations('get_SL', sk='ok323')
                                           )

        assert retrieve_response.json()['errors'][0]['errorType'] == AUTH_ERROR and \
               success_assertion("appropriate errorType message")

        assert retrieve_response.json()['errors'][0]['message'] == AUTH_ERROR_MESSAGE and \
               success_assertion("appropriate validation message")

    def test_retrieve_short_link_and_validate_its_details(self):
        # create a shortlink and verify the details of the same
        sl = "ajaytestautomation11"
        des = "test automation using python requests"
        url = "https://en.wikipedgia.org/wiki/Enigma_machine"

        create_sl_response = request_method(POST, url=base_url,
                                            headers={
                                                "Authorization": self.header},
                                            json=operations('create', sl=sl, des=des, url=url)
                                            )
        # retrieve a the above created SL and asserts the details of the same
        retrieve_sl_response = request_method(POST, url=base_url,
                                              headers={
                                                  "Authorization": self.header},
                                              json=operations('get_SL', sk=sl)
                                              ).json()

        # deleting the above created SL
        pk = retrieve_sl_response['data']['getShortcut']['pk']
        uid = retrieve_sl_response['data']['getShortcut']['uid']
        del_res = request_method(POST, url=base_url, headers={"Authorization": self.header},
                                 json=operations('delete', sk=sl, pk=pk, uid=uid))

        assert retrieve_sl_response['data']['getShortcut']['url'] == url
        assert retrieve_sl_response['data']['getShortcut']['description'] == des
