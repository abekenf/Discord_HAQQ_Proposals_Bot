from datetime import datetime
from time import sleep
import discord
import iso8601
import pytz
from requests import get


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
                    j['submit_time'][:-1]) > datetime.now(tz=pytz.UTC):  # from this moment only later proposals will be highlighting
                number = j['id']
                title = j['title']
                message = f"{text.upper()}\nProposal {number} is in voting stage!\n{title}"
                print(message)

    except Exception as e:  # standard Exception way to display all possible errors while running code
        print(e)


sleep(1800)  # It will check for new proposals every 30 minutes. No need for that with some of the web servers.


client.run('TOKEN') # place you token here
