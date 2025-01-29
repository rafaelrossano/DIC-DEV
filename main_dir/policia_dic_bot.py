import telebot
from telebot.handler_backends import ContinueHandling

import telebot
import base64
from PIL import Image
from io import BytesIO

from telebot import types

from handle_payment import create_payment, check_payment
#from habbo import send_attack_sign

import config


bot = telebot.TeleBot(config.TEMP_BOT_TOKEN)

def verificar(mensagem):
    if mensagem.text() == "comando":
        return True
    else:
        return False
    

accounts_comando = ["NicolePereira15", "kprand", "cristianss04", "PedroVLA", "Thainan464", "Lyftz"]
accounts_core = ["torvi_hb", "kprand", "ysetheus", "helpier011", "golerobom196", "valenteb1", "gbgmss", "Tarkeru", "crucisx"]
accounts_goe = ["arcanjo887", "cristianss04", "LeviLanik01", "vtmnctoputo", "vtmnctoputo", "vicvaporub12", "guihwz", "breeh21", "StilverL", "bFloriela", "ggPedrosa"]
accounts_cg = ["carlosfavaleca", "arcanjo887", "iisabelaa"]
accounts_pres = ["fcswolfs", "miguel99mc", "brendo164", "lettt91"]


def check_permissions(message, *args):
    for list in args:
        for account in list:
            if message.from_user.username == account:
                return True
    
    return False

@bot.message_handler(commands=["comando"])
def responder(mensagem):
    try:
        with open('mensagem_comandante.txt', "r") as file:
            bot.reply_to(mensagem, file.read())
    except Exception as e:
        print(e)


@bot.message_handler(commands=['atualizar_comando'])
def responder(message):
    if check_permissions(message, accounts_comando, accounts_core, accounts_cg, accounts_pres):
        bot_sent = bot.send_message(message.chat.id, 'Insira a nova mensagem. ')
        bot.register_next_step_handler(bot_sent, add_comando)
    else:
        bot.send_message(message.chat.id, "Você não possui permissão de usar esse comando.")

def add_comando(message):
    try:
        with open('mensagem_comandante.txt', 'w') as file:
            file.write(f'{message.text}')
            bot.send_message(message.chat.id, 'Mensagem atualizada no sistema.')
    except Exception as e:
        print(e)


@bot.message_handler(commands=["core"])
def responder(mensagem):
    try:
        with open('mensagem_core.txt', "r") as file:
            bot.reply_to(mensagem, file.read())
    except Exception as e:
        print(e)


@bot.message_handler(commands=['atualizar_core'])
def responder(message):
    if check_permissions(message, accounts_core, accounts_cg, accounts_pres):
        bot_sent = bot.send_message(message.chat.id, 'Insira a nova mensagem. ')
        bot.register_next_step_handler(bot_sent, add_core)
    else:
        bot.send_message(message.chat.id, "Você não possui permissão de usar esse comando.")

def add_core(message):
    try:
        with open('mensagem_core.txt', 'w') as file:
            file.write(f'{message.text}')
            bot.send_message(message.chat.id, 'Mensagem atualizada no sistema.')
    except Exception as e:
        print(e)

 #--       

@bot.message_handler(commands=["goe"])
def responder(mensagem):
    try:
        with open('mensagem_goe.txt', "r") as file:
            bot.reply_to(mensagem, file.read())
    except Exception as e:
        print(e)


@bot.message_handler(commands=['atualizar_goe'])
def responder(message):
    if check_permissions(message, accounts_goe, accounts_core, accounts_cg, accounts_pres):
        bot_sent = bot.send_message(message.chat.id, 'Insira a nova mensagem. ')
        bot.register_next_step_handler(bot_sent, add_goe)
    else:
        bot.send_message(message.chat.id, "Você não possui permissão de usar esse comando.")

def add_goe(message):
    try:
        with open('mensagem_goe.txt', 'w') as file:
            file.write(f'{message.text}')
            bot.send_message(message.chat.id, 'Mensagem atualizada no sistema.')
    except Exception as e:
        print(e)

#--

@bot.message_handler(commands=["vendedores"])
def responder(mensagem):
    try:
        with open('mensagem_vendedores.txt', "r") as file:
            bot.reply_to(mensagem, file.read())
    except Exception as e:
        print(e)

@bot.message_handler(commands=['atualizar_vendedores'])
def responder(message):
    if check_permissions(message, accounts_comando, accounts_core, accounts_cg, accounts_pres):
        bot_sent = bot.send_message(message.chat.id, 'Insira a nova mensagem. ')
        bot.register_next_step_handler(bot_sent, add_vendedores)
    else:
        bot.send_message(message.chat.id, "Você não possui permissão de usar esse comando.")

def add_vendedores(message):
    try:
        with open('mensagem_vendedores.txt', 'w') as file:
            file.write(f'{message.text}')
            bot.send_message(message.chat.id, 'Mensagem atualizada no sistema.')
    except Exception as e:
        print(e)

#--

@bot.message_handler(commands=["comandogeral"])
def responder(mensagem):
    try:
        with open('mensagem_comandog.txt', "r") as file:
            bot.reply_to(mensagem, file.read())
    except Exception as e:
        print(e)


@bot.message_handler(commands=['atualizar_cg'])
def responder(message):
    if check_permissions(message, accounts_comando, accounts_core, accounts_cg, accounts_pres):
        bot_sent = bot.send_message(message.chat.id, 'Insira a nova mensagem. ')
        bot.register_next_step_handler(bot_sent, add_comandog)
    else:
        bot.send_message(message.chat.id, "Você não possui permissão de usar esse comando.")

def add_comandog(message):
    try:
        with open('mensagem_comandog.txt', 'w') as file:
            file.write(f'{message.text}')
            bot.send_message(message.chat.id, 'Mensagem atualizada no sistema.')
    except Exception as e:
        print(e)


@bot.message_handler(commands=["apr"])
def responder(mensagem):
    try:
        with open('mensagem_apr.txt', "r") as file:
            bot.reply_to(mensagem, file.read())
    except Exception as e:
        print(e)


@bot.message_handler(commands=['atualizar_apr'])
def responder(message):
    if check_permissions(message, accounts_comando, accounts_core, accounts_cg, accounts_pres):
        bot_sent = bot.send_message(message.chat.id, 'Insira a nova mensagem. ')
        bot.register_next_step_handler(bot_sent, add_apr)
    else:
        bot.send_message(message.chat.id, "Você não possui permissão de usar esse comando.")

def add_apr(message):
    try:
        with open('mensagem_apr.txt', 'w') as file:
            file.write(f'{message.text}')
            bot.send_message(message.chat.id, 'Mensagem atualizada no sistema.')
    except Exception as e:
        print(e)

@bot.message_handler(commands=["csi"])
def responder(mensagem):
    try:
        with open('mensagem_csi.txt', "r") as file:
            bot.reply_to(mensagem, file.read())
    except Exception as e:
        print(e)


@bot.message_handler(commands=['atualizar_csi'])
def responder(message):
    if check_permissions(message, accounts_core, accounts_pres):
        bot_sent = bot.send_message(message.chat.id, 'Insira a nova mensagem. ')
        bot.register_next_step_handler(bot_sent, add_csi)
    else:
        bot.send_message(message.chat.id, "Você não possui permissão de usar esse comando.")

def add_csi(message):
    try:
        with open('mensagem_csi.txt', 'w') as file:
            file.write(f'{message.text}')
            bot.send_message(message.chat.id, 'Mensagem atualizada no sistema.')
    except Exception as e:
        print(e)


#https://t.me/c/2266352451/758/791
@bot.message_handler(commands=['ataque'])
def cmd_ataque(message):
    try:
        if message.chat.id != -1002266352451:
            return

        #send_attack_sign()

    except Exception as e:
        print(e)

@bot.message_handler(commands=['start'])
def cmd_start(message):
    dic_logo = Image.open("base\img\dic_logo.jpg")
    dic_logo_output = dic_logo.convert('RGB')
    bot.send_photo(message.from_user.id, dic_logo_output, "Olá! Sou o bot oficial da Polícia DIC ® e auxiliarei sua compra de cargo. \n\nO pagamento ocorre de forma automática e, após a venda, será automaticamente informado ao Corpo de Superiores sobre seu novo cargo.", parse_mode='HTML')
    #bot.send_message(message.chat.id, "Olá! Sou o bot oficial da Polícia DIC ® e auxiliarei sua compra de cargo. \n\nO pagamento ocorre de forma automática e, após a venda, será automaticamente informado ao Corpo de Superiores sobre seu novo cargo.")

    button_agente = types.InlineKeyboardButton('Agente / R$ 3,80', callback_data='agente')
    button_analista = types.InlineKeyboardButton('Analista / R$ 5,70', callback_data='analista')
    button_coordenador = types.InlineKeyboardButton('Coordenador / R$ 7,60', callback_data='coordenador')
    button_promotor = types.InlineKeyboardButton('Promotor / R$ 9,50', callback_data='promotor')
    button_advogado = types.InlineKeyboardButton('Advogado / R$ 11,40', callback_data='advogado')
    button_administrador = types.InlineKeyboardButton('Administrador / R$ 13,30', callback_data='administrador')
    button_delegado = types.InlineKeyboardButton('Delegado / R$ 15,20', callback_data='delegado')
    button_investigador = types.InlineKeyboardButton('Investigador / R$ 19,00', callback_data='investigador')

    # Botões para os cargos superiores
    button_detetive = types.InlineKeyboardButton('Detetive / R$ 38,00', callback_data='detetive')
    button_supervisor = types.InlineKeyboardButton('Supervisor / R$ 66,50', callback_data='supervisor')
    button_lider = types.InlineKeyboardButton('Líder / R$ 114,00', callback_data='lider')
    button_lider_executivo = types.InlineKeyboardButton('Líder-Executivo / R$ 190,00', callback_data='lider_executivo')
    button_chanceler = types.InlineKeyboardButton('Chanceler / R$ 855,00', callback_data='chanceler')

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(button_agente)
    keyboard.add(button_analista)
    keyboard.add(button_coordenador)
    keyboard.add(button_promotor)
    keyboard.add(button_advogado)
    keyboard.add(button_administrador)
    keyboard.add(button_delegado)
    keyboard.add(button_investigador)
    keyboard.add(button_detetive)
    keyboard.add(button_supervisor)
    keyboard.add(button_lider)
    keyboard.add(button_lider_executivo)
    keyboard.add(button_chanceler)


    bot.send_message(message.chat.id, "Selecione seu cargo de interesse:", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def agente(call):
    if call.data == "agente":
        response = payment_message('3.80', call)
        if check_payment(response):
            approved_payment(call, 'agente')
    elif call.data == "analista":
        response = payment_message('5.70', call)
        if check_payment(response):
            approved_payment(call, 'analista')
    elif call.data == "coordenador":
        response = payment_message('7.60', call)
        if check_payment(response):
            approved_payment(call, 'coordenador')
    elif call.data == "promotor":
        response = payment_message('9.50', call)
        if check_payment(response):
            approved_payment(call, 'promotor')
    elif call.data == "advogado":
        response = payment_message('11.40', call)
        if check_payment(response):
            approved_payment(call, 'advogado')
    elif call.data == "administrador":
        response = payment_message('13.30', call)
        if check_payment(response):
            approved_payment(call, 'administrador')
    elif call.data == "delegado":
        response = payment_message('15.20', call)
        if check_payment(response):
            approved_payment(call, 'delegado')
    elif call.data == "investigador":
        response = payment_message('19.00', call)
        if check_payment(response):
            approved_payment(call, 'investigador')
    elif call.data == "detetive":
        response = payment_message('38.00', call)
        if check_payment(response):
            approved_payment(call, 'detetive')
    elif call.data == "supervisor":
        response = payment_message('66.50', call)
        if check_payment(response):
            approved_payment(call, 'supervisor')
    elif call.data == "lider":
        response = payment_message('114.00', call)
        if check_payment(response):
            approved_payment(call, 'lider')
    elif call.data == "lider_executivo":
        response = payment_message('190.00', call)
        if check_payment(response):
            approved_payment(call, 'lider_executivo')
    elif call.data == "chanceler":
        response = payment_message('855.00', call)
        if check_payment(response):
            approved_payment(call, 'chanceler')


def approved_payment(message, patente):
    button_grupo = types.InlineKeyboardButton('Clique neste botão para acessar o grupo.', callback_data='grupo', url='https://t.me/+WEb-0uPqGOtkMjU5')
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(button_grupo)
    bot.send_message(message.from_user.id, f'🎉 Pagamento Aprovado! 🎉\n\nParabéns, {message.from_user.first_name}! Seu pagamento foi aprovado com sucesso.\n\nEntre no grupo disponibilizado abaixo para finalizar os procedimentos de venda.', reply_markup=keyboard)
    bot.send_message(1761647464, f'Venda de cargo realizada. \n\nDados:\nComprador: {message.from_user.username} | Cargo: {patente}')


def handle_nickname(message):
    bot.send_message(message.chat.id, f'Nick registrado: {message.text}\n\n Digite seu nick novamente para confirmar.\n(Caso tenha inserido errado, digite /nickname)')



def payment_message(value, message):
    payment, response = create_payment(value)
    pix_copia_cola = payment['response']['point_of_interaction']['transaction_data']['qr_code']
    qr_code = payment['response']['point_of_interaction']['transaction_data']['qr_code_base64']
    qr_code = base64.b64decode(qr_code)
    qr_code_img = Image.open(BytesIO(qr_code))
    qrcode_output = qr_code_img.convert('RGB')
    bot.send_photo(message.from_user.id, qrcode_output, "📸 Escaneie o QR code acima para realizar o pagamento ou copie o código abaixo!\n\nPara copiar, segure a mensagem e clique em 'Copiar'. 👇🏻", parse_mode='HTML')
    bot.send_message(message.from_user.id, f'<code>{pix_copia_cola}</code>', parse_mode='HTML')
    bot.send_message(message.from_user.id, 'O código expira em 5 minutos.')

    return response

bot.polling()