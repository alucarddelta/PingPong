import sched, time
import requests
import threading
from pythonping import ping

s = sched.scheduler(time.time, time.sleep)

def do_icmp(x):
    try:
        response_list = ping(x['address'], size=40, count=3, timeout=10)
        rate = response_list.rtt_avg_ms
        if int(response_list.rtt_avg_ms) == 10000 and int(response_list.rtt_max_ms) == 10000 and int(response_list.rtt_min_ms) == 10000:
            rate = 0
        print("ICMP - {} - {} ms".format(x['name'], float(rate)))
        data = {'value': float(rate), 'request': x['xid']}
        try:
            rp = requests.post('http://localhost:5151/app/request_result', json = data)
        except requests.exceptions.ConnectionError:
            return
    except:
        rate = 0
        print("ICMP - {} - {} ms".format(x['name'], float(rate)))
        data = {'value': float(rate), 'request': x['xid']}
        rp = requests.post('http://localhost:5151/app/request_result', json = data)

def do_tcp(x):
    try:
        t = requests.get('http://{}'.format(x['address']))
        if int(t.status_code) == int(x['expected_status']):
            r = t.elapsed.total_seconds()
            print("TCP - {} - {} ms".format(x['name'], r*1000))
    except requests.exceptions.ConnectionError:
        r = 0
        print("TCP - {} - {} ms".format(x['name'], r*1000))
    data = {'value': float(r*1000), 'request': x['xid']}
    try:
        tp = requests.post('http://localhost:5151/app/request_result', json = data)
    except requests.exceptions.ConnectionError:
        return
        

#def do_heartbeat(x):
#    data = {"token": x['token']}
#    t = requests.post('http://{}:{}/app/heartbeat_recieve/beat'.format(x['address'], x['port']), json=data)
#    if int(t.status_code) != 200:
#        print("Error sending Heatbeat to {}, Status code {}".format(x['name'], t.status_code))

def get_targets():
    try:
        r = requests.get('http://localhost:5151/app/get_request').json()
        if r['data'] != None:
            r = r['data']
        else:
            print("No Services")
            r = []
        for x in r:
            if x != None:
                if x['check_type'] == 'ICMP':
                    t = threading.Thread(target=do_icmp, args=[x] )
                if x['check_type'] == 'TCP':
                    t = threading.Thread(target=do_tcp, args=[x] )
                t.start()
    except requests.exceptions.ConnectionError:
        return

#    try:    
#        hs = requests.get('http://localhost:5151/app/heartbeat_send').json()
#        if hs['data'] != None:
#            hs = hs['data']
#        for x in hs:
#            if x != None:
#                do_heartbeat(x)  
#    except requests.exceptions.ConnectionError:
#        return
        #hr = requests.get('http://localhost:5151/app/heartbeat_recieve').json()
        #if hr['data'] != None:
        #    hr = hr['data']
        


def do_it():
    time.sleep(10)
    print("Opening")
    s.enter(1, 1, get_targets, ())
    while True:
        t = threading.Thread(target=s.run())    
        s.enter(60, 1, get_targets, ())