from pycoingecko import CoinGeckoAPI
from telegram import Bot
import asyncio
import time
import creds

def price_tracking():
    cg = CoinGeckoAPI()
    k = int(input("Enter the number of crypto currencies: "))
    targets = {}
    for i in range(k):
        currency = input("Enter crypto currency: ").lower()
        value = float(input("Enter the targeted value [$]: "))
        targets[currency] = value

    while True:
        hit_target = {}

        for crypto, target_price in targets.items():
            response = cg.get_price(ids=crypto, vs_currencies='usd')
            current_price = response[crypto]['usd']
            
            if current_price >= target_price:
                hit_target[crypto] = current_price
        
        if hit_target:
            message = ''
            for crypto, value in hit_target.items():
                current_price = value
                target_price = targets[crypto]
                message += (f'{crypto.upper()}\n'
                            f'Current price: ${current_price}\n'
                            f'Your target price: ${target_price}\n\n')
            asyncio.run(send_telegram_mess(message))
            # Remove the crypto from targets once the target is reached
            for crypto in hit_target:
                del targets[crypto]
        
        if not targets:
            print("All targets have been reached.")
            break

        time.sleep(60)

async def send_telegram_mess(message):
    

    bot = Bot(token=creds.bot_token)
    await bot.send_message(chat_id=creds.chatID, text=message)

price_tracking()