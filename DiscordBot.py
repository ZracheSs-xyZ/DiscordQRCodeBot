import discord
from SecretStorage import *
from QRCodeBot import *
from datetime import datetime
from pathlib import Path

#initializing qr folder
from pathlib import Path
Path("qr").mkdir(parents=True, exist_ok=True)

client = discord.Client()

@client.event
async def on_ready():
    print('\nWe are logged in as {0.user}'.format(client))

@client.event
# Listen for an incomming message
async def on_message(message):
    # If the author is the robot itself, then do nothing!
    if message.author == client.user:
        return
    # If the user writes $qr
    if message.content == "$qr":
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print('\n')
        # This for loop check for all the user's DiscordID in the Database
        if str(message.author.id) in ScholarsDict:
            print("This user received his QR Code : " + message.author.name)
            print("Discord ID : " + str(message.author.id))
            print("Current time : ", current_time)
            
            #converting discordID to string
            discordID = str(message.author.id)
            qrImg = 'qr/QRCode-'+discordID+'.png';
            
            # value with discordID
            botPlaceHolders = ScholarsDict[str(message.author.id)]
            # discordID's privateKey from the database
            accountPrivateKey = botPlaceHolders[2]
            # discordID's EthWalletAddress from the database
            accountAddress = botPlaceHolders[1]
            # Get a message from AxieInfinty
            rawMessage = getRawMessage()
            # Sign that message with accountPrivateKey
            signedMessage = getSignMessage(rawMessage, accountPrivateKey)
            # Get an accessToken by submitting the signature to AxieInfinty
            accessToken = submitSignature(signedMessage, rawMessage, accountAddress)
            # Create a QrCode with that accessToken
            QrCode = getQRCode(accessToken,qrImg)
            # Send the QrCode the the user who asked for
            await message.author.send(
                "------------------------------------------------\n\n\nHello " + message.author.name + "\nHere is your new QR Code to login : ")
            await message.author.send(file=discord.File(qrImg))
            return
        else:
            print("This user didn't receive a QR Code : " + message.author.name)
            print("Discord ID : " + str(message.author.id))
            print("Current time : ", current_time)
            return

print('\nThis Discord QR Code Bot has been developed by ZracheSs | xyZ')
print('Thank you for your donations!')
print('Ronin Wallet Address : ronin:a04d88fbd1cf579a83741ad6cd51748a4e2e2b6a')
print('Ethereum Wallet Address : 0x3C133521589daFa7213E5c98C74464a9577bEE01')


#Run the client (This runs first)
client.run(DiscordBotToken)
