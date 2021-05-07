import json
from datetime import datetime
from data_service.views.affiliates import AffiliatesView
from data_service.store.affiliates import Affiliates
from data_service.utils.utils import create_id
from .. import test_app
from pytest import raises
from pytest_mock import mocker

class AffiliateQueryMock:
    affiliate_instance = Affiliates()

    def __init__(self):
        pass

    def fetch(self) -> list:
        return [self.affiliate_instance]


affiliate_data_mock: dict = {
    "uid": create_id(),
    "affiliate_id": create_id(),
    "last_updated": datetime.now(),
    "total_recruits": 0,
    "is_active": True,
    "is_deleted": False
}


# noinspection PyShadowingNames
def test_register_affiliate(mocker):

    mocker.patch('google.cloud.ndb.Model.put', return_value=create_id())
    mocker.patch('google.cloud.ndb.Model.query', return_value=AffiliateQueryMock())
    mocker.patch('data_service.store.affiliates.AffiliatesValidators.user_already_registered', return_value=False)

    with test_app().app_context():
        affiliates_view_instance = AffiliatesView()
        response, status = affiliates_view_instance.register_affiliate(affiliate_data=affiliate_data_mock)
        print("status: {}".format(status))
        response_dict: dict = response.get_json()
        assert status == 200, response_dict['message']
        affiliate_data_mock['uid'] = ""
        # print(affiliate_data_mock)
        response, status = affiliates_view_instance.register_affiliate(affiliate_data=affiliate_data_mock)
        print("status: {}".format(status))
        assert status != 200, "registering affiliate without uid"

def test_increment_total_recruits():
    pass

def test_delete_affiliate():
    pass

def test_mark_active():
    pass

def test_get_affiliate():
    pass

def test_get_all_affiliate():
    pass

def get_active_affiliates():
    pass

def get_inactive_affiliates():
    pass

def get_deleted_affiliates():
    pass


