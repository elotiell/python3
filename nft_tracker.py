from solana.rpc.api import Client
import time
import requests

# Замените 'YOUR_API_KEY' на ваш API ключ от Solana
solana_client = Client('https://api.mainnet-beta.solana.com', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjcmVhdGVkQXQiOjE3MTQ0MjQzNjYwOTAsImVtYWlsIjoia2Vuem9ob2xkQGdtYWlsLmNvbSIsImFjdGlvbiI6InRva2VuLWFwaSIsImlhdCI6MTcxNDQyNDM2Nn0.0LYeZ9_h-QKqYIgqT9VNVp047zLoy17Qo0dKcv0EY6k')

# Замените 'YOUR_TELEGRAM_BOT_TOKEN' на токен вашего Telegram бота
telegram_bot_token = '7127266130:AAER6Jfsu0YVgvv1Hn-gIav2bmubK8z8CdA'

# Замените 'YOUR_CHAT_ID' на ваш Chat ID в Telegram
chat_id = '7127266130:AAER6Jfsu0YVgvv1Hn-gIav2bmubK8z8CdA'

# Список адресов кошельков, которые вы хотите отслеживать
wallet_addresses = ['G7GvPPhwhUZXbgq36eA58LEnG1qU8dwPBpi3yWQaGjPN', 'EXTyiQ5S4cvowZG4AjKFLipMkxa7MtiTUuNYwGs6mohh', 'AtfofJ76WLSTDoWMJBZhwCrqdnv4yudjFjQCGzbYTwHZ','FCciUyYgCRV2yCYdXM7MVKWAEw3PEbqLaAjsG7m4suMB', 'AMkjYfQEPUzTC4DYwXy8Q7RpaLokXVGVbyu2Judg8LoY','9BGfvrHcXsWwgHLwyVsJhA1sTRaGD1aE4NayDRpVtjYd']

def check_nft_received():
    last_checked_slot = solana_client.get_recent_blockhash()['slot']
    
    while True:
        current_slot = solana_client.get_recent_blockhash()['slot']
        transactions = solana_client.get_confirmed_blocks(last_checked_slot, current_slot)
        
        for transaction in transactions:
            for tx in transaction['transactions']:
                for instruction in tx['transaction']['message']['instructions']:
                    if instruction['program'] == 'TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA':
                        if instruction['parsed']['type'] == 'transfer':
                            destination_address = instruction['parsed']['info']['destination']
                            if destination_address in wallet_addresses:
                                send_telegram_message(f"NFT - {destination_address} Received")
        last_checked_slot = current_slot
        time.sleep(10)  # Проверка каждые 10 секунд

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot7127266130:AAER6Jfsu0YVgvv1Hn-gIav2bmubK8z8CdA/sendMessage"
    payload = {
        "7127266130:AAER6Jfsu0YVgvv1Hn-gIav2bmubK8z8CdA": chat_id,
        "NFT RECEIVED": message
    }
    requests.post(url, json=payload)

if __name__ == "__main__":
    check_nft_received()