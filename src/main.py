import click
import logconfig
import yaml
import sys
import time
#from interchange import interchange
from interchange2 import Recv
from proton.reactor import Container
LOG = logconfig.init_logging("root")

from MQTT import NW3MQTT

@click.command()
@click.option("-config", help="Path to configfile for the application", required=True, type=click.Path(exists=True))

def main(config):
    LOG.info("Starting system")
    try:
        with open(config,'r') as f:
            cfg = yaml.safe_load(f) #Open file and load content to cfg
    except yaml.scanner.ScannerError as e:
        LOG.error("Error reading file: {}".format(config))
        sys.exit(1)    
    
    # reciever = Recv(
    #     cfg["AMQP_URL"], 
    #     10,
    #     cfg["AMQP_ca"],
    #     cfg["AMQP_certfile"],
    #     cfg["AMQP_keyfile"],
    #     cfg["AMQP_keyfile_password"],
    #     cfg["AMQP_source"]
    #     )
    # Container(reciever).run()
    
    # ix = interchange(cfg["AMQP_URL"],
    #     cfg["AMQP_ca"],
    #     cfg["AMQP_certfile"],
    #     cfg["AMQP_keyfile"],
    #     cfg["AMQP_keyfile_password"],cfg["AMQP_source"])
    mqtt = NW3MQTT(cfg["MQTT_URL"],cfg["MQTT_port"],cfg["MQTT_Topics"],cfg["MQTT_ca_cert"],cfg["MQTT_certfile"],cfg["MQTT_keyfile"])
    try:
        while True:
            mqtt()
            time.sleep(0.1)
    except KeyboardInterrupt:
        LOG.info("Stopping system from ctrl+c")
        sys.exit(0)

    #mqtt(cfg["MQTT_Topics"]["publish"],)

if __name__ == '__main__':
    main()
