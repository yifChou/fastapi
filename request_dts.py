import requests
import  time
import random
from ramdom_sequence import save_dts_batch_record
headers ={
    "Content-Type":"application/json",
}

def shipping_order(shipping_number,bag_number,waybills,url = "http://192.168.88.175:5000",system_code="YT"):
    '''
    发货单创建-并绑定袋子
    :param shipping_number: 发货单号
    :param bag_number: 袋子数量
    :param waybills: 运单数量
    :return:
    '''
    bag_list =[]
    if type(bag_number) == int:
        for i in range(bag_number):
            data = add_bag(YD_order(waybill_number="YIF", sum=waybills), update_type="A", system_code="YT")
            print(data)
            response = requests.post(url=url + "/api/ExternalApi/AddBagInfo", json=data)
            print(response.text)
            bag_list.append(data["bag_number"])
    elif type(bag_number) == list:
        for i in bag_number:
            data = add_bag(YD_order(waybill_number="YIF", sum=waybills), update_type="A", system_code="YT")
            data["bag_number"] = i
            print(data)
            response = requests.post(url=url + "/api/ExternalApi/AddBagInfo", json=data)
            print(response.text)
            bag_list.append(data["bag_number"])
    data={
     "over_weight": random.randint(1,20),
     "shipping_type": random.choice([1,2]),
     "service_code": "CC",
     "loading_type": random.choice([1,2]),
     "car_type": random.choice([1,2]),
     "shipping_number": shipping_number,
     "shipping_location": "74",
     "departure_time": time.strftime("%Y-%m-%d %H:%M:%S"),
     "destinationai_time": time.strftime("%Y-%m-%d %H:%M:%S"),
     "car_number": "car"+time.strftime("%Y%m%d"),
     "destination": "深圳",
     "is_need": "Y",
     "bag_numbers":bag_list,
     "system_code":system_code
     }
    print(data)
    response = requests.post(url=url + "/api/ExternalApi/CreateShipment",json=data)
    if "发货单号已存在" not in response.text:
        print(response.text)
    else:
        print("发货单请求地址："+url,response.text)
    return bag_list

def order(waybill_number):
    data = {"waybill_number": waybill_number + time.strftime("%m%d%H%M%S")+str(random.randint(10000,99999))+str(random.randint(10000,99999)),
            "refer_number": waybill_number + str(random.randint(1000, 9999)),
            "server_type": str(random.randint(1, 4)),
            "package_weight": str(random.randint(10, 100)),
            "weight_type": str(random.randint(1, 4)),
            "package_long": str(random.randint(100, 1000)),
            "package_width": str(random.randint(1000, 10000)),
            "package_high": str(random.randint(1000, 10000)),
            "label_url": "label" + waybill_number + str(random.randint(1000, 10000)),
            "label_size": "label_size" + waybill_number + str(random.randint(1, 4))}
    return data
def order_exist(waybill_number):
    data = {"waybill_number": waybill_number,
            "refer_number": waybill_number + str(random.randint(1000, 9999)),
            "server_type": str(random.randint(1, 4)),
            "package_weight": str(random.randint(10, 100)),
            "weight_type": str(random.randint(1, 4)),
            "package_long": str(random.randint(100, 1000)),
            "package_width": str(random.randint(1000, 10000)),
            "package_high": str(random.randint(1000, 10000)),
            "label_url": "label" + waybill_number + str(random.randint(1000, 10000)),
            "label_size": "label_size" + waybill_number + str(random.randint(1, 4))}
    return data
def YD_order_exist(list_waybill):
    list_data = []
    for i in list_waybill:
        list_data.append(order_exist(i))
    return list_data
def YD_order(waybill_number,sum):
    list_data =[]
    for i in range(sum):
        list_data.append(order(waybill_number))
    return list_data
def add_bag(waybills,update_type,system_code="YT"):
    server_list = ['B','P','D']
    data = {
 "bag_number":"TE"+time.strftime("%m%d%H%M%S")+str(random.randint(1000,9999))+str(random.randint(1000,9999)),
 "bag_weight":random.random(),
 "bag_volume_weight":str(random.randint(10,100)),
 "bag_long":str(random.randint(10,100)),
 "bag_width":str(random.randint(10,100)),
 "bag_high":str(random.randint(10,100)),
 "product_type": random.choice(server_list),#"channel_code":random.choice(server_list),
 "server_type":str(random.randint(1,4)),
 "rfid_code":"rfid_code"+time.strftime("%Y%m%d%H%M%S"),
 "rfid_lable_code":"rfid_lable_code"+time.strftime("%Y%m%d%H%M%S"),
 "update_type":update_type,#新增A 修改E 删除D
 "waybills":waybills,
 "system_code":system_code,
 "bag_overweight": 111.111,
"bag_overlength": 222.222,
"bag_overwidth": 333.333,
"bag_overheight": 444.444,
 }
    print(data["bag_number"])
    return data
def add_shipping(shipping_number):
    response = requests.post(url="http://192.168.88.175:5000/api/ExternalApi/CreateShipment",json=shipping_order(shipping_number))
    if "发货单号已存在" not in response.text:
        print(response.text)

def add_shipping_bags(shiping,number):
    '''参数填写 发货单号，袋子号'''
    data = add_bag(shiping,YD_order(waybill_number="YIF",sum=number))
    print(data)
    response = requests.post(url="http://192.168.88.175:5000/api/ExternalApi/AddBagInfo",json=data)
    print(response.text)
def update_shipping_bags(number,type,bag_number):
    '''参数填写 发货单号，运单数量 更新操作【新增，修改，删除】'''
    data = add_bag(YD_order(waybill_number="YD",sum=number),update_type=type)
    if type=="A":
        data=data
        print(data)
    elif type=="E":
        data["bag_number"]=bag_number
        print(data)
    elif type=="D":
        data["bag_number"] = bag_number
        print(data)
    response = requests.post(url="http://192.168.88.175:5000/api/ExternalApi/UpadateBagInfo",json=data,headers=headers)
    print(response.text)

#update_shipping_bags(shiping="test2019120200",number=3,type="E",bag_number="OS120216504072632620")
# for shipping in range(2,2000):
#     shipping_code = "tests20191223000" + str(shipping)
#     for i in range(500):
#         add_shipping_bags(shipping_code, random.choice([100, 120, 130, 140, 150, 160, 80, 90,70]))
#     print(shipping_code)
def batch_creation_old(batch_number,bag_list,url = "http://192.168.88.175:5000",system_code="YT"):
    '''
    发货单创建-并绑定袋子
    :param shipping_number: 发货单号
    :param bag_list: 袋子
    :return:
    '''
    if url =="http://192.168.88.175:5000":
        product_line_name = random.choice(["AMS-IT-CP","新增推送代码","测试路由","AMS-MA-P-BK"]) #
    #["ASDSD","AMS的产品线2","AMS的产品线","特惠普货","测试02","末端-有空运清关1","末端-有空运清关","ASDSD","AMS的产品线2","AMS的产品线","末端","test2"]
    elif url =="http://dts.uat.yunexpress.com":
        product_line_name = random.choice(["ASDSD", "AMS的产品线2", "AMS的产品线", "测试02"])
    else:
        product_line_name = random.choice(["推送产品线测试","合并路由","AMS-MA-P-BK","AMS-IT-CP"])
    tape_color = random.choice(["青,青","蓝蓝","紫紫","赤赤","橙橙","黄黄","绿绿"])
    product_type=['B','P','D']
    data={"batch_number":batch_number,
            "product_line_name":product_line_name,
            "tape_color":tape_color,
            "product_type": random.choice(product_type),
            "og_id":74,
            "shipping_time":time.strftime("%Y-%m-%d %H:%M:%S"),
            "bag_numbers":bag_list,
            "system_code": system_code
          }
    print(data)
    response = requests.post(url=url + "/api/ExternalApi/CreateBatch",json=data)
    print("批次请求地址："+url,response.text)
    return response.text

def batch_creation(batch_number,bag_number,waybills):
    '''
    发货单创建-并绑定袋子
    :param shipping_number: 发货单号
    :param bag_number: 袋子数量
    :param waybills: 运单数量
    :return:
    '''
    bag_list =[]
    for i  in range(bag_number):
        data = add_bag(YD_order(waybill_number="YIF", sum=waybills),update_type="A")
        print(data)
        response = requests.post(url="http://192.168.88.175:5000/api/ExternalApi/AddBagInfo", json=data)
        print(response.text)
        bag_list.append(data["bag_number"])
    product_line_name = random.choice([ "AMS-MA-P-BK", "LAX-SK-USPS", "AMS-IT-CP","LHR-RM-P"])
    data={"batch_number":batch_number,
            "product_line_name":random.choice(product_line_name),
            "product_type": "D",
            "tape_color":"胶带颜色",
            "og_id":74,
            "shipping_time":time.strftime("%Y-%m-%d %H:%M:%S"),
            "bag_numbers":bag_list
          }
    print(data)
    response = requests.post(url="http://192.168.88.175:5000/api/ExternalApi/CreateBatch",json=data)
    print(response.text)
    return response.text

def dts_batch_get(url,bag_number,waybills,patch_number):
    '''
    :param url:请求地址
    :param bag_number:每个批次袋子数量
    :param waybills:每个批次运单数量
    :param patch_number: 生成多少个批次
    :return:
    '''
    dts_batch_data = save_dts_batch_record(input_batch_number=patch_number)
    if dts_batch_data[0]:
        number = dts_batch_data[1]  # 2020081810 批次号
        patch_number = patch_number #10 多少个批次
        bag_number = bag_number
        waybills = waybills
        systemcode = "YT"
        if systemcode:
            if type(bag_number) == int:
                res_list = []
                for i in range(patch_number):
                    '''线上环境脚本'''
                    bag_list = shipping_order(shipping_number="send_" + str(number + i), bag_number=bag_number,
                                              waybills=waybills,
                                              url=url, system_code=systemcode)
                    res_batch = batch_creation_old(batch_number="BA_" + str(number + (i + 1)), bag_list=bag_list, url=url
                                       , system_code=systemcode)
                    res_list.append(res_batch)
                return {"data":"成功!!! 批次生成"+str(patch_number)+"条,请到【空运配板】查看数据",
                        "detail":res_list}
    else:
        return {"error":"遇到错误,请重新请求生成数据"}
def dts_batch_baglist_get(url,bag_list,waybills):
    '''
    :param url:请求地址
    :param bag_number:袋子是list
    :param waybills:每个批次运单数量
    :param patch_number: 生成多少个批次
    :return:
    '''
    # 袋子可以填数量也可以填数组
    # bag_number = [['BAG033002043020', 'BAG033002043021', 'BAG033002043022', 'BAG033002043023', 'BAG033002043024', 'BAG033002043025', 'BAG033002043026', 'BAG033002043027', 'BAG033002043028', 'BAG033002043029', 'BAG033002043030', 'BAG033002043031', 'BAG033002043032', 'BAG033002043033', 'BAG033002043034', 'BAG033002043035', 'BAG033002043036', 'BAG033002043037', 'BAG033002043038', 'BAG033002043039', 'BAG033002043040', 'BAG033002043041']]
    # bag_number = [['BAG033002072010', 'BAG033002072011', 'BAG033002072012', 'BAG033002072013', 'BAG033002072014', 'BAG033002072015', 'BAG033002072016', 'BAG033002072017', 'BAG033002072018', 'BAG033002072019', 'BAG033002072020', 'BAG033002072021', 'BAG033002072022', 'BAG033002072023', 'BAG033002072024', 'BAG033002072025', 'BAG033002072026', 'BAG033002072027', 'BAG033002072028', 'BAG033002072029', 'BAG033002072030', 'BAG033002072031', 'BAG033002072032', 'BAG033002072033', 'BAG033002072034', 'BAG033002072035', 'BAG033002072036', 'BAG033002072037', 'BAG033002072038', 'BAG033002072039', 'BAG033002072040', 'BAG033002072041', 'BAG033002072042', 'BAG033002072043', 'BAG033002072044', 'BAG033002072045', 'BAG033002072046']]
    # bag_number = [['BAG033002462910', 'BAG033002462911', 'BAG033002462912', 'BAG033002462913', 'BAG033002462914', 'BAG033002462915', 'BAG033002462916', 'BAG033002462917', 'BAG033002462918', 'BAG033002462919']]
    # bag_number = [['BAG033002081710', 'BAG033002081711', 'BAG033002081712', 'BAG033002081713', 'BAG033002081714', 'BAG033002081715', 'BAG033002081716', 'BAG033002081717', 'BAG033002081718', 'BAG033002081719', 'BAG033002081720', 'BAG033002081721', 'BAG033002081722', 'BAG033002081723', 'BAG033002081724', 'BAG033002081725', 'BAG033002081726', 'BAG033002081727', 'BAG033002081728', 'BAG033002081729', 'BAG033002081730', 'BAG033002081731', 'BAG033002081732', 'BAG033002081733', 'BAG033002081734', 'BAG033002081735', 'BAG033002081736', 'BAG033002081737', 'BAG033002081738', 'BAG033002081739', 'BAG033002081740', 'BAG033002081741', 'BAG033002081742', 'BAG033002081743', 'BAG033002081744', 'BAG033002081745', 'BAG033002081746', 'BAG033002081747', 'BAG033002081748', 'BAG033002081749', 'BAG033002081750', 'BAG033002081751', 'BAG033002081752', 'BAG033002081753', 'BAG033002081754', 'BAG033002081755', 'BAG033002081756', 'BAG033002081757']]
    #run_select = "线上" #UAT 测试
    b_number = len(bag_list)
    dts_batch_data = save_dts_batch_record(input_batch_number=b_number)
    number = dts_batch_data[1]  # 2020081810 批次号
    waybills = waybills
    systemcode = "YT"
    if systemcode:
        j = 1
        res_list = []
        for bag_number in bag_list:
            bag_list = shipping_order(shipping_number="send_" + str(number + j), bag_number=bag_number,
                                      waybills=waybills,
                                      url=url, system_code=systemcode)
            res_batch = batch_creation_old(batch_number="BA_" + str(number + j), bag_list=bag_list, url=url
                               , system_code=systemcode)
            res_list.append(res_batch)
            j = j + 1
        return {"data": " 批次生成" + str(b_number) + "条,请到【空运配板】查看数据",
                "detail":res_list}

    else:
        return {"error": "遇到错误,请重新请求生成数据"}
if __name__ == "__main__":
    print("test")
    bag_list=[[
        "BAG0333220082130",
        "BAG0333220082131"
    ]]
    #dts_batch_get(url="http://192.168.88.175:5000",waybills=2,patch_number=2,bag_number=2)
    a = dts_batch_baglist_get(url="http://192.168.88.175:5000",bag_list=bag_list,waybills=2)
    print(a)