import schedule
import time
from monitor import monitor

print("📦 Iniciando monitor de preços com schedule...")

# Agenda a função para rodar a cada 30 minutos
schedule.every(30).minutes.do(monitor)

# Executa imediatamente na inicialização (opcional) 
monitor()

# Loop principal
try:
    while True:
        schedule.run_pending()
        time.sleep(1)
except KeyboardInterrupt:
    print("🛑 Execução interrompida pelo usuário.")
except Exception as e:
    print(f"⚠️ Erro inesperado: {e}")