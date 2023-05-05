from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import requests
import fastapi
import uvicorn


def get_appointments(service: str):
    URL = "https://service.berlin.de/dienstleistungen/"

    options = Options()
    options.headless = True
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280x1024")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--remote-debugging-port=9222")
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(URL)

        # navigate to a with 'Personalausweis beantragen'
        driver.find_element(By.LINK_TEXT, service).click()
        time.sleep(1)

        # navigate to a with 'Termin berlinweit suchen'
        driver.find_element(By.LINK_TEXT, "Termin berlinweit suchen").click()
        time.sleep(1)

        # find all td elements with class 'buchbar'
        cells = driver.find_elements(By.CSS_SELECTOR, "td.buchbar")

        days = []
        for cell in cells:
            a = cell.find_element(By.TAG_NAME, "a")
            try:
                a = cell.find_element(By.TAG_NAME, "a")
                days.append(a.get_attribute("title").split(" -")[0])
            except:
                days.append(cell.text)

        message = ""
        if len(days) > 0:
            message = f"""
            @everyone
            Appointments on:
            {", ".join(days)}

            https://service.berlin.de/dienstleistungen/#dl_P
            """
    except Exception as e:
        message = f"Error: {e}"

    driver.quit()

    return message


app = fastapi.FastAPI()


@app.get("/")
def root():
    message = get_appointments(service="Personalausweis beantragen")
    return {"message": message}


@app.post("/appointments")
def appointments(service: str, discord_webhook: str, report_failed: bool):
    message = get_appointments(service)
    if discord_webhook:
        if message:
            requests.post(discord_webhook, json={"content": message})
        elif report_failed:
            requests.post(discord_webhook, json={"content": "No appointments found"})
    return {"message": message}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)