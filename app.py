from application import app
if __name__ == "__main__":
    app.run()
    #app.run(host="0.0.0.0",port=4040,debug=True)
# <VirtualHost *:80>
# ServerName mywebsite.com
# ServerAdmin admin@mywebsite.com
# WSGIScriptAlias / /var/www/FlaskApp/flaskapp.wsgi
# <Directory /var/www/FlaskApp/FlaskApp/>
# Order allow,deny
# Allow from all
# </Directory>
# Alias /static /var/www/FlaskApp/FlaskApp/static
# <Directory /var/www/FlaskApp/FlaskApp/static/>
# Order allow,deny
# Allow from all
# </Directory>
# ErrorLog ${APACHE_LOG_DIR}/error.log
# LogLevel warn CustomLog ${APACHE_LOG_DIR}/access.log combined
# </VirtualHost>



# <VirtualHost *:80>
#         # The ServerName directive sets the request scheme, hostname and port that
#         # the server uses to identify itself. This is used when creating
#         # redirection URLs. In the context of virtual hosts, the ServerName
#         # specifies what hostname must appear in the request's Host: header to
#         # match this virtual host. For the default virtual host (this file) this
#         # value is not decisive as it is used as a last resort host regardless.
#         # However, you must set it for any further virtual host explicitly.
#         #ServerName www.example.com
#         ServerName 127.0.0.1
#         ServerAdmin webmaster@localhost

#         WSGIScriptAlias / /var/www/FlaskApp/flaskapp.wsgi 

#         <Directory /var/www/FlaskApp/FlaskApp/static/>
#             Order deny,allow
#             Allow from all
#         </Directory>
#         Alias /static /var/www/FlaskApp/FlaskApp/static
        
#         <Directory /var/www/FlaskApp/FlaskApp/static/>
#             Order allow,deny
#             Allow from all
#         </Directory>
#         # Available loglevels: trace8, ..., trace1, debug, info, notice, warn,
#         # error, crit, alert, emerg.
#         # It is also possible to configure the loglevel for particular
#         # modules, e.g.
#         #LogLevel info ssl:warn

#         ErrorLog ${APACHE_LOG_DIR}/error.log LogLevel warn 
#         CustomLog ${APACHE_LOG_DIR}/access.log combined 

#         # For most configuration files from conf-available/, which are
#         # enabled or disabled at a global level, it is possible to
#         # include a line for only one particular virtual host. For example the
#         # following line enables the CGI configuration for this host only
#         # after it has been globally disabled with "a2disconf".
#         #Include conf-available/serve-cgi-bin.conf
# </VirtualHost>

# # vim: syntax=apache ts=4 sw=4 sts=4 sr noet