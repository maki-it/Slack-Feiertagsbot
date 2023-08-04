import locale
import os
import re
import ssl
from datetime import timedelta, date, datetime

import certifi
import requests
from slack import WebClient


class Holidays:
    def __init__(self):
        current_year = datetime.now().year
        self.url = "https://feiertage-api.de/api/"
        self.valid_states = {
            "NATIONAL": "Deutschland",
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
        self.seasons = [
            ('winter', (date(current_year, 1, 1), date(current_year, 3, 20))),
            ('spring', (date(current_year, 3, 21), date(current_year, 6, 20))),
            ('summer', (date(current_year, 6, 21), date(current_year, 9, 22))),
            ('autumn', (date(current_year, 9, 23), date(current_year, 12, 20))),
            ('winter', (date(current_year, 12, 21), date(current_year, 12, 31)))
        ]
        self.seasons_emojis = {
            'winter': '❄️',
            'spring': '🌱',
            'summer': '🌞',
            'autumn': '🍂'
        }
        self.emojis = {
            'Weihnachtstag': '🎅',
            'Ostermontag': '🐰',
            'Tag der Arbeit': '🛠️',
            'Christi Himmelfahrt': '✝️',
            'Tag der Deutschen Einheit': '🇩🇪',
            'Neujahrstag': '🎆',
            'Heilige Drei Könige': '👑'
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
        if not state or state.upper() == "ALL":
            pass
        else:
            if self.validate_state(state.upper()):
                state_param = f"nur_land={state}"

        return requests.get(f"{self.url}?jahr={year}&{state_param}").json()

    def get_season(self, now: date | datetime = date.today()):
        """ Get season from given date or datetime

        :param now:
        :return:
        """

        try:
            if isinstance(now, datetime):
                now = now.date()
            return next(season for season, (start, end) in self.seasons if start <= now <= end)
        except Exception as e:
            print(f"{holiday_date}", e)


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
    # Edit these lines to set the search range
    SEARCH_WEEKS = int(os.getenv("SEARCH_WEEKS", 2))
    timerange = timedelta(weeks=SEARCH_WEEKS)
    search_start = datetime.today()
    search_end = search_start.date() + timerange

    slack_token = os.getenv("SLACK_TOKEN")
    if slack_token:
        slackbot = Slack(token=slack_token)
    else:
        raise ValueError("SLACK_TOKEN is undefined")

    holidays = Holidays()
    locale.setlocale(locale.LC_TIME, 'de_DE.UTF-8')

    state = os.getenv("STATE", "ALL")
    all_holidays = holidays.get(year=search_end, state=state)
    text = ""

    if state and state != "ALL":
        for name, data in all_holidays.items():
            holiday_date = datetime.strptime(data["datum"], "%Y-%m-%d").date()
            holiday_season = holidays.get_season(holiday_date)

            if search_start.date() < holiday_date <= search_end:
                date = datetime.strptime(data["datum"], '%Y-%m-%d')
                day_name = date.strftime("%A")
                date_converted = date.strftime('%d.%m.%Y')

                if name in holidays.emojis:
                    emoji = holidays.emojis[name]
                else:
                    emoji = holidays.seasons_emojis[holiday_season]

                if not data["hinweis"]:
                    text += f"{emoji} *{name}* am {day_name}, {date_converted}\n"
                else:
                    text += f"{emoji} *{name}* am {day_name}, {date_converted}\n> _{data['hinweis']}_\n"

        if text:
            text = f"*Anstehende Feiertage der nächsten {SEARCH_WEEKS} Wochen in {holidays.valid_states[state]}:*\n{text}"
    else:
        holiday_list = all_holidays.items()
        for entry in holiday_list:
            state = entry[0]
            if state == "NATIONAL":
                continue

            for name, data in entry[1].items():
                holiday_date = datetime.strptime(data["datum"], "%Y-%m-%d").date()
                holiday_season = holidays.get_season(holiday_date)

                if search_start.date() < holiday_date <= search_end:
                    date = datetime.strptime(data["datum"], '%Y-%m-%d')
                    day_name = date.strftime("%A")
                    date_converted = date.strftime('%d.%m.%Y')

                    if name in holidays.emojis:
                        emoji = holidays.emojis[name]
                    else:
                        emoji = holidays.seasons_emojis[holiday_season]

                    text += f"{emoji} *{holidays.valid_states[state]}* | *{name}* am {day_name}, {date_converted}\n"
                    if data["hinweis"]:
                        text += f"> _{data['hinweis']}_\n"

        if text:
            text = f"*Anstehende Feiertage der nächsten {SEARCH_WEEKS} Wochen:*\n{text}"

    if text:
        print(text)
        slackbot.post(channel=os.getenv("SLACK_CHANNEL", "holiday-test"), message=text)
