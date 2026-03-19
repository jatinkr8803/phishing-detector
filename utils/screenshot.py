from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def take_screenshot(url, output="screenshot.png"):

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=options)

    driver.get(url)

    driver.save_screenshot(output)

    driver.quit()

    return output


'''if __name__ == "__main__":
    url = "https://google.com"
    path = take_screenshot(url)

    print("Screenshot saved:", path)'''