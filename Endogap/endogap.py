import discord
from discord.ext import commands
import re
import time
import urllib.request

class Endogap:
    """Retrieves endorsement gap between Coupers and Resistance"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def endogap(self):
        """Retrieves endorsement gap between Coupers and Resistance"""
		
		# ----------------------------------------------- Set Variables ------------------------------------------------------ #

        # NationStates requires you to identify yourself, or give at least enough basic information so they can contact you
        # if anything goes wrong. I don't know how anything could go wrong with this script, but it is best to provide it
        # regardless.
        user_agent = 'Script info: requests 1 API shard per nation, for two nations at a time. User info: Mount Seymour'
        # Set User-Agent #
        header = {'User-Agent': user_agent}
        
        # Create result lists #
        coup_endos = []
        res_endos = []
        results = []
        
        # ------------------------------------------------- Get Data --------------------------------------------------------- #
        
        coup_nations = ['Funkadelia', 'Killer Kitty', 'Scum', 'Chef Big Dog', 'Aroostook County']
        res_nations = ['Courlany', 'Loftegen', 'Alunya', 'Skadifron']
        
        # ----------------------------------------- Calculate For Every Couper ----------------------------------------------- #
        
        # For every nation in our list #
        for nation in coup_nations:
            # Ask the user to give us the nation's name #
            nation_name = nation
            # Convert nation_name to something the API understands (aka lowercase and underscores) #
            nation_name_url = nation_name.replace(' ', '_')
            nation_name_url = nation_name_url.lower()
        
            # Put the URL together which we'll use to ask the API for our data
            url = 'https://www.nationstates.net/cgi-bin/api.cgi?nation=' + nation_name_url + ';q=census;scale=66'
        
            # Wait one second to respect the API ratelimit
            time.sleep(1)
        
            # Ask the API for our data #
            request = urllib.request.Request(url, None, headers=header)
            # Read the response the API gives us #
            with urllib.request.urlopen(request) as response:
                data = response.read()
        
            # Convert the response to a string
            data = str(data)
        
            # The following line filters out everything between the <SCORE> and </SCORE> tags
            data = re.findall("<SCORE>(.*?)</SCORE>", data)
        
            # Save the items in our list to appropriately named variables
            endorsements = float(data[0])
        
            # Add result to list #
            nation_stat = [nation_name, endorsements]
            coup_endos.append(nation_stat)
            
        coup_lead = max(coup_endos, key=lambda item: item[1])
        coup_lead_name = coup_lead[0]
        coup_lead_endos = coup_lead[1]

        # ------------------------------------ Calculate For Every Resistance Member ------------------------------------------ #
        
        # For every nation in our list #
        for nation in res_nations:
            # Ask the user to give us the nation's name #
            nation_name = nation
            # Convert nation_name to something the API understands (aka lowercase and underscores) #
            nation_name_url = nation_name.replace(' ', '_')
            nation_name_url = nation_name_url.lower()
        
            # Put the URL together which we'll use to ask the API for our data
            url = 'https://www.nationstates.net/cgi-bin/api.cgi?nation=' + nation_name_url + ';q=census;scale=66'
        
            # Wait one second to respect the API ratelimit
            time.sleep(1)
        
            # Ask the API for our data #
            request = urllib.request.Request(url, None, headers=header)
            # Read the response the API gives us #
            with urllib.request.urlopen(request) as response:
                data = response.read()
        
            # Convert the response to a string
            data = str(data)
        
            # The following line filters out everything between the <SCORE> and </SCORE> tags
            data = re.findall("<SCORE>(.*?)</SCORE>", data)
        
            # Save the items in our list to appropriately named variables
            endorsements = float(data[0])
        
            # Add result to list #
            nation_stat = [nation_name, endorsements]
            res_endos.append(nation_stat)
            
        res_lead = max(res_endos, key=lambda item: item[1])
        res_lead_name = res_lead[0]
        res_lead_endos = res_lead[1]
            
        # --------------------------------------------------- Calculate ------------------------------------------------------ #
        
        result = coup_lead_endos - res_lead_endos

        # ---------------------------------------------------- Output -------------------------------------------------------- #

        embed = discord.Embed(
            description="Endorsement Gap",
            colour=0xd0a047)
        embed.add_field(name="**{}** endorsements".format(str(result)), value="between [{}](https://nationstates.net/{}) and [{}](https://nationstates.net/{})".format(coup_lead_name, coup_lead_name, res_lead_name, res_lead_name))
        embed.set_footer(text="{}: {} | {}: {}".format(coup_lead_name, coup_lead_endos, res_lead_name, res_lead_endos))
        await self.bot.say(embed=embed)

def setup(bot):
    bot.add_cog(Endogap(bot))
