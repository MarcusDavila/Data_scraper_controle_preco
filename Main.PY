import requests
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook
from dotenv import load_dotenv
import os
import json

# Carrega variáveis de ambiente do .env
load_dotenv()

PRODUCT_URL = os.getenv("PRODUCT_URL")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
HEADERS = json.loads(os.getenv("HEADERS"))

# Arquivo para armazenar o último valor
LAST_PRICE_FILE = "last_price.txt"


def get_price():
    response = requests.get(PRODUCT_URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
   # Seletor direcionado para Amazon 
    price_tag = soup.select_one(".a-price .a-offscreen")

    if price_tag:
        price_text = price_tag.text.strip().replace("R$", "").replace(".", "").replace(",", ".")
        price_value = float(price_text)
        print(f"Preço encontrado: R$ {price_value:.2f}")
    else:
        print("Preço não encontrado.")
    
    


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
            print(f"Preço atual salvo: R$ {current_price:.2f}")
            save_price(current_price)
        elif current_price != last_price:
            print(f"Preço alterado de R$ {last_price:.2f} para R$ {current_price:.2f}")
            send_discord_alert(last_price, current_price)
            save_price(current_price)
        else:
            print("Sem alterações de preço.")
    except Exception as e:
        print(f"Erro ao monitorar: {e}")


if __name__ == "__main__":
    monitor()
