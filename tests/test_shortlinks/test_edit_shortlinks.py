from tests.common.common_methods import *
from tests.common.constants import *
import os


class TestGetShorLinks:
    header = os.environ['TOKEN']

    def test_edit_shorlink_with_valid_data(self):
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
        retrieve_sl_response_json = retrieve_sl_response.json()

        # editing the above created SL
        pk = retrieve_sl_response_json['data']['getShortcut']['pk']
        uid = retrieve_sl_response_json['data']['getShortcut']['uid']
        sl_new = 'editedviaautomation'
        edit_sl_response = request_method(POST, url=base_url,
                                          headers={
                                              "Authorization": self.header},
                                          json=operations('edit', sl=sl_new, des='edited description', url=url, sk=sl,
                                                          pk=pk, uid=uid)
                                          )

        # retrieving the above edited SL to ensure the edit operation is successful
        retrieve_edited_sl_response = request_method(POST, url=base_url,
                                                     headers={
                                                         "Authorization": self.header},
                                                     json=operations('get_SL', sk=sl_new))

        # deleting the above created SL

        del_res = request_method(POST, url=base_url, headers={"Authorization": self.header},
                                 json=operations('delete', sk=sl_new, pk=pk, uid=uid))

        assert retrieve_edited_sl_response.json()['data']['getShortcut'][
                   'shortlink'] == 'o/' + sl_new and success_assertion("Edit operation success")

    def test_edit_shorlink_with_invalid_shortlink_name(self):
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
        retrieve_sl_response_json = retrieve_sl_response.json()

        # editing the above created SL
        pk = retrieve_sl_response_json['data']['getShortcut']['pk']
        uid = retrieve_sl_response_json['data']['getShortcut']['uid']
        sl_new = 'editedviaAutomation'
        edit_sl_response = request_method(POST, url=base_url,
                                          headers={
                                              "Authorization": self.header},
                                          json=operations('edit', sl=sl_new, des='edited description', url=url, sk=sl,
                                                          pk=pk, uid=uid)
                                          )
        # deleting the above created SL

        del_res = request_method(POST, url=base_url, headers={"Authorization": self.header},
                                 json=operations('delete', sk=sl, pk=pk, uid=uid))

        assert edit_sl_response.json()['errors'][0][
                   'message'] == 'Please pass a valid shortlink value for shortlink' and success_assertion(
            "appropriate validation message")

    def test_validation_when_trying_to_edit_an_invalid_shortlink(self):
        # editing the above created SL
        edit_sl_response = request_method(POST, url=base_url,
                                          headers={
                                              "Authorization": self.header},
                                          json=operations('edit', sl='invalidnew',
                                                          des='edited description',
                                                          url='https://en.wikipedgia.org/wiki/Enigma_machine',
                                                          sk='invalid_old',
                                                          pk='ORG#123453453', uid='435435435434')
                                          )
        assert edit_sl_response.json()['errors'][0]['message'] == 'The shortcut does not exist' and success_assertion(
            "appropriate validation message")
