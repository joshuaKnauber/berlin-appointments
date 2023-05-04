from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests
import fastapi
import uvicorn


def get_appointments():
    URL = "https://service.berlin.de/dienstleistungen/"

    driver = webdriver.Chrome()
    driver.get(URL)

    # navigate to a with 'Personalausweis beantragen'
    driver.find_element(By.LINK_TEXT, "Personalausweis beantragen").click()
    time.sleep(1)

    # navigate to a with 'Termin berlinweit suchen'
    driver.find_element(By.LINK_TEXT, "Termin berlinweit suchen").click()
    time.sleep(1)

    # find all td elements with class 'buchbar'
    cells = driver.find_elements(By.CSS_SELECTOR, "td.nichtbuchbar")

    days = []
    for cell in cells:
        # get three parents up
        table = cell.find_element(By.XPATH, "..").find_element(
            By.XPATH, "..").find_element(By.XPATH, "..")
        month = table.find_element(By.CSS_SELECTOR, "th.month")
        days.append(f"{cell.text} {month.text}")

    message = ""
    if len(days) > 0:
        message = f"""
        @everyone
        Appointments on:
        {", ".join(days)}

        https://service.berlin.de/dienstleistungen/#dl_P
        """

    driver.quit()

    return message


app = fastapi.FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.post("/appointments")
def appointments():
    message = get_appointments()
    if message:
        discord_webhook = "https://discord.com/api/webhooks/1084195487848075374/dUBzfNjmQd-BA872zAMm9eaKI1GHIvE2B3G0d1mArXvlkaQyCCNvSdF4-NWD_NDvkgUC"
        requests.post(discord_webhook, json={"content": message})
    return {"message": message}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
