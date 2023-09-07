import main

import pytest
from unittest import mock
from connect import engine

from sqlalchemy.orm import Session

from models import Activity

BASE_URL = "http://www.boredapi.com/api/activity/"
TEST_ACTIVITY = Activity(
    name="Learn a new programming language",
    type="education",
    participants=1,
    price=0.1,
    accessibility=0.2,
    link="",
    key=3943506
)
VALID_PARAMS = {
    "type": "education",
    "participants": 1,
    "price": 0.1,
    "accessibility": 0.2,
    "link": "",
    "key": "3943506"
}
INVALID_PARAMS = {
    "type": "invalid",
}

TEST_ERROR = {
    "error": "No activity found with the specified parameters"
}


@pytest.fixture
def mock_requests_get():
    with mock.patch("requests.get") as mocked_get:
        yield mocked_get


def test_perform_api_call(mock_requests_get):
    mock_requests_get.return_value.json.return_value = TEST_ACTIVITY

    response = mock_requests_get.ca(BASE_URL, VALID_PARAMS)
    assert response == TEST_ACTIVITY

    response = mock_requests_get(BASE_URL, INVALID_PARAMS)
    assert response == TEST_ERROR


def test_save_activity_to_the_db():
    session = Session(bind=engine)
    main.save_activity_to_the_db(TEST_ACTIVITY)

    with mock.patch('sqlalchemy.orm.Session.add') as mock_add:
        mock_add.assert_called_once()

    with mock.patch('sqlalchemy.orm.Session.commit') as mock_commit:
        mock_commit.assert_called_once()

    activity = session.add.call_args[0][0]
    assert activity.name == TEST_ACTIVITY["activity"]
    assert activity.type == TEST_ACTIVITY["type"]
    assert activity.participants == TEST_ACTIVITY["participants"]
    assert activity.price == TEST_ACTIVITY["price"]
    assert activity.accessibility == TEST_ACTIVITY["accessibility"]
    assert activity.link == TEST_ACTIVITY["link"]
    assert activity.key == TEST_ACTIVITY["key"]


def test_print_the_activity_information(capsys):
    main.print_the_activity_information(TEST_ACTIVITY)
    captured = capsys.readouterr()

    expected_output = f"Activity: {TEST_ACTIVITY['activity']}\n" \
                      f"Type: {TEST_ACTIVITY['type']}\n" \
                      f"Participants: {TEST_ACTIVITY['participants']}\n" \
                      f"Price: {TEST_ACTIVITY['price']}\n" \
                      f"Accessibility: {TEST_ACTIVITY['accessibility']}\n" \
                      f"Link: {TEST_ACTIVITY['link']}\n"
    assert captured.out == expected_output

