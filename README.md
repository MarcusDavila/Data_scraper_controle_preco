# 📦 Monitor de Preços com Notificações via Discord

Este projeto é um web scraper desenvolvido em Python que monitora o preço de um produto em um site específico. Sempre que houver alteração no valor, uma mensagem automática é enviada para um canal do Discord, notificando a mudança.

## 🔍 Objetivo

Automatizar o acompanhamento de preços de um produto específico em tempo real, útil para promoções, quedas de preço ou monitoramento de flutuações.

## 🚀 Funcionalidades

- ✅ Rastreia o valor de um produto em um site (ex: Kabum, Amazon, etc.)
- ✅ Detecta mudanças no valor
- ✅ Envia mensagens de alerta para um canal do Discord via webhook
- ✅ Pode ser executado de forma agendada (cron, scheduler ou Lambda)

## 🛠️ Tecnologias utilizadas

- Python 3.11+
- requests
- BeautifulSoup
- discord-webhook
- schedule (opcional, para execução periódica)
- dotenv (para variáveis sensíveis)

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

## 🧠 Como funciona

1. O scraper acessa a URL do produto usando requests.
2. Com o BeautifulSoup, ele extrai o preço atual da página.
3. O preço atual é comparado com o último valor salvo.
4. Se houver diferença, uma mensagem é enviada ao Discord e o novo valor é salvo.

## 💬 Exemplo de mensagem no Discord

> 🛒 O preço do produto **Cadeira Gamer X** mudou!  
> 💰 Valor anterior: R$ 1.299,00  
> 🔻 Novo valor: R$ 1.099,00  
> 🔗 [Ver produto](https://www.site.com/produto-desejado)

## ⏰ Agendamento

Você pode configurar o script para rodar em intervalos usando:
- schedule (rodando localmente)
- cron no Linux
- AWS Lambda + EventBridge (para execução em nuvem)

## 🙋‍♂️ Autor

Desenvolvido por Marcus D'Avila (https://github.com/MarcusDavila)  
Contribuições, sugestões e feedbacks são bem-vindos!
