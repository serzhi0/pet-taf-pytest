from playwright.sync_api import expect
from pytest import mark
from playwright import sync_api
from conftest import BASE_URL

@mark.smoke_ui
def test_window_opens(function_fixture):
    page = function_fixture
    expect(page).to_have_url('asd.com')





