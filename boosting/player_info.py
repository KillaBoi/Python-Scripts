from steam.client import SteamClient
from csgo.client import CSGOClient
from csgo.enums import ECsgoGCMsg, ECsgoSteamUserStat
from steam.steamid import SteamID
import logging
#logging.basicConfig(format='[%(asctime)s] %(levelname)s %(name)s: %(message)s', level=logging.DEBUG)

client = SteamClient()
cs = CSGOClient(client)


@client.on('logged_on')
def start_csgo():
    cs.launch()


@cs.on('ready')
def gc_ready():
    old_experience = ""
    while True:
        accountid = SteamID() # Enter SteamID64 here
        #print(accountid.id)
        # send messages to gc
        cs.request_player_profile(accountid.id)
        response, = cs.wait_event('player_profile')
        current_private_rank = response.player_level
        current_experience = str(response.player_cur_xp)[-4:]
        if current_experience == old_experience:
            print("Current Level: " + str(current_private_rank))
            print("Current Experience: " + current_experience)
        else:
            print("WE EARNED XP!")
            print("Current Level: " + str(current_private_rank))
            print("Current Experience: " + current_experience)
            old_experience = current_experience

        client.sleep(10)


client.cli_login(username="", password="") # Enter Username and Password Here.
client.run_forever()
