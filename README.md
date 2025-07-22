# 📦 Monitor de Preços com Notificações via Discord

Este projeto é um web scraper desenvolvido em Python que monitora o preço de um produto em um site específico. Sempre que houver alteração no valor, uma mensagem automática é enviada para um canal do Discord, notificando a mudança.

## 🔍 Objetivo

Automatizar o acompanhamento de preços de um produto específico em tempo real, útil para promoções, quedas de preço ou monitoramento de flutuações.

## 🚀 Funcionalidades

- ✅ Rastreia o valor de um produto em um site (ex: Kabum, Amazon, etc.)
- ✅ Detecta mudanças no valor
- ✅ Envia mensagens de alerta para um canal do Discord via webhook
- ✅ Pode ser executado em intervalo automático (schedule)

## 🛠️ Tecnologias utilizadas

- Python 3.11+
- requests
- BeautifulSoup
- discord-webhook
- schedule
- dotenv 

## 📦 Instalação

1. Clone o repositório:
   git clone https://github.com/seu-usuario/monitor-precos-discord.git
   cd monitor-precos-discord

2. Crie um ambiente virtual e ative:
   python -m venv venv
   source venv/bin/activate   # No Windows: venv\Scripts\activate

3. Instale as dependências:
   pip install -r requirements.txt

4. Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

   PRODUCT_URL=https://www.site.com/produto-desejado
   DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/xxxxxxxxxx
   HEADERS={Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36}
5.Execute o script principal:

   python main.py

## 🧠 Como funciona

1. O scraper acessa a URL do produto usando requests.
2. Com o BeautifulSoup, ele extrai o preço atual da página.
3. O preço atual é comparado com o último valor salvo.
4. Se houver diferença, uma mensagem é enviada ao Discord e o novo valor é salvo.

## 🛠 Arquivos principais

1. monitor.py`: Funções de scraping e alerta
2. main.py: Agendador de execução com `schedule`
3. .env`: Configurações sensíveis (não subir no GitHub)
4. last_price.txt`: Armazena o último preço encontrado

## ✅ Exemplo de mensagem no Discord

> 🛒 O preço do produto mudou!  
> 💰 Valor anterior: R$ 999,00  
> 🔻 Novo valor: R$ 799,00  
> 🔗 [Ver produto](https://www.amazon.com.br/dp/EXEMPLO)


## 🙋‍♂️ Autor

Desenvolvido por Marcus D'Avila (https://github.com/MarcusDavila)  
Contribuições, sugestões e feedbacks são bem-vindos!
