import random
import sys
import time
from datetime import datetime
from kafka.client import SimpleClient
from kafka.producer import KeyedProducer
source_file = 'org_charging_stn_data.csv'
target_file = 'charging_station_history_1.csv'
topic = 'charging_stn_data'
import csv


class Producer():
    print("here")
    
    def __init__(self, addr):
        self.client = SimpleClient(addr)
        self.producer = KeyedProducer(self.client)

    def produce_msgs(self, source_symbol):
        
        print(" Simulating sensor data for charging stations....Press Ctrl C to abort..")
        while True:
            with open(source_file) as csvfile:
                for data in csv.reader(csvfile):
                    
                    ingestion_time = datetime.now().strftime("%Y%m%d %H%M%S")
                    
                    available_spots = random.randint(0,10)
                    #datetime, station_name, stnid, lat, lon, city, state, zipcode, connectors, available_spots
                    message = (ingestion_time + ","+ data[1]+ "," + data[27]+ ","+data[24] +"," + data[25] + ","+ data[4] + "," + data[5] + "," + data[6] + "," + data[37] + "," + str(available_spots))  
                    print(message)
                   
                    self.producer.send_messages(topic, source_symbol, message)
            csvfile.close()
            print("***********************Sleeping for 10 seconds**********************************************************")
            time.sleep(10)
            print("********************************************************************************************************")
            
            
                   
            

if __name__ == "__main__":
    args = sys.argv
    ip_addr = str(args[1])
    partition_key = str(args[2])
    prod = Producer(ip_addr)
    prod.produce_msgs(partition_key)
    
