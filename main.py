import requests
from bs4 import BeautifulSoup
from typing import List
import time
from dotenv import load_dotenv
import os
import resend


load_dotenv()
resend.api_key = os.getenv("RESEND_API_KEY")


def get_url(serviceId: str, locationId: str) -> str:
    URL = f"https://service.berlin.de/terminvereinbarung/termin/tag.php?termin=1&anliegen[]={serviceId}&dienstleisterlist=122210,122217,327316,122219,327312,122227,327314,122231,327346,122238,122243,327348,122254,331011,349977,122252,329742,122260,329745,122262,329748,122271,327278,122273,327274,122277,327276,330436,122280,327294,122282,327290,122284,327292,122291,327270,122285,327266,122286,327264,122296,327268,150230,329760,122301,327282,122297,327286,122294,327284,122312,329763,122314,329775,122304,327330,122311,327334,122309,327332,317869,122281,327352,122279,329772,122283,122276,327324,122274,327326,122267,329766,122246,327318,122251,327320,327653,122257,327322,122208,327298,122226,327300"
    if locationId:
        URL = f"https://service.berlin.de/terminvereinbarung/termin/tag.php?termin=1&dienstleister={locationId}&anliegen[]={serviceId}"
    return URL


def get_appointments(url: str) -> List[str]:
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    cells = soup.find_all("td", class_="buchbar")
    if not cells:
        return []

    dates = [cell.find("a").get("title").split(" ")[0] for cell in cells]

    return dates


def get_message(url: str, discord: bool) -> str:
    try:
        dates = get_appointments(url)
        if dates:
            dateString = "\n- ".join(dates)
            if discord:
                return f"@everyone **New appointments available:**\n- {dateString}\n\n{url}"
            else:
                return f"New appointments available:\n- {dateString}\n\n{url}"
        return ""
    except Exception as e:
        return f"Something went wrong: {e}"


def send_discord_message(message: str):
    requests.post(os.getenv("DISCORD_WEBHOOK"), json={"content": message})


def send_email(message: str):
    params: resend.Emails.SendParams = {
        "from": f"Bürgeramt Appointments <{os.getenv('RESEND_SENDER')}>",
        "to": os.getenv("RESEND_RECIPIENTS").split(","),
        "subject": "New Appointments Report",
        "html": f"<p>{message}</p>",
    }
    resend.Emails.send(params)


if __name__ == "__main__":
    while True:
        print("Checking for appointments...", flush=True)
        url = get_url(os.getenv("SERVICE_ID"), os.getenv("LOCATION_ID"))
        msg = get_message(url, os.getenv("RESEND_API_KEY") == None)
        if msg:
            print("Found appointments!", flush=True)
            if os.getenv("RESEND_API_KEY"):
                send_email(msg)
            else:
                send_discord_message(msg)
            print("Sent message", flush=True)
        elif (
            os.getenv("REPORT_FAILED") == "true" or os.getenv("REPORT_FAILED") == "True"
        ):
            print("No appointments found")
            if os.getenv("RESEND_API_KEY"):
                send_email("No appointments found", flush=True)
            else:
                send_discord_message("No appointments found")
        print("Sleeping...", flush=True)
        time.sleep(
            int(os.getenv("INTERVAL")) if os.getenv("INTERVAL") else 60 * 3
        )  # every 3 minutes or env
