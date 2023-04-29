

# ### Passo a passo:
#
#    **Passo 1** - Importar os módulos e bibliotecas.
#
#    **Passo 2** - Pegar dados do Ibovespa e do Dólar no Yahoo Finance.
#
#    **Passo 3** - Manipular os dados para deixá-los nos formatos necessários para fazer as contas.
#
#    **Passo 4** - Calcular o retorno diário, mensal e anual.
#
#    **Passo 5** - Localizar, dentro das tabelas de retornos, os valores de fechamento de mercado que irão pro texto  anexado no e-mail.
#
#    **Passo 6** - Fazer os gráficos dos ativos.
#
#    **Passo 7** - Enviar o e-mail.

# # 1: - Importando os módulos necessários.


import os  # gerenciamento de locais
from dotenv import load_dotenv
import pandas as pd
import datetime  # manipula as datas
import yfinance as yf  # busca os dados dentro do site da Yahoo Finance
from matplotlib import pyplot as plt  # plota o Gráfico
import mplcyberpunk  # edita o Gráfico
import smtplib  # email
from email.message import EmailMessage  # email
from datetime import datetime, timedelta


# # 2: - Pegando dados no Yahoo Finance.

ativos = ["^BVSP", "BRL=X"]
hoje = datetime.now()
um_ano_atras = hoje - timedelta(days=365)
dados_mercado = yf.download(ativos, um_ano_atras, hoje)


print(dados_mercado)


# # Passo 3.1: Manipulando os dados - seleção e exclusão de dados.


dados_fechamento = dados_mercado['Adj Close']
dados_fechamento.columns = ['dolar', 'ibovespa']

dados_fechamento = dados_fechamento.dropna()

dados_fechamento


# # Passo 3.2: Manipulando os dados - Criando tabelas com outros timeframes

dados_fechamento_mensal = dados_fechamento.resample("M").last()
dados_fechamento_anual = dados_fechamento.resample("Y").last()
dados_fechamento_anual


# # Passo 4: - Calcular fechamento do dia, retorno no ano e retorno no mês dos ativos.

retorno_no_ano = dados_fechamento_anual.pct_change().dropna()
retorno_no_mes = dados_fechamento_mensal.pct_change().dropna()
retorno_no_dia = dados_fechamento.pct_change().dropna()
retorno_no_mes


# # Passo 5: - Localizar o fechamento do dia anterior, retorno no mês e retorno no ano.
#  - loc -> referenciar elementos a partir do nome
#  + iloc -> selecionar elementos como uma matriz

retorno_dia_dolar = retorno_no_dia.iloc[-1, 0]
retorno_dia_ibovespa = retorno_no_dia.iloc[-1, 1]

retorno_mes_dolar = retorno_no_mes.iloc[-1, 0]
retorno_mes_ibovespa = retorno_no_mes.iloc[-1, 1]

retorno_ano_dolar = retorno_no_ano.iloc[-1, 0]
retorno_ano_ibovespa = retorno_no_ano.iloc[-1, 1]


retorno_dia_dolar = round(retorno_dia_dolar * 100, 2)
retorno_dia_ibovespa = round(retorno_dia_ibovespa * 100, 2)

retorno_mes_dolar = round(retorno_mes_dolar * 100, 2)
retorno_mes_ibovespa = round(retorno_mes_ibovespa * 100, 2)

retorno_ano_dolar = round(retorno_ano_dolar * 100, 2)
retorno_ano_ibovespa = round(retorno_ano_ibovespa * 100, 2)


# # Passo 6: - Fazer os gráficos da performance do último dos ativos


plt.style.use("cyberpunk")

dados_fechamento.plot(y='dolar', use_index=True, legend=False)

plt.title("Dólar")

plt.savefig('dolar.png', dpi=300)


plt.style.use("cyberpunk")

dados_fechamento.plot(y='ibovespa', use_index=True, legend=False)

plt.title("Ibovespa")

plt.savefig('ibovespa.png', dpi=300)


# # Passo 7: Enviar e-mail
# ##### https://myaccount.google.com/apppasswords

'''para não correr o risco de compartilhar seus dados sensíveis com terceiros, abra um bloco de notas e 
coloque seus dados: senha=suasenha 
                    email=seuemail@.com 
e salve como arquivo .venv.
Obs: é importante que o bloco de notas esteja dentro da pasta onde está sendo criado do código
'''


load_dotenv()


senha = os.environ.get("senha")
email = os.environ.get("email")
meu_email = os.environ.get("meu_email")


msg = EmailMessage()
msg['subject'] = "Enviando email com o Python"
msg['From'] = email
msg['To'] = meu_email


msg.set_content(f'''Prezado diretor. segue o relatório diário:


Bolsa:

No ano o Ibovespa está tendo uma rentabilidade de {retorno_ano_ibovespa}%, 
enquanto no mês a rentabilidade é de {retorno_mes_ibovespa}%.

No último dia útil, o fechamento do Ibovespa foi de {retorno_dia_ibovespa}%.

Dólar:

No ano o Dólar está tendo uma rentabilidade de {retorno_ano_dolar}%, 
enquanto no mês a rentabilidade é de {retorno_mes_dolar}%.

No último dia útil, o fechamento do Dólar foi de {retorno_dia_dolar}%.


Abs,

Seu colaborador




'''

                )


with open('dolar.png', 'rb') as content_file:  # abre o arquivo
    content = content_file.read()  # pega o conteudo do arquivo
    # anexa como imagem no email
    msg.add_attachment(content, maintype='application',
                       subtype='png', filename='dolar.png')


with open('ibovespa.png', 'rb') as content_file:
    content = content_file.read()
    msg.add_attachment(content, maintype='application',
                       subtype='png', filename='ibovespa.png')


with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:

    smtp.login(email, senha)
    smtp.send_message(msg)
