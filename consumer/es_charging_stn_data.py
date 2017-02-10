from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import json, datetime, os, time

from elasticsearch import Elasticsearch


# check if an index is present or not in elasticsearch, if not present create index and mapping
def check_create_index(es, INDEX_NAME):
    if not es.indices.exists(INDEX_NAME):
        os.system('curl -X PUT ec2-52-36-245-111.us-west-2.compute.amazonaws.com:9200/'+INDEX_NAME+'/')

        bb= """curl -X PUT ec2-52-36-245-111.us-west-2.compute.amazonaws.com:9200/+"""+INDEX_NAME+"""/"""+INDEX_NAME+"""/_mapping -d '{"""+
            INDEX_NAME+""" : {
                "properties": {
                    "location": {
                        "type": "geo_point",
                        "lat_lon": true,
                        "geohash": true
                    }
                }
            }
        }'
        """
        os.system(bb)

# insert/update document based on its presence in the index
def create_index(data):
    # connect to the elasticsearch instance
	es = Elasticsearch("ec2-52-36-245-111.us-west-2.compute.amazonaws.com:9200")

	INDEX_NAME = 'charging_station_idx'

   	d = {}
        d['time'] = data[0][0]
        d['charging_station_name'] = data[0][1]
        location = {}
        location['lat'] = data[0][2]
        location['lon'] = data[0][3]
        d['location'] = location
        d['availability'] = data[1]

    # get the details about the document with id = charging_station_name
	res = es.get(index=INDEX_NAME, doc_type=INDEX_NAME, id=data[0][1], ignore=404)

	#if the document with id do not exist, create it
	if not res['found']:
        	es.index(index=INDEX_NAME, doc_type=INDEX_NAME, id=data[0][1], body=d, refresh=True)
	else:
		#update the document
		qq = '{"doc": { "availability":'+str(data[1])+'  }}'
		es.update(index=INDEX_NAME, doc_type=INDEX_NAME,id=data[0][1], body=qq)

	return d

# input is in this format "Fri Sep 25 2015 06:13:28 GMT+0000 (UTC)"
def get_unix_time(ctime):
    time_list = ctime.split()
    # convert to unix ctime 'Tue Sep 15 15:16:58 2015'

    # convert to ctime - this is for hourly analysis and hence ignoring
    time_list = time_list[ :-2]

    temp = time_list[-1]
    time_list[-1] = time_list[-2]
    time_list[-2] = temp

    new_time = " ".join(time_list)
    b = datetime.datetime.strptime(new_time, "%a %b %d %H:%M:%S %Y")
    formatted_time = ""
    formatted_time += str(b.year)+str(b.month)+str(b.day)+str(b.hour)
    return formatted_time

# create tuple of the format((timestamp, name, lat, lon), availability)
def create_tuple(line):
    result = []
    time, station_name, lat, long, available_spots = line[1].split(',')
	result.append(time, station_name, lat, long, available_spots)
	
    #{ (('timestamp' : time, 'station_name' : station_name, 'coords':[lon, lat]),  'available_spots': available_spots )}
    return result;

   

# Create a local StreamingContext with two working thread and batch interval of 5 second
sc = SparkContext("spark://ip-172-31-2-135:7077")

# stream interval of 5 seconds
topic = "charging_station_data"
brokers = "ec2-52-32-40-49.us-west-2.compute.amazonaws.com:9092"
ssc = StreamingContext(sc, 5)
directKafkaStream = KafkaUtils.createDirectStream(ssc, [topic], {"metadata.broker.list": brokers})
#directKafkaStream.repartition(50)

messages = directKafkaStream.flatmap(lambda s: create_tuple(s[1])).reduceByKey(lambda a,b: (int(a)+int(b))/2)
messages1 = messages.filter(lambda s: s[1] > 0)
#messages.print()

es = Elasticsearch("ec2-52-36-245-111.us-west-2.compute.amazonaws.com")

INDEX_NAME = 'charging_stn_loc'

# if index is not present, create it
check_create_index(es, INDEX_NAME)
time.sleep(2)

m2 =messages1.map(lambda s: create_index(s))
m2.pprint()

ssc.start()             # Start the computation
ssc.awaitTermination()  # Wait for the computation to terminate

