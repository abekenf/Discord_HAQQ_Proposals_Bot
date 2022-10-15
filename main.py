from datetime import datetime
from time import sleep
import discord
import iso8601
import pytz
from requests import get
import logging



client = discord.Client()


def app(update, context):
    text = update.message.text
    context.user_data["choice"] = text

    url = f"https://haqq-t.api.manticore.team/{text.lower()}/proposals"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
                                                                         Chrome/106.0.5249.103 Safari/537.36',
               'Accept': 'application/json'
               }
    data = get(url, headers=headers).json()

    try:
        for j in data:
            if j['proposal_status'] == 'PROPOSAL_STATUS_VOTING_PERIOD' and iso8601.parse_date(
                    j['submit_time'][:-1]) > datetime.now(tz=pytz.UTC):  # с этого момента будут освещаться только более поздние предложения
                number = j['id']
                title = j['title']
                message = f"{text.upper()}\nProposal {number} is in voting stage!\n{title}"
                print(message)

    except Exception as e:
        print(e)


sleep(1800)  # бот будет проверять наличие новых предложений каждые 30 минут

client.run('TOKEN') # вставьте свой токен бота

RPC_ADDRESS = "http://YOUR IP:PORT" # Синхронизированный IP-адрес RPC

ogging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)


def start(update, context):
    update.message.reply_text('Привет! Я бот, который поможет вам проверить баланс вашего кошелька HAQQ') # Отправить сообщение при выдаче команды /start

# Help command handler.
def help(update, context):
    update.message.reply_text('Отправьте свой кошелек HAQQ, и я покажу сумму вашего баланса') # Отправить сообщение при выдаче команды /help

def get_wallet_info(endpoint):
    haqq_http_available = '{}/cosmos/bank/v1beta1/balances/{}'.format(RPC_ADDRESS, endpoint)
    haqq_http_delegated = '{}/cosmos/staking/v1beta1/delegations/{}'.format(RPC_ADDRESS, endpoint)
    haqq_http_unbounding = '{}/cosmos/staking/v1beta1/delegations/{}/unbonding_delegations'.format(RPC_ADDRESS, endpoint)
    haqq_http_rewards = '{}/cosmos/distribution/v1beta1/delegators/{}/rewards'.format(RPC_ADDRESS, endpoint)

    available = requests.get(haqq_http_available).json()
    delegated = requests.get(haqq_http_delegated).json()

    unbounding = requests.get(haqq_http_unbounding).json()
    rewards = requests.get(haqq_http_rewards).json()

    try:
        assert available['balances'][0]["denom"] == "aISLM"
        av_amt = int(available['balances'][0]["amount"])/1_000_000_000_000_000_000
    except (IndexError, KeyError):
        av_amt = 0

    try:
        del_amt = 0
        for delega in delegated['delegation_responses']:
            assert delega['balance']["denom"] == "aISLM"
            del_amt += int(delega['balance']["amount"])/1_000_000_000_000_000_000
    except (IndexError, KeyError):
        del_amt = 0


    try:
        unb_amt = 0
        for delega in unbounding['unbonding_responses']:
            assert delega['balance']["denom"] == "aISLM"
            unb_amt += int(delega['balance']["amount"])/1_000_000_000_000_000_000
    except (IndexError, KeyError):
        unb_amt = 0

    try:
        assert rewards['total'][0]["denom"] == "aISLM"
        rew_amt = float(rewards['total'][0]["amount"])/1_000_000_000_000_000_000
    except (IndexError, KeyError):
        rew_amt = 0

    message = '''
*Your Balance Info:*
*Your wallet:* [{wallet}](http://API NODE/haqq/account/{wallet})
🔸 *Available amount:* {av_amt} ISLM.
🔸 *Delegated amount:* {del_amt} ISLM.
🔸 *Unbounding amount:* {unb_amt} ISLM.
🔸 *Staking Reward amount:* {rew_amt} ISLM.
    '''.format(wallet=endpoint, av_amt="%.18f" % round(av_amt,18), del_amt="%.18f" % round(del_amt,18), unb_amt="%.18f" % round(unb_amt,18), rew_amt="%.18f" % round(rew_amt,18))
    return message

def send_balances(update, context):
    try:
        assert update.message.text[:5] == 'haqq1'
        update.message.reply_text(get_wallet_info(endpoint=update.message.text), parse_mode= 'Markdown', disable_web_page_preview=True)
    except AssertionError:
        update.message.reply_text('Пожалуйста, пришлите действительный кошелек haqq')

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    updater = Updater(BOT_TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    dp.add_handler(MessageHandler(Filters.text, send_balances))

    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
