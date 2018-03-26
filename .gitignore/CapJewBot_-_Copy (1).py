import discord
import requests
import threading
import datetime
import asyncio

client = discord.Client()


# Inserts a comma between every 3 chars in a string from the period backwards, if there is no period than from the end.
def number_fixer(number):
    period_place = number.find(".")
    for comma in range(int(period_place/3-0.1)):
        comma_place = period_place - ((comma+1) * 3)
        number = number[:comma_place] + "," + number[comma_place:]
    return number


# Limits the decimal point to eight digits
def decimal_pointer(number):
    return number[:number.find(".")+9]


# Grabs cmc price for coins every five seconds.
def grab_coin_cost():
    threading.Timer(60.0, grab_coin_cost).start()
    global coin_jsons
    coin_jsons = requests.get("https://api.coinmarketcap.com/v1/ticker/?limit=0").json()
    global coin_index
    coin_index = index_coins(coin_jsons)


# Indexes the large json of coins.
def index_coins(coin_jsons):
    coin_index = {}
    for count in range(len(coin_jsons)):
        if (coin_jsons[count]["id"].upper() != coin_jsons[count]["symbol"].upper()):
            coin_index[coin_jsons[count]["id"].upper()] = [count]
        if coin_jsons[count]["symbol"] in coin_index:
            coin_index[coin_jsons[count]["symbol"]].append(count)
        else:
            coin_index[coin_jsons[count]["symbol"]] = [count]
    return coin_index


# Creates an embed for a certain coin's json.
def create_embed(coin_json):
    return 1



@client.event
async def on_ready():
    grab_coin_cost()
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print("Operating in")
    for server in client.servers:
       print(server.name)

@client.event
async def on_message(message):
    if message.author.id != client.user.id:
        print("-----\nRequest from channel id " + message.channel.id + " message id " + message.id + ".\nIt said: " + message.content)
        user_input = message.content.split()

        if len(user_input) > 1:
            # Catches the .cap command
            if user_input[0] == ".cap":

                # Removes the command call from the input
                user_input.remove(user_input[0])

                # Calls global json and index
                global coin_jsons
                global coin_index
                global stuff

                # Goes over every input item fe (.cap eth btc produces 2 items which are eth and btc)
                for count in range(len(user_input)):

                    # Turns the input into uppercase
                    user_input[count] = user_input[count].upper()

                    # Makes sure the input exists in coin_index
                    if user_input[count] in coin_index:

                        # Goes over every value in the coin_index dictionary
                        for coin in coin_index[user_input[count]]:

                            # Grabs the coin_json for the coin requested
                            coin_json = coin_jsons[coin]

                            # Sends the info for that coin as a message
                            embed = discord.Embed(description=":large_orange_diamond: BTC: **" + number_fixer(coin_json["price_btc"]) + "**\n"
                                                              #"<:eth:401849079484645386> ETH: **" + decimal_pointer(number_fixer(str(float(coin_json["price_btc"]) / float(coin_jsons[coin_index["ETHEREUM"][0]]["price_btc"])))) + "**\n"
                                                              ":dollar: USD: **$" + number_fixer(coin_json["price_usd"]) + "**\n"
                                                              ":trophy: Rank: **" + number_fixer(coin_json["rank"]) + "**\n"
                                                              ":moneybag: MarketCap: **$" + number_fixer(coin_json["market_cap_usd"]) + "**\n"
                                                              ":bank: Available Supply: **" + number_fixer(coin_json["available_supply"]) + "** " + coin_json["name"] + "\n"
                                                              ":money_mouth: 24h Volume: **$" + number_fixer(coin_json["24h_volume_usd"]) + "**\n"
                                                              "<:benis:400661513800777740> 1h: **" + number_fixer(coin_json["percent_change_1h"]) + "**\n"
                                                              "<:benis:400661513800777740> 24h: **" + number_fixer(coin_json["percent_change_24h"]) + "**\n"
                                                              "<:benis:400661513800777740> 7d: **" + number_fixer(coin_json["percent_change_7d"]) + "**\n")
                            embed.set_author(name=coin_json["name"], url="https://coinmarketcap.com/currencies/" + coin_json["id"], icon_url = "https://files.coinmarketcap.com/static/img/coins/128x128/" + coin_json["id"] + ".png")
                            await client.send_message(message.channel, embed=embed)

#bot's code
client.run('NDI3OTAzODc4OTYxNTYxNjIw.DZrUjQ.WQrKS9PW2JTQXPwx5KssvNr6Tso')
