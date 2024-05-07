import streamlit as st
import pandas as pd
import locale
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


# Definindo o local para o formato desejado (no caso, o Brasil)
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# FUNÇÃO PARA FORMATAR OS NÚMEROS
def format_number(x):
    if pd.notnull(x):
        return locale.currency(x, grouping=True, symbol=False)
    else:
        return x


# CONFIGURA A TELA PARA TIPO WIDE COM O INTUITO DE AMPLIAR AS TABELAS E GRÁFICOS
st.set_page_config(layout='wide')

# APLICANDO CSS PARA CENTRALIZAR TEXTOS

st.markdown("""
<style>
h1 {
    text-align: center;
}
            
p {
    font-size: 25px !important;
    font-weight: bold !important;
}

p{
    padding: 12px 24px !important;  /* Ajusta a altura e largura das abas */
}
            
</style>
""", unsafe_allow_html=True)

# CRIANDO UM TÍTULO PARA O DASHBOARD
st.title('DASHBOARD INVESTIMENTOS')

# IMPORTANDO A TABELA
df_apos_2023 = pd.read_csv('saldo_contas.csv', index_col=0)

# PREENCHENDO OS DDOS NULOS COM '0'
df_apos_2023 = df_apos_2023.fillna(0)

# FORMATANDO OS NÚMEROS
# df_apos_2023 = df_apos_2023.applymap(format_number)


# Função para formatar valores em formato de moeda brasileira
def format_as_currency_brl(value):
    """ Formata o valor para o formato de moeda brasileiro. """
    return f'R$ {value:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')


# CRIANDO OS GRÁFICOS


def grafico_pizza_distribuicao_total():

    data = df_apos_2023.loc['2024-04-15']
    renda_fixa = data.get('CDB/LCI/LCA', 0) + data.get('TESOURO DIRETO', 0) + data.get('CASHBACK', 0)
    saldo_contas = data.get('CONTAS PF', 0)
    renda_variavel = data.get('EXTERIOR', 0) + data.get('FIIS', 0) + data.get('AÇÕES', 0)

    # Criar o gráfico de pizza
    fig, ax = plt.subplots(figsize=(8, 8))
    sizes = [renda_fixa, saldo_contas, renda_variavel]
    labels = ['Renda Fixa', 'Saldo', 'Renda Variável']
    wedges, texts, autotexts = ax.pie(
        sizes, labels=labels, startangle=90, autopct='%1.1f%%', pctdistance=0.85, 
        textprops={'color': "black", 'weight': 'bold'}
    )

    # Centralizar texto do autopct dentro das fatias
    for autotext in autotexts:
        autotext.set_color('white')

  

    labels_with_values = [f'{label}: {format_as_currency_brl(size)}' for label, size in zip(labels, sizes)]
    
    plt.legend(labels_with_values, title="Categorias e Valores", loc='upper center', bbox_to_anchor=(0.2, 1.0))

    # plt.title('Distribuição dos investimentos')
    st.pyplot(plt)


def grafico_pizza_renda_variavel():

    data = df_apos_2023.loc['2024-04-15']

    # Calcular categorias agregadas
    acoes = data.get('AÇÕES', 0)
    fiis = data.get('FIIS', 0)
    exterior = data.get('EXTERIOR', 0)

    # Criar o gráfico de pizza
    fig, ax = plt.subplots(figsize=(8, 8))
    sizes = [acoes, fiis, exterior]
    labels = ['Ações', 'FIIs', 'Exterior']
    wedges, texts, autotexts = ax.pie(
        sizes, labels=labels, startangle=90, autopct='%1.1f%%', pctdistance=0.85, 
        textprops={'color': "black", 'weight': 'bold'}
    )

    # Centralizar texto do autopct dentro das fatias
    for autotext in autotexts:
        autotext.set_color('white')

    # Criar legendas com valores em formato de moeda brasileiro

    labels_with_values = [f'{label}: {format_as_currency_brl(size)}' for label, size in zip(labels, sizes)]
    plt.legend(labels_with_values, title="Categorias e Valores", loc='upper center', bbox_to_anchor=(0.2, 1.0))

    # plt.title('Distribuição investimento em renda variável')
    st.pyplot(plt)

def grafico_linha_distribuicao_total():

    fig, ax = plt.subplots(figsize=(10, 6))  # Ajustar tamanho conforme necessário
    ax.plot(df_apos_2023.index, df_apos_2023['renda_fixa'], label='Renda Fixa')
    ax.plot(df_apos_2023.index, df_apos_2023['renda_variavel'], label='Renda Variável')

    y_min = min(df_apos_2023['renda_fixa'].min(), df_apos_2023['renda_variavel'].min())
    y_max = max(df_apos_2023['renda_fixa'].max(), df_apos_2023['renda_variavel'].max())
    ax.set_ylim(float(y_min) - 100000, float(y_max) + 200000)  # Convert to float for more precision

    ax.grid(True)

    # Atualizar as labels e os valores para a legenda
    labels = ['Renda Fixa', 'Renda Variável']
    sizes = [df_apos_2023['renda_fixa'].iloc[-1], df_apos_2023['renda_variavel'].iloc[-1]]
    labels_with_values = [f'{label}: {format_as_currency_brl(size)}' for label, size in zip(labels, sizes)]
    plt.legend(labels_with_values, title="VALORES ATUAIS", loc="upper left")  
    plt.xticks(rotation=45)
    st.pyplot(plt)




def grafico_linha_evolucao():

    df_apos_2023.index = pd.to_datetime(df_apos_2023.index)

    # Your existing plotting code
    plt.figure(figsize=(15, 9))
    df_apos_2023[['TOTAL']].plot()

    plt.grid(True)

    labels = ['Total']
    sizes = [df_apos_2023['TOTAL'].iloc[-1]]
    labels_with_values = [f'{label}: {format_as_currency_brl(size)}' for label, size in zip(labels, sizes)]
    plt.legend(labels_with_values, title="Saldo atual:", loc="upper left")

    # Accessing the current axis
    ax = plt.gca()

    # Setting date formats for x-axis
    locator = mdates.MonthLocator()  # A tick per month if many days
    fmt = mdates.DateFormatter('%Y-%m')
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(fmt)

    plt.xticks(rotation=45)

    # Adjusting y-axis limits for better visibility
    y_min, y_max = df_apos_2023['TOTAL'].min(), df_apos_2023['TOTAL'].max()
    ax.set_ylim(y_min - 0.5 * (y_max - y_min), y_max + 0.5 * (y_max - y_min))

    plt.tight_layout()
    st.pyplot(plt)



def grafico_linha_dist_renda_variavel():

    # Calcular categorias agregadas
    acoes = df_apos_2023.get('AÇÕES', 0)
    fiis = df_apos_2023.get('FIIS', 0)
    exterior = df_apos_2023.get('EXTERIOR', 0)


    fig, ax = plt.subplots(figsize=(10, 6))  # Ajustar tamanho conforme necessário
    ax.plot(df_apos_2023.index, df_apos_2023['AÇÕES'], label='Ações')
    ax.plot(df_apos_2023.index, df_apos_2023['FIIS'], label='FIIs')
    ax.plot(df_apos_2023.index, df_apos_2023['EXTERIOR'], label='Exterior')

    ax.grid(True)

    labels = ['Ações', 'FIIs', 'Exterior']
    sizes = [df_apos_2023['AÇÕES'].iloc[-1], df_apos_2023['FIIS'].iloc[-1], df_apos_2023['EXTERIOR'].iloc[-1]]
    labels_with_values = [f'{label}: {format_as_currency_brl(size)}' for label, size in zip(labels, sizes)]
    plt.legend(labels_with_values, title="VALORES ATUAIS", loc="upper left")

    y_min, y_max = df_apos_2023['EXTERIOR'].min(), df_apos_2023['AÇÕES'].max()
    ax.set_ylim(y_min - 0.1 * (y_max - y_min), y_max + 0.5 * (y_max - y_min))
    plt.xticks(rotation=45)
    st.pyplot(plt)

# VISUALIZAÇÃO NO SITE

aba1, aba2 = st.tabs(['DASHBOARD', 'TABELA'])

with aba1:
    st.markdown('<br>', unsafe_allow_html=True)
    coluna1, coluna2, coluna3, coluna4, coluna5 = st.columns([4,4,4,4,4])
    with coluna1:
        st.metric('Saldo em jan/2023', 'R$ ' + format_number(df_apos_2023['TOTAL'].iloc[0]))
    with coluna2:
        st.metric('Saldo atual', 'R$ ' + format_number(df_apos_2023['TOTAL'].iloc[-1]))
    with coluna3:
        x = ((df_apos_2023['TOTAL'].iloc[-1]/df_apos_2023['TOTAL'].iloc[0])-1)*100
        percentual_formatado = '{:.2f} %'.format(x)
        st.metric('Crescimento total', percentual_formatado)
    with coluna4:
        x = ((df_apos_2023['renda_fixa'].iloc[-1]/df_apos_2023['renda_fixa'].iloc[0])-1)*100
        percentual_formatado = '{:.2f} %'.format(x)
        st.metric('Crescimento renda fixa', percentual_formatado)
    with coluna5:
        x = ((df_apos_2023['renda_variavel'].iloc[-1]/df_apos_2023['renda_variavel'].iloc[0])-1)*100
        percentual_formatado = '{:.2f} %'.format(x)
        st.metric('Crescimento renda variável', percentual_formatado)


    st.markdown('<br><br><br>', unsafe_allow_html=True)
    st.title('Evolução dos Investimentos após 2023')
    coluna1, coluna2, coluna3 = st.columns([2,5,2])

    with coluna1:
        st.write('')
    with coluna2:
        grafico_linha_evolucao()
    with coluna3:
        st.write('')
    
    st.markdown('<br><br><br>', unsafe_allow_html=True)
    st.title('Distribuição dos investimentos')
    st.markdown('<br><br>', unsafe_allow_html=True)


    coluna1, coluna2, coluna3 = st.columns([5,1,5])

    with coluna1:
        st.title('Total  investimentos')
        grafico_pizza_distribuicao_total()

    with coluna2:
        st.write('')

    with coluna3:
        st.title('Renda variável')
        grafico_pizza_renda_variavel()

    coluna1, coluna2 = st.columns(2)

    with coluna1:
        st.title('Evolução de investimento Renda fixa e variável')
        grafico_linha_distribuicao_total()

    with coluna2:
        st.title('Evolução de investimento variável')
        grafico_linha_dist_renda_variavel()

with aba2:
        st.dataframe(df_apos_2023, width=1600, height=600)

  
    
