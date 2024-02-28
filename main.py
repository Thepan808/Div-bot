import tinydb
from tinydb import Query
import asyncio
from telebot import TeleBot
from telebot import types
import threading
import time
adms_db = tinydb.TinyDB('adms.json', indent=4, separators=(', ', ': '))
grupo_db = tinydb.TinyDB('grupo.json', indent=4, separators=(',', ': '))
bot = TeleBot('7077537700:AAFgjRgkc2t_FaIH1dUKMdhRLenkQcl-0og')
query = Query()

MENSAGEM = ''
TRAVA = False
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Olá {message.from_user.first_name}, seja bem vindo ao bot de divulgação')
    bot.send_message(message.chat.id, f'Para adicionar um administrador digite /add_adm')
    bot.send_message(message.chat.id, f'Para remover um administrador digite /remove_adm')
    bot.send_message(message.chat.id, f'Para ver a lista de administradores digite /adm_lista')
    bot.send_message(message.chat.id, f'Para adicionar um grupo de divulgação digite /add_grupo')
    bot.send_message(message.chat.id, f'Para remover um grupo de divulgação digite /remove_grupo')
    bot.send_message(message.chat.id, f'Para ver a lista de grupos de divulgação digite /grupo_lista')
    bot.send_message(message.chat.id, f'Para Definir uma mensagem para todos os grupos digite /mensagem')
    bot.send_message(message.chat.id, f'Para Enviar as mensagens digite /enviar_mensagens')

@bot.message_handler(commands=['add_adm'])
def insere_adm(message):
    validar_adm = adms_db.search(query.usuario == message.from_user.username)
    if validar_adm:
        bot.send_message(message.chat.id, 'Informe o nome de usuario sem o @')
        bot.register_next_step_handler(message, inserir_adm)
    else:
        bot.send_message(message.chat.id, 'Você não é um administrador')
        
        

@bot.message_handler(commands=['adm_lista'])
def inserir_grupo(message):
    adms = adms_db.search(query.usuario.exists())
    validar_adm = adms_db.search(query.usuario == message.from_user.username)
    if validar_adm:
        bot.send_message(message.chat.id, f'Lista de administradores: ')
        for adm in adms:
            bot.send_message(message.chat.id, f'@{adm["usuario"]}')



@bot.message_handler(commands=['remove_adm'])
def remover_adm(message):
    validar_adm = adms_db.search(query.usuario == message.from_user.username)
    if validar_adm:
        bot.send_message(message.chat.id, 'Informe o nome de usuario sem o @')
        bot.register_next_step_handler(message, remove_adm)
    else:
        bot.send_message(message.chat.id, 'Você não é um administrador')


@bot.message_handler(commands=['add_grupo'])
def insere_grupo(message):
    validar_adm = adms_db.search(query.usuario == message.from_user.username)
    if validar_adm:
        bot.send_message(message.chat.id, 'ok')
        id_ = message.chat.id
        tipo = message.chat.type
        titulo = message.chat.title
        pesquisar = grupo_db.search(query.id == id_)
        if not pesquisar:
            grupo_db.insert({'id': id_, 'tipo': tipo, 'titulo': titulo})
            bot.send_message(message.chat.id, f'Grupo {titulo} inserido na lista de grupos')
        else:
            bot.send_message(message.chat.id, f'Grupo {titulo} já existe na lista de grupos')
            
        
    else:
        bot.send_message(message.chat.id, 'Você não é um administrador')
        
        
        

@bot.message_handler(commands=['grupo_lista'])
def listar_grupo(message):
    grupos = grupo_db.search(query.id.exists())
    validar_adm = adms_db.search(query.usuario == message.from_user.username)
    if validar_adm:
        print('valido')
        bot.send_message(message.chat.id, f'Lista de grupos: ')
        for grupo in grupos:
            bot.send_message(message.chat.id, f'Grupo:\n {grupo["titulo"]}\n ID: \n {grupo["id"]}\n\n')
    else:
        bot.send_message(message.chat.id, 'Você não é um administrador')
        

@bot.message_handler(commands=['remove_grupo'])
def remover_grupo(message):
    validar_adm = adms_db.search(query.usuario == message.from_user.username)
    if validar_adm:
        bot.send_message(message.chat.id, 'Informe o nome do grupo')
        bot.register_next_step_handler(message, delete_grupo)
    else:
        bot.send_message(message.chat.id, 'Você não é um administrador')
      
      
        
@bot.message_handler(commands=['mensagem'])
def set_mensagem(message):
     
    validar_adm = adms_db.search(query.usuario == message.from_user.username)
    if validar_adm:
        bot.send_message(message.chat.id, 'Informe a mensagem')
        bot.register_next_step_handler(message, set_mensagem_db)
        
    else:
        bot.send_message(message.chat.id, 'Você não é um administrador')
    
 #------------------------------------- funções next_step       
def set_mensagem_db(message):
    global MENSAGEM
    MENSAGEM = message.text
    validar_adm = adms_db.search(query.usuario == message.from_user.username)
    if validar_adm:
        bot.send_message(message.chat.id, f'Mensagem salva: ')
        bot.send_message(message.chat.id, f'{MENSAGEM}')
        bot.send_message(message.chat.id, f'Para enviar a mensagem digite /enviar_mensagem')
        bot.send_message(message.chat.id, f'A mensagem será enviada para:')
        grupos = grupo_db.search(query.id.exists())
        for grupo in grupos:
            bot.send_message(message.chat.id, f'\n {grupo["titulo"]}\n\n')   
    else:
        bot.send_message(message.chat.id, 'Você não é um administrador')
        


def inserir_adm(message):
    if message.text[0] != '@': 
        adms_db.insert({'usuario': message.text})
        bot.send_message(message.chat.id, f'{message.text} inserido na lista de administradores')
    else:
        bot.send_message(message.chat.id, 'Informe o nome de usuario sem o @')

def remove_adm(message):
    if message.text[0] != '@':
        adms_db.remove(query.usuario == message.text)
        bot.send_message(message.chat.id, f'{message.text} removido da lista de administradores')
    else:
        bot.send_message(message.chat.id, 'Informe o nome de usuario sem o @')
    
def delete_grupo(message):
    grupo_db.remove(query.titulo == message.text)
    bot.send_message(message.chat.id, f'Grupo {message.text} removido da lista de grupos')


@bot.message_handler(commands=['enviar_mensagem'])
def enviar_mensagem(message):
    global MENSAGEM
    validar_adm = adms_db.search(query.usuario == message.from_user.username)
    menu = types.ReplyKeyboardMarkup(row_width=4)
    itembtn1 = types.KeyboardButton('1 min')
    itembtn2 = types.KeyboardButton('3 horas')
    itembtn3 = types.KeyboardButton('5 horas')
    itembtn4 = types.KeyboardButton('8 horas')
    itembtn5 = types.KeyboardButton('10 horas')
    itembtn6 = types.KeyboardButton('12 horas', )
    menu.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6)
    
    
    if validar_adm:
        bot.send_message(message.chat.id, MENSAGEM)
        bot.send_message(message.chat.id, 'Informe o Intervalo das mensagens', reply_markup=menu)
        grupos = grupo_db.search(query.id.exists())
        #for grupo in grupos:
            #bot.send_message(grupo['id'], f'{MENSAGEM}')
    else:
        bot.send_message(message.chat.id, 'Você não é um administrador')
    
@bot.message_handler(commands=['stop'])
def stop(message):
    global TRAVA
    TRAVA = True
    bot.send_message(message.chat.id, 'Divulgação parada')

def disparar(tempo, message):
    bot.send_message(message.chat.id, f'Envio Iniciado, digite /stop quando quiser')
    if MENSAGEM:
        while not TRAVA:
                for grupo in grupo_db.search(query.id.exists()):
                    bot.send_message(grupo['id'], f'{MENSAGEM}')
                time.sleep(tempo)
    else:
        
        bot.send_message(message.chat.id, f'Digite /mensagem antes de prosseguir')
@bot.message_handler(func=lambda message: True, content_types=['text'])
def enviar_mensagem(message):
    if message.text == '1 min':
        tempo = 60
        disparar(tempo, message)
        
    if message.text == '3 horas':
        tempo = 10800
        disparar(tempo, message)
        
    if message.text == '5 horas':
        tempo = 18000
        disparar(tempo, message)
    
    if message.text == '8 horas':
        tempo = 28800
        disparar(tempo, message)
        
    if message.text == '10 horas': 
        tempo = 36000
        disparar(tempo, message)
    
    if message.text == '12 horas':
        tempo = 43200
        disparar(tempo, message)
    
bot.polling(none_stop=True)