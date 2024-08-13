import pandas as pd
import pywhatkit as kit
import time

# Carregar as planilhas
abordagens_df = pd.read_excel('abordagens_setor.xlsx')
clientes_df = pd.read_excel('teste.xlsx')

# Função para enviar mensagens
def enviar_mensagens():
    for index, cliente in clientes_df.iterrows():
        setor_cliente = cliente['setor']
        telefone = cliente['telefone']
        
        # Filtrar a abordagem correspondente ao setor do cliente
        abordagem = abordagens_df[abordagens_df['setor'].str.contains(setor_cliente, case=False, na=False)]['abordagem'].values
        
        if len(abordagem) > 0:
            mensagem = abordagem[0]
            try:
                # Enviar mensagem via WhatsApp
                kit.sendwhatmsg_instantly(f"+{telefone}", mensagem, 15, True)
                print(f"Mensagem enviada para {cliente['empresas']} ({telefone})")
                time.sleep(5)  # Pausa para evitar problemas de sobrecarga
            except Exception as e:
                print(f"Erro ao enviar mensagem para {telefone}: {str(e)}")
        else:
            print(f"Nenhuma abordagem encontrada para o setor: {setor_cliente}")

# Executar a função
enviar_mensagens()