import stomp
import time


def test():
    conn = stomp.Connection10([('192.168.10.109', 61613)])
    conn.connect()
    conn.send(
        body='{"blockId":"284700","blockName":"江山大厦","buildArea":48.0,"buildYear":0,"cityCode":"nj","decoration":"精装","district":"江宁","floorCode":2,"forward":"南北","hallCount":1,"hasLift":0,"houseId":"42610537","id":0,"listTime":"20191117","platformId":5,"propertyRightYear":0,"roomCount":2,"subDistrict":"竹山路","title":"科学园竹山路 江山大厦 精装两房 随时看房","toiletCount":0,"totalFloor":11,"totalPrice":149.0,"unitPrice":31000.0,"url":"https://nj.5i5j.com/ershoufang/42610537.html"}',
        destination='/queue/handler')
    time.sleep(2)
    conn.disconnect()


if __name__ == '__main__':
    test()
