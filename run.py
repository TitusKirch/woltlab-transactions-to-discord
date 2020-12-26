import settings
import requests
import os
import json
import sys
import time
from discord_webhook import DiscordWebhook, DiscordEmbed

# get last transaction id
if not os.path.exists(settings.WL_LASTTRANSACTIONID_FILE):
    tmp_file = open(settings.WL_LASTTRANSACTIONID_FILE, "w+")
    tmp_file.write(str(1))
    tmp_file.close()

wl_lastTransactionID_file = open(settings.WL_LASTTRANSACTIONID_FILE, "r")
wl_lastTransactionID = wl_lastTransactionID_file.readline()
wl_lastTransactionID_file.close()

# setup api routes
wl_api_transactions_url = 'https://api.woltlab.com/1.1/vendor/transaction/list.json'
wl_api_transactions_params = {
    "vendorID": settings.WL_VENDORID,
    "apiKey": settings.WL_APIKEY,
    "lastTransactionID": wl_lastTransactionID
}

# make wl api transactions request
wl_api_transactions_response = requests.post(
    wl_api_transactions_url, data=wl_api_transactions_params)

# create discord webhook
dc_webhook = DiscordWebhook(url=settings.DISCORD_WEBHOOK_URL)

if (wl_api_transactions_response.text):

    # get response as json
    wl_api_transactions_response_json = json.loads(
        wl_api_transactions_response.text)

    # check status
    if wl_api_transactions_response_json['status'] != 200:
        sys.exit()

    # handle data
    embed_count = 0
    for transaction in wl_api_transactions_response_json['transactions']:

        # update embed count
        embed_count += 1

        # checl embed count and if max execute message and sleep
        if embed_count > settings.DISCORD_WEBHOOK_MAX_EMBEDS_PER_MESSAGE:
            dc_webhook_response = dc_webhook.execute()
            time.sleep(5)
            embed_count = 1
            dc_webhook = DiscordWebhook(url=settings.DISCORD_WEBHOOK_URL)

        # create discord embed
        dc_embed = DiscordEmbed()

        # check type and set title, color and description
        if transaction['withdrawal']:
            dc_embed.set_title('Withdrawal')
            dc_embed.set_color(settings.DISCORD_EMBED_COLOR_WITHDRAWAL)
            dc_embed.set_description(transaction['reason'])
        else:
            dc_embed.set_title('Purchase')
            dc_embed.set_color(settings.DISCORD_EMBED_COLOR_PURCHASE)
            dc_embed.set_description(transaction['reason'].split('\'')[1])

        # set other data
        dc_embed.add_embed_field(
            name='Credit', value=transaction['credit'] + '€')
        dc_embed.add_embed_field(
            name='Balance', value=transaction['balance'] + '€')
        dc_embed.set_timestamp(transaction['time'])

        # add embed
        dc_webhook.add_embed(dc_embed)

    # execute webhook
    if wl_api_transactions_response_json['count'] % settings.DISCORD_WEBHOOK_MAX_EMBEDS_PER_MESSAGE:
        dc_webhook_response = dc_webhook.execute()

    # update last transaction id if needed
    if (wl_api_transactions_response_json['lastTransactionID'] > 0 and wl_api_transactions_response_json['lastTransactionID'] != wl_lastTransactionID):
        wl_lastTransactionID_file = open(
            settings.WL_LASTTRANSACTIONID_FILE, "w")
        wl_lastTransactionID_file.write(
            str(wl_api_transactions_response_json['lastTransactionID']))
        wl_lastTransactionID_file.close()
