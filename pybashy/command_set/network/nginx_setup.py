
class NginxServer():
    def __init__(self,listen_port,listen_ssl): 
        self.listen_port    = '80'
        self.listen_ssl       = '443'
        self.new_server_name  = 'devbiscuits.net'
        self.new_server_root     = '/var/www/devbiscuits.net'
        self.base_server_root    = '/var/www/html'
        self.new_server_index  = 'index index.html index.htm index.nginx-debian.html'
        self.base_server_index = 'index.html'
        self.base_server = '''
server {
    listen {lport} default_server;
    listen [::]:{lport} default_server;
    # SSL configuration
    listen {lport_ssl} ssl default_server;
    listen [::]:{lport_ssl} ssl default_server;
    include snippets/snakeoil.conf;
    root {s_root};
    index {s_index};
    server_name _;
    location / {
        try_files $uri $uri/ =404;
    }
}
'''
        self.server_block_1.format(lport = self.listen_port,
                              lport_ssl  = self.listen_ssl,
                              s_root    = self.base_server_root,
                              s_index   = self.base_server_index
                             )
        self.new_server = '''
server {
    listen {lport};
    listen [::]:{lport};
    server_name {s_name};
    root {s_root};
    index {s_index};
    location / {
        try_files $uri $uri/ =404;
    }
}'''
        self.new_server.format(lport = self.listen_port,
                        lport_ssl    = self.listen_ssl,
                        s_name       = self.new_server_name,
                        s_root       = self.new_server_root,
                        s_index      = self.new_server_index
                       )
        def add_web_sevice():
            pass