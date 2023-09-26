import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext
import requests
import time

# Botunuzun tokenı
BOT_TOKEN = '6698926728:AAH-o4MQ-BINcXA2qc9X5TkTo5SAa3qhPJo'

# Bot nesnesini oluşturun
bot = telegram.Bot(token=BOT_TOKEN)

def start(update, context):
    update.message.reply_text('Bot başlatıldı.')

def check_for_new_notification(context: CallbackContext):
    # Web sitesinin URL'sini belirtin
    website_url = 'https://yhgm.saglik.gov.tr/TR-34915/dhy-tebligatlari.html'

    # Web sitesinden içeriği alın
    response = requests.get(website_url)

    if response.status_code == 200:
        # İçerik başarılı bir şekilde alındı
        website_content = response.text

        if '112.Dönem Devlet Hizmeti' in website_content:
            # Yeni tebligat var, bildirim gönderin
            chat_id = '-1001808455604'  # Bildirimi almak istediğiniz chat ID'sini buraya ekleyin
            bot.send_message(chat_id, 'Yeni bir tebligat var!')

        # Web sitesini her 5 saniyede bir kontrol etmek için bir sonraki kontrolü planlayın
        context.job_queue.run_once(check_for_new_notification, 5)

    else:
        # Web sitesine erişilemiyor
        chat_id = '-1001808455604'  # Bildirimi almak istediğiniz chat ID'sini buraya ekleyin
        bot.send_message(chat_id, 'Web sitesine erişilemiyor.')

def main():
    # Updater nesnesini oluşturun
    updater = Updater(token=BOT_TOKEN, use_context=True)

    # Komut işleyicilerini ve mesaj işleyicilerini tanımlayın
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))

    # Web sitesini kontrol etmek için bir işlem planlayın
    updater.job_queue.run_once(check_for_new_notification, 0)

    # Botunuzu çalıştırın
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
