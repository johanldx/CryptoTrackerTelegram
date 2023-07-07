from models import User
from api import Blockchain, Crypto
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging
import pytz
from datetime import datetime

ADMINISTRATORS = ['ADMINISTRATOR_ID', 'ADMINISTRATOR_ID']
API_KEY = 'BLOCKCYPHER_API_KEY'

temp = {}

logging.basicConfig(filename='infos.log',
                    level=logging.INFO,
                    format='%(asctime)s:%(levelname)s: %(message)s')

bot = telebot.TeleBot(token='TELEGRAM_BOT_TOKEN', parse_mode=None)
logging.info("Le bot Telegram est connecté.")

@bot.message_handler(commands=['start'])
def start_command(message):
    user = User(user_id=message.from_user.id)
    markup = InlineKeyboardMarkup()
    
    markup.add(InlineKeyboardButton("🆕 Suivre une nouvelle transaction", callback_data="new_transaction"))
    markup.add(InlineKeyboardButton(f"🗂️ Mes transactions suivies ({len(user.get_all_transactions())})", callback_data="my_transactions:1"))
    markup.add(InlineKeyboardButton("⚙️ Paramètres", callback_data="settings"))
        
    bot_message = bot.send_message(message.chat.id, '*🤖 Accueil*\nBonjour, je suis *CryptoTracker* votre assistant pour vous aider à suivre vos transactions en cryptomonnaies.' , reply_markup=markup, parse_mode='Markdown')
    
    temp[message.from_user.id] = {'message': bot_message.id, 'new_transaction': {}}


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    
    user = User(user_id=call.from_user.id)
    markup = InlineKeyboardMarkup()

    
    match call.data:
        case 'new_transaction':
            bot.clear_step_handler_by_chat_id(call.from_user.id)
            bot.answer_callback_query(call.id)
            
            markup.add(InlineKeyboardButton("❌ Annuler", callback_data="back_to_menu"))
            markup.add(InlineKeyboardButton("BTC", callback_data="new_transaction_btc"),
                       InlineKeyboardButton("ETH", callback_data="new_transaction_eth"),
                       InlineKeyboardButton("LTC", callback_data="new_transaction_ltc")
                       )
            
            message = bot.edit_message_text(chat_id=call.from_user.id, 
                                            message_id=temp[call.from_user.id]['message'],
                                            text="🧾 De quelle cryptomonnaie s'agit-il ?", 
                                            reply_markup=markup,
                                            parse_mode='Markdown')
            
        case 'new_transaction_btc':
            bot.clear_step_handler_by_chat_id(call.from_user.id)
            bot.answer_callback_query(call.id)
            
            temp[call.from_user.id]['new_transaction'] = {'txid': '', 'name': '', 'coin_symbol': Crypto.BITCOIN, 'finished': None}
            
            markup.add(InlineKeyboardButton("❌ Annuler", callback_data="back_to_menu"))
            
            message = bot.edit_message_text(chat_id=call.from_user.id, 
                                            message_id=temp[call.from_user.id]['message'],
                                            text="🧾 *Entrez votre TXID*\n\nBlockchain : BTC", 
                                            reply_markup=markup,
                                            parse_mode='Markdown')
            
            bot.register_next_step_handler(message, new_transaction_step_txid)
            
        
        case 'new_transaction_eth':
            bot.clear_step_handler_by_chat_id(call.from_user.id)
            bot.answer_callback_query(call.id)
            
            temp[call.from_user.id]['new_transaction'] = {'txid': '', 'name': '', 'coin_symbol': Crypto.ETHEREUM, 'finished': None}

            markup.add(InlineKeyboardButton("❌ Annuler", callback_data="back_to_menu"))
            
            message = bot.edit_message_text(chat_id=call.from_user.id, 
                                            message_id=temp[call.from_user.id]['message'],
                                            text="🧾 *Entrez votre TXID*\n\nBlockchain : ETH", 
                                            reply_markup=markup,
                                            parse_mode='Markdown')
            
            bot.register_next_step_handler(message, new_transaction_step_txid)
        
        case 'new_transaction_ltc':
            bot.clear_step_handler_by_chat_id(call.from_user.id)
            bot.answer_callback_query(call.id)
            
            temp[call.from_user.id]['new_transaction'] = {'txid': '', 'name': '', 'coin_symbol': Crypto.LITECOIN, 'finished': None}
            
            markup.add(InlineKeyboardButton("❌ Annuler", callback_data="back_to_menu"))
            
            message = bot.edit_message_text(chat_id=call.from_user.id, 
                                            message_id=temp[call.from_user.id]['message'],
                                            text="🧾 *Entrez votre TXID*\n\nBlockchain : LTC", 
                                            reply_markup=markup,
                                            parse_mode='Markdown')
            
            bot.register_next_step_handler(message, new_transaction_step_txid)
        
        case 'settings':
            bot.clear_step_handler_by_chat_id(call.from_user.id)
            bot.answer_callback_query(call.id)
            
            markup.add(InlineKeyboardButton("↪️ Menu principal", callback_data="back_to_menu"))
            markup.add(InlineKeyboardButton("📪 Contacter le créateur", callback_data="contact"))
            markup.add(InlineKeyboardButton("⚠️ Supprimer mon compte", callback_data="delete_account"))
            
            data = '"' + str(call.from_user.id) + '": ' + str(user.get_all_informations())
            if len(data) > 2000:
                data = "Données trop longues pour être affiché."
            
            message = bot.edit_message_text(chat_id=call.from_user.id, 
                                            message_id=temp[call.from_user.id]['message'],
                                            text=f'⚙️ *Paramètres*\nAccéder à vos informations et gérer votre compte.\n\n*Une copie de vos données que nous possédons :*\n' + data, 
                                            reply_markup=markup,
                                            parse_mode='Markdown')
        case 'back_to_menu':
            bot.clear_step_handler_by_chat_id(call.from_user.id)
            bot.answer_callback_query(call.id)
            
            markup.add(InlineKeyboardButton("🆕 Nouvelle transaction", callback_data="new_transaction"))
            markup.add(InlineKeyboardButton(f"🗂️ Mes transactions suivis ({len(user.get_all_transactions())})", callback_data="my_transactions:1"))
            markup.add(InlineKeyboardButton("⚙️ Paramètres", callback_data="settings"))
            
            message = bot.edit_message_text(chat_id=call.from_user.id, 
                                            message_id=temp[call.from_user.id]['message'],
                                            text='*🤖 Accueil*\nBonjour, je suis *CryptoTracker* votre assistant pour vous aider à suivre vos transactions en cryptomonnaies.', 
                                            reply_markup=markup,
                                            parse_mode='Markdown')
        
        case 'contact':
            bot.clear_step_handler_by_chat_id(call.from_user.id)
            bot.answer_callback_query(call.id)
            
            markup.add(InlineKeyboardButton("↪️ Menu principal", callback_data="back_to_menu"))
            
            message = bot.edit_message_text(chat_id=call.from_user.id, 
                                            message_id=temp[call.from_user.id]['message'],
                                            text="📭 *Écrivez votre message*\nIl sera envoyé par Telegram au créateur du bot. Votre identifiant unique ainsi que votre nom d'utilisateur sera aussi transmis.", 
                                            reply_markup=markup,
                                            parse_mode='Markdown')
            
            bot.register_next_step_handler(message, contact_send_message)
            
        case 'delete_account':
            bot.clear_step_handler_by_chat_id(call.from_user.id)
            bot.answer_callback_query(call.id)
            
            markup.add(InlineKeyboardButton("↪️ Menu principal", callback_data="back_to_menu")) 
            markup.add(InlineKeyboardButton("❌ Supprimer mon compte", callback_data="delete_account_confirm"))
            
            message = bot.edit_message_text(chat_id=call.from_user.id, 
                                            message_id=temp[call.from_user.id]['message'],
                                            text="⚠️ *Supprimer vos données*\nVous êtes sur le point de supprimer toutes vos informations enregistrés.", 
                                            reply_markup=markup,
                                            parse_mode='Markdown')
            
        case 'delete_account_confirm':
            bot.clear_step_handler_by_chat_id(call.from_user.id)
            bot.answer_callback_query(call.id)
            
            user.delete()
            
            message = bot.edit_message_text(chat_id=call.from_user.id, 
                                            message_id=temp[call.from_user.id]['message'],
                                            text="*👋 Au revoir !*\n\nToute les données que nous avions sur vous ont été supprimé avec succès. Si vous renvoyez un message, un nouveau compte sera créé.", 
                                            reply_markup=markup,
                                            parse_mode='Markdown')
            
        case 'nothing':
            bot.clear_step_handler_by_chat_id(call.from_user.id)
            bot.answer_callback_query(call.id)
            
    if call.data.startswith('my_transactions:'):
        bot.clear_step_handler_by_chat_id(call.from_user.id)
        bot.answer_callback_query(call.id)
        
        page = int(call.data[16:])
            
        nb_transactions = len(user.get_all_transactions())
        nb_page = 0
            
        while nb_transactions > 0:
            nb_page +=1
            nb_transactions -= 5
        if nb_page == 0:
            nb_page = 1
            
        markup.add(InlineKeyboardButton("↪️ Menu principal", callback_data="back_to_menu"))
        
        all_transactions = user.get_all_transactions()
        transactions = []
        for i in range(len(user.get_all_transactions())):  
            if (page*5)-5 <= i <= (page*5)-1:
                transactions.append(InlineKeyboardButton(f"🪙 {all_transactions[i][1]['name']} ({all_transactions[i][1]['coin_symbol'].upper()})", callback_data=f"transaction:{all_transactions[i][0][:20]}"))
        
        for transaction in transactions:
            markup.add(transaction)
        
        buttons = []
        if nb_page == 1 and page == 1:
            markup.add(InlineKeyboardButton("❌", callback_data="nothing"),
                   InlineKeyboardButton(f"Page {page}/{nb_page}", callback_data="nothing"),
                   InlineKeyboardButton("❌", callback_data="nothing"))
        elif page == 1:
            markup.add(InlineKeyboardButton("❌", callback_data="nothing"),
                   InlineKeyboardButton(f"Page {page}/{nb_page}", callback_data="nothing"),
                   InlineKeyboardButton("➡️", callback_data="my_transactions:" + str(page + 1)))
        elif page >= nb_page:
            markup.add(InlineKeyboardButton("⬅️", callback_data="my_transactions:" + str(page - 1)),
                   InlineKeyboardButton(f"Page {page}/{nb_page}", callback_data="nothing"),
                   InlineKeyboardButton("❌", callback_data="nothing"))
        else:
            markup.add(InlineKeyboardButton("⬅️", callback_data="my_transactions:" + str(page - 1)),
                   InlineKeyboardButton(f"Page {page}/{nb_page}", callback_data="nothing"),
                   InlineKeyboardButton("➡️", callback_data="my_transactions:" + str(page + 1)))
    
    
            
        message = bot.edit_message_text(chat_id=call.from_user.id, 
                                        message_id=temp[call.from_user.id]['message'],
                                        text="*📂 Mes transactions enregistrées *\nAccéder et gérer mes transactions enregistrés.", 
                                        reply_markup=markup,
                                        parse_mode='Markdown')
        
    if call.data.startswith('transaction:'):
        bot.clear_step_handler_by_chat_id(call.from_user.id)
        bot.answer_callback_query(call.id)
        
        bc = Blockchain(api_key=API_KEY)
        
        transaction_txid = call.data[12:]
        transaction_data = user.get_transaction(txid=transaction_txid)
        
        markup.add(InlineKeyboardButton("↪️ Retour", callback_data="my_transactions:1"))  
        markup.add(InlineKeyboardButton("❌ Supprimer le suivi", callback_data=f"delete_transaction:{transaction_data[0][:20]}"))
        
        transaction_infos = bc.check_transaction(transaction_id=transaction_data[0],
                                                 coin_symbol=transaction_data[1]['coin_symbol'])
        
        
        if transaction_infos: 
            
            inputs, outputs = '', ''
        
            for input_addresse in transaction_infos['inputs']:
                inputs = inputs + f"{input_addresse['addresses']}\n"
            
            for output_addresse in transaction_infos['outputs']:
                outputs = outputs + f"{output_addresse['addresses']}\n" 
                
            inputs, outputs = inputs.replace("'", ""), outputs.replace("'", "")

            date = transaction_infos['received'].strftime("%d/%m/%Y %H:%M:%S")

            text = f"*📂 Transaction {transaction_data[1]['name']}*\n\n*🔗 Blockchain*\n{transaction_data[1]['coin_symbol'].upper()}\n\n*🪪 TXID*\n{transaction_data[0]}\n\n*🛫 De*\n{ inputs }\n*🛬 Vers*\n{ outputs }\n*💵 Prix*\n{ '{:f}'.format(bc.convert(transaction_data[1]['coin_symbol'], transaction_infos['total']))  } {transaction_data[1]['coin_symbol'].upper()}\n\n*{'✅' if transaction_infos['confirmations'] >= 6 else '⚠️'} Confirmations*\n{transaction_infos['confirmations']} {'' if transaction_infos['confirmations'] >= 6 else '(Après 6 confirmations, la transaction est considéré comme terminé et irréversible.)'}\n\n*🗓️ Reçu*\n{date} UTC"
            text.replace("\n\n", "\n")

              
            message = bot.edit_message_text(chat_id=call.from_user.id, 
                                            message_id=temp[call.from_user.id]['message'],
                                            text=text, 
                                            reply_markup=markup,
                                            parse_mode='Markdown')
        else:
            message = bot.edit_message_text(chat_id=call.from_user.id, 
                                            message_id=temp[call.from_user.id]['message'],
                                            text=f"*📂 Transaction {transaction_data[1]['name']}*\n\nBlockchain : {transaction_data[1]['coin_symbol'].upper()}\nTXID : {transaction_data[0]}\n\n*⚠️ La transaction que vous essayer de suivre est introuvable !*", 
                                            reply_markup=markup,
                                            parse_mode='Markdown')

    if call.data.startswith('delete_transaction:'):
        bot.clear_step_handler_by_chat_id(call.from_user.id)
        bot.answer_callback_query(call.id)
        
        transaction_txid = call.data[19:]
        
        markup.add(InlineKeyboardButton("↪️ Retour", callback_data="my_transactions:1"))  
        
        if user.del_transaction(txid=transaction_txid):
            message = bot.edit_message_text(chat_id=call.from_user.id, 
                                    message_id=temp[call.from_user.id]['message'],
                                    text="*🧾 Le suivis à été supprimé.*", 
                                    reply_markup=markup,
                                    parse_mode='Markdown')
        else:
            message = bot.edit_message_text(chat_id=call.from_user.id, 
                                    message_id=temp[call.from_user.id]['message'],
                                    text="*⚠️ Une erreur est survenue lors de la supression*", 
                                    reply_markup=markup,
                                    parse_mode='Markdown')
            
            
            
def contact_send_message(message):
    for administrator_id in ADMINISTRATORS:
        bot.send_message(administrator_id, f"*🔔 Vous avez un nouveau message !*\n\nMessage de : {message.from_user.username} ({message.from_user.id})\n{message.text}", parse_mode='Markdown')     
        
    bot.delete_message(message.chat.id, message.id)
    
    markup = InlineKeyboardMarkup()
    
    markup.add(InlineKeyboardButton("↪️ Retour au menu principal", callback_data="back_to_menu"))
    
    message = bot.edit_message_text(chat_id=message.chat.id, 
                                    message_id=temp[message.from_user.id]['message'],
                                    text="✅ Votre message à bien été reçu !", 
                                    reply_markup=markup,
                                    parse_mode='Markdown')   
    
    
def new_transaction_step_txid(message):
    bot.delete_message(message.chat.id, message.id)
    
    user = User(user_id=message.from_user.id)
    
    temp[message.from_user.id]['new_transaction']['txid'] = message.text
    
    markup = InlineKeyboardMarkup()
    
    markup.add(InlineKeyboardButton("❌ Annuler", callback_data="back_to_menu"))
    
    message = bot.edit_message_text(chat_id=message.chat.id, 
                                    message_id=temp[message.from_user.id]['message'],
                                    text=f"🧾 *Entrer le nom de la transaction*\n\nBlockchain : {temp[message.from_user.id]['new_transaction']['coin_symbol'].upper()}\nTXID : {message.text}", 
                                    reply_markup=markup,
                                    parse_mode='Markdown')   
    
    bot.register_next_step_handler(message, new_transaction_step_name)
    
def new_transaction_step_name(message):
    bot.delete_message(message.chat.id, message.id)
    
    user = User(user_id=message.from_user.id)
    
    temp[message.from_user.id]['new_transaction']['name'] = message.text

    user.add_transaction(txid= temp[message.from_user.id]['new_transaction']['txid'],
                         name= temp[message.from_user.id]['new_transaction']['name'],
                         coin_symbol= temp[message.from_user.id]['new_transaction']['coin_symbol'],
                         finished= temp[message.from_user.id]['new_transaction']['finished']
                         )
    
    markup = InlineKeyboardMarkup()
    
    markup.add(InlineKeyboardButton("↪️ Retour au menu principal", callback_data="back_to_menu"))
    
    message = bot.edit_message_text(chat_id=message.chat.id, 
                                    message_id=temp[message.from_user.id]['message'],
                                    text=f"✅ *Nouveau suivi ajouté*\n\nNom : {temp[message.from_user.id]['new_transaction']['name']}\nBlockchain : {temp[message.from_user.id]['new_transaction']['coin_symbol'].upper()}\nTXID : {temp[message.from_user.id]['new_transaction']['txid']}", 
                                    reply_markup=markup,
                                    parse_mode='Markdown') 
    
      
bot.infinity_polling()