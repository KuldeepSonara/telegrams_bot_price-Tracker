import requests
from bs4 import BeautifulSoup
from telegram import Bot
from time import sleep

# --- Your details ---
BOT_TOKEN = "8071915495:AAEz5Y_G3b1u-KV22mpNqQCtz59LPRvoOQQ"
CHAT_ID = "6839144377"  # your Telegram ID

# --- Flipkart product link (your purifier) ---
URL = "https://www.flipkart.com/native-urban-company-m1-copper-needs-no-service-2-years-10-stage-purifier-8-l-ro-uv-minerals-alkaline-water/p/itm120599ceaeae4?pid=WAPHFYVWETFVH53Y"

# --- Browser headers so Flipkart doesn’t block ---
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

def get_price():
    r = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(r.text, "html.parser")

    # --- Flipkart price containers (fallback system) ---
    possible_classes = [
        "Nx9bqj CxhGGd",  # current class
        "Nx9bqj",         # fallback (partial match)
        "_30jeq3 _16Jk6d" # old class
    ]

    price_tag = None
    for cls in possible_classes:
        price_tag = soup.find("div", {"class": cls})
        if price_tag:
            break

    if price_tag:
        return int(price_tag.get_text().replace("₹", "").replace(",", "").strip())
    return None

def send_message(msg):
    bot = Bot(token=BOT_TOKEN)
    bot.send_message(chat_id=CHAT_ID, text=msg)

# ---- MAIN LOOP ----
last_price = None
send_message("🤖 Bot started! Tracking Flipkart product price...")

while True:
    try:
        price = get_price()
        print("Current price:", price)

        if price:
            if last_price is None:
                send_message(f"✅ Tracking started.\nCurrent price: ₹{price}\n{URL}")
            elif price != last_price:
                change = "decreased 🔻" if price < last_price else "increased 🔺"
                send_message(f"⚡ Price {change}!\nFrom ₹{last_price} → ₹{price}\n{URL}")
            last_price = price

    except Exception as e:
        print("Error:", e)

    sleep(3)  # check every 1 hour (3600 sec) instead of every 3 sec
