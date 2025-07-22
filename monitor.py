import requests
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook
from dotenv import load_dotenv
import os
import json

load_dotenv()

PRODUCT_URL = os.getenv("PRODUCT_URL")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
HEADERS = json.loads(os.getenv("HEADERS"))
LAST_PRICE_FILE = "last_price.txt"

def get_price():
    response = requests.get(PRODUCT_URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    
    price_tag = soup.select_one("#tp_price_block_total_price_ww .a-offscreen")

    if price_tag:
        price_text = price_tag.text.strip().replace("R$", "").replace(".", "").replace(",", ".")
        price_value = float(price_text)
        print(f"Preço encontrado: R$ {price_value:.2f}")
        return price_value
    else:
        print("Preço não encontrado.")
        raise Exception("Não foi possível encontrar o preço na página.")

def get_last_price():
    try:
        with open(LAST_PRICE_FILE, "r") as file:
            return float(file.read())
    except:
        return None

def save_price(price):
    with open(LAST_PRICE_FILE, "w") as file:
        file.write(str(price))

def send_discord_alert(old_price, new_price):
    content = (
        f"🛒 O preço do produto mudou!\n"
        f"💰 Valor anterior: R$ {old_price:.2f}\n"
        f"🔻 Novo valor: R$ {new_price:.2f}\n"
        f"🔗 [Ver produto]({PRODUCT_URL})"
    )

    webhook = DiscordWebhook(url=DISCORD_WEBHOOK_URL, content=content)
    webhook.execute()

def monitor():
    try:
        current_price = get_price()
        last_price = get_last_price()

        if last_price is None:
            save_price(current_price)
        elif current_price != last_price:
            send_discord_alert(last_price, current_price)
            save_price(current_price)
        else:
            print("Sem alterações de preço.")
    except Exception as e:
        print(f"Erro ao monitorar: {e}")