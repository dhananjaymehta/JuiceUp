import random
import sys
import six
from datetime import datetime
from kafka.client import SimpleClient
from kafka.producer import KeyedProducer
source_file = 'test1.csv'
class Producer(object):
    
    def __init__(self, addr):
        self.client = SimpleClient(addr)
        self.producer = KeyedProducer(self.client)

    def produce_msgs(self, source_symbol):
        
        while True:
            f = open(source_file, 'r')
            f.next();
            for line in f:
                data = line.split(",") 
                message_info = line.rstrip();
                ingestion_time = datetime.now().strftime("%Y%m%d %H%M%S")
                available_spots = random.randint(0,10)
                message_info += ","+ingestion_time +","+str(available_spots)
                print message_info
                self.producer.send_messages('new_price_data_part4', source_symbol, message_info)
            f.close()

if __name__ == "__main__":
    args = sys.argv
    ip_addr = str(args[1])
    partition_key = str(args[2])
    prod = Producer(ip_addr)
    prod.produce_msgs(partition_key)
    
