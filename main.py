import argparse

from sqlalchemy.orm import Session

import requests

from connect import engine

from models import Activity

from parser_validators import CommandValidator, TypeValidator, ParticipantsValidator, \
    PriceValidator, AccessibilityValidator

BASE_URL = "http://www.boredapi.com/api/activity/"


def parse_arguments_to_the_console() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="A program that generates a new activity based on some criteria "
                                                 "or lists all the possible types of activities")

    parser.add_argument("command", help="The command to execute, must be either 'new' or 'list'",
                        action=CommandValidator)
    parser.add_argument("--type", help="The type of activity", action=TypeValidator)
    parser.add_argument("--participants", type=int, help="The number of participants for the activity, "
                                                         "must be a positive integer",
                        action=ParticipantsValidator)
    parser.add_argument("--price_min", type=float, help="The minimum price for the activity, "
                                                        "must be a number between 0 and 1",
                        action=PriceValidator)
    parser.add_argument("--price_max", type=float, help="The maximum price for the activity, "
                                                        "must be a number between 0 and 1",
                        action=PriceValidator)
    parser.add_argument("--accessibility_min", type=float, help="The minimum accessibility for the activity, "
                                                                "must be between 0 and 1",
                        action=AccessibilityValidator)
    parser.add_argument("--accessibility_max", type=float, help="The maximum accessibility for the activity, "
                                                                "must be between 0 and 1",
                        action=AccessibilityValidator)
    return parser.parse_args()


def perform_api_call(args: argparse.Namespace) -> dict:
    params = {
        "type": args.type,
        "participants": args.participants,
        "minprice": args.price_min,
        "maxprice": args.price_max,
        "minaccessibility": args.accessibility_min,
        "maxaccessibility": args.accessibility_max
    }
    return requests.get(BASE_URL, params=params).json()


def save_activity_to_the_db(response: dict) -> None:
    session = Session(bind=engine)
    try:
        activity = Activity(
            name=response["activity"],
            type=response["type"],
            participants=response["participants"],
            price=response["price"],
            accessibility=response["accessibility"],
            link=response["link"],
            key=response["key"]
        )
    except KeyError:
        print(response["error"])
        exit()

    session.add(activity)
    session.commit()


def print_the_activity_information(response: dict) -> None:
    print(f"Activity: {response['activity']}")
    print(f"Type: {response['type']}")
    print(f"Participants: {response['participants']}")
    print(f"Price: {response['price']}")
    print(f"Accessibility: {response['accessibility']}")
    print(f"Link: {response['link']}")


def print_last_activities() -> None:
    print(Activity.get_last_activities(5))


def main() -> None:
    args: argparse.Namespace = parse_arguments_to_the_console()
    if args.command == "new":
        response: dict = perform_api_call(args)
        save_activity_to_the_db(response)
        print_the_activity_information(response)
    else:
        print_last_activities()


if __name__ == "__main__":
    main()
