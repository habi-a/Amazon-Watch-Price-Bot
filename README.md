# Amazon-Watch-Price-Bot

## Setup 

### Add bot to your discord server  
https://discord.com/api/oauth2/authorize?client_id=1173365701709398047&permissions=534723951696&scope=bot  

### Run the bot server side
Install and run on Debian/Ubuntu by running setup.sh with the following synthax:  
```./setup.sh <tokenBot> <guildId> <channelId>```  
NOTE: You can install on differents plateform by replacing in the script aptitude instructions by the right package manager

#### Usage
First search the product you want to monitore:  
```/amazon_search```  
It will return the 5 firsts results in the Amazon search page

Next add the choosen article to the watch list:  
```/amazon_watch```  

You can always check what articles are in the watch list  
```/amazon_watchlist```  

If you want to remove an article from the watchlist  
```/amazon_unwatch```  
