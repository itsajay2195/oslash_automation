import time

from tests.common.common_methods import *
from tests.common.constants import *
from tests.common.global_fixtures import *
import os


class TestGetShorLinks:
    # header = os.environ['TOKEN']
    header="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImpkNzFpUnY5bFNOVm9RYUFpTHRTMCJ9.eyJodHRwczovL2F1dGguZGVtYW5kd29yay5jb20vZW1haWwiOiJhamF5cWFlOTVAZ21haWwuY29tIiwiaXNzIjoiaHR0cHM6Ly9sb2dpbi5vc2xhc2guY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTE0NzE0NTEwNjc4NTY1MTM1Njc1IiwiYXVkIjpbImh0dHBzOi8vYXV0aC5kZW1hbmQud29yayIsImh0dHBzOi8vZGVtYW5kd29yay5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjI4NzAwMDg4LCJleHAiOjE2MzEyOTIwODgsImF6cCI6IjRoQ1BtdEQ1NFNadXlxS0JtdGRqSzJqNEZXcVRLbGtRIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbXX0.PHF_48RA4su14RvWgUkYAAEpQz9VG6696hmW2bH5DOi1VzQWgDZxwaDNAM-JavbR_DiaDdjp_c8sfCQ0hCdCeIlkGEOAwiq4t4BvkG1ydv2lTsnE8zWEHbEBcUzAVkUr3PuMPfuV9lffWzEZzYEfFyR5dv-DNz0JpQUX41guh-1KYv7hPTUBGjVlEaQWXzk01wBIdjGNkMjkICmIWAxZg_FiDt-BEK41Hi9doWH71HGnCHlzHqpKfQ2qL2Xj0LZMX_f_gBP964DLYQrix6V8XEPkxi6gRAwLPma2UYh01zncrXNK9hrWS-4MfcJCBkxCRbDcDreuckdflxLeyBDjUw"

    def test_retrieve_all_available_sl_should_yield_http_200(self):

        # creating number of shortlinks as desired
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
                                           json=operations('get_All', limit=count*2)
                                           )

        # deleting the above created SLS
        for shortlink_deletion in range(0, count):
            request_method(POST, url=base_url, headers={"Authorization": self.header},
                           json=operations('delete', sk=sls[shortlink_deletion], pk=pks[shortlink_deletion],
                                           uid=uids[shortlink_deletion]))

        assert retrieve_response.status_code == 200
        assert retrieve_response.json()['data']['queryShortcuts']['total'] == count and success_assertion(
            "Shortlinks retrieval successful and appropriate total is returned"), "shotrlinks retrieval failed"

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

        assert retrieve_sl_response.status_code == 200, "short link retrieval failed"
        assert retrieve_sl_response_json['data']['getShortcut']['shortlink'] == "o/" + sl
        assert retrieve_sl_response_json['data']['getShortcut']['url'] == url and success_assertion(
            "short link retrieval success"), "short link retrieval failed"

    def test_retrieve_invalid_short_link_yield_404(self):
        retrieve_response = request_method(POST, url=base_url,
                                           headers={
                                               "Authorization": self.header},
                                           json=operations('get_SL', sk='ok323')
                                           )

        assert retrieve_response.json()['errors'][0]['message'] == SL_DOES_NOT_EXIST

        assert retrieve_response.status_code == 404 and success_assertion("appropriate validation"), \
            'Inappropriate status code'

    def test_retrieve_short_link_with_invalid_token_should_yield_401(self):
        retrieve_response = request_method(POST, url=base_url,
                                           headers={
                                               "Authorization": 'invalid'},
                                           json=operations('get_SL', sk='ok323')
                                           )

        assert retrieve_response.json()['errors'][0]['errorType'] == AUTH_ERROR

        assert retrieve_response.json()['errors'][0]['message'] == AUTH_ERROR_MESSAGE and \
               success_assertion("appropriate validation messages")

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
        assert retrieve_sl_response['data']['getShortcut']['description'] == des and success_assertion(
            "shortlink retrieval successful"), 'shortlink retrieval unsuccessful'
