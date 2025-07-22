import requests
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook
from dotenv import load_dotenv
import os
import json
import time
import random

load_dotenv()

PRODUCT_URL = os.getenv("PRODUCT_URL")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
HEADERS = json.loads(os.getenv("HEADERS", "{}"))
LAST_PRICE_FILE = "last_price.txt"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"
]

def get_price():
    try:
        headers = HEADERS.copy()
        headers["User-Agent"] = random.choice(USER_AGENTS)
        headers["Accept-Language"] = "pt-BR,pt;q=0.9"
        headers["Accept-Encoding"] = "gzip, deflate, br"
        
        response = requests.get(
            PRODUCT_URL, 
            headers=headers, 
            timeout=15,
            cookies={"session-id": "132-9999999-9999999"}
        )
        
        if response.status_code != 200:
            if response.status_code == 500:
                print("⚠️ Erro 500: Servidor indisponível. Tentando novamente...")
                time.sleep(30)
                return get_price()
            raise Exception(f"Erro HTTP {response.status_code} ao acessar o produto")
            
        soup = BeautifulSoup(response.text, "html.parser")
        
        selectors = [
            "#tp_price_block_total_price_ww .a-offscreen",
            ".a-price-whole",
            "#priceblock_ourprice",
            "#price_inside_buybox"
        ]
        
        for selector in selectors:
            price_tag = soup.select_one(selector)
            if price_tag and price_tag.text.strip():
                price_text = price_tag.text.strip()
                price_text = price_text.replace("R$", "").replace("$", "").replace(",", ".").replace("\xa0", "")
                if "." in price_text and price_text.rfind(".") < len(price_text) - 3:
                    price_text = price_text.replace(".", "")
                price_value = float(price_text)
                print(f"💰 Preço encontrado: R$ {price_value:.2f}")
                return price_value
        
        with open("debug_page.html", "w", encoding="utf-8") as f:
            f.write(response.text)
        raise Exception("❌ Preço não encontrado. HTML salvo em debug_page.html")
            
    except Exception as e:
        raise Exception(f"Falha ao obter preço: {str(e)}")

def get_last_price():
    try:
        with open(LAST_PRICE_FILE, "r") as file:
            return float(file.read().strip())
    except (FileNotFoundError, ValueError):
        return None

def save_price(price):
    with open(LAST_PRICE_FILE, "w") as file:
        file.write(str(price))

def send_discord_alert(old_price, new_price):
    content = (
        f"🛒 **Alerta de Preço!**\n"
        f"🔗 [Ver Produto]({PRODUCT_URL})\n\n"
        f"📉 **Antigo:** R$ {old_price:.2f}\n"
        f"📈 **Novo:** R$ {new_price:.2f}\n"
        f"💸 **Diferença:** R$ {new_price - old_price:+.2f}"
    )

    webhook = DiscordWebhook(
        url=DISCORD_WEBHOOK_URL, 
        content=content,
        rate_limit_retry=True
    )
    response = webhook.execute()
    
    if response.status_code == 200:
        print("✅ Alerta enviado ao Discord.")
    else:
        print(f"⚠️ Erro ao enviar alerta (HTTP {response.status_code}): {response.text}")

# NOVA FUNÇÃO PARA ALERTA INICIAL
def send_initial_alert(price):
    content = (
        f"🔔 **Monitoramento Iniciado!**\n"
        f"🛒 Produto sendo monitorado:\n"
        f"🔗 [Clique aqui para ver o produto]({PRODUCT_URL})\n\n"
        f"💰 **Preço Atual:** R$ {price:.2f}\n"
        f"⏱️ Irei verificar mudanças a cada 5-15 minutos."
    )

    webhook = DiscordWebhook(
        url=DISCORD_WEBHOOK_URL, 
        content=content,
        rate_limit_retry=True
    )
    response = webhook.execute()
    
    if response.status_code == 200:
        print("✅ Alerta inicial enviado ao Discord.")
    else:
        print(f"⚠️ Erro ao enviar alerta inicial (HTTP {response.status_code}): {response.text}")

def monitor():
    try:
        print(f"\n🔍 Iniciando monitoramento: {PRODUCT_URL}")
        current_price = get_price()
        last_price = get_last_price()

        if last_price is None:
            save_price(current_price)
            print(f"💾 Preço inicial salvo: R$ {current_price:.2f}")
            send_initial_alert(current_price)  # ENVIA ALERTA INICIAL
        elif abs(current_price - last_price) > 0.01:
            print(f"✅ Alteração detectada! De R$ {last_price:.2f} para R$ {current_price:.2f}")
            send_discord_alert(last_price, current_price)
            save_price(current_price)
        else:
            print(f"ℹ️ Preço mantido: R$ {current_price:.2f}")
            
    except Exception as e:
        print(f"❌ Erro crítico: {str(e)}")
        error_webhook = DiscordWebhook(
            url=DISCORD_WEBHOOK_URL,
            content=f"🚨 **Falha no monitoramento!**\nErro: {str(e)[:200]}...\nURL: {PRODUCT_URL}"
        )
        error_webhook.execute()

if __name__ == "__main__":
    while True:
        monitor()
        sleep_time = random.randint(300, 900)
        print(f"⏳ Próxima verificação em {sleep_time//60} minutos...")
        time.sleep(sleep_time)