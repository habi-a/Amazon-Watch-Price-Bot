# Amazon-Watch-Price-Bot

## Setup

### Add bot to your discord server  
https://discord.com/api/oauth2/authorize?client_id=1173365701709398047&permissions=534723951696&scope=bot  

### Run the bot server side
Install and run on Debian/Ubuntu by running setup.sh with the following synthax:  
```./setup.sh <tokenBot>```  

#### Usage
First search the product you want to watch:  
```/amazon_search```  
It will return the 5 firsts results in the Amazon search page

Next add the choosen article to the watchlist:  
```/amazon_watch```  

You can always check what articles are in the watchlist  
```/amazon_watchlist```  

If you want to remove an article from the watchlist  
```/amazon_unwatch```  
