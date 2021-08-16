from tests.common.common_methods import *
from tests.common.constants import *
from tests.common.global_fixtures import *
import os


class TestGetShorLinks:

    header = os.environ['TOKEN']

    def test_create_shorlink_should_yield_201(self):
        # create a shortlink and verify the details of the same
        sl = "ajaytestautomation11"
        des = "test automation using python requests"
        url = "https://en.wikipedgia.org/wiki/Enigma_machine"

        create_sl_response = request_method(POST, url=base_url,
                                            headers={
                                                "Authorization": self.header},
                                            json=operations('create', sl=sl, des=des, url=url)
                                            )

        # retrieving the above created SL to ensure the create operation is successful
        retrieve_sl_response = request_method(POST, url=base_url,
                                              headers={
                                                  "Authorization": self.header},
                                              json=operations('get_SL', sk=sl))

        # convering the retrieve sl response to json
        retrieve_sl_response_json = retrieve_sl_response.json()

        # deleting the above created SL
        pk = retrieve_sl_response_json['data']['getShortcut']['pk']
        uid = retrieve_sl_response_json['data']['getShortcut']['uid']
        del_res = request_method(POST, url=base_url, headers={"Authorization": self.header},
                                 json=operations('delete', sk=sl, pk=pk, uid=uid))

        assert retrieve_sl_response_json['data']['getShortcut']['shortlink'] == 'o/' + sl
        assert retrieve_sl_response_json['data']['getShortcut']['url'] == url
        assert retrieve_sl_response_json['data']['getShortcut']['description'] == des and success_assertion(
            "Shortlink creation successful"), "shorlink creation failed"
        assert create_sl_response.status_code == 201 and success_assertion("appropriate status code"), \
            "inappropriate status code"

    def test_create_shortlink_url_field_without_entering_the_extension_name(self):
        sl = "ajaytestautomation11"
        des = "test automation using python requests"
        url = "https://en.wikipedgia"
        create_sl_response = request_method(POST, url=base_url,
                                            headers={
                                                "Authorization": self.header},
                                            json=operations('create')
                                            ).json()
        print(create_sl_response)
        assert create_sl_response['errors'][0]['message'] == URL_VALIDATION and success_assertion(
            "appropriate error validation"), 'invalid error validation'

    def test_the_URL_field_by_entering_only_extension(self):
        sl = "ajaytestautomation11"
        des = "test automation using python requests"
        url = "https://en.in"
        create_sl_response = request_method(POST, url=base_url,
                                            headers={
                                                "Authorization": self.header},
                                            json=operations('create')
                                            ).json()
        print(create_sl_response)
        assert create_sl_response['errors'][0]['message'] == URL_VALIDATION and success_assertion(
            "appropriate error validation"), 'invalid error validation'

    def test_the_shortlink_field_validation_by_having_it_empty(self):
        sl = ""
        des = "test automation using python requests"
        url = "https://en.org.in"
        create_sl_response = request_method(POST, url=base_url,
                                            headers={
                                                "Authorization": self.header},
                                            json=operations('create')
                                            ).json()
        print(create_sl_response)
        assert create_sl_response['errors'][0]['message'] == URL_VALIDATION and success_assertion(
            "appropriate error validation"), 'invalid error validation'
