import stomp
import time


def test():
    conn = stomp.Connection10([('192.168.10.221', 61613)])
    conn.connect()
    conn.send(
        body='{"id": 21169, "cityCode": "nj", "platformId": 2, "houseId": "103107011075", "url": "https://nj.lianjia.com/ershoufang/103107011075.html", "title": "金地名京 3室2厅 780万", "district": "建邺", "subDistrict": "湖西街", "blockName": "金地名京", "blockId": "1411000000346", "totalPrice": 780.0, "unitPrice": 52349.0, "roomCount": 3, "hallCount": 2, "toiletCount": 2, "totalFloor": 11, "floorCode": 3, "forward": "南北", "decoration": "精装", "buildArea": 149.0, "buildYear": 2010, "official_id": null, "propertyRightYear": 70, "listTime": null, "hasLift": 1, "is_process": 1, "percent": null, "create_time": 1574293926000}',
        destination='/queue/handler')
    # time.sleep(1)
    conn.disconnect()


sql = "select cityCode,platformId,houseId,url,title,district,subDistrict,blockName,blockId,totalPrice,unitPrice,roomCount,hallCount,toiletCount,totalFloor,floorCode,forward,decoration,buildArea,buildYear,propertyRightYear,listTime,hasLift from     crawl_sell_compare_copy order by id desc limit 10;"

if __name__ == '__main__':
    test()
