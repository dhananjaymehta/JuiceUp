import random,csv
import sys
import time, yaml
from datetime import datetime
from kafka.client import SimpleClient
from kafka.producer import KeyedProducer




with open("config-properties.yaml", 'r') as props:
	try:
		CONFIG = yaml.load(props)
	except yaml.YAMLError as error:
		print(error)

source_file = CONFIG['SOURCE_FILE']
topic = CONFIG['TOPIC']


class Producer():
    print("here")
    
    def __init__(self, addr):
        self.client = SimpleClient(addr)
        self.producer = KeyedProducer(self.client)
        self.countZeroOutlets =0
        
    #Sum the values in the EV Level 1, EV Level 2 and DC Fast count fields
    def getNumberOfChargingOutlets(self,data):
        level1 = data[17] 
        level2 = data[18]
        dcfast = data[19]
        
        if level1 is None or level1 == "":
            level1 = 0
        if level2 is None or level2 == "":
            level2 = 0
        if dcfast is None or dcfast == "":
            dcfast = 0
        
        if level1 == 0 and level2 == 0 and dcfast == 0 :
            self.countZeroOutlets += 1
            return 0
        
        return int(level1) + int(level2) + int(dcfast) 
    
    
    #NREL API data is not updated in real time, so simulate open spots count based on hour of the day
    def simulateOpenSpots(self,totalCount, dtime,status):
        hour = dtime.split()[1][:2]
        
        #If the status of the charging station is P as in 'Planned' then return 0 as there are no outlets in use
        if (status == '' or status == 'P'):
            return 0
        #If the status of the charging station is 'E' - In use or 'T' - Temporarily out of service but does not include a count then return 1 as atleast one outlet must be at this charging station
        if (totalCount == 0):
            return 1
        
        if hour < 7 and hour > 21 :
            return random.randint(int(totalCount)/2 , totalCount)
        else:
            return random.randint(0, int(totalCount)/2) 
               
            
        
        
    def produce_msgs(self, source_symbol):
        
        print(" Simulating sensor data for charging stations....Press Ctrl C to abort..")
        print (" Streaming to Kafka topic : " + topic)
        while True:
            self.countZeroOutlets = 0
            with open(source_file) as csvfile:
                csvreader = csv.reader(csvfile)
                csvreader.next()
                
                for data in csvreader:
                    ingestion_time = datetime.now().strftime("%Y%m%d %H%M%S")
                    total_spots = self.getNumberOfChargingOutlets(data)
                    status_code = data[9].strip()
                    available_spots = self.simulateOpenSpots(total_spots, ingestion_time, status_code)
                    #(datetime, station_name, street, status_code, stnid, lat, lon, city, state, zipcode, connectors,other EV type, available_spots)
                    message = (str(ingestion_time) + "|"+ data[1]+ "|" + data[2]+ "|" + data[9]+ "|" +data[27]+ "|"+data[24] +"|" + data[25] + "|"+ data[4] + "|" + data[5] + "|" + data[6] + "|" + str(data[37]) + "|"+ str(data[20]) +"|" + str(available_spots) )  
                    print(message)
                    self.producer.send_messages(topic, source_symbol, message)
                   
                csvfile.close()
                print("Charging stations with zero outlets === ",self.countZeroOutlets)
                print("***********************Sleeping for 10 seconds**********************************************************")
                time.sleep(10)
                print("********************************************************************************************************")
               
                   
            

if __name__ == "__main__":
    args = sys.argv
    ip_addr = str(args[1])
    partition_key = str(args[2])
    prod = Producer(ip_addr)
    prod.produce_msgs(partition_key)
    
