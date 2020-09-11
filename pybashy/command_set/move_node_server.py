TODO: jsonify and stepify this


cd /home/<redacted>/api
git pull

cd /home/<redacted>
sudo mkdir -p /var/www/api
sudo rsync -avr /home/<redacted>/api/* /var/www/api --exclude=.git --exclude=.gitignore --exclude=README.md --exclude=node_modules --exclude=.env

sudo mkdir -p /etc/systemd/system/nodeapi.service.d
sudo rm -f /etc/systemd/system/nodeapi.service.d/local.conf
sudo touch /etc/systemd/system/nodeapi.service.d/local.conf

printf '%s\n%s\n%s\n%s\n%s\n%s\n' '[Service]' 'Environment="DBUSER=<redacted>"' 'Environment="DBPW=<redacted>"' 'Environment="DBPORT=<redacted>"' 'Environment="PORT=<redacted>"' 'Environment="DEBUG_LEVEL=0"' | sudo tee -a /etc/systemd/system/nodeapi.service.d/local.conf

sudo systemctl daemon-reload

cd /var/www/api
sudo npm install

sudo service nodeapi restart
