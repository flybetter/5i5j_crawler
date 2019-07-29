import time
import sys

import stomp


class MyListener(stomp.ConnectionListener):
    def on_error(self, headers, message):
        print('received an error "%s"' % message)

    def on_message(self, headers, message):
        print('received a message "%s"' % message)


conn = stomp.Connection10([('192.168.105.105', 61613)])
conn.set_listener('', MyListener())
conn.start()
conn.connect('admin', 'admin', wait=True)

conn.subscribe(destination='/queue/test', id=1, ack='auto')


time.sleep(100000)
conn.disconnect()
