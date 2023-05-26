import os
import re
import ssl
from datetime import timedelta, date, datetime

import certifi
import requests
from slack import WebClient


class Holidays:
    def __init__(self):
        self.url = "https://feiertage-api.de/api/"
        self.valid_states = {
            "NATIONAL": "National holidays",
            "BW": "Baden-Württemberg",
            "BY": "Bayern",
            "BE": "Berlin",
            "BB": "Brandenburg",
            "HB": "Bremen",
            "HH": "Hamburg",
            "HE": "Hessen",
            "MV": "Mecklenburg-Vorpommern",
            "NI": "Niedersachsen",
            "NW": "Nordrhein-Westfalen",
            "RP": "Rheinland-Pfalz",
            "SL": "Saarland",
            "SN": "Sachsen",
            "ST": "Sachsen-Anhalt",
            "SH": "Schleswig-Holstein",
            "TH": "Thüringen"
        }

    def validate_state(self, state: str) -> bool | Exception:
        """Validate the given string for a valid german state

        :param state: Short name of a german state
        :return: Returns True if short name is ok, otherwise it raises an exception
        """

        if state not in self.valid_states.keys():
            raise ValueError(f"State value '{state}' is invalid. Must be one of {self.valid_states}")
        else:
            return True

    @staticmethod
    def validate_year(year: str) -> bool | Exception:
        """Validate the format of a given year

        :param year: Year to validate the format for
        :return: Returns True if format is ok, otherwise it raises an exception
        """

        if not re.match('^[0-9]{4}', year) and not re.match('^[0-9]{4}-[0-9]{2}[0-9]{2}', year):
            raise ValueError(f"Year '{year}' has wrong format. Must be either YYYY or YYYY-MM-DD:")
        else:
            return True

    def get(self, year: int | str | date = date.today(), state: str = None) -> dict:
        """Returns all holidays of a year

        :param year: Empty for current year or pass a specific year
        or date you want the holidays for (Date Format: YYYY-MM-DD)
        :param state: Empty or pass the german short form of a german Bundesland/State you want the holidays for.
        NATIONAL = Get only holidays, that are recognized in all states.
        Specific: BY = Bavaria, BW = Baden-Württemberg, NI = Lower Saxony, HH = Hamburg
        :return: Returns a dict with all holidays of the passed year/date
        """

        self.validate_year(str(year))

        state_param = ""
        if state is None:
            pass
        else:
            if self.validate_state(state.upper()):
                state_param = f"nur_land={state}"

        return requests.get(f"{self.url}?jahr={year}&{state_param}").json()


class Slack:
    def __init__(self, token: str | None = None):
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        self.client = WebClient(token=token, ssl=ssl_context)

    def post(self, channel: str = None, message: str = None):
        self.client.chat_postMessage(
            channel=channel,
            text=message
        )


if __name__ == '__main__':
    slackbot = Slack(token=os.getenv("SLACK_TOKEN", None))
    holidays = Holidays()

    next_week = date.today() + timedelta(days=3)  # TODO Change hardcoded timedelta to "next monday"

    all_holidays = holidays.get(year=next_week, state="BY")

    for name, data in all_holidays.items():
        if data["datum"] == str(next_week):  # TODO Change this so that it checks over all days of the next week for upcoming holidays
            date = datetime.strptime(data["datum"], '%Y-%m-%d').strftime('%d.%m.%y')
            if not data["hinweis"]:
                text = f"Nächster Feiertag: {name} am {date}"
            else:
                text = f"Nächster Feiertag: {name} am {data['datum']}\nHinweis: {date}"

            print(name, data["datum"], data["hinweis"])
            slackbot.post(channel=os.getenv("SLACK_CHANNEL", "holiday-test"), message=text)
