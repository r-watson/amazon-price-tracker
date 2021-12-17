amazon_url = "https://smile.amazon.com/Qanba-Q3-PS4-01E-Obsidian-Arcade-Pearl-Joystick/dp/B08BHBHGR2/ref=sr_1_5?keywords=arcade+stick&qid=1639758720&sr=8-5"
target_price = 220.00

def scrape_amazon():
    # scrape amazon product page for html output
    import requests
    headers = {
        "Accept-Language": "en-US,en;q=0.9,vi;q=0.8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    }
    request = requests.get(amazon_url, headers=headers)
    request_html = request.text
    with open("amazon.html", mode="w", encoding="utf-8") as file:
        file.write(request_html)
    return request_html

def make_soup():
    # make soup from amazon HTML. extract price and title.
    import lxml
    from bs4 import BeautifulSoup
    with open("amazon.html", encoding="utf-8") as file:
        a_file = file.read()
    soup = BeautifulSoup(a_file, "lxml")
    price = soup.find(id="priceblock_ourprice").get_text()
    price_fpn = float(price.split("$")[1])
    product_title = soup.find(id="productTitle").get_text().strip()
    if price_fpn < target_price:
        email_alert(price_fpn, product_title)

def email_alert(price, product_title):
    import os
    from dotenv import load_dotenv
    import smtplib

    load_dotenv(r"C:\Users\watsorob\Google Drive\Programming\Python\EnvironmentVariables\.env.txt")
    mtrap_un = os.getenv("MAILTRAP_UN")
    mtrap_pw = os.getenv("MAILTRAP_PW")

    sender = "Deal Alert <dealAlert@example.com>"
    receiver = "A Test User <to@example.com>"

    message = f"""Subject: Deal Alert!\nTo: {receiver}\nFrom: {sender}\n
    {product_title}\nis now ${price}\npurchase here: {amazon_url}.""".encode('utf-8')

    with smtplib.SMTP("smtp.mailtrap.io", 587) as server:
        server.set_debuglevel(1)
        server.starttls()
        server.login(mtrap_un, mtrap_pw)
        server.sendmail(sender, receiver, message)


try:
    with open("amazon.html", encoding="utf-8") as file:
        amazon_html = file.read()
except FileNotFoundError:
    amazon_html = scrape_amazon()

make_soup()