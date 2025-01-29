import string
import telebot
import time
import threading
import asyncio

from datetime import datetime
from PIL import Image

from g_python.gextension import Extension
from g_python.htools import Direction, HMessage, RoomUsers, RoomFurni
from g_python.hpacket import HPacket
from g_python.hparsers import HFloorItem


import shared_data
import static
import controllers


bot = telebot.TeleBot('7698697430:AAEa14QgM1w_5NWTYBfktT4ND98e-win6-U')


extension_info = {
    "title": "Torvi. Teste",
    "description": "Teste DIC",
    "version": "1.0",
    "author": "Torvi."
}

CHAT_ID = -1002266352451


ext = Extension(extension_info, ('-p', '9092'))
ext.start()

current_room_id = ''
unique_id_ready = threading.Event()


def get_timestamp():
    return datetime.now().strftime("%H:%M:%S %d/%m/%Y")


def handle_flat_controllers(message):
    packet = message.packet
    room_id = packet.read_int()
    user_count = packet.read_int()

    shared_data.portadores_nicks.clear()

    for i in range(user_count):
        user_data = {
            'id': packet.read_int(),
            'nick': packet.read_string()
        }

        shared_data.portadores_nicks.append({'id': user_data['id'], 'nick': user_data['nick']})

    print(shared_data.portadores_nicks)

def connect_to_room(base_id):
    try:
        ext.send_to_server(HPacket('GetGuestRoom', base_id, 0, 1))
        shared_data.room_id = base_id
        print(shared_data.room_id)

        ext.send_to_server(HPacket('GetFlatControllers', current_room_id))

        ext.intercept(Direction.TO_CLIENT, handle_flat_controllers, 'FlatControllers')
    except Exception as e:
        print(e)


#connect_to_room(shared_data.b1_room_id) # Entrar no quarto assim que iniciar a extensão.



def on_ver_answer(message):
    (i, text, i, i, i, i, i) = message.packet.read('isiiiii')

    
    if text != "!ver" and text != '!ataque':
        text.replace("/", "\n")
        shared_data.portadores_em_base.append(text)
        print(shared_data.portadores_em_base)

    if 'TOTAL:' in text:
        ext.remove_intercept('Whisper')

    

def on_ver_command():
    ext.send_to_server(HPacket("Chat", "!ver", 1, 1)) # Envia o pacote de fala com o texto !ver para o servidor

    ext.intercept(Direction.TO_CLIENT, on_ver_answer, 'Whisper')


def on_attack_command(message):
    (i, text, i, i, i, i, i) = message.packet.read('isiiiii')

    if text == "!ataque":
        threading.Thread(target=send_attack_sign, args=()).start()


ext.intercept(Direction.TO_CLIENT, on_attack_command, 'Whisper')

def handle_attack_listener():
    print('entrei')
    print(shared_data.on_attack_listener_b1)
    time.sleep(30)
    shared_data.on_attack_listener_b1 = False
    print(shared_data.on_attack_listener_b1)
    #with ("")
    #bot.send_document(CHAT_ID,)
    

def send_attack_sign():

    print("Ataque reportado")

    bot.send_message(-1002266352451, static.core_message, message_thread_id=758)
    time.sleep(0.2)
    bot.send_message(-1002266352451, static.goe_message)
    time.sleep(0.2)

    bot.send_message(-1002266352451, 'ATAQUE EM BASE REPORTADO!')

    time.sleep(0.5)
    on_ver_command()

    message = None

    bot.send_message(-1002266352451, 'Inicializando os procedimentos de registro.')

    bot.send_message(-1002266352451, 'Analisando entrada e saída de portadores...', message_thread_id=2)
    bot.send_message(-1002266352451, 'Armazenando mensagens, fluxo de usuários e movimentação de mobílias...', message_thread_id=2)

    shared_data.on_attack = True
    shared_data.on_attack_listener_b1 = True

    threading.Thread(target=monitor_portadores_list, args=(message, -1002266352451, 2)).start()
    threading.Thread(target=handle_attack_listener).start()

    time.sleep(0.2)

    #bot.send_message(-1002266352451, 'teste', message_thread_id=2)

    controllers.screnshot()

    screen = Image.open(r"base\img\screenshot.jpg")
    screen_output = screen.convert('RGB')
    bot.send_photo(-1002266352451, screen_output, message_thread_id=2)



def process_new_user(users):
    for user in users:
        temp = str(user).split(": ")

        if len(temp) == 2:
            user_id = temp[0]
            nick = temp[1].split(" - ")[0]

            shared_data.users_b1.append({user_id: nick})

            if shared_data.on_attack == True:
                for portador in shared_data.portadores_nicks:
                    if nick == portador['nick']:
                        bot.send_message(CHAT_ID, f'Portador {nick} entrou em base. - {get_timestamp()}', message_thread_id=2)
            
            if nick in shared_data.portadores_nicks:
                shared_data.portadores_em_base.append(nick)

    print(shared_data.users_b1)


def process_user_leave(user):
    temp = str(user).split(": ")

    if len(temp) == 2:
        user_id = temp[0]
        nick = temp[1].split(" - ")[0]

        shared_data.users_b1 = [user for user in shared_data.users_b1 if user_id not in user]

        if shared_data.on_attack == True:
                for portador in shared_data.portadores_nicks:
                    if nick == portador['nick']:
                        bot.send_message(CHAT_ID, f'Portador {nick} saiu de base. - {get_timestamp()}', message_thread_id=2)

        if nick in shared_data.portadores_nicks:
                shared_data.portadores_em_base.append(nick)

    print(shared_data.users_b1)

room_users = RoomUsers(ext)
room_users.on_new_users(lambda users: process_new_user(users))
room_users.on_remove_user(lambda users: process_user_leave(users))

def handle_new_user(message):
    try:
        (i, user_unique_id, nick, s, s, user_index, i, i, s, i, i, s, i, i, i, i, b) = message.packet.read("iisssiiisiisiiiib")
        
        # shared_data.users_b1.append({'unique_id': user_unique_id, 'index': user_index, 'nick': nick})
        # print(shared_data.users_b1)

        for user in shared_data.b1_ban_list:
            if user['nick'] == nick:
                ext.send_to_server(HPacket('BanUserWithDuration', 80599039, 149281613, "RWUAM_BAN_USER_PERM"))
                # [user for user in shared_data.users_b1 if user_id not in user]
                shared_data.b1_ban_list = [user for user in shared_data.b1_ban_list if user['nick'] != nick]
                bot.reply_to(user['message'], f"{user['nick']} banido.")
                print(shared_data.b1_ban_list)
    
    except Exception as e:
        pass

ext.intercept(Direction.TO_CLIENT, handle_new_user, 'Users')
#ext.send_to_server(HPacket('BanUserWithDuration', 87008097, 149281613, "RWUAM_BAN_USER_PERM"))


def check_ban_room(message, user_list):
    print(shared_data.users_b1)
    for nick in [user_list]:
        print(nick)
        in_base = any(nick in user.values() for user in shared_data.users_b1)
        print(in_base)
        
        if in_base:
            return True
    return False
        


def read_id(message):
    packet = message.packet
    foo = message.packet.read_int()
    user_count = message.packet.read_int()

    users_result = []


    try:
        for i in range(user_count):
            user_data = {
                'unique_id': packet.read_int(),
                'nick': packet.read_string(),
                '1': packet.read_int(),
                '2': packet.read_int(),
                '3': packet.read_int(),
            }
            users_result.append(user_data)
    except Exception as e:
        print(f"Erro ao ler o pacote: {e}")

    #print(int(users_result[0]['unique_id']))

    shared_data.user_unique_id_temp = int(users_result[0]['unique_id'])

    unique_id_ready.set()

    #bot.send_message(CHAT_ID, unique_id)



def get_user_id(nick):
    ext.send_to_server(HPacket('HabboSearch', f'{nick}'))
    #{out:HabboSearch}{s:"x-Tears--DEP"}
    # X-Tears--DEP

    ext.intercept(Direction.TO_CLIENT, read_id, 'HabboSearchResult')
    unique_id_ready.wait()
    unique_id_ready.clear()
    print(shared_data.user_unique_id_temp)
    return shared_data.user_unique_id_temp


def monitor_portadores_list(message, id = None, thread = None):
    timeout = 5 # Tempo máximo de espera em segundos
    start_time = time.time()

    while len(shared_data.portadores_em_base) < 3:
        if time.time() - start_time > timeout:
            if not id:
                bot.reply_to(message, "Erro no comando.")
                return
            else:
                bot.send_message(id, "Erro no comando.")
                return

        time.sleep(0.5)

    if len(shared_data.portadores_em_base) >= 3:
            # Formata o índice 1
            nomes_brutos = shared_data.portadores_em_base[1]
            nomes_formatados = '\n'.join(nomes_brutos.split(' / '))  # Formata os nomes
            mensagem_final = (
                f"{shared_data.portadores_em_base[0]}\n\n"  # Índice 0
                f"{nomes_formatados}\n\n"                   # Índice 1 formatado
                f"{shared_data.portadores_em_base[2]}"    # Índice 2
            )
            

    if id == None:
        bot.reply_to(message, f"{mensagem_final}")
    elif id != None and thread == None:
        bot.send_message(id, f"{mensagem_final}")
    else:
        bot.send_message(id, f"{mensagem_final}", message_thread_id=thread)

    shared_data.portadores_em_base.clear()


def ban_control(message, user_list, base = None):
    if not base:
        for nick in user_list:

            if not check_ban_room(message, nick):
                
                shared_data.b1_ban_list.append({'nick': nick, 'message': message})
                shared_data.b2_ban_list.append({'nick': nick, 'message': message})

            elif check_ban_room(message, nick):
                user_unique_id = get_user_id(nick)
                ext.send_to_server(HPacket('BanUserWithDuration', user_unique_id, current_room_id, "RWUAM_BAN_USER_PERM"))
                bot.reply_to(message, f"{nick} banido.")

        print(shared_data.b1_ban_list)
        print(shared_data.b2_ban_list)

    if base == 1:
        for nick in user_list:
            shared_data.b1_ban_list.append({'nick': nick, 'message': message})
        print(shared_data.b1_ban_list)

    elif base == 2:
        for nick in user_list:
            shared_data.b2_ban_list.append({'nick': nick, 'message': message})
        print(shared_data.b2_ban_list)


@bot.message_handler(commands=['ver'])
def ver_portadores(message):
    on_ver_command()

    threading.Thread(target=monitor_portadores_list, args=(message,)).start()

def parse_ban_command(message):
    if len(message.text.split(" ")) == 1: # /ban (duas etapas)
        bot_sent = bot.send_message(message.chat.id, 'Insira o nick do policial.')
        bot.register_next_step_handler(bot_sent, handle_ban)
        return

    elif len(message.text.split(" ")) == 2: # /ban nickname
        nick = message.text.split(" ")[1]
        ban_control(message, [nick])
        return
        
    elif "-b" in message.text:
        temp = message.text.split(" ")
        flag_index = temp.index('-b')
        base = int(temp[flag_index + 1])

        if base < 1 or base > 2:
            bot.reply_to(message, "Base especificada inexistente. Tente novamente.")

        temp.pop(flag_index + 1)
        temp.pop(flag_index)

        temp = temp[1:]  # Remove o comando '/ban' da lista
        ban_control(message, temp, int(base))  

        return

    elif "-base" in message.text:
        temp = message.text.split(" ")
        flag_index = temp.index('-base')
        base = int(temp[flag_index + 1])

        temp.pop(flag_index + 1)
        temp.pop(flag_index)

        temp = temp[1:]  # Remove o comando '/ban' da lista
        ban_control(message, temp, int(base))

        return


@bot.message_handler(commands=['ban'])
def ban_command(message):
    parse_ban_command(message)

def handle_ban(message):
    temp = message.text.split(" ")

    if temp[0] == "/ban":
        temp = temp[1:]

    ban_control(message, temp)


# @bot.message_handler(commands=['id'])
# def get_id(message):
#     bot_sent = bot.send_message(message.chat.id, 'Insira o nick do policial.')
#     bot.register_next_step_handler(bot_sent, aaa)

# def aaa(message):
#     print(message.text)
#     get_user_id(message.text)
#     #ext.send_to_server(HPacket('HabboSearch', f'{message.text}'))


#ext.send_to_server(HPacket('HabboSearch', f'X-Tears--DEP'))



#UNBAN COMMAND

def unban_control(message, user_list, base = None):
    if not base:
        for nick in user_list:
            shared_data.b1_ban_list = [user for user in shared_data.b1_ban_list if user['nick'] != nick]
            shared_data.b2_ban_list = [user for user in shared_data.b1_ban_list if user['nick'] != nick]

            unique_id = get_user_id(nick)

            if unique_id is not None:
                # Enviar pacotes de desbanimento
                ext.send_to_server(HPacket('UnbanUserFromRoom', 80599039, shared_data.room_id))
                bot.reply_to(message, f'{nick} foi desbanido.')
            else:
                # Caso o unique_id seja inválido
                bot.reply_to(message, f'Erro: Não foi possível encontrar o ID do usuário {nick}.')

    if base == 1:
        for nick in user_list:
            shared_data.b1_ban_list = [user for user in shared_data.b1_ban_list if user['nick'] != nick]

            unique_id = get_user_id(nick)

            ext.send_to_server(HPacket('UnbanUserFromRoom', 80599039, 149281613))
            bot.reply_to(message, f'{nick} foi desbanido.')
            
        print(shared_data.b1_ban_list)

    elif base == 2:
        for nick in user_list:
            shared_data.b2_ban_list = [user for user in shared_data.b1_ban_list if user['nick'] != nick]

            ext.send_to_server(HPacket('UnbanUserFromRoom', 80599039, 149281613))
            bot.reply_to(message, f'{nick} foi desbanido.')

        print(shared_data.b2_ban_list)

def parse_unban_command(message):
    if len(message.text.split(" ")) == 1: # /unban (duas etapas)
        bot_sent = bot.send_message(message.chat.id, 'Insira o nick do policial.')
        bot.register_next_step_handler(bot_sent, handle_unban)
        return

    elif len(message.text.split(" ")) == 2: # /unban nickname
        nick = message.text.split(" ")[1]
        unban_control(message, [nick])
        return
        
    elif "-b" in message.text:
        temp = message.text.split(" ")
        flag_index = temp.index('-b')
        base = int(temp[flag_index + 1])

        if base < 1 or base > 2:
            bot.reply_to(message, "Base especificada inexistente. Tente novamente.")

        temp.pop(flag_index + 1)
        temp.pop(flag_index)

        temp = temp[1:]  # Remove o comando '/unban' da lista
        unban_control(message, temp, int(base))  

        return

    elif "-base" in message.text:
        temp = message.text.split(" ")
        flag_index = temp.index('-base')
        base = int(temp[flag_index + 1])

        temp.pop(flag_index + 1)
        temp.pop(flag_index)

        temp = temp[1:]  # Remove o comando '/unban' da lista
        unban_control(message, temp, int(base))

        return

@bot.message_handler(commands=['unban'])
def unban_command(message):
    parse_unban_command(message)

def handle_unban(message):
    temp = message.text.split(" ")

    if temp[0] == "/unban":
        temp = temp[1:]
    unban_control(message, temp)

#ext.send_to_server(HPacket('UnbanUserFromRoom', 83845001, shared_data.b1_room_id))
#ext.send_to_server('{out:HabboSearch}{s:"X-Tears--DEP"}')

def handle_message_filter(message):
    if shared_data.on_attack_listener_b1 == True:
        store_messages(message)

ext.intercept(Direction.TO_CLIENT, handle_message_filter, 'Chat')
ext.intercept(Direction.TO_CLIENT, handle_message_filter, 'Shout')
    
def store_messages(message):
    if shared_data.on_attack == True or shared_data.listening_to_messages_b1 == True:
        
        (user_index, text, i, i, i, i) = message.packet.read("isiiii")

        user_nick = None
        for user in shared_data.users_b1:
            if str(user_index) in user:
                user_nick = user[str(user_index)]
                break  

        if user_nick:
            shared_data.messages_b1.append({'user_nick': user_nick, 'message': text})

            print(shared_data.messages_b1)

            with open("messages.txt", "a") as file:
                file.write(f'[{get_timestamp()}] {user_nick}: {text}\n')

def send_message_file(chat_id, thread_id = None):
    with open("messages.txt", "a") as file:
        while True:
            if shared_data.message_attack_file_ready == True:
                if thread_id:
                    bot.send_document(chat_id, file, message_thread_id=thread_id)
                    return
                bot.send_document(chat_id, file)
                return


def start_onattack_message_listener(message):
    def listener(message):
        initial_time = time.time()
        while time.time() - initial_time < 10:
            store_messages(message)


    threading.Thread(target=listener, args=(message,)).start()


def new_ban_handler(nick):
    if nick in shared_data.portadores_nicks['nick']:
        bot.send_message(CHAT_ID, f"Portador {nick} banido da base - {get_timestamp()}\n\nPortadores em base no momento: {shared_data.portadores_em_base}", message_thread_id=2)



def handle_ban_list(message):
    packet = message.packet

    # Lendo dados do pacote
    room_id = packet.read_int()
    user_count = packet.read_int()

    # Lista atual dos banidos no pacote
    new_banned = []

    try:
        for _ in range(user_count):
            user_data = {
                'unique_id': packet.read_int(),
                'nick': packet.read_string()
            }
            new_banned.append(user_data['nick'])

        # Se a lista base ainda não foi inicializada
        if not shared_data.ban_list_ready:
            # Preencher apenas com valores únicos
            shared_data.base_banned = list(set(new_banned))
            shared_data.ban_list_ready = True
            print(f"Portadores em base no momento: {shared_data.base_banned}")
            return

        # Identificar novos nicks
        added_banned = [nick for nick in new_banned if nick not in shared_data.base_banned]

        # Processar novos nicks
        for nick in added_banned:
            new_ban_handler(nick)

        # Atualizar a lista base garantindo unicidade
        shared_data.base_banned = list(set(new_banned))
        print(f"Portadores em base no momento: {shared_data.base_banned}")

    except Exception as e:
        print(f"Erro ao processar banidos: {e}")


def ban_listener():
    while True:
        time.sleep(5)
        ext.send_to_server(HPacket('GetBannedUsersFromRoom', 148212967))
        ext.intercept(Direction.TO_CLIENT, handle_ban_list, 'BannedUsersFromRoom')




def get_height_map():
    ext.send_to_server('{out:GetHeightMap}')


def handle_ver_base(message):
    shared_data.users_b1.clear()
    get_height_map()

    excluded_nicks = {"Antônio", "Sorteador", "AntÃ´nio"}
    users = []
    time.sleep(1)

    message_answer = f"Usuários em base ({len(shared_data.users_b1)}):\n"

    nicks = ", \n".join([
    list(item.values())[0] for item in shared_data.users_b1 
    if list(item.values())[0] not in excluded_nicks])

    final = f'{message_answer}\n\n{nicks}'

    return final

@bot.message_handler(commands=['ver_base'])
def ver_base_command(message):
    msg = handle_ver_base(message)
    bot.reply_to(message, msg)

@bot.message_handler(commands=['get_msg'])
def get_msgs(message):
    with open('messages.txt', "rb") as file:
        bot.send_document(message.chat.id, file, message_thread_id=758)

@bot.message_handler(commands=['fim_ataque'])
def finalizar_ataque(message):
    shared_data.on_attack = False

@bot.message_handler(commands=['ataque'])
def cmd_ataque(message):
    try:
        if message.chat.id != -1002266352451:
            bot.reply_to(message, "Você não possui permissão de usar esse comando.")

        send_attack_sign()

    except Exception as e:
        print(e)

threading.Thread(target=ban_listener, args=()).start()
connect_to_room(149281613)


bot.infinity_polling()
