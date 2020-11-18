from proton import Message, SSLDomain
from proton.handlers import MessagingHandler
from proton.reactor import Container



class Recv(MessagingHandler):
    def __init__(self, url, count, ca, cert,keyfile,keyfilepassword,queue):
        super(Recv, self).__init__()
        self.url = url
        self.expected = count
        self.received = 0
        self.ca = ca
        self.cert = cert
        self.keyfile = keyfile
        self.keyfilepassword = keyfilepassword
        self.queue = queue

    def on_start(self, event): 
        event.container.ssl.client.set_trusted_ca_db(self.ca)
        event.container.ssl.client.set_peer_authentication(SSLDomain.ANONYMOUS_PEER) 
        event.container.ssl.client.set_credentials(self.cert,  self.keyfile, self.keyfilepassword) 
        url =self.url# + "/" + self.queue
        event.container.create_receiver(url)

    def on_message(self, event): 
        if event.message.id and event.message.id < self.received:
            # ignore duplicate message
            return
        if self.expected == 0 or self.received < self.expected:
            print(event.message.body)
            self.received += 1
            if self.received == self.expected:
                event.receiver.close()
                event.connection.close()

# parser = optparse.OptionParser(usage="usage: %prog [options]")
# parser.add_option("-a", "--address", default="localhost:5672/examples",
#                   help="address from which messages are received (default %default)")
# parser.add_option("-m", "--messages", type="int", default=100,
#                   help="number of messages to receive; 0 receives indefinitely (default %default)")
# opts, args = parser.parse_args()

# try:
    
# except KeyboardInterrupt: pass