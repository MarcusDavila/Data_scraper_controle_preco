import schedule
import time
from monitor import monitor

schedule.every(30).minutes.do(monitor)

print("Monitor de preços iniciado. Pressione Ctrl+C para parar.")
while True:
    schedule.run_pending()
    time.sleep(1)