import requests
import telebot
import time
from datetime import datetime

# Configurações iniciais
today = datetime.now().strftime("%Y-%m-%d")
token = 'confidential'
chat_id = 'confidential'
bot = telebot.TeleBot(token)
jogos_enviados = []
TIME_GAME = 45



def obter_dados_api():
    url = "confidential"
    headers = {
    'confidential'
}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print('erro na requisição:', e)
        return None

def construir_mensagem(game, strategy):
    home_team = game["homeTeam"]["name"]
    away_team = game["awayTeam"]["name"]
    league = game["league"]["name"]
    home_score = game['scores']['homeTeamScore']
    away_score = game['scores']['awayTeamScore']
    minute = game["currentTime"]["minute"]
    convert_nome = home_team.replace(" ", "+")
    link_bet365 = f"https://www.bet365.com/#/AX/K%5E{convert_nome}/"
    

    mensagem = f'''🔥 JOGO QUENTE 🔥

🆚 <b>{home_team} x {away_team}</b>
🏆 {league}
⏰ {minute}' minutos

🚨 <b>{strategy}</b>

📛 Odd recomendada: +1.30
💰 Stake: 1% a 5%
⚠️ Respeite sua meta diária!

🔍 <b>Estatísticas(Casa - Fora):</b>
📈 Placar: {home_score} - {away_score}
⛳️ Escanteios: {game['stats']['corners']['home']} - {game['stats']['corners']['away']}

📲 <a href="{link_bet365}">Bet365</a>'''

    return mensagem

def analisar_jogo(game):
    minute = game.get("currentTime", {}).get("minute")
    addedtime = game['currentTime']['addedTime']
    

    if minute is None or not isinstance(minute, int):
        return
    if 'stats' in game and game['stats'] is not None and game['fixtureId'] not in jogos_enviados:

        home_score = game['scores']['homeTeamScore']
        away_score = game['scores']['awayTeamScore']
        score_difference = abs(home_score - away_score)
        home_redcards = game['stats']['redcards']['home']
        away_redcards = game['stats']['redcards']['away']
        home_corners = game['stats']['corners']['home']
        away_corners = game['stats']['corners']['away']
        home_attacks = game['stats']['attacks']['home']
        away_attacks = game['stats']['attacks']['away']
        home_dangerousattacks = game['stats']['dangerousAttacks']['home']
        away_dangerousattacks = game['stats']['dangerousAttacks']['away']
        home_shotsoffgoal = game['stats']['shotsOffgoal']['home']
        away_shotsoffgoal = game['stats']['shotsOffgoal']['away']
        home_shotsongoal = game['stats']['shotsOngoal']['home']
        away_shotsongoal = game['stats']['shotsOngoal']['away']

        #estratégias com o placar 0 x 0
        if home_score == 0 and away_score == 0:

            # Estratégia BTS
            if addedtime is not None and minute - addedtime <= TIME_GAME or minute <= TIME_GAME:
                if home_shotsongoal + away_shotsongoal >= 6 and home_shotsongoal > 1 and away_shotsongoal > 1:
                    if home_corners >= 2 and away_corners >= 2:
                        if home_shotsongoal + home_shotsoffgoal + away_shotsongoal + away_shotsoffgoal + home_corners + away_corners >= 10:
                            if home_dangerousattacks >= 10 and away_dangerousattacks >= 10:
                                if home_redcards + away_redcards == 0:
                                    return "BTS"
                                
            ##testando o bot
            #if minute <= 40:
            #    return "Teste"

            #teste  over antes dos 20                  
            if minute <= 20:
                if home_shotsongoal + away_shotsongoal >= 3:
                    if home_corners >= 2 and away_corners >= 2:
                        if home_dangerousattacks >= 5 and away_dangerousattacks  >= 5:
                            return "Estratégia gol no primeiro tempo"

        #estratégias com o placar 1 x 0
        elif score_difference == 1:

            #teste  over 1.5 segundo tempo                 
            if addedtime is not None and minute - addedtime <= 45 or minute <= 45:
                if home_score == 0:
                    if home_corners >= 2 and home_shotsongoal >= 5 and home_dangerousattacks >= 20:
                        return "Estratégia over 1.5"
                else:
                    if away_corners >= 2 and away_shotsongoal >= 5 and home_dangerousattacks >= 20:
                        return "Estratégia over 1.5"
    return None

def verificar_dados_e_enviar(dados):
    if dados is None:
        return

    for game in dados['data']:
        if game['stats'] is None:
            pass
        fixture_id = game['fixtureId']
        if fixture_id in jogos_enviados:
            pass

        strategy = analisar_jogo(game)
        if strategy:
            mensagem = construir_mensagem(game, strategy)
            enviar_mensagem_telegram(mensagem, chat_id)
            jogos_enviados.append(fixture_id)

def enviar_mensagem_telegram(mensagem, chat_id):
    try:
        bot.send_message(chat_id, mensagem, disable_web_page_preview=True, parse_mode='HTML')
    except Exception as e:
        return

while True:
    dados = obter_dados_api()
    verificar_dados_e_enviar(dados)
    time.sleep(180)  # Intervalo entre verificações