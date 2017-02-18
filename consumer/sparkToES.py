from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from elasticsearch import Elasticsearch
import math

ES_INDEX = 'geo_charging_stn_loc'


#convert csv data to json format
def create_json(line):
   
    dtime, station_name, stn_id, lat, lon, city, state, zipcode, connectors, available_spots = line[1].split("|")
    
    return {"event_time": str(dtime),   "location" : [float(lon), float(lat)]  , "station_id" : stn_id , "station_name" : station_name, "city": city, "state":state, "zipcode": zipcode, "connectors":connectors,  "available_spots": available_spots }
            
   
def sendToES(line) :
    
    es = Elasticsearch(['ec2-52-36-245-111.us-west-2.compute.amazonaws.com'], http_auth=('elastic', 'changeme'), verify_certs=False)
    
    es.index(index='geo_charging_stn_loc', doc_type='stations' , body=line )
    

   
def main():
    # Create a local StreamingContext with two working thread and batch interval of 5 second
    sc = SparkContext("spark://ip-172-31-2-135:7077")
            
    # stream interval of 5 seconds
    topic = "topic_stream"
    brokers = "ec2-52-32-103-136.us-west-2.compute.amazonaws.com:9092, ec2-35-163-79-107.us-west-2.compute.amazonaws.com:9092, ec2-52-32-40-49.us-west-2.compute.amazonaws.com:9092"
    ssc = StreamingContext(sc, 5)
    directKafkaStream = KafkaUtils.createDirectStream(ssc, [topic], {"metadata.broker.list": brokers})
    
    messages = directKafkaStream.map(create_json)
    messages.foreachRDD(lambda rdd : rdd.foreach(sendToES))

    ssc.start()             # Start the computation
    ssc.awaitTermination()  # Wait for the computation to terminate

if __name__ == '__main__':
    main()
