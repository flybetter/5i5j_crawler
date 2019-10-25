import sys
import time
import sys
import stomp


class MyListener(object):
    def on_error(self, headers, message):
        print('received an error %s' % message)

    def on_message(self, headers, message):
        print('received a message %s' % headers)


if __name__ == '__main__':
    conn = stomp.Connection10([('192.168.10.221', 61613)])
    conn.set_listener('logicServerQueue', MyListener())
    conn.start()
    conn.connect(wait=True)
    conn.subscribe(destination='testQueue', headers={'selector': "consumerId = '88.3@6006'"})
    while True:
        try:
            time.sleep(1)
        except:
            break
