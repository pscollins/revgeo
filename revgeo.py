import requests
import csv
import ipdb
import time
from sys import argv
from time import localtime, strftime


base_string = "http://maps.googleapis.com/maps/api/directions/json"
#fields = ("state","st_case","ve_total","route",
#          "tway_id","tway_id2","latitude","longitud","date"
#          ,"time","date_time","mp")


def build_loc(row, toshift=0):
    lat = row['latitude']
    long = row['longitud']
    if toshift:
        last_long =  int(long[-1]) - 1 if int(long[-1]) else 1
        long = long[:-1] + `last_long`
    return "{0}, {1}".format(lat, long)

def build_output(row, resp):
    loc = resp['routes'][0]['summary']
    dir = resp['routes'][0]['legs'][0]['steps'][0]['html_instructions'].split()[1][3:-4]
    return (row['latitude'], row['longitud'], loc, dir)

outfile = open(argv[2], 'a')
writer = csv.writer(outfile)


log = open("err.txt", 'a')
logwriter = csv.writer(log)

writer.writerow(("Latitude","Longitude","Location","Direction"))



with open(argv[1], 'r') as data:
    fields = data.readline().split(",")
    reader = csv.DictReader(data, fields)
    
    logwriter.writerow(fields + ["Response", "Timestamp"])

    #skip the first argv[3] lines
    for i in range(int(argv[3])):
        reader.next()

    for row in reader:
#        print row
        origin = build_loc(row)
        dest = build_loc(row, 1)
        
#        print origin
#        print dest
        
        r = requests.get(base_string, params={'origin': origin,
                                              'destination':dest,
                                              'sensor':'false'})

#        ipdb.set_trace()  
        
#        print r.status_code
 #       print r.json()
        time.sleep(1)
        
        try:
            print(build_output(row, r.json()))
            writer.writerow(build_output(row, r.json()))
        except IndexError:
            print "Something went wrong! Response: {0}".format(r.json())
            print(row)
            print(r.text)
            print(strftime("%X, %a %d %b", localtime()))
            logwriter.writerow(row.items() + [r.text, strftime("%X, %a %d %b", localtime())])
            time.sleep(3)
