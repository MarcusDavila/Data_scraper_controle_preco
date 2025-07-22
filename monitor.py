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
    response = requests.get(PRODUCT_URL, headers=HEADERS, timeout=15)
    if response.status_code != 200:
        raise Exception(f"Erro HTTP {response.status_code} ao acessar o produto.")

    soup = BeautifulSoup(response.text, "html.parser")
    price_tag = soup.select_one("#tp_price_block_total_price_ww .a-offscreen")

    if price_tag and price_tag.text.strip():
        price_text = price_tag.text.strip().replace("R$", "").replace(".", "").replace(",", ".")
        price_value = float(price_text)
        print(f"💰 Preço encontrado: R$ {price_value:.2f}")
        return price_value
    else:
        raise Exception("❌ Não foi possível encontrar o preço na página.")

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
        f"📉 De: R$ {old_price:.2f}\n"
        f"📈 Para: R$ {new_price:.2f}\n"
        f"🔗 [Ver produto]({PRODUCT_URL})"
    )

    webhook = DiscordWebhook(url=DISCORD_WEBHOOK_URL, content=content)
    response = webhook.execute()
    if response.status_code == 200:
        print("✅ Alerta enviado ao Discord.")
    else:
        print(f"⚠️ Erro ao enviar alerta Discord: {response.status_code}")

def monitor():
    try:
        current_price = get_price()
        last_price = get_last_price()

        if last_price is None:
            save_price(current_price)
            print("💾 Preço inicial salvo.")
        elif current_price != last_price:
            send_discord_alert(last_price, current_price)
            save_price(current_price)
        else:
            print("ℹ️ Sem alterações de preço.")
    except Exception as e:
        print(f"❌ Erro ao monitorar: {e}")

if __name__ == "__main__":
    monitor()
