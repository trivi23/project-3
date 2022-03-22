import paho.mqtt.client as mqtt
import pandas as pd
sub_client = mqtt.Client()
sub_client.connect('broker.hivemq.com',1883)
print("broker connected")

sub_client.subscribe('gpcet/ai')

data = []
i = 0
def notification(sub_client,userdata,msg):
    global data
    global i
    k = msg.payload.decode('utf-8')
    k = k.split(': ')
    h = int(k[1].split(',')[0])
    t= int(k[-1][:-1])
    label = 0
    if(h>40 and h<=60):
        label = 1
    elif(h>60 and h<=80):
        label = 2
    elif(h>80 and h<=100):
        label =3
    dummy = []
    dummy.append(h)
    dummy.append(t)
    dummy.append(label)
    data.append(dummy)
    print(i)
    i +=1
    if(i == 300):
        df = pd.DataFrame(data)
        df.to_csv('dataset.csv')
        i=0
sub_client.on_message=notification
sub_client.loop_forever()