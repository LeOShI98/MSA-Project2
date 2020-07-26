import random
import time
from azure.iot.device import IoTHubDeviceClient, Message

CONNECTION_STRING1 = "HostName=IoT-hub-Leo.azure-devices.net;DeviceId=Device1;SharedAccessKey=Q9+hW/I4gFKYVqSk3bRyyK//2PiKclWQN75n/sqR9z0="
CONNECTION_STRING2 = "HostName=IoT-hub-Leo.azure-devices.net;DeviceId=Device2;SharedAccessKey=YSgdpATm+WET0v5OFEtlTX2JevGkG2nFER5j4O+JhSc="
CONNECTION_STRING3 = "HostName=IoT-hub-Leo.azure-devices.net;DeviceId=Device3;SharedAccessKey=aJ2n+AWa0RThxHG/LOr+pvJrE85hrSvTJSYB/t2AP/k="
PERCENTAGE = 20
MSG_TXT = '{{"diving_depth": {diving_depth},"duration": {duration},"diverID":{diverID},"state":{state}}}'
DIVING_DEPTH_MIN = 9
DIVING_DEPTH_MAX = 18
DURATION_MAX = 30
DURATION_MIN = 5


diving_depth1 = 9
diving_depth2 = 9
diving_depth3 = 9
duration1 =7 
duration2 =7
duration3 =7
#STATE = ["WA","VIC","NSW","QLD","SA","TAS"]




# Generate Data
def data_gen(current_value,min_value,max_value):
  value = current_value*(1+((PERCENTAGE/100)*(2*random.random()-1)))
  value = max(value,min_value)
  value = min(value,max_value)
  return value

# Create an IoT Hub client
def iothub_client_init(c_string):
    client = IoTHubDeviceClient.create_from_connection_string(c_string)
    return client

# Build message to be sent to IoT Hub
def buid_message(diving_depth, duration,diverID):
    ranint = random.randint(0,5)
    #state =STATE[ranint]
    json = MSG_TXT.format(diving_depth=diving_depth, duration=duration, diverID=diverID,state = ranint)
    message = Message(json)
    return message


# Create Client and Send Messgae
def iothub_client_telemetry_sample_run():

    try:
        client1 = iothub_client_init(CONNECTION_STRING1)
        client2 = iothub_client_init(CONNECTION_STRING2)
        client3 = iothub_client_init(CONNECTION_STRING3)
        print ( "IoT Hub device sending periodic messages, press Ctrl-C to exit" )

        while True:
            # Build the message with simulated telemetry values.
            global diving_depth1
            global diving_depth2
            global diving_depth3
            global duration1
            global duration2
            global duration3

            diving_depth1 = data_gen(diving_depth1,DIVING_DEPTH_MIN, DIVING_DEPTH_MAX)
            duration1 = data_gen(duration1,DURATION_MIN,DURATION_MAX)
            message1 = buid_message(diving_depth1, duration1,'1')

            diving_depth2 = data_gen(diving_depth2,DIVING_DEPTH_MIN, DIVING_DEPTH_MAX)
            duration2 = data_gen(duration2,DURATION_MIN,DURATION_MAX)
            message2 = buid_message(diving_depth2, duration2,'2')

            diving_depth3 = data_gen(diving_depth3,DIVING_DEPTH_MIN, DIVING_DEPTH_MAX)
            duration3 = data_gen(duration3,DURATION_MIN,DURATION_MAX)
            message3 = buid_message(diving_depth3, duration3,'3')

    

            # Send the message.
            print( "Sending message1: {}".format(message1) )
            print( "Sending message2: {}".format(message2) )
            print( "Sending message3: {}".format(message3) )
            client1.send_message(message1)
            client2.send_message(message2)
            client3.send_message(message3)



            print ( "Message successfully sent" )
            time.sleep(2)

    except KeyboardInterrupt:
        print ( "IoTHubClient stopped" )

if __name__ == '__main__':
    print ( "Simulating Devices..." )
    print ( "Press Ctrl-C to exit" )
    iothub_client_telemetry_sample_run()