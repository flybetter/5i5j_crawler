import urllib3
import logging


def send():
    logging.getLogger("urllib3").setLevel(logging.DEBUG)
    http = urllib3.PoolManager(retries=urllib3.Retry(5, redirect=1000000))
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
    r = http.request('GET', 'https://nj.5i5j.com/ershoufang/43183776.html', headers=headers)
    print(r.data.decode('utf-8'))
    print(r.headers)


if __name__ == '__main__':
    send()
