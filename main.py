import requests
from bs4 import BeautifulSoup
import fastapi
import uvicorn


def get_url(serviceId: str, locationId: str) -> str:
    URL = f"https://service.berlin.de/terminvereinbarung/termin/tag.php?termin=1&anliegen[]={serviceId}&dienstleisterlist=122210,122217,327316,122219,327312,122227,327314,122231,327346,122238,122243,327348,122254,331011,349977,122252,329742,122260,329745,122262,329748,122271,327278,122273,327274,122277,327276,330436,122280,327294,122282,327290,122284,327292,122291,327270,122285,327266,122286,327264,122296,327268,150230,329760,122301,327282,122297,327286,122294,327284,122312,329763,122314,329775,122304,327330,122311,327334,122309,327332,317869,122281,327352,122279,329772,122283,122276,327324,122274,327326,122267,329766,122246,327318,122251,327320,327653,122257,327322,122208,327298,122226,327300"
    if locationId:
        URL = f"https://service.berlin.de/terminvereinbarung/termin/tag.php?termin=1&dienstleister={locationId}&anliegen[]={serviceId}"
    return URL


def get_appointments(url: str) -> list[str]:
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    cells = soup.find_all("td", class_="buchbar")
    if not cells:
        return []

    dates = [cell.find("a").get("title").split(" ")[0] for cell in cells]

    return dates


def get_discord_message(url: str) -> str:
    try:
        dates = get_appointments(url)
        if dates:
            dateString = "\n- ".join(dates)
            return f"@everyone **New appointments available:**\n- {dateString}\n\n{url}"
        return ""
    except Exception as e:
        return f"Something went wrong: {e}"


app = fastapi.FastAPI()


@app.get("/health")
def root():
    url = get_url(serviceId="324325", locationId="330132")
    msg = get_discord_message(url)
    return {"message": msg}


@app.post("/appointments")
def appointments(
    serviceId: str, locationId: str, discord_webhook: str, report_failed: bool
):
    url = get_url(serviceId, locationId)
    msg = get_discord_message(url)
    if discord_webhook:
        if msg:
            requests.post(discord_webhook, json={"content": msg})
        elif report_failed:
            requests.post(discord_webhook, json={"content": "No appointments found"})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    # url = get_url(serviceId="324325", locationId="330132")
    # msg = get_discord_message(url)
    # print(msg)
