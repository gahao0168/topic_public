# publish

# Import standard python modules.
import sys
import time

# Import Adafruit IO MQTT client.
from Adafruit_IO import MQTTClient

from ttyd.models import FeedTime
from datetime import datetime

from my_secrets import secrets

ADAFRUIT_IO_USERNAME = secrets.ADAFRUIT_IO_USERNAME
ADAFRUIT_IO_KEY = secrets.ADAFRUIT_IO_KEY

# Topic Name
topic_name = 'TTYD'
topic_feed_one = 'feedtime'


# Define callback functions which will be called when certain events happen.
def connected(client):
    # Connected function will be called when the client is connected to Adafruit IO.
    # This is a good place to subscribe to topic changes.  The client parameter
    # passed to this function is the Adafruit IO MQTT client so you can make
    # calls against it easily.
    print(f'Listening for changes on {topic_name}.{topic_feed_one}')
    # Subscribe
    client.subscribe(f'{topic_name}.{topic_feed_one}')

def disconnected(client):
    # Disconnected function will be called when the client disconnects.
    print('Disconnected from Adafruit IO!')
    sys.exit(1)

def message(client, topic_id, payload):
    # Message function will be called when a subscribed topic has a new value.
    # The topic_id parameter identifies the topic, and the payload parameter has
    # the new value.
    if payload == "remsg":
        user = FeedTime.objects.filter(username=username)
        pre_feedtime = datetime.now().strftime('%Y-%m-%d %H:%M')
        user.update(pre_feedtime=pre_feedtime)
    print('從 {0} 收到新的值: {1}'.format(topic_id, payload))

def pub(value, user):
    global username
    username = user
    client.publish(topic_feed_one, value, topic_name)
    print('Publishing {0} to {1}.{2}.'.format(value, topic_name, topic_feed_one))
    time.sleep(3)


# Create an MQTT client instance.
client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Setup the callback functions defined above.
client.on_connect    = connected
client.on_disconnect = disconnected
client.on_message    = message

# Connect to the Adafruit IO server.
client.connect()

# Now the program needs to use a client loop function to ensure messages are
# sent and received.  There are a few options for driving the message loop,
# depending on what your program needs to do.

# The first option is to run a thread in the background so you can continue
# doing things in your program.
client.loop_background()

# Now send new values every 5 seconds.
# print('Publishing a new message every 5 seconds (press Ctrl-C to quit)...')
