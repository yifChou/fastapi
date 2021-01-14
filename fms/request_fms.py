import requests
from fms.config import *
from fms.common_util import *
import time
from fms.fee_data_pqm import fee_to_pqm,fee_to_kunei,fee_to_zhuanyun,fee_to_qingguan,fee_to_diaobo,fee_to_chongpai,fee_to_paisong,fee_to_air_diaobo,fee_to_wt
import json
from fms.request_wcf_api import *
#from fake_useragent import UserAgent

headers={"Content-Type": "application/json"}
def get_customer_all(customerCode,source):
    '''
    查询所有客户的接口获取客户信息
    get_bill_data调用
    :param customerCode:
    :return:
    '''
    if source ==1:
        source="YT"
    elif source ==2:
        source = "WT"
    headers = {
        'Authorization': 'Basic SCrPikqtr1zLXNUFVnIwdLaUGzHG7dgZc2zE8zU4rcfakWVX0WQllw%3d%3d'
    }
    request_rul =url.crm_url +  "/api/BusinessConnector?CustomerCode="+customerCode+"&&"+"SourceCode="+source
    print(request_rul)
    data = requests.get(url=request_rul,data="",headers=headers).text

    redata = data.replace("true", '"true"').replace("false", '"false"').replace("null", '"null"')
    for customer in eval(redata):
        if customer["customer_code"] == customerCode:
            print(customer)
            return customer
        else:
            print("请求url",request_rul,"客户信息",data)
            break
def data_yt(waybill_number,customerCode,transfertype,servercode,source):
    '''

    :param waybill_number: 运单序列号
    :param customerCode: 客户
    :param transfertype: 运单中转状态
    :return:
    '''
    customer_info = get_customer_all(customerCode,source)
    #serverchannelcode = ["SGDHL","SCEMS","TEST007","TEST002","TEST001","HERMES","ABCZ","SHQ"]
    serverchannelcode_dict = {
        #"TEST008":[],
        "yif":url.yifserverchannelcode,#"GZYJ","SPLUSZ"
        "AB123":url.AB123serverchannelcode,#"HERMES","ABCZ"
        "5555555": url.fiveserverchannelcode,
        "kenny_code": url.yifserverchannelcode,
        "BJYWW":url.yifserverchannelcode
    }
    if servercode not in serverchannelcode_dict.keys():
        print("服务商不存在，请确认")
        return 0
    if source==1:
        ProductCode = url.ProductCode #["PK0461","ZH20207","USZMTK","XYLXB","1103"]
    else:
        ProductCode = url.wt_ProductCode
    #ProductCode = ["PK0001", "PK0002", "PK0003", "PK0031", "PK0034", "PK0347", "PK0351"]
    '''中转状态(S正常走货,X国外销毁,T未收安检退件(退全款),C国外重派,I国外退件(不退款),V已收未出国退件(只退运费,收挂号费))'''
    TransferstatusType =["S","X","T","C","I","V"]
    OperationStatus = ["CI","CL","CO","PA","SP","ST"]
    '''//财务系统现有(I签入,O签出,P制单,E作废,T已申报)
            //业务系统传过来的(CI签入,CL换单,CO签出,PA分配,SP发货,ST分拣)
            //财务系统新增(L换单,A分配,D发货,S分拣)'''
    ShipperCode = "YF" + str(waybill_number) + time.strftime("%H%M%S") + str(random.randint(1000, 9999))
    data = {
    "BsnEntity": {
        "ShipperCode": ShipperCode,
        "ReferCode": "ReferCode" + ShipperCode,
        "ServerCode": "RE" + ShipperCode,
        "ProductCode": random.choice(ProductCode),
        "CountryCode": "US",
        "ShipperChargeWeight": round(random.random(), 3),
        "ShipperOgId": customer_info["og_id"],
        "ShipperOgCode": customer_info["og_shortcode"],
        "Saller": customer_info["express_sallerid"],
        "SallerCode": "",
        "CustomerCode": customerCode,
        "ServerChannelCode": random.choice(serverchannelcode_dict[servercode]),
        "TransferstatusType": "S",
        "PostCode": random.randint(10000,99999),
        "IsHold": "",
        "OperationStatus":  random.choice(OperationStatus),
        "IssueKindCode": "",
        "ReturnRemark": "",
        "ReturnType": "",
        "ServerWeight": random.randint(10,99),
        "ShipperWeight": random.randint(10,99),
        "ReturnDate": "",
        "CheckOutOn": now(),
        "CheckInOn": now(),
        "ArrivalDate": now(),
        "SourceSystem": source,
        "BodyId": customer_info["customer_bodyid"],
        "ServerBodyId": 2
    },
    "InvoceList": [
        {
            "InvoiceName": "test_invoicename",
            "InvoiceQuantity": 0,
            "InvoiceTotalcharge": 1.10,
            "InvoiceCurrencycode": "USD",
            "InvoiceTotalWeight": 0.295,
            "ChildTrackNumber": "",
            "ChildNumber": "",
            "BoxNo": ""
        },
        {
            "InvoiceName": "test_invoicename1",
            "InvoiceQuantity": 0,
            "InvoiceTotalcharge": 1.10,
            "InvoiceCurrencycode": "USD",
            "InvoiceTotalWeight": 0.295,
            "ChildTrackNumber": "",
            "ChildNumber": "",
            "BoxNo": ""
        }
    ],
    "VolumeList": [
        {
            "involume_length": 1.00,
            "involume_width": 2.00,
            "involume_height": 3.00,
            "involume_grossweight": 0.295,
            "involume_volumeweight": 1000,
            "involume_chargeweight": 0.0,
            "package_weight": 0.0,
            "child_forecast_number": "",
            "child_track_number": ""
        },
    {
            "involume_length": 1.00,
            "involume_width": 2.00,
            "involume_height": 3.00,
            "involume_grossweight": 0.295,
            "involume_volumeweight": 1000,
            "involume_chargeweight": 0.0,
            "package_weight": 0.0,
            "child_forecast_number": "",
            "child_track_number": ""
        }
    ],
    "SendCompanyEntity": {
        "shipper_name": "Zhiwei yiwu",
        "shipper_company": "Zhiwei yiwu"
    }
    }
    if transfertype!=1:
        data["BsnEntity"]["TransferstatusType"] = random.choice(TransferstatusType)
    else:
        data["BsnEntity"]["TransferstatusType"] = "S"
    print(type(data),data)
    return data
def yingshou_fee(shippercode,MDservercode,currency):
    list_fee = []
    fee_code = ["E2", "L3"]
    for fee in fee_code:
        data = {
            "Fk_code": "E2",
            "Unit_code": "KG",
            "Ic_amount": random.randint(10, 99),
            "Currency_code": currency,
            "Id_zoneid": None,
            "Ic_currencyrate": None,
            "Note": None
        }
        data["Fk_code"] = fee
        list_fee.append(data)
    request_data ={
	"Waybill_Code": shippercode,
	"Server_Type": "PS",
	"Server_Id": MDservercode,
	"Id_OccurDate": now(),
	"Charge_Weight": 1.852,
	"Charge_Weight_Unit": 0.0,
	"System_Source": "1",
	"feeDetails": list_fee
}
    request_url = url.fms + "/api/EndFee/CreateEndFee"
    print(request_url)
    data = requests.post(url=request_url, json=request_data).text
    if eval(data)["message"] == "成功":
        print("应付费用推送fms成功！！！", request_data)
    else:
        print("应付费用推送fms失败", request_url, data, request_data)
def yt_yingshou_fee(Waybill_Code,customercode,currency,source):
    if source ==1:
        source="YT"
        currency_list = ["RMB","USD"]
    else:
        source="WT"
        currency_list = ["RMB", "USD", "EUR", "HKD"]
    request_data =[]
    fee_code_list = ["E1","QQ","H5","E2"]
    #currency_list=["RMB","USD","EUR","HKD"]
    for fee_code in fee_code_list:
        data = {
            "Waybill_Code": Waybill_Code,
            "Fee_Code": fee_code,
            "Fee_Name": "AUTO_FEE",
            "Fee_Expense_Time": now(),
            "Zone_Code": 1,
            "Zone_Name": "美国",
            "Price_Total_Value": random.randint(10,99)+random.random(),
            "Currency": random.choice(currency_list),
            "system_source": str(source),
            "Fk_type": "N",
            "calculate_unit": "KG",
            "note": "",
            "income_type": "PS",
            "price_level": "1",
            "Customer_Code": customercode,
            "Charge_Weight": 5.0
        }
        if source=="YT":
            if fee_code=="E1":
                data["Currency"]="RMB"
        request_data.append(data)
    request_url = url.fms + "/api/BillIncomeFee/CreateBillIncomeFee"
    data = requests.post(url=request_url, json=request_data).text
    print(request_url, "结果" + data)
    if "成功" in data:
        print("运单应收费用推送fms成功！！！")
        print(request_data)
    else:
        print("运单应收费用推送fms失败:", data, request_url, request_data)
def yt_yingfu_fee(Waybill_Code,Server_code,source):
    if source ==1:
        source="YT"
    else:
        source="WT"
    fee_data =[]
    fee_code_list = ["E2","L3"]
    for fee_code in fee_code_list:
        data = {
		"Fk_code": fee_code,
		"Unit_code": "KG",
		"Ic_amount": 5.0,
		"Currency_code": "RMB",
		"Id_zoneid": 99,
		"Ic_currencyrate": 1.11,
		"Note": "备注"
	}
        fee_data.append(data)
    request_data = {
            "Waybill_Code": Waybill_Code,
            "Server_Type": "PS",
            "Server_Id": Server_code,
            "Id_OccurDate": now(),
            "Charge_Weight": 1.852,
            "Charge_Weight_Unit": 0.0,
            "System_Source": source,
            "feeDetails": fee_data
        }
    request_url = url.fms + "/api/EndFee/CreateEndFee"
    data = requests.post(url=request_url, json=request_data).text
    print(request_url, "结果" + data)
    if "成功" in data:
        print("运单应付费用推送fms成功！！！")
        print(request_data)
    else:
        print("运单应付费用推送fms失败:", data, request_url, request_data)
# def fee_to_wt(waybill_code,huan_jie,source):
#     '''
#     :param waybill_code:
#     :param huan_jie: KY 空运  ZY 转运 MD 末端
#     :param source:
#     :return:
#     '''
#     if source==1:
#         system_source="YT"
#     else:
#         system_source = "WT"
#     request_data ={
# 	"waybill_code": waybill_code,
# 	"jsonstring": "{\"Waybill_Code\":\""+waybill_code+"\",\"Currency_Code\":\"YD\",\"Customer_Code\":\"AUTO-CUSTO\",\"Product_Code\":\"PK0029\",\"Server_Code\":\"\",\"Server_Type\":\"PS\",\"ServerPlace_Code\":\"\",\"System_Code\":\"YT\",\"Og_id_ChargeFirst\":\"YT-HQB-SZ\",\"Og_id_ChargeSecond\":\"\",\"Arrival_Date\":\"2020-12-14T19:50:08\",\"Country\":\"AR\",\"Postcode\":\"518000\",\"City\":\"005001\",\"Province\":\"005\",\"Charge_Weight\":5.0,\"Unit_Code\":\"KG\",\"Unit_Length\":\"CM\",\"Unit_Area\":null,\"Unit_Bulk\":null,\"Unit_Volume\":null,\"ExtraService\":\"ss\",\"ExtraService_Coefficient\":\"0.8\",\"Pieces\":5,\"Category_Code\":\"5\",\"Declared_Value\":0.8,\"Currency\":null,\"Tariff\":\"0.6\",\"Airline\":\"中国南方\",\"Departure_Airport\":\"宝安机场\",\"Destination_Airport\":\"伦敦机场\",\"Customs_Clearance_Port\":\"QHKA\",\"Start_Place\":\"MD\",\"end_Place\":\"MX\",\"Remark\":null,\"Ticket\":5,\"HS_Code\":5,\"Box_Number\":5,\"First_Long\":0.0,\"Two_Long\":0.0,\"Three_Long\":0.0,\"BusinessTime\":\"2020-12-14T19:50:08\",\"airline_two_code\":\"BR\",\"detailEntities\":null,\"Goods_Code\":null,\"IsFinalCharge\":false,\"ChargType\":null,\"HCustomsNumber\":0.0,\"MCustomsNumber\":0.0,\"LCustomsNumber\":0.0,\"HCargoValueNumber\":0.0,\"MCargoValueNumber\":0.0,\"LCargoValueNumber\":0.0,\"Charge_Volume\":5.0,\"Truck_Number\":1,\"Tray_Number\":1,\"TimeUnti\":\"Day\",\"TimeVaule\":5,\"TrackingNumber\":\"33P\"}",
# 	"system_source": system_source,
# 	"product_code": "LHR-CC-LVB",
# 	"income_type": huan_jie
# }
#     request_url = "http://192.168.88.21:5000/api/BilJsoncharged/AddBilJsoncharged"
#     print(request_url)
#     data = requests.post(url=request_url, json=request_data).text
#     print(data)
#     if '"Code":0' in data:
#         print("WT计费数据推送PQM成功！！！", request_data)
#     else:
#         print("WT计费数据推送PQM失败", request_url, data, request_data)

def request_yt(waybill_number,customerCode,transfertype,servercode,if_pqm,source):
    '''
    :param waybill_number: 运单序列号
    :param customerCode: 客户
    :param transfertype: 运单中转状态
    :return:
    '''
    request_data = data_yt(waybill_number,customerCode,transfertype,servercode,source)
    if source==2:
        request_data["BsnEntity"]["ArrivalDate"]= now()#y_m_d() + " 23:03:03"
    #print("请求数据：",request_data)
    yt_number = request_data["BsnEntity"]["ShipperCode"]
    request_url = url.fms + "api/WayBillBusiness/CreateWayBillBusiness"
    data = requests.post(url=request_url, json=request_data,headers=headers).text
    print(request_url,"结果"+data)
    # 派送费用-应付
    if if_pqm:
        fee_to_paisong(Waybill_Code=yt_number,ServerPlace_Code="TEST008",Server_Code="BJYWW",B_time= now_T())
    else:
        yt_yingfu_fee(Waybill_Code=yt_number, Server_code="BJYWW", source=source)
    # else:
    #     yingshou_fee(yt_number, MDservercode="BJYWW", currency=currency)
    # '''应收费用直接调用fms应收接口'''
    # yingshou_fee_code =["E1" ,"E2", "H5"]
    #shipper_yingshou_fee(yt_number, customerCode, request_data["BsnEntity"]["ProductCode"], yingshou_fee_code)
    # return yt_number
    '''返点费用'''
    request_data = data_fandian_income(yt_number, source, customerCode)
    request_url = url.fms + "/api/ReceivableRebate/CreateReceivableRebate"
    print(request_url)
    data = requests.post(url=request_url, json=request_data).text
    if eval(data)["message"] == "成功":
        print("应收返点信息推送fms成功！！！", request_data)
    else:
        print("应收返点信息推送fms失败", request_url, data, request_data)
    request_data = data_fandian(yt_number, source)
    request_url = url.fms + "/api/PayableRebate/CreatePayableRebate"
    print(request_url)
    data = requests.post(url=request_url, json=request_data).text
    if eval(data)["message"] == "成功":
        print("应付返点推送fms成功！！！", request_data)
    else:
        print("应付返点推送fms失败", request_url, data, request_data)
    '''应收费用经过pqm'''
    if source==1:
        if if_pqm:
            if eval(data)["message"] == "成功":
                print("运单推送fms成功！！！")
                print(request_data)
                request_pqm_url = url.pqm_url + "api/FreightSellingCharge/JobCharge"
                base_dict = {"Waybill_Code": yt_number, "Currency_Code": "YD", "Customer_Code": "AUTO-CUSTO",
                             "Product_Code": "PK0029", "Server_Code": "", "Server_Type": "PS", "ServerPlace_Code": "",
                             "System_Code": "YT", "Og_id_ChargeFirst": "YT-HQB-SZ", "Og_id_ChargeSecond": "",
                             "Arrival_Date": now_T(), "Country": "AR", "Postcode": "518000", "City": "005001",
                             "Province": "005", "Charge_Weight": 5.0, "Unit_Code": "KG", "Unit_Length": "CM", "Unit_Area": None,
                             "Unit_Bulk": None, "Unit_Volume": None, "ExtraService": "ss", "ExtraService_Coefficient": "0.8",
                             "Pieces": 5, "Category_Code": "5", "Declared_Value": 0.8, "Currency": None, "Tariff": "0.6",
                             "Airline": "中国南方", "Departure_Airport": "宝安机场", "Destination_Airport": "伦敦机场",
                             "Customs_Clearance_Port": "QHKA", "Start_Place": "MD", "end_Place": "MX", "Remark": None,
                             "Ticket": 5,
                             "HS_Code": 5, "Box_Number": 5, "First_Long": 0.0, "Two_Long": 0.0, "Three_Long": 0.0,
                             "BusinessTime": now_T(), "airline_two_code": "BR", "detailEntities": None,
                             "Goods_Code": None, "IsFinalCharge": False, "ChargType": None, "HCustomsNumber": 0.0,
                             "MCustomsNumber": 0.0, "LCustomsNumber": 0.0, "HCargoValueNumber": 0.0, "MCargoValueNumber": 0.0,
                             "LCargoValueNumber": 0.0, "Charge_Volume": 5.0, "Truck_Number": 1, "Tray_Number": 1,
                             "TimeUnti": "Day",
                             "TimeVaule": 5, "TrackingNumber": "33P"}
                request_pqm_url_1 = url.pqm_url + "api/Income/AddBillJson"
                json_data_1 = {
                    "id": 0,
                    "waybill_code": yt_number,
                    "jsonstring":json.dumps(base_dict, ensure_ascii=False),
                    "error_count": "",
                    "error_message": "",
                    "system_source": "YT",
                    "income_type":"PS"
                }
                if source==2:
                    json_data_1["system_source"]="WT"
                data = requests.post(url=request_pqm_url_1, json=json_data_1).text
                print(request_pqm_url_1, "结果" + data)
                if "Code" in data:
                    print("运单推送PQM计费表成功！！！")
                    print(json_data_1)
                    return yt_number
                else:
                    print("运单推送PQM计费表失败:", data, request_pqm_url_1, json_data_1)
        else:
            yt_yingshou_fee(Waybill_Code=yt_number, customercode=customerCode, currency="RMB", source=source)
            return yt_number
    elif source==2:
        '''WT末端应收费用'''
        if if_pqm:
            fee_to_wt(Waybill_Code=yt_number, Server_Code=servercode, Product_Code="FDXGR-CA",
                      Customer_Code="100002", income_type="PS", source=source)
            return yt_number
        else:
            yt_yingshou_fee(Waybill_Code=yt_number, customercode=customerCode, currency="RMB", source=source)
            return yt_number
        # json_data = {
        #     "billno": yt_number,
        #     "isPulsh": True,
        #     "jsonstr": json.dumps(base_dict, ensure_ascii=False),
        #     "income_type": "PS"
        # }
        # print("未处理的数据：", json_data)
        # data = requests.post(url=request_pqm_url, json=json_data).text
        # print(request_pqm_url, "结果" + data)
        # if "Code" in data:
        #     print("运单费用推送PQM成功！！！")
        #     print(json_data)
        # else:
        #     print("运单费用推送PQM失败:", data, request_pqm_url, json_data)
        # return yt_number
    else:
        print("运单推送fms失败:", data,request_url,request_data)
        return 0
def data_car(car_number,CountryCode,transit_country,servicecode,source):
    car_code = ["YB", "GA", "JA", "GC"]
    data = {
              "virtual_number":random.choice(car_code)+str(random.randint(10000,99999)) +time_str(),
              "car_number":random.choice(car_code) + "-"  + time_str() + str(car_number) +str(random.randint(1,9)),
              "customer_code": "customer_code",
              "customer_name": "customer_name",
              "productCode": "productCode",
              "CountryCode":CountryCode,
              "transit_country":transit_country,
              "number_count": 7,
              "bag_count": 8,
              "departure_time": now(),
              "arrival_time": now(),
              "volume_weight": 27.0,
              "chargeable_weight": 3.0,
              "transit_weight": 2.0,
              "volume_unit": "VKG",
              "chargeable_unit": "CKG",
              "transit_unit": "LKG",
              "service_code": servicecode,
              "service_bodyId": 2,
              "og_bodyId": 25,
              "source_id": source,
              "customer_bodyId": 1,
              "transit_volume": 4.0,
              "chargeable_volume": 5.0,
              "transit_plates": 6.0,
              "sum_amount": 9.0,
              "currency": "RMB",
              "remark": "sample string 14",
              "start_transit": "美东仓",
              "end_transit": "美西仓",
              "postCode": "51800",
              "metering_unit": "m",
              "customer_weight": 26.0,
              "service_bodycode":"service_bodycode"
         }
    # print(data)
    return data
def data_car_with_bag(virtual_number,car_number,bag_list,source,iffahuo):
    #iffahuo 如果是1，这是发货中转，2则为海外中转
    data = {
        "virtual_number":virtual_number,
        "car_number": car_number,
        "departure_time":now(),
        "BagItems": bag_list,
        "source_id": source
    }
    data_fahuo = {
        "departure_number": virtual_number,
        "car_number": car_number,
        "delivery_day": now(),
        "bagItems": bag_list,
        "source_id": source
    }
    if iffahuo==2:
        #发货中转
        return data_fahuo
    elif iffahuo==1:
        return data
def data_car_bag(virtual_number,car_number,bag_number,waybill_number,customerCode,yt_number,servercode,transfertype,source,iffahuo):
    #iffahuo 如果是1，这是发货中转，2则为海外中转
    bag_list = []
    data = {
        "virtual_number":virtual_number,
        "car_number": car_number,
        "departure_time":now(),
        "BagItems": bag_list,
        "source_id": source
    }
    data_fahuo = {
        "departure_number": virtual_number,
        "car_number": car_number,
        "delivery_day": now(),
        "bagItems": bag_list,
        "source_id": source
    }
    if iffahuo==2:
        #发货中转
        for i in range(bag_number):
            bag = request_bag_yt(waybill_number,customerCode,yt_number,servercode,transfertype,source)
            bag_list.append(bag["bag_labelcode"])
        data_fahuo["bagItems"] = bag_list
        return data_fahuo
    elif iffahuo==1:
        for i in range(bag_number):
            bag = request_bag_yt(waybill_number,customerCode,yt_number,servercode,transfertype,source)
            bag_list.append(bag["bag_labelcode"])
        data["BagItems"] = bag_list
        return data
def data_car_fee(car_number,departure_number,servercode,ifoversea = 1):
    Fk_code = ["TT", "A8","B1", "B3"]  # 卡车中转费 TT  提货费 A8 其他费用:转口证B1 垫材费B3
    FK_code_dict = {
        "D4": "清关费",
        "A8": "提货费",
        "B1": "转口证",
        "B3": "垫材费",
    }
    '''每个费用项'''
    fee_list = []
    for i in range(len(FK_code_dict.keys())):
        fee_data = {
                "amount": random.randint(1,100),
                "fk_code": "2",
                "charg_unit": "KG",
                "charg_type": "单价",
                "currency": "RMB",
                "occur_time": now(),
                "rate": 0.9
            }
        fee_code = Fk_code[i]
        fee_data["fk_code"] = fee_code
        fee_list.append(fee_data)
    data = {
        "car_number": car_number,
        "departure_number": departure_number,
        "delivery_day": now(),
        "feeItems": fee_list,
        "price_number": 4, #	报价价格编号
        "ptype": ifoversea, #	订单类型(1海外中转2发货中转3调拨)
        "server_code":servercode
    }
    print(data)
    return data
def request_diaobo_fee(bag_number,waybill_number,customerCode,yt_number,transfertype,transport_type_code,servercode,if_pqm,source):
    print("调拨数据是:",transport_type_code)
    car_data = request_diaobo(bag_number,waybill_number,customerCode,yt_number,transfertype,transport_type_code,servercode,if_pqm ,source)
    if transport_type_code == "KC" or transport_type_code == "WL":  #运输方式(KC卡车、AN航空、WL快递)
        fee_to_diaobo(car_data,transport_type_code ,now_T())
        return car_data["allocation_labelcode"]
    elif transport_type_code == "AN":
        fee_to_diaobo(car_data, transport_type_code, now_T())
        #fee_to_air_diaobo(lading_number=car_data["allocation_labelcode"],Server_Code=servercode,source=source,Charge_Weight=10,Currency="RMB",bs_time=now_T())
        return car_data["allocation_labelcode"]
    # request_data = data_car_fee(car_data["transport_hawbcode"],departure_number="11", ifoversea=3)
    # request_url = url.fms + "/api/TransferFee/CreateTransferFee"
    # data = requests.post(request_url, json=request_data).text
    # print(request_data)
    # if eval(data)["message"] == "成功":
    #     print(request_url,"调拨费用推送fms成功！！！")
    #     return request_data
    # else:
    #     print(request_url,"调拨费用推送fms失败！！！",data,request_data)
def request_car_fee_withoutbag(car_number,CountryCode,transit_country,customerCode,servercode,if_pqm,source):
    car_data = request_car_withoutbag(car_number,CountryCode,transit_country,customerCode,servercode,source)
    if source==1:
        fee_to_zhuanyun(Car_Number=car_data["car_number"],Waybill_Code=car_data["virtual_number"],Server_Code=servercode,source=source,Charge_Weight=car_data["chargeable_weight"],Start_Place=CountryCode,end_Place=transit_country,BusinessTime=now_T())
        return car_data["car_number"]
    elif source==2:
        if if_pqm:
            fee_to_wt(Waybill_Code=car_data["virtual_number"], Server_Code=servercode, Product_Code="PK0055",
                      Customer_Code="100001", income_type="ZY", source=source)
            return car_data["virtual_number"]
        #fee_to_wt(waybill_code=car_data["virtual_number"],huan_jie="ZY",source=source)
        #customerCode = "100001"  # 100001  C02672
        else:
            fee_code_list =["TT","A4","B7","tp","P4"]
            currency_list = ["RMB", "USD", "EUR", "HKD"]
            request_data= []
            for fee_code in fee_code_list:
                data = {
                "Waybill_Code": car_data["virtual_number"],
                "Customer_Code": customerCode,
                "express_sallerid": "",
                "business_ownership": "WWW",
                "Product_Code": "FDXGR-CA",
                "Product_Name": "美国快线GR美西（单件服务）",
                "Fee_Code": fee_code,
                "Fee_Name": "速递运费",
                "Arrival_Date": now_T(),
                "Fee_Expense_Time": now_T(),
                "Zone_Code": "US",
                "Zone_Name": "邮编分区",
                "Price_Value": random.randint(10,99),
                "Price_Total_Value": random.randint(10,99),
                "Currency": random.choice(currency_list),
                "system_source": "WT",
                "Fk_type": "N",
                "calculate_unit": "KG",
                "note": "",
                "income_type": "ZY",
                "price_level":random.randint(1,3),
                "Charge_Weight":random.randint(1000,9999)+random.random()
                }
                request_data.append(data)
            request_url = url.fms + "/api/BillIncomeFee/CreateBillIncomeFee"
            print(request_url)
            data = requests.post(url=request_url, json=request_data).text
            if eval(data)["message"] == "成功":
                print("WT中转费用推送fms成功！！！", request_data)
                return car_data["car_number"]
            else:
                print("WT中转费用推送fms失败", request_url, data, request_data)
def request_car_fee(car_number,CountryCode,transit_country,bag_number,waybill_number,customerCode,yt_number,servercode,transfertype,source,iffahuo):
    car_data = request_car(car_number,CountryCode,transit_country,bag_number,waybill_number,customerCode,yt_number,servercode,transfertype,source,iffahuo)
    if source==1:
        #fee_to_zhuanyun(Car_Number=car_data[0]["car_number"],Waybill_Code=car_data[0]["virtual_number"],Server_Code=servercode,source=source,Charge_Weight=car_data[0]["chargeable_weight"],Start_Place=CountryCode,end_Place=transit_country,BusinessTime=now_T())
        ifoversea=1
        request_data = data_car_fee(car_number=car_data[0]["car_number"],departure_number=car_data[0]["virtual_number"],servercode=servercode, ifoversea=ifoversea)
        data = requests.post(url=url.fms + "/api/TransferFee/CreateTransferFee", json=request_data).text
        print(request_data)
        if eval(data)["message"] == "成功":
            if ifoversea == 1:
                print("中转卡车费用推送fms成功！！！", request_data)
            elif ifoversea == 2:
                print("发货中转费用推送fms成功！！！", request_data)
            return request_data["car_number"]
        else:
            if ifoversea == 1:
                print("中转卡车费用推送fms失败")
            elif ifoversea == 2:
                print("发货中转费用推送fms失败")
        return car_data[0]["car_number"]
    elif source==2:
        #customerCode = "100001"  # 100001  C02672
        request_data = [{
            "Waybill_Code": car_data[0]["virtual_number"],
            "Customer_Code": customerCode,
            "express_sallerid": "",
            "business_ownership": "WWW",
            "Product_Code": "FDXGR-CA",
            "Product_Name": "美国快线GR美西（单件服务）",
            "Fee_Code": "A4",
            "Fee_Name": "速递运费",
            "Arrival_Date": now_T(),
            "Fee_Expense_Time": now_T(),
            "Zone_Code": "US",
            "Zone_Name": "邮编分区",
            "Price_Value": random.randint(10,99),
            "Price_Total_Value": random.randint(10,99),
            "Currency": "RMB",
            "system_source": "WT",
            "Fk_type": "N",
            "calculate_unit": "kg",
            "note": "",
            "income_type": "ZY"
        }]
        request_url = url.fms + "/api/BillIncomeFee/CreateBillIncomeFee"
        print(request_url)
        data = requests.post(url=request_url, json=request_data).text
        if eval(data)["message"] == "成功":
            print("WT中转费用推送fms成功！！！", request_data)
            return car_data[0]["car_number"]
        else:
            print("WT中转费用推送fms失败", request_url, data, request_data)


def request_car_with_bag(virtual_number,car_number,bag_list,source,iffahuo):
    '''
    中转卡车和袋子关系
    :param lading_number:
    :param bag_number:
    :return:
    '''
    bag_list = data_car_with_bag(virtual_number, car_number, bag_list, source, iffahuo)
    if iffahuo==1:
        data = requests.post(url=url.fms + "api/CarBag/CreateCarBag", data=bag_list).text
        print(bag_list)
        if eval(data)["message"] == "成功":
            print("中转卡车和袋子关系推送fms成功！！！")
            return bag_list
        else:
            print("中转卡车和袋子关系推送fms失败")
    elif iffahuo==2:
        data = requests.post(url=url.fms + "api/TransitTransport/CreateCarBag", data=bag_list).text
        print(bag_list)
        if eval(data)["message"] == "成功":
            print("发货中转和袋子关系推送fms成功！！！")
            return bag_list
        else:
            print("发货中转和袋子关系推送fms失败")
def request_car_bag(virtual_number,car_number,bag_number,waybill_number,customerCode,yt_number,servercode,transfertype,source,iffahuo):
    '''
    中转卡车和袋子关系
    :param lading_number:
    :param bag_number:
    :return:
    '''
    bag_list = data_car_bag(virtual_number,car_number,bag_number,waybill_number,customerCode,yt_number,servercode,transfertype,source,iffahuo)
    if iffahuo==1:
        data = requests.post(url=url.fms + "api/CarBag/CreateCarBag", data=bag_list).text
        print(bag_list)
        if eval(data)["message"] == "成功":
            print("中转卡车和袋子关系推送fms成功！！！")
            return bag_list
        else:
            print("中转卡车和袋子关系推送fms失败")
    elif iffahuo==2:
        data = requests.post(url=url.fms + "api/TransitTransport/CreateCarBag", data=bag_list).text
        print(bag_list)
        if eval(data)["message"] == "成功":
            print("发货中转和袋子关系推送fms成功！！！")
            return bag_list
        else:
            print("发货中转和袋子关系推送fms失败")
def request_car_withoutbag(data,CountryCode,transit_country,customerCode,servercode,source):
    '''
        空运提单接口成功后执行提单和袋子接口
        :param data: xxx-2020+0904
        :return:
        '''
    request_data = data_car(data,CountryCode,transit_country,servercode,source)
    if source ==2:
        print("WT中转-----------------------------------")
        customer=get_customer_all(customerCode=customerCode,source=source)
        #customerCode = "100001"  # 100001  C02672
        productCode = random.choice(["DHL-NL", "FDXGR-CA"])
        request_data["customer_code"]=customer["customer_code"]
        request_data["customer_name"]=customer["customer_shortname"]
        request_data["productCode"]=productCode
        request_data["customer_bodyId"] = customer["customer_bodyid"]
        request_data["departure_time"]=now() #y_m_d() +  " 21:21:21"
    data = requests.post(url=url.fms + "api/Transfer/CreateTransfer", json=request_data).text
    # print(data)
    if eval(data)["message"] == "成功":
        print("中转卡车推送fms成功！！！")
        print(request_data)
        return request_data
    else:
        print("中转卡车推送fms失败:", data)
        return 0
def request_car_with_bag_fee(data,CountryCode,transit_country,bag_list,customerCode,servercode,source,if_pqm,iffahuo):
    '''
        空运提单接口成功后执行提单和袋子接口
        :param data: xxx-2020+0904
        :return:
        '''
    request_data = data_car(data,CountryCode,transit_country,servercode,source)
    if source ==2:
        print("WT中转-----------------------------------")
        #customerCode = "100001"  # 100001  C02672
        request_data["customer_code"] = customerCode
        request_data["customer_name"] = "WT客户名称_脚本中转"
        request_data["productCode"] = "WT_Productcode_ZZ"
        pass
    car_number = request_data["car_number"]
    virtual_number =request_data["virtual_number"]
    Charge_Weight = request_data["chargeable_weight"]
    data = requests.post(url=url.fms + "api/Transfer/CreateTransfer", json=request_data).text
    # print(data)
    if eval(data)["message"] == "成功":
        print("中转卡车推送fms成功！！！")
        print(request_data)
        #卡车和袋子关系
        bag_list = data_car_with_bag(virtual_number, car_number, bag_list, source, iffahuo)
        if iffahuo == 1:
            data = requests.post(url=url.fms + "api/CarBag/CreateCarBag", data=bag_list).text
            print(bag_list)
            if eval(data)["message"] == "成功":
                print("中转卡车和袋子关系推送fms成功！！！")
            else:
                print("中转卡车和袋子关系推送fms失败")
        if source == 1:
            if if_pqm:
                fee_to_zhuanyun(Car_Number=car_number,Waybill_Code=virtual_number,Server_Code=servercode,source=source,Charge_Weight=Charge_Weight,Start_Place=CountryCode,end_Place=transit_country,BusinessTime=now_T())
            else:
                ifoversea = 1
                request_data = data_car_fee(car_number=car_number,departure_number=virtual_number,servercode=servercode, ifoversea=ifoversea)
                data = requests.post(url=url.fms + "/api/TransferFee/CreateTransferFee", json=request_data).text
                print(request_data)
                if eval(data)["message"] == "成功":
                    if ifoversea == 1:
                        print("中转卡车费用推送fms成功！！！", request_data)
                    elif ifoversea == 2:
                        print("发货中转费用推送fms成功！！！", request_data)
                    return request_data["car_number"]
                else:
                    if ifoversea == 1:
                        print("中转卡车费用推送fms失败")
                    elif ifoversea == 2:
                        print("发货中转费用推送fms失败")
                return car_number
        elif source == 2:
            # customerCode = "100001"  # 100001  C02672
            request_data = [{
                "Waybill_Code": virtual_number,
                "Customer_Code": customerCode,
                "express_sallerid": "",
                "business_ownership": "WWW",
                "Product_Code": "FDXGR-CA",
                "Product_Name": "美国快线GR美西（单件服务）",
                "Fee_Code": "A4",
                "Fee_Name": "速递运费",
                "Arrival_Date": now_T(),
                "Fee_Expense_Time": now_T(),
                "Zone_Code": "US",
                "Zone_Name": "邮编分区",
                "Price_Value": random.randint(10, 99),
                "Price_Total_Value": random.randint(10, 99),
                "Currency": "RMB",
                "system_source": "WT",
                "Fk_type": "N",
                "calculate_unit": "kg",
                "note": "",
                "income_type": "ZY"
            }]
            request_url = url.fms + "/api/BillIncomeFee/CreateBillIncomeFee"
            print(request_url)
            data = requests.post(url=request_url, json=request_data).text
            if eval(data)["message"] == "成功":
                print("WT中转费用推送fms成功！！！", request_data)
                return car_number
            else:
                print("WT中转费用推送fms失败", request_url, data, request_data)
    else:
        print("中转卡车推送fms失败:", data)
def request_car(data,CountryCode,transit_country,bag_number,waybill_number,customerCode,yt_number,servercode,transfertype,source,iffahuo):
    '''
        空运提单接口成功后执行提单和袋子接口
        :param data: xxx-2020+0904
        :return:
        '''
    request_data = data_car(data,CountryCode,transit_country,servercode,source)
    if source ==2:
        print("WT中转-----------------------------------")
        #customerCode = "100001"  # 100001  C02672
        request_data["customer_code"] = customerCode
        request_data["customer_name"] = "WT客户名称_脚本中转"
        request_data["productCode"] = "WT_Productcode_ZZ"
        pass
    car_number = request_data["car_number"]
    virtual_number =request_data["virtual_number"]
    data = requests.post(url=url.fms + "api/Transfer/CreateTransfer", json=request_data).text
    # print(data)
    if eval(data)["message"] == "成功":
        print("中转卡车推送fms成功！！！")
        print(request_data)
        bag_list = request_car_bag(virtual_number,car_number,bag_number,waybill_number,customerCode,yt_number,servercode,transfertype,source,iffahuo)
        #结算需要空运起飞时间
        add_airlading(bag_list["BagItems"], bag_number, yt_number, servercode, source)
        return request_data, bag_list
    else:
        print("中转卡车推送fms失败:", data)
        return 0
def data_customer(lading_number,bag_list,count_number,servercode,source):
    data={
  "lading_number": lading_number,
  "server_code": servercode,#"yif",#"服务商代码",
  "port": "AMS",#"目的港口",
  "complete_time": now(),#"清关完成时间",
  "customer_bodyId": 25,#"客户签约主体-WT使用"
  "source_id": source,#"系统来源(1 YT,2 WT)",
  "count_number":  count_number,#"总票数",
  "bag_count": len(bag_list),#"总箱数",
  "chargeable_weight": 30,#"提单计费重",
  "currency": "RMB",#"申报币种",
  "sum_amount": "40",#"sample string 11",
  "batch_number": "batch_number001",#"批次号-WT使用",
  "customer_code": "customer_code",#"客户编号-WT使用",
  "customer_name": "customer_name",#"客户名称-WT使用",
  "productCode": "productCode",#"产品编码-WT使用",
  "postCode": "postCode",
  "isclear": "Y",#"是否周末清关(Y是N否)",
  "volume_weight": 40,#"材积重",
  "lading_weight": 50,#" 提单实重",
  "low_value": 60,#"低等货值",
  "medium_value": 70,#" 中等货值",
  "declared_value": 80,#"中等货值申报总价值",
  "hight_value": 90,#"高等货值",
  "hightdeclared_value": 100,#"高等货值申报总价值",
  "server_bodyId": 2,#"服务商签约主体",
  "og_bodyId": 25,#"业务归属签约主体" WT用,
  "volume_unit": "VKG",#"材积重计量单位",
  "chargeable_unit": "CKG",#"计费重计量单位",
  "lading_unit": "LKG",#"实重计量单位"
  "customer_weight":110,
  "lading_bags":bag_list

}
    data["billing_method"] = "L"
    return data
def data_airlading(lading_number,bag_count,count_number,servercode,source):
    '''提单3字简码'''
    lading_threecode = ["100"]#,"101","102","010"
    data ={
  "lading_number": random.choice(lading_threecode)+"-"+str(lading_number) + date_now(),
  "board_weight": 2.0,
  "airline_company": "YI",
  "service_code": servercode,
  "originai_rport": "HKG",
  "destinationai_rport": "AMS",
  "originai_time": now(),
  "destinationai_time": now(),
  "lading_time": now(),
  "remark": "remark 13",
  "volume_coefficient": 6000, #材积系数
  "customer_bodyId": "37", # tms csi_server 字段customer_bodyid
  "source_id": source,
  "og_id": 74,#云途通运物流深圳总公司
  "og_bodyId": 25,#测试主体  sys pt_organization 字段body_id
  "lading_weight": 20.0,#实重
  "volume_weight": 21.0,#材积重
  "chargeable_weight": 22.0,#计费重
  "bsn_chargeWeight": 23.0,
  "lading_volume": 24.0,
  "count_number": count_number,
  "bag_count": bag_count,
  "batch_number": "batch_number_001",
  "customer_code": "customer_code_001",
  "customer_name": "customer_name_001",
  "productCode": "productCode_001",
  "customer_weight": 36.0,
  "service_bodyid": random.randint(28,66),
  "volume_unit": "KGV",
  "chargeable_unit": "KGC",
  "lading_unit": "KG",
  "AirService_type":1, #(" 空运服务类型 1代表正常空运  2代表调拨空运")
  "lading_items":[]
}
    #print(data)
    return data
def data_bag_shipper_list(bag_number,waybill_number,customerCode,yt_number,servercode,transfertype,source):
    bag_list = []
    shipper_list = []
    bag_shipper_list =[]
    for i in range(bag_number):
        bag_data = {
            "bag_label_code": "bag_label_code1",
            "shipper_hawbcode_list": ["3"]
        }
        bag = request_bag_yt(waybill_number,customerCode,yt_number,servercode,transfertype=transfertype,source=source)
        bag_list.append(bag["bag_labelcode"])
        shipper_list = shipper_list +bag["shipperItems"]
        bag_data["bag_label_code"] = bag["bag_labelcode"]
        bag_data["shipper_hawbcode_list"] = bag["shipperItems"]
        bag_shipper_list.append(bag_data)
        print(bag_list,shipper_list)
    return bag_list,shipper_list,bag_shipper_list
def data_lading_bag(bag_number,waybill_number,customerCode,yt_number,servercode,transfertype,source):
    bag_list = []
    for i in range(bag_number):
        bag = request_bag_yt(waybill_number,customerCode,yt_number,servercode,transfertype=transfertype,source=source)
        bag_list.append(bag)
    return bag_list
def data_bag_yt(waybill_number,customerCode,yt_number,transfertype,servercode,source):
    bag_title = ["BAG","CAG","DAG","EAG","FAG","GAG"]
    data = {
    "shipperItems":[],
    "source_id":source,
    "bag_labelcode": random.choice(bag_title) + time.strftime("%m%d%H%M%S") + str(random.randint(1000, 9999)) + str(random.randint(100, 999)),
    "bag_count": 2,
    "grossweight": str(random.randint(1, 10)),
    "chargeweight": str(random.randint(1, 10)),
    "setup_weight": str(random.randint(1, 10)),
    "setup_length": str(random.randint(10, 100)),
    "setup_width": str(random.randint(10, 100)),
    "setup_height": str(random.randint(10, 100)),
    "weight": random.randint(10, 100),
    "length": random.randint(10, 100),
    "width": random.randint(10, 100),
    "height": random.randint(10, 100),
    "createdon": now()
    }
    yt_list = []
    if source==1:
        customers_list=["C00223","C00144","C00126","C00350","C00261"]
        a = random.choice(customers_list)
    else:
        a=customerCode  # 100001  C02672
    customerCode=a
    for i in range(yt_number):
        yt = request_yt(waybill_number,customerCode,transfertype,servercode,0,source)
        if yt:
            yt_list.append(yt)
    data["shipperItems"] = yt_list
    data["bag_count"] = len(yt_list)
    return data
def request_bag_yt(waybill_number,customerCode,yt_number,servercode,transfertype=1,source=1):
    '''
    袋子和运单关系
    :param
    source:
    :return:
    '''
    request_data = data_bag_yt(waybill_number=waybill_number,
                               customerCode = customerCode,yt_number = yt_number,servercode=servercode,transfertype=transfertype,source=source)
    request_url = url.fms +  "/api/Bag/CreateBag"
    data = requests.post(url=request_url,data=request_data).text
    if eval(data)["message"]=="成功":
        print("袋子和运单推送fms成功！！！")
        bag_label = request_data["bag_labelcode"]
        print(request_data)
        return request_data
    else:
        print("袋子和运单推送fms失败",request_url+data)
def request_airlading_withbag_fee(lading_number,bag_list,shipper_list,customerCode,servercode,Charge_Weight,fee_number,currency,source):
    '''
    空运提单接口成功后执行提单和袋子接口
    :param data: xxx-2020+0904
    :return:
    '''
    bag_count = len(bag_list)
    count_number=len(shipper_list)
    request_data = data_airlading(lading_number,bag_count,count_number,servercode,source)
    if source==2:
        customerCode = get_customer_all(customerCode=customerCode,source=source)
        print("WT提单-----------------------------------")
        #customerCode = "100001"  # 100001  C02672
        request_data["customer_code"]=customerCode
        request_data["customer_name"]="WT客户名称_脚本"
        request_data["productCode"]="WT_Productcode"
        request_data["productCode"] = "WT_Productcode"
    request_data["lading_items"] = bag_list
    lading_number = request_data["lading_number"]
    print("休眠2s")
    time.sleep(2)
    request_url = url.fms + "api/AirTransport/CreateAircost"
    data = requests.post(url=request_url,json=request_data).text
    print(request_url)
    if eval(data)["message"]=="成功":
        print("提单推送fms成功！！！")
        print(request_data)
        #空运费用
        air_lading_fee(lading_number, Charge_Weight, fee_number, currency,source, ifotherfee=0)
        return lading_number
    else:
        print("提单推送fms失败:",data,request_data)
        return 0
def air_lading_fee(lading_number, Charge_Weight, fee_number, currency,source, ifotherfee):
    volume_weight =Charge_Weight*3
    if source==1:
        fee_to_pqm(lading_number=lading_number, Charge_Weight=Charge_Weight, Volume_Weight=volume_weight,AirService_type="KY")
        request_data = data_airlading_fee(lading_number, Charge_Weight, fee_number, currency, ifotherfee)
        request_url = url.fms + "/api/AirFee/CreateAirFee"
        print(request_url)
        data = requests.post(url=request_url, json=request_data).text
        if eval(data)["message"] == "成功":
            print("空运费用推送fms成功！！！", request_data)
            #return lading_number, bags
        else:
            print("空运费用推送fms失败", request_url, data, request_data)
        #return lading_number, bags
    elif source==2:
        Product_Code=random.choice(['DHL-NL','FDXGR-CA'])
        request_data = [{
        "Waybill_Code": lading_number,
        "Customer_Code": customerCode,
        "express_sallerid": "",
        "business_ownership": "WWW",
        "Product_Code": Product_Code,
        "Product_Name": "美国快线GR美西(随便不用校验)",
        "Fee_Code": "A4",
        "Fee_Name": "速递运费",
        "Arrival_Date": now_T(),
        "Fee_Expense_Time": now_T(),
        "Zone_Code": "US",
        "Zone_Name": "邮编分区",
        "Price_Value": 16.0,
        "Price_Total_Value": 16.0,
        "Currency": "RMB",
        "system_source": "WT",
        "Fk_type": "N",
        "calculate_unit": "kg",
        "note": "",
        "income_type":"KY"
    }]
        request_url = url.fms+"/api/BillIncomeFee/CreateBillIncomeFee"
        print(request_url)
        data = requests.post(url=request_url, json=request_data).text
        if eval(data)["message"] == "成功":
            print("WT空运费用推送fms成功！！！",request_data)
            #return lading_number,bags
        else:
            print("WT空运费用推送fms失败", request_url,data, request_data)
def request_airlading(lading_number,bag_number,waybill_number,customerCode,yt_number,servercode,transfertype,source):
    '''
    空运提单接口成功后执行提单和袋子接口
    :param data: xxx-2020+0904
    :return:
    '''
    bags = data_lading_bag(bag_number,waybill_number,customerCode,yt_number,servercode,transfertype,source)
    bag_list = []
    bag_count = len(bags)
    count_number = 0
    for i in range(len(bags)):
        bag_list.append(bags[i]["bag_labelcode"])
        count_number=count_number + len(bags[i]["shipperItems"])
    request_data = data_airlading(lading_number,bag_count,count_number,servercode,source)
    if source==2:
        print("WT提单-----------------------------------")
        #customerCode = "100001"  # 100001  C02672
        request_data["customer_code"]=customerCode
        request_data["customer_name"]="WT客户名称_脚本"
        request_data["productCode"]="WT_Productcode"
    request_data["lading_items"] = bag_list
    lading_number = request_data["lading_number"]
    print("休眠2s")
    time.sleep(2)
    request_url = url.fms + "api/AirTransport/CreateAircost"
    data = requests.post(url=request_url,json=request_data).text
    print(request_url)
    if eval(data)["message"]=="成功":
        print("提单推送fms成功！！！")
        print(request_data)
        return lading_number,bags
    else:
        print("提单推送fms失败:",data,request_data)
        return 0
def request_airlading_withoutbag(lading_number,customerCode,servercode,source):
    '''
    空运提单接口成功后执行提单和袋子接口
    :param data: xxx-2020+0904
    :return:
    '''
    request_data = data_airlading(lading_number,random.randint(10,99),random.randint(10,99),servercode,source)
    if source==2:
        customer=get_customer_all(customerCode=customerCode,source=source)
        print("WT提单-----------------------------------")
        #customerCode = "100001"  # 100001  C02672
        productCode = random.choice(["DHL-NL", "FDXGR-CA"])
        request_data["customer_code"]=customer["customer_code"]
        request_data["customer_name"]=customer["customer_shortname"]
        request_data["productCode"]=productCode
        request_data["customer_bodyId"] = customer["customer_bodyid"]
        request_data["originai_time"]=now()#y_m_d() +  " 11:11:11"
    lading_number = request_data["lading_number"]
    print("休眠10s")
    #time.sleep(10)
    request_url = url.fms + "api/AirTransport/CreateAircost"
    data = requests.post(url=request_url,json=request_data).text
    print(request_url)
    if eval(data)["message"]=="成功":
        print("提单推送fms成功！！！")
        print(request_data)
        return lading_number
    else:
        print("提单推送fms失败:",data,request_data)
        return 0
def request_airlading_fee_withoutbag(lading_index,customerCode,Charge_Weight,servercode,if_pqm,source=1):
    '''
    :param lading_index: 提单序列号，避免重复
    :param bag_number:  提单袋子数量
    :param Charge_Weight: 提单重量
    :param fee_number: 费用项数量
    :param ifotherfee: 是否需要其他费用
    :return:
    '''
    lading_number= request_airlading_withoutbag(lading_number=lading_index,customerCode=customerCode,servercode=servercode,source=source)
    volume_weight = Charge_Weight * 3
    if source==1:
        fee_to_pqm(lading_number=lading_number, Charge_Weight=Charge_Weight, Volume_Weight=volume_weight,AirService_type="KY")
        return lading_number
    elif source==2:
        if if_pqm:
            fee_to_wt(Waybill_Code=lading_number, Server_Code=servercode, Product_Code="PK0054",
                      Customer_Code="C02672", income_type="KY", source=source)
            return lading_number
        #fee_to_wt(waybill_code=lading_number, huan_jie="KY", source=source)
        else:
            Product_Code=random.choice(['DHL-NL','FDXGR-CA'])
            request_data = []
            fee_code_list=["A8","A4","F9"]
            currency_list = ["RMB", "USD", "EUR", "HKD"]
            for fee_code in fee_code_list:
                data = {
                "Waybill_Code": lading_number,
                "Customer_Code": customerCode,
                "express_sallerid": "",
                "business_ownership": "WWW",
                "Product_Code": Product_Code,
                "Product_Name": "美国快线GR美西(随便不用校验)",
                "Fee_Code": fee_code,
                "Fee_Name": "速递运费",
                "Arrival_Date": now_T(),
                "Fee_Expense_Time": now_T(),
                "Zone_Code": "US",
                "Zone_Name": "邮编分区",
                "Price_Value": 16.0,
                "Price_Total_Value": 16.0,
                "Currency": random.choice(currency_list),
                "system_source": "WT",
                "Fk_type": "N",
                "calculate_unit": "KG",
                "note": "",
                "income_type":"KY",
                "price_level":random.randint(1,3),
                "Charge_Weight":3.69
                }
                request_data.append(data)
            request_url = url.fms+"/api/BillIncomeFee/CreateBillIncomeFee"
            print(request_url)
            data = requests.post(url=request_url, json=request_data).text
            if eval(data)["message"] == "成功":
                print("WT空运费用推送fms成功！！！",request_data)
                return lading_number
            else:
                print("WT空运费用推送fms失败", request_url,data, request_data)
def request_customer_withoutbag(data,servercode,customerCode,source=1):
    '''
    清关提单接口成功后执行清关和袋子接口
    :param data: xxx-2020+0904
    :return:
    '''
    request_data= data_customer(lading_number=data,bag_list=[],count_number=0,servercode=servercode,source=source)
    lading_number = request_data["lading_number"]
    if source ==2:
        #customerCode="100001" #100001  C02672
        print("WT提单-----------------------------------")
        customer = get_customer_all(customerCode=customerCode, source=source)
        productCode=random.choice(["DHL-NL","FDXGR-CA"])
        request_data["customer_code"] = customerCode
        request_data["customer_name"] = "WT客户名称_脚本QG"
        request_data["productCode"] = productCode
        request_data["customer_bodyId"] = customer["customer_bodyid"]
        request_data["complete_time"] =now()# y_m_d() +" 02:02:02",
        request_data["count_number"] = 222,
        request_data["bag_count"] = 111
    request_url = url.fms + "api/CustomsClear/CreateCustoms"
    data = requests.post(url=request_url, data=request_data).text
    print(request_url)
    if eval(data)["message"] == "成功":
        print("清关提单推送fms成功！！！")
        print(request_data)
        return request_data
    else:
        print("清关提单推送fms失败:",request_url, data)
        return 0
def request_customer_withbag_fee(lading_number, bag_list,shipper_list,qg_servercode, customerCode,if_vat=0, source = 1):
    '''
    :param lading_index: 空运提单序列列号
    :param bag_number:  空运袋子数量
    :param Charge_Weight: 空运提单重量
    :param fee_number:  空运费用项个数
    :param ifotherfee:  空运费用是否需要其他费用项
    :param source: 数据来源 1 yt 2 wt
    :return:
    '''
    request_customer(lading_number, bag_list,len(shipper_list),qg_servercode, customerCode,source) #清关提单基础信息
    #request_custmoer_bag(lading_number, bag_list, source) #清关提单袋子关系
    server_port_currency={
        "YFQG":["AMS","RMB","yif"],
        "YS":["LAX","USD","ysqgfw"],
    }
    if qg_servercode in server_port_currency.keys():
        Customs_Clearance_Port,Currency,ServerPlace_Code=server_port_currency[qg_servercode]
    else:
        Customs_Clearance_Port, Currency, ServerPlace_Code=["AMS","RMB","yif"]
    if source==1:
        #fee_to_qingguan(Waybill_Code=lading_number,ServerPlace_Code=ServerPlace_Code, Server_Code=qg_servercode, source=source, Charge_Weight=Charge_Weight, Customs_Clearance_Port=Customs_Clearance_Port, Currency=Currency, BusinessTime=now_T())
        request_data = data_customer_fee(lading_number, qg_servercode)
        request_url = url.fms + "/api/CustomsFee/CreateCustomsFee"
        data = requests.post(url=request_url, json=request_data).text
        print(request_url, "结果：" + data)
        if eval(data)["message"] == "成功":
            print("清关提单费用推送fms成功！！！", request_data)
            return lading_number
        else:
            print("清关提单费用推送fms失败", request_url, data, request_data)
        #vat费用
        if if_vat==1:
            print("VATVATVATVATVATVATVATVAT")
            request_data = data_vat_fee(lading_number,shipper_list,Customs_Clearance_Port)
            request_url = url.fms + "/api/CustomsFee/CreateCustomsVatFee"
            data = requests.post(url=request_url, json=request_data).text
            print(request_url, "结果：" + data)
            if eval(data)["message"] == "成功":
                print("清关提单vat费用推送fms成功！！！", request_data)
                return lading_number
            else:
                print("清关提单vat费用推送fms失败", request_url, data, request_data)
        else:
            return lading_number
    elif source==2:
        print("WT清关提单-----------------------------------")
        request_data = [{
            "Waybill_Code": lading_number,
            "Customer_Code": customerCode,
            "express_sallerid": "",
            "business_ownership": "WWW",
            "Product_Code": "FDXGR-CA",
            "Product_Name": "美国快线GR美西（单件服务）",
            "Fee_Code": "A4",
            "Fee_Name": "速递运费",
            "Arrival_Date": now_T(),
            "Fee_Expense_Time": now_T(),
            "Zone_Code": "US",
            "Zone_Name": "邮编分区",
            "Price_Value": random.randint(10,99),
            "Price_Total_Value": random.randint(10,99),
            "Currency": "RMB",
            "system_source": "WT",
            "Fk_type": "N",
            "calculate_unit": "kg",
            "note": "",
            "income_type": "QG"
        }]
        request_url = url.fms + "/api/BillIncomeFee/CreateBillIncomeFee"
        print(request_url)
        data = requests.post(url=request_url, json=request_data).text
        if eval(data)["message"] == "成功":
            print("WT清关费用推送fms成功！！！", request_data)
            return lading_number
        else:
            print("WT清关费用推送fms失败", request_url, data, request_data)
    #return lading_number
def request_customer_fee(lading_index, bag_number,servercode,qg_servercode, waybill_number, customerCode, Charge_Weight, yt_number, fee_number, transfertype,if_vat=0, ifotherfee = 0, source = 1):
    '''
    :param lading_index: 空运提单序列列号
    :param bag_number:  空运袋子数量
    :param Charge_Weight: 空运提单重量
    :param fee_number:  空运费用项个数
    :param ifotherfee:  空运费用是否需要其他费用项
    :param source: 数据来源 1 yt 2 wt
    :return:
    '''
    lading_number,bags = request_airlading_fee(lading_index=str(lading_index),bag_number=bag_number,
                              waybill_number=waybill_number,customerCode=customerCode,
                              Charge_Weight=Charge_Weight,yt_number=yt_number,
                              fee_number=fee_number,transfertype=transfertype,
                              ifotherfee=ifotherfee,servercode=servercode,source=source)
    bag_list = []
    shipper_list = []
    for bag in bags:
        bag_list.append(bag["bag_labelcode"])
        shipper_list += bag["shipperItems"]
    request_customer(lading_number, bag_list,yt_number*len(bags),qg_servercode, customerCode,source) #清关提单基础信息
    bag_list=[]
    shipper_list=[]
    for bag in bags:
        bag_list.append(bag["bag_labelcode"])
        shipper_list += bag["shipperItems"]
    #request_custmoer_bag(lading_number, bag_list, source) #清关提单袋子关系
    server_port_currency={
        "YFQG":["AMS","RMB","yif"],
        "YS":["LAX","USD","ysqgfw"],
    }
    if qg_servercode in server_port_currency.keys():
        Customs_Clearance_Port,Currency,ServerPlace_Code=server_port_currency[qg_servercode]
    else:
        Customs_Clearance_Port, Currency, ServerPlace_Code=["AMS","RMB","yif"]
    if source==1:
        #fee_to_qingguan(Waybill_Code=lading_number,ServerPlace_Code=ServerPlace_Code, Server_Code=qg_servercode, source=source, Charge_Weight=Charge_Weight, Customs_Clearance_Port=Customs_Clearance_Port, Currency=Currency, BusinessTime=now_T())
        request_data = data_customer_fee(lading_number, qg_servercode)
        request_url = url.fms + "/api/CustomsFee/CreateCustomsFee"
        data = requests.post(url=request_url, json=request_data).text
        print(request_url, "结果：" + data)
        if eval(data)["message"] == "成功":
            print("清关提单费用推送fms成功！！！", request_data)
            #return lading_number
        else:
            print("清关提单费用推送fms失败", request_url, data, request_data)
        #vat费用
        if if_vat==1:
            print("VATVATVATVATVATVATVATVAT")
            request_data = data_vat_fee(lading_number,shipper_list,Customs_Clearance_Port)
            request_url = url.fms + "/api/CustomsFee/CreateCustomsVatFee"
            data = requests.post(url=request_url, json=request_data).text
            print(request_url, "结果：" + data)
            if eval(data)["message"] == "成功":
                print("清关提单vat费用推送fms成功！！！", request_data)
                return lading_number
            else:
                print("清关提单vat费用推送fms失败", request_url, data, request_data)
        else:
            return lading_number
    elif source==2:
        print("WT清关提单-----------------------------------")
        request_data = [{
            "Waybill_Code": lading_number,
            "Customer_Code": customerCode,
            "express_sallerid": "",
            "business_ownership": "WWW",
            "Product_Code": "FDXGR-CA",
            "Product_Name": "美国快线GR美西（单件服务）",
            "Fee_Code": "A4",
            "Fee_Name": "速递运费",
            "Arrival_Date": now_T(),
            "Fee_Expense_Time": now_T(),
            "Zone_Code": "US",
            "Zone_Name": "邮编分区",
            "Price_Value": random.randint(10,99),
            "Price_Total_Value": random.randint(10,99),
            "Currency": "RMB",
            "system_source": "WT",
            "Fk_type": "N",
            "calculate_unit": "kg",
            "note": "",
            "income_type": "QG"
        }]
        request_url = url.fms + "/api/BillIncomeFee/CreateBillIncomeFee"
        print(request_url)
        data = requests.post(url=request_url, json=request_data).text
        if eval(data)["message"] == "成功":
            print("WT清关费用推送fms成功！！！", request_data)
            return lading_number
        else:
            print("WT清关费用推送fms失败", request_url, data, request_data)
    #return lading_number

def request_customer(data,bag_number,count_number,servercode,customerCode,source=1):
    '''
    清关提单接口成功后执行清关和袋子接口
    :param data: xxx-2020+0904
    :return:
    '''
    request_data= data_customer(data,bag_number,count_number,servercode,source)
    lading_number = request_data["lading_number"]
    if source ==2:
        #customerCode="100001" #100001  C02672
        productCode=random.choice(["DHL-NL","FDXGR-CA"])
        request_data["customer_code"] = customerCode
        request_data["customer_name"] = "WT客户名称_脚本QG"
        request_data["productCode"] = productCode

    request_url = url.fms + "api/CustomsClear/CreateCustoms"
    data = requests.post(url=request_url, data=request_data).text
    print(request_url)
    if eval(data)["message"] == "成功":
        print("清关提单推送fms成功！！！")
        print(request_data)
        return request_data
    else:
        print("清关提单推送fms失败:",request_url, data)
        return 0

def request_customer_fee_withoutbag(lading_index,servercode,qg_servercode, customerCode, Charge_Weight,if_pqm, source = 1):
    '''
    :param lading_index: 空运提单序列列号
    :param bag_number:  空运袋子数量
    :param Charge_Weight: 空运提单重量
    :param fee_number:  空运费用项个数
    :param ifotherfee:  空运费用是否需要其他费用项
    :param source: 数据来源 1 yt 2 wt
    :return:
    '''
    lading_number = request_airlading_fee_withoutbag(lading_index=str(lading_index),customerCode=customerCode,Charge_Weight=Charge_Weight,servercode=servercode,if_pqm=if_pqm,source=source)
    request_customer_withoutbag(lading_number,qg_servercode, customerCode,source) #清关提单基础信息
    if source==2:
        print("WT清关提单-----------------------------------")
        Product_Code = random.choice(['DHL-NL', 'FDXGR-CA'])
        if if_pqm:
            #fee_to_wt_qingguan(Waybill_Code=lading_number,Server_Code=qg_servercode,Customer_Code=customerCode,source=source)
            fee_to_wt(Waybill_Code=lading_number, Server_Code=qg_servercode, Product_Code="PK0053", Customer_Code="C02621", income_type="QG", source=source)
            return lading_number
        else:
            request_data = []
            fee_code_list = ["F9", "D4", "P8","BF","B7"]
            currency_list = ["RMB", "USD", "EUR", "HKD"]
            for fee_code in fee_code_list:
                data = {
                    "Waybill_Code": lading_number,
                    "Customer_Code": customerCode,
                    "express_sallerid": "",
                    "business_ownership": "WWW",
                    "Product_Code": Product_Code,
                    "Product_Name": "美国快线GR美西(随便不用校验)",
                    "Fee_Code": fee_code,
                    "Fee_Name": "速递运费",
                    "Arrival_Date": now_T(),
                    "Fee_Expense_Time": now_T(),
                    "Zone_Code": "US",
                    "Zone_Name": "邮编分区",
                    "Price_Value": 16.0,
                    "Price_Total_Value": 16.0,
                    "Currency": random.choice(currency_list),
                    "system_source": "WT",
                    "Fk_type": "N",
                    "calculate_unit": "KG",
                    "note": "备注",
                    "income_type": "QG",
                    "price_level": random.randint(1, 3),
                    "Charge_Weight": 3.69
                }
                request_data.append(data)
            request_url = url.fms + "/api/BillIncomeFee/CreateBillIncomeFee"
            print(request_url)
            data = requests.post(url=request_url, json=request_data).text
            if eval(data)["message"] == "成功":
                print("WT清关费用推送fms成功！！！", request_data)
                return lading_number
            else:
                print("WT清关费用推送fms失败", request_url, data, request_data)
    #return lading_number

# def request_lading_bag(lading_number,bag_number,source):
#     '''
#     空运提单和袋子关系
#     :param lading_number:
#     :param bag_number:
#     :return:
#     '''
#     bag_list = data_lading_bag(bag_number,source)
#     request_url = url.fms + "api/AirBag/CreateAirBag"
#     data = requests.post(url=request_url, data=bag_list).text
#     print(request_url)
#     if eval(data)["message"] == "成功":
#         print("提单袋子关系推送fms成功！！！")
#         return bag_list
#     else:
#         print("提单袋子关系推送fms失败",request_url,data)
def request_custmoer_bag(lading_number,bag_list,source):
    '''
    清关提单和袋子关系
    :param lading_number:
    :param bag_number:
    :return:
    '''
    request_data = {
    "lading_number": lading_number,
    "bagItems": bag_list,
    "source_id": source
    }
    request_url = url.fms + "api/CustomsFee/CreateCustomsBag"
    data = requests.post(url=request_url, data=request_data).text
    print(request_url)
    if eval(data)["message"] == "成功":
        print("清关提单袋子关系推送fms成功！！！",request_data)
    else:
        print("清关提单袋子关系推送fms失败",request_url,request_data)
def data_vat_fee(lading_number,shipper_list,port):
    '''每个运单费用项'''
    shipper_fee_list = []
    for i in shipper_list:
        fee_data = {
                    "lading_number":lading_number,
                    "shippercode": i,
                    "port":port,
                    "feeItems": [
                        {
                            "amount": random.randint(1, 100),
                            "fk_code": "VA",
                            "charg_unit": "KG",
                            "charg_type": "单价",
                            "currency": "RMB",
                            "occur_time": now(),
                            "calculate_unit": "W",
                            "rate": 0.9
                        },
                        {
                            "amount": random.randint(1, 100),
                            "fk_code": "P8",
                            "charg_unit": "KG",
                            "charg_type": "单价",
                            "currency": "RMB",
                            "occur_time": now(),
                            "calculate_unit": "W",
                            "rate": 0.9
                        },
                        {
                            "amount": random.randint(1, 100),
                            "fk_code": "A8",
                            "charg_unit": "KG",
                            "charg_type": "单价",
                            "currency": "RMB",
                            "occur_time": now(),
                            "calculate_unit": "W",
                            "rate": 0.9
                        }
                    ]
                    }
        shipper_fee_list.append(fee_data)
    return shipper_fee_list
def data_customer_fee(lading_number,servercode):
    Fk_code = ["D4", "Z4","P8","F4","Z5","th","Z6","Z8"]  # 清关费 D4 机场操作费 提货费 A8
    '''清关费	D4
        关税	P8
        机场操作费	" Z4"
        提单处理费	F4
        低价值清关费	Z5
        机场提货费	th
    '''
    # 装板费O1 装板杂费J3 报关费A5 提货费A8 安检费D7 其他费用:转口证B1 垫材费B3
    FK_code_dict = {
        "D4": "清关费",
        "Z4": "机场操作费",
        "A8": "提货费",
        "B1": "转口证",
        "B3": "垫材费",
    }

    '''每个费用项'''
    fee_list = []
    for i in range(len(Fk_code)):
        fee_data = {
                "amount": random.randint(1,100),
                "fk_code": "2",
                "charg_unit": "KG",
                "charg_type": "DJ",
                "currency": "RMB",
                "calculate_unit":"W",
                "occur_time": now(),
                "rate": 0.9,
                "billing_method":"L"
            }
        fee_data1 = {
                "amount": random.randint(1,100),
                "fk_code": "2",
                "charg_unit": "KG",
                "charg_type": "DJ",
                "currency": "RMB",
                "calculate_unit":"S",
                "occur_time": now(),
                "rate": 0.9
            }
        fee_data2 = {
                "amount": random.randint(1,100),
                "fk_code": "2",
                "charg_unit": "KG",
                "charg_type": "DJ",
                "currency": "RMB",
                "calculate_unit":"BL",
                "occur_time": now(),
                "rate": 0.9
            }
        fee_data3 = {
            "amount": random.randint(1, 100),
            "fk_code": "VA",
            "charg_unit": "KG",
            "charg_type": "DJ",
            "currency": "RMB",
            "calculate_unit": "M",
            "occur_time": now(),
            "rate": 0.9
        }
        fee_data4 = {
            "amount": random.randint(1, 100),
            "fk_code": "P8",
            "charg_unit": "KG",
            "charg_type": "DJ",
            "currency": "RMB",
            "calculate_unit": "M",
            "occur_time": now(),
            "rate": 0.9
        }
        fee_data["fk_code"] = Fk_code[i]
        fee_list.append(fee_data)
        if i==0:
            fee_list.append(fee_data1)
            fee_list.append(fee_data2)
            fee_list.append(fee_data3)
            fee_list.append(fee_data4)
            fee_data1["fk_code"] = Fk_code[i]
            fee_data2["fk_code"] = Fk_code[i]
    data = {
        "lading_number": lading_number,
        "lading_weight": 3.33,
        "port": "AMS",
        "price_number": 2,
        "feeItems": fee_list,
        "server_code":servercode
    }
    print(data)
    return data
def data_airlading_fee(lading_number,Charge_Weight,fee_number,currency="RMB",ifotherfee=0):
    Fk_code = ["Q6","v7","v8","F7","F9","G7","O1","J3","A5","A8","D7"] #航空运费 A4 TC Q6 MYC v7 SCC v8 RAC F7 文件费 F9 卸货费G7
    other_fk_code = ["B1","B3"]
    # 装板费O1 装板杂费J3 报关费A5 提货费A8 安检费D7 其他费用:转口证B1 垫材费B3
    FK_code_dict = {
        "A4":"航空运费",
        "Q6":"TC",
        "v7":"MYC",
        "v8":"SCC",
        "F7":"RAC",
        "F9":"文件费",
        "G7":"卸货费",
        "O1":"装板费",
        "J3":"装板杂费",
        "A5":"报关费",
        "A8":"提货费",
        "D7":"安检费",
        "B1": "转口证",
        "B3": "垫材费",
    }
    '''每个费用项'''
    fee_list = []
    fee_flag = []
    fee_list_totalfee = 0
    for i in range(fee_number):
        Air_Price_Value = random.randint(10, 100)
        fee_data = {
            "air_Price_Value": Air_Price_Value,
            "air_Price_TotalValue": Air_Price_Value,
            "fk_code": "FDA",
            "getPrice_Type": "ZJ",
            "currency": currency,
            "unit_Code": "KG"
        }
        fee_code = random.choice(Fk_code)
        if fee_code not in fee_flag:
            fee_flag.append(fee_code)
            fee_data["fk_code"] = fee_code
            fee_data["Fee_Name"] = FK_code_dict[fee_code]
            fee_list.append(fee_data)
            fee_list_totalfee = fee_list_totalfee+fee_data["air_Price_TotalValue"]
        else:
            print("随机费用重复")
    #航空运费
    Air_Price_Value = random.randint(10, 100)
    fee_data = {
        "air_Price_Value": Air_Price_Value,
        "air_Price_TotalValue": Air_Price_Value,
        "fk_code": "A4",
        "getPrice_Type": "ZJ",
        "currency": currency,
        "unit_Code": "KG"
    }
    fee_list.append(fee_data)
    if ifotherfee:
        for fee_code in other_fk_code:
            Air_Price_Value = random.randint(10, 100)
            fee_data = {
                "air_Price_Value": Air_Price_Value,
                "air_Price_TotalValue": Air_Price_Value,
                "fk_code": fee_code,
                "getPrice_Type": "ZJ",
                "currency": currency,
                "unit_Code": "KG"
            }
            fee_data["fk_code"] = fee_code
            fee_data["Fee_Name"] = FK_code_dict[fee_code]
            fee_list.append(fee_data)
            fee_list_totalfee = fee_list_totalfee + fee_data["air_Price_TotalValue"]
    else:
        print("不需要其他费用项")
    data = {
    "airChargeResultValues": fee_list,
    "price_number": 1,
    "waybill_Code": lading_number,
    "airService_type": 1, # (" 空运服务类型 1代表正常空运  2代表调拨空运")
    "volume_Weight": Charge_Weight*3,
    "charge_Weight": Charge_Weight,
    "lading_Weight": Charge_Weight*2,
    "server_Code": "yif",
    "Current_date": now_T()
}
    #print(data)
    return data
def request_airlading_fee(lading_index,bag_number,waybill_number,customerCode,Charge_Weight,yt_number,fee_number,servercode,transfertype,ifotherfee=0,source=1):
    '''
    :param lading_index: 提单序列号，避免重复
    :param bag_number:  提单袋子数量
    :param Charge_Weight: 提单重量
    :param fee_number: 费用项数量
    :param ifotherfee: 是否需要其他费用
    :return:
    '''
    lading_number,bags = request_airlading(lading_number=lading_index,bag_number=bag_number,
                                      waybill_number=waybill_number,customerCode=customerCode,
                                      yt_number=yt_number,servercode=servercode,transfertype=transfertype,source=source)
    volume_weight = Charge_Weight * 3
    if source==1:
        fee_to_pqm(lading_number=lading_number, Charge_Weight=Charge_Weight, Volume_Weight=volume_weight,AirService_type="KY")
        currency = "RMB"
        request_data = data_airlading_fee(lading_number, Charge_Weight, fee_number, currency, ifotherfee)
        request_url = url.fms + "/api/AirFee/CreateAirFee"
        print(request_url)
        data = requests.post(url=request_url, json=request_data).text
        if eval(data)["message"] == "成功":
            print("空运费用推送fms成功！！！", request_data)
            return lading_number, bags
        else:
            print("空运费用推送fms失败", request_url, data, request_data)
        return lading_number, bags
    elif source==2:
        Product_Code=random.choice(['DHL-NL','FDXGR-CA'])
        request_data = [{
        "Waybill_Code": lading_number,
        "Customer_Code": customerCode,
        "express_sallerid": "",
        "business_ownership": "WWW",
        "Product_Code": Product_Code,
        "Product_Name": "美国快线GR美西(随便不用校验)",
        "Fee_Code": "A4",
        "Fee_Name": "速递运费",
        "Arrival_Date": now_T(),
        "Fee_Expense_Time": now_T(),
        "Zone_Code": "US",
        "Zone_Name": "邮编分区",
        "Price_Value": 16.0,
        "Price_Total_Value": 16.0,
        "Currency": "RMB",
        "system_source": "WT",
        "Fk_type": "N",
        "calculate_unit": "kg",
        "note": "",
        "income_type":"KY"
    }]
        request_url = url.fms+"/api/BillIncomeFee/CreateBillIncomeFee"
        print(request_url)
        data = requests.post(url=request_url, json=request_data).text
        if eval(data)["message"] == "成功":
            print("WT空运费用推送fms成功！！！",request_data)
            return lading_number,bags
        else:
            print("WT空运费用推送fms失败", request_url,data, request_data)

    # currency="RMB"
    # request_data = data_airlading_fee(lading_number,Charge_Weight,fee_number,currency,ifotherfee)
    # request_url = url.fms+"/api/AirFee/CreateAirFee"
    # print(request_url)
    # data = requests.post(url=request_url, json=request_data).text
    # if eval(data)["message"] == "成功":
    #     print("空运费用推送fms成功！！！",request_data)
    #     return lading_number,bags
    # else:
    #     print("空运费用推送fms失败", request_url,data, request_data)
def data_lipei(shipper_hawbcode,server_code,source_id):
    serverchannelcode = ["SGDHL", "SCEMS", "TEST007"]
    ProductCode = ["PK0001", "PK0002", "PK0003", "PK0031", "PK0034", "PK0347", "PK0351"]
    data = {
  "shipper_hawbcode": shipper_hawbcode,
  "source_id": source_id,
  "product_code": random.choice(ProductCode),
  "service_channels_code": random.choice(serverchannelcode),
  "service_code":server_code,
  "amount": random.randint(1,99),
  "costs_source": "D7",#安检费
  "currency": "RMB",
  "claims_reasons": "脚本理赔数据",
  "service_bodyid": 25,#服务商签约主体
  "declared_currency":"RMB",#申报价值币种
  "declared_value":random.randint(1,99),#申报价值
  "apply_time": now()
}
    return data
def request_lipei_with_bag(shipper_list,servercode,source):
    for shipper_hawbcode in shipper_list:
        request_data = data_lipei(shipper_hawbcode,servercode,source)
        request_url = url.fms+"/api/SettlementClaims/CreateSettlementClaims"
        print(request_url)
        data = requests.post(url=request_url, json=request_data).text
        if eval(data)["message"] == "成功":
            print("理赔数据推送fms成功！！！",request_data)
        else:
            print("理赔数据推送fms失败", request_url,data, request_data)
def request_lipei(waybill_number,customerCode,transfertype,servercode,if_pqm,source):
    shipper_hawbcode = request_yt(waybill_number=waybill_number,customerCode=customerCode,transfertype=transfertype,servercode=servercode,if_pqm=0,source=source)
    request_data = data_lipei(shipper_hawbcode,servercode,source)
    request_url = url.fms+"/api/SettlementClaims/CreateSettlementClaims"
    print(request_url)
    data = requests.post(url=request_url, json=request_data).text
    if eval(data)["message"] == "成功":
        print("理赔数据推送fms成功！！！",request_data)
        return shipper_hawbcode
    else:
        print("理赔数据推送fms失败", request_url,data, request_data)
def data_chongpai(shipperCode,source):
    severCode = ["BJYWW"]#"MIAEND","BJYWW","yif","A1109",
    countryCode = ["US","BR","CA","CU"]
    serverchannelcode = [ "TEST008"]#"SGDHL", "SCEMS",
    data = {
        "shipperCode": shipperCode,
        "dispatchCode": shipperCode+"-1",
        "serverCode": random.choice(countryCode)+shipperCode,
        "countryCode": random.choice(countryCode),
        "shipperChargeWeight": random.random()*100,
        "shipperOgCode": "6",
        "serverChannelCode": random.choice(serverchannelcode),
        "transferstatusType": "C", #中转状态(S正常走货,X国外销毁,T未收安检退件(退全款),C国外重派,I国外退件(不退款),V已收未出国退件(只退运费,收挂号费))
        "postCode": "postCode"+str(random.randint(100,999)),
        "returnDate": now(),
        "returnRemark": "脚本退件原因",
        "returnType": "P",#推荐类型 P重派
        "dispatchDate": now(),
        "sourceId": source,
        "serverBodyCode": "15" #末端服务商的签约主体代码
    }
    return data
def data_chongpai_fee(waybill_Code,server_code,source):
    if source == 1:
        system_Source="YT"
    else:
        system_Source="WT"
    data = {
        "waybill_Code": waybill_Code,
        "server_Type": "",
        "server_Id":server_code,
        "id_OccurDate": now_T(),
        "charge_Weight":5.0,
        "feeDetails":[],
        "system_Source": system_Source
    }
    data_list=[]
    fee_code_list = ["L3","E1","M1","H6","K4","T9","L6"]
    for fee_code in fee_code_list:
        fee_data = {
            "fk_code": "L3",
            "unit_code": "KG",
            "ic_amount": random.randint(10, 99),
            "currency_code": "RMB",
            "id_zoneid": "分区测试",
            "note": "备注",
            "id_OccurDate": now_T(),
            "Ic_currencyrate": 1
        }
        fee_data["fk_code"]=fee_code
        data_list.append(str(fee_data))
    data_list=[eval(data) for data in data_list]
    data["feeDetails"]=data_list
    print(data)
    return data
def request_chongpai_withbag_fee(shipper_list,customerCode,servercode,if_pqm,source):
    for shipper_hawbcode in shipper_list:
        chonpai_data = data_chongpai(shipper_hawbcode, source)
        request_url = url.fms + "/api/OverseasDispatch/CreateOverseasDispatch"
        print(request_url)
        data = requests.post(url=request_url, json=chonpai_data).text
        if eval(data)["message"] == "成功":
            print("重派数据推送fms成功！！！", chonpai_data)
            if if_pqm:
                fee_to_chongpai(chonpai_data,customerCode,ServerPlace_Code="TEST008",serverCode="BJYWW",db_time= now_T(),source=source)
            else:
                request_data = data_chongpai_fee(chonpai_data["dispatchCode"], servercode, source)
                request_url = url.fms + "/api/OverseasDispatch/CreateDispatchFee"
                print(request_url)
                data = requests.post(url=request_url, json=request_data).text
                if eval(data)["message"] == "成功":
                    print("重派费用数据推送fms成功！！！", request_data)
                else:
                    print("重派费用数据推送fms失败", request_url, data, request_data)
        else:
            print("重派数据推送fms失败", request_url, data, chonpai_data)

def request_chongpai_fee(waybill_number,customerCode,transfertype,servercode,source):
    shipper_hawbcode = request_chongpai(waybill_number,customerCode,transfertype,servercode,source)
    # fee_to_chongpai(shipper_hawbcode,customerCode,ServerPlace_Code="TEST008",serverCode="BJYWW",db_time= now_T(),source=source)
    # return shipper_hawbcode["shipperCode"]
    request_data = data_chongpai_fee(shipper_hawbcode["dispatchCode"],servercode,source)
    request_url = url.fms+"/api/OverseasDispatch/CreateDispatchFee"
    print(request_url)
    data = requests.post(url=request_url, json=request_data).text
    if eval(data)["message"] == "成功":
        print("重派费用数据推送fms成功！！！", request_data)
        return shipper_hawbcode["shipperCode"]
    else:
        print("重派费用数据推送fms失败", request_url,data, request_data)
def request_paisong_fee(waybill_number,customerCode,transfertype,servercode,source):
    shipper_hawbcode = request_chongpai(waybill_number,customerCode,transfertype,servercode,source)
    return shipper_hawbcode["shipperCode"]
def request_chongpai(waybill_number,customerCode,transfertype,servercode,source):
    shipper_hawbcode = request_yt(waybill_number=waybill_number,customerCode=customerCode,transfertype=transfertype,servercode=servercode,if_pqm=0, source=source)
    request_data = data_chongpai(shipper_hawbcode,source)
    request_url = url.fms+"/api/OverseasDispatch/CreateOverseasDispatch"
    print(request_url)
    data = requests.post(url=request_url, json=request_data).text
    if eval(data)["message"] == "成功":
        print("重派数据推送fms成功！！！", request_data)
        return request_data
    else:
        print("重派数据推送fms失败", request_url,data, request_data)
def data_yd_fee(waybill_number, fee_number, source):
    data_list = []
    severCode = ["MIAEND", "BJYWW", "yif", "A1109"]
    server_Id = random.choice(severCode)
    Fk_code = ["E1", "E2", "E4", "H5", "H6"]  # 速递运费E1 挂号费E2 保险费E4 燃油附加费H5 偏远燃油附加费H6
    if source==1:
        source = "YT"
    elif source==2:
        source = "WT"
    else:
        source = "YT"
        print("填写不正确，自动赋值YT")

    if fee_number>len(Fk_code):
        print("脚本没有这么多费用项")
    else:
        for i in range(fee_number):
            data_fee = {
                "waybill_Code": waybill_number,
                "server_Id": server_Id,
                "fk_code": "3",
                "unit_code": "单价",
                "ic_amount": random.randint(1, 99),
                "currency_code": "RMB",
                "pm_currencyrate": 0.8,
                "id_zoneid": "8",
                "note": "脚本末端费用",
                "id_OccurDate": now(),
                "system_Source": source
            }
            data_fee["fk_code"] = Fk_code[i]
            data_list.append(data_fee)
    print(data_list)
    return data_list
def request_yd_fee(waybill_number,fee_number,customerCode,transfertype,servercode,source):
    shipper_hawbcode = request_yt(waybill_number=waybill_number,customerCode=customerCode,transfertype=transfertype,servercode=servercode,if_pqm=0,source=source)
    request_data = data_yd_fee(shipper_hawbcode, fee_number, source)
    request_url = url.fms+"/api/EndFee/CreateEndFee"
    print(request_url)
    data = requests.post(url=request_url, json=request_data).text
    if eval(data)["message"] == "成功":
        print("运单末端费用推送fms成功！！！",request_data )
        return shipper_hawbcode
    else:
        print("运单末端费用推送fms失败", request_url,data, request_data)
def data_fandian(shipperCode,source):
    data = {"shipperCode": shipperCode,
     "serviceOrderNumber": "serviceOrderNumber" + shipperCode,
     "serverCode": random.choice(sys_data.severCode),
     "ytAmount": random.randint(1,99),
     "ytCurrency": "RMB",
     "serviceAmount": random.randint(1,99),
     "serviceCurrency": "RMB",
     "sourceId": source,
     "serviceBillAmount": random.randint(1,99),
     "chargeweight": random.random()*10,
     "productCode": "productCode"+str(random.randint(10000,99999)),
     "serverChannelCode":"serverChannelCode"+str(random.randint(10000,99999)),
     "shipperOgId": 74,
     "branchAmount":random.randint(1,99),
     "sallerId": 99,
     "sallerAmount": random.randint(1,99),
     "costAmount": random.randint(1,99),
     "billCycle":ymd() + "-" + ymd()
            }
    print(data)
    return data
def request_fandian(waybill_number, fee_number, customerCode, transfertype,servercode, source):#返点应付
    shipper_hawbcode = request_yd_fee(waybill_number, fee_number, customerCode, transfertype,servercode, source)
    request_data = data_fandian(shipper_hawbcode,source)
    request_url = url.fms+"/api/PayableRebate/CreatePayableRebate"
    print(request_url)
    data = requests.post(url=request_url, json=request_data).text
    if eval(data)["message"] == "成功":
        print("应付返点推送fms成功！！！",request_data )
        return shipper_hawbcode
    else:
        print("应付返点推送fms失败", request_url,data, request_data)
def data_diaobo(transport_hawbcode,transport_type_code,bag_list):
    #transport_type_code = ["KC","AN","WL"]
    load_type_code = ["A","S"]
    orig_warehouse_code =["YT-GZ"]#"YT-SZ",,,"YT-SH","YT-CD","YT-CS"
    dest_warehouse_code = ["YT-XM"]#"YT-CS","YT-XM","YT-CS" "YT-HQB-SZ", "YT-BT-SZ", "YTFZ", "YTXZ""YT-XM","YT-XM", "YT-HQB-SZ"
    data = {
     "allocation_labelcode":"DBDH" + str(transport_hawbcode),
     "transport_hawbcode": "DB" + str(transport_hawbcode), #运输单号 (卡车号、提单号、快递单号)
     "transport_server_code": sys_data.severCode,
     "bag_count": random.randint(10,99),
     "transport_total_weight": random.randint(5,10),
     "weight_unit_code": "KG",
     "orig_warehouse_code": random.choice(orig_warehouse_code),
     "dest_warehouse_code": random.choice(dest_warehouse_code),
     "transport_send_time": now(),
     "transport_receive_time": now(),
     "transport_type_code": transport_type_code, #运输方式(KC卡车、AN航空、WL快递)
     "load_type_code": "",#装车方式A整车、 S拼车（运输方式为卡车时才提供）
     "transport_service_body_code": 1,#运输服务商签约主体
     "system_source_code": 101,
     "transport_bag_list": bag_list,
     "box_type":"N"
    }
    if data["transport_type_code"] == "KC":
        data["load_type_code"] = random.choice(load_type_code)
    print(data)
    return data
def request_diaobo_withbag_fee(bag_list,shipper_list,diaobo_number,transport_type_code,servercode,if_pqm,source):
    for shipper in shipper_list:
        request_kunei_fee(shipper,if_pqm,source)
    print("休眠2秒")
    time.sleep(2)
    request_data = data_diaobo(diaobo_number,transport_type_code,bag_list)
    request_data["bag_count"] = len(bag_list)
    request_url = url.fms + "/api/Transport/CreateTransport"
    print(request_url)
    request_data_diaobo=request_data
    data = requests.post(url=request_url, json=request_data).text
    if eval(data)["message"] == "成功":
        print("调拨数据推送fms成功！！！", request_data)
        if if_pqm:
            if transport_type_code == "KC" or transport_type_code == "WL":  # 运输方式(KC卡车、AN航空、WL快递)
                fee_to_diaobo(request_data, transport_type_code, now_T())
                return request_data["allocation_labelcode"]
            elif transport_type_code == "AN":
                fee_to_diaobo(request_data, transport_type_code, now_T())
                return request_data["allocation_labelcode"]
        else:
            if transport_type_code == "KC" or transport_type_code == "WL":
                ifoversea= 3
                request_data1 = data_car_fee(request_data["transport_hawbcode"], departure_number=request_data["allocation_labelcode"],servercode=servercode,ifoversea=ifoversea)
                request_url = url.fms + "/api/TransferFee/CreateTransferFee"
                data = requests.post(request_url, json=request_data1).text
                print(request_data1)
                if eval(data)["message"] == "成功":
                    print(request_url, "调拨费用推送fms成功！！！")
                    return request_data["allocation_labelcode"]
                else:
                    print(request_url, "调拨费用推送fms失败！！！", data, request_data1)
            else:
                ifoversea = 1
                #调用空运计费的接口程序带编写

    else:
        print("调拨数据推送fms失败", request_url, data, request_data)

def request_diaobo(bag_number,waybill_number,customerCode,yt_number,transfertype,transport_type_code,servercode,if_pqm,source):
    bag_list = []

    for i in range(bag_number):
        bag_data = {
            "bag_label_code": "bag_label_code1",
            "shipper_hawbcode_list": [ "3"]
        }
        bag = request_bag_yt(waybill_number,customerCode,yt_number,servercode=servercode,transfertype=transfertype,source=source)
        bag_data["bag_label_code"] = bag["bag_labelcode"]
        bag_data["shipper_hawbcode_list"] = bag["shipperItems"]
        for shipper in bag["shipperItems"]:
            request_kunei_fee(shipper,if_pqm,source)
        bag_list.append(bag_data)
    print("休眠10秒")
    time.sleep(2)
    request_data = data_diaobo(waybill_number,transport_type_code,bag_list)
    request_data["bag_count"] = len(bag_list)
    request_url = url.fms + "/api/Transport/CreateTransport"
    print(request_url)
    request_data_diaobo=request_data
    data = requests.post(url=request_url, json=request_data).text
    if eval(data)["message"] == "成功":
        print("调拨数据推送fms成功！！！", request_data)
        #需要空运的起飞时间做结算
        request_data = data_airlading(lading_number=random.randint(1000,9999), bag_count=bag_number, count_number=bag_number * yt_number,
                                      servercode=servercode, source=source)
        if source == 2:
            print("WT提单-----------------------------------")
            # customerCode = "100001"  # 100001  C02672
            request_data["customer_code"] = customerCode
            request_data["customer_name"] = "WT客户名称_脚本"
            request_data["productCode"] = "WT_Productcode"
        bags = []
        for bag in bag_list:
            bags.append(bag["bag_label_code"])
        request_data["lading_items"] = bags
        lading_number = request_data["lading_number"]
        print("休眠2s")
        time.sleep(2)
        request_url = url.fms + "api/AirTransport/CreateAircost"
        data = requests.post(url=request_url, json=request_data).text
        print(request_url)
        if eval(data)["message"] == "成功":
            print("提单推送fms成功！！！")
            print(request_data,lading_number)
        else:
            print("提单推送fms失败:", data, request_data)
        return request_data_diaobo
    else:
        print("调拨数据推送fms失败", request_url, data, request_data)


def data_diaobo_kunei(shipper_hawbcode,operation_type_code):
    #operation_type_code = ["ST","CL","CI","CO","PU"]
    orig_warehouse_code = ["YT-SZ", "YT-GZ",  "YT-SH", "YT-CD"]#"YT-CS",
    dest_warehouse_code = ["YT-XM", "YT-HQB-SZ", "YT-BT-SZ", "YTFZ", "YTXZ"]
    data ={"shipper_hawbcode":shipper_hawbcode,
    "dest_warehouse_code":random.choice(dest_warehouse_code),
    "dest_warehouse_service_body_code":1,
    "operation_type_code":operation_type_code,#操作节点(ST分拣  CL换单、CI签入、CO签出、PU打包)
    "orig_warehouse_og_code":random.choice(orig_warehouse_code),
    "orig_warehouse_service_body_code":2,
    "system_source_code":101,}
    print(data)
    return data
def request_diaobo_kunei(shipper_hawbcode,operation_type_code):
    request_data = data_diaobo_kunei(shipper_hawbcode,operation_type_code)
    request_url = url.fms + "/api/Transport/CreateOpeLabrary"
    print(request_url)
    data = requests.post(url=request_url, json=request_data).text
    if eval(data)["message"] == "成功":
        print("库内调拨数据推送fms成功！！！", request_data)
        return request_data["shipper_hawbcode"],request_data["orig_warehouse_og_code"]
    else:
        print("库内调拨数据推送fms失败", request_url, data, request_data)
def data_fandian_income(shipperCode,source,customerCode):
    data ={"shipperCode":shipperCode,
            "ablerebateAmount":random.random()*10,
            "currency":"RMB",
            "sourceId":source,
            "customerCode":customerCode,
            "billCycle":ymd(),
            "productCode":"productCode"+str(random.randint(1000,9999)),
            "chargeweight":random.random()*10,
            "shipperOgId":1,
            "totaleFreight":random.random()*10
           }
    print(data)
    return data
def request_data_fandian_income(waybill_number,customerCode,transfertype,servercode,source):
    shipper_hawbcode = request_yt(waybill_number,customerCode,transfertype,servercode,0,source)
    request_data = data_fandian_income(shipper_hawbcode,source,customerCode)
    request_url = url.fms + "/api/ReceivableRebate/CreateReceivableRebate"
    print(request_url)
    data = requests.post(url=request_url, json=request_data).text
    if eval(data)["message"] == "成功":
        print("应收返点信息推送fms成功！！！", request_data)
        return request_data["shipperCode"]
    else:
        print("应收返点信息推送fms失败", request_url, data, request_data)
def request_data_fandian_all(waybill_number,customerCode,transfertype,servercode,source):
    shipper_hawbcode = request_yt(waybill_number,customerCode,transfertype,servercode,0,source)
    request_data = data_fandian_income(shipper_hawbcode,source,customerCode)
    request_url = url.fms + "/api/ReceivableRebate/CreateReceivableRebate"
    print(request_url)
    data = requests.post(url=request_url, json=request_data).text
    if eval(data)["message"] == "成功":
        print("应收返点信息推送fms成功！！！", request_data)
    else:
        print("应收返点信息推送fms失败", request_url, data, request_data)
    request_data = data_fandian(shipper_hawbcode,source)
    request_url = url.fms+"/api/PayableRebate/CreatePayableRebate"
    print(request_url)
    data = requests.post(url=request_url, json=request_data).text
    if eval(data)["message"] == "成功":
        print("应付返点推送fms成功！！！",request_data )
        return shipper_hawbcode
    else:
        print("应付返点推送fms失败", request_url,data, request_data)
def data_kunei_fee(shipper_hawbcode,operation_type_code,source):
    fee_type = ["ST", "CL", "CI", "CO", "PU"]
    data = {"shipper_hawbcode":shipper_hawbcode,
            "fee_type":operation_type_code,#费用类型(ST分拣  CL换单、CI签入、CO签出、PU打包)
            "amount":random.randint(10,99),
            "charg_unit":"KG",
            "currency":"RMB",
            "occur_time":now(),
            "source_id":source}
    print("库内费用：",data)
    return data
def request_kunei_fee(shipper_hawbcode,if_pqm,source):
    operation_type_code = ["OL", "O3", "O4", "O5", "O6","O0"]
    #operation_type_code = random.choice(operation_type_code)
    fee_number = random.choice([1, 2, 3, 4, 5,6])
    print(fee_number,"条费用")
    for i in range(fee_number):
        print("第",i,"条费用")
        shipper_hawbcode,Og_id_ChargeFirst = request_diaobo_kunei(shipper_hawbcode,operation_type_code[i])
        if if_pqm:
            fee_to_kunei(shipper_hawbcode, now_T(), operation_type_code[i], Og_id_ChargeFirst) #费用到PQM
        else:
            request_data = data_kunei_fee(shipper_hawbcode,operation_type_code[i],source)
            request_url = url.fms + "/api/Transport/CreateOpeLabraryFee"
            print(request_url)
            data = requests.post(url=request_url, json=request_data).text
            if eval(data)["message"] == "成功":
                print("库内调拨费用推送fms成功！！！", request_data)
                #return request_data["shipper_hawbcode"]
            else:
                print("库内调拨费用推送fms失败", request_url, data, request_data)
def request_kunei_fee2(waybill_number,customerCode,yt_number,servercode,transfertype,source):
    bag = request_bag_yt(waybill_number,customerCode,yt_number,servercode,transfertype,source)
    for shipper_hawbcode in bag["shipperItems"]:
        request_kunei_fee(shipper_hawbcode, source)
    return bag["shipperItems"]
def data_fahuo(server_code,box,bill_count,charge_weight,org_code,destination,source):
    car_code=["de","des"]
    car_code2 = ["YB", "GA", "JA", "GC"]
    data = {
  "departure_number": random.choice(car_code) + "-"  + time_str() + "8888" +str(random.randint(1,9)),
  "car_number": random.choice(car_code2) + "-"  + time_str() +str(random.randint(1,9)),
  "source": source,
  "server_code": server_code,
  "body_id": 5,
  "box": box,
  "bill_count": bill_count,
  "weight": 8.0,
  "charge_weight": charge_weight,
  "unit": "KG",
  "org_code": org_code,
  "org_body_id": 12,
  "destination": destination,
  "delivery_day": y_m_d(),
  "delivery_time": now_T(),
  "arrival_time": now_T()
}
    return data
def request_fahuo(server_code,box,bill_count,charge_weight,org_code,destination,source,iffahuo,waybill_number,customerCode,transfertype):
    request_data = data_fahuo(server_code,box,bill_count,charge_weight,org_code,destination,source)
    request_url = url.fms + "/api/TransitTransport/CreateTransitTransport"
    print(request_url)
    data = requests.post(url=request_url, json=request_data).text
    if eval(data)["message"] == "成功":
        print("发货中转信息推送fms成功！！！", request_data)
        bag_list = request_car_bag(request_data["departure_number"], request_data["car_number"], box, waybill_number, customerCode, bill_count,
                                   server_code, transfertype, source, iffahuo)
        #结算需要空运
        add_airlading(bag_list["bagItems"],box,bill_count,servercode="yif",source=source)
        return request_data,bag_list
    else:
        print("发货中转信息推送fms失败", request_url, data, request_data)
def request_fahuo_withbag_fee(bag_list,shipper_list,org_code,destination,charge_weight,servercode,if_pqm,source):
    bill_count = len(shipper_list)
    car_data = fahuo_with_bag(bag_list,servercode, bill_count, charge_weight, org_code, destination, source)
    if if_pqm:
        fee_to_zhuanyun(Car_Number=car_data["car_number"],Waybill_Code=car_data["departure_number"],Server_Code=servercode,source=source,Charge_Weight=charge_weight,Start_Place=org_code,end_Place=destination,BusinessTime=now_T())
        return car_data["car_number"]
    else:
        ifoversea = 2
        request_data = data_car_fee(car_number=car_data["car_number"], departure_number=car_data["departure_number"], servercode=servercode,
                                    ifoversea=ifoversea)
        data = requests.post(url=url.fms + "/api/TransferFee/CreateTransferFee", json=request_data).text
        print(request_data)
        if eval(data)["message"] == "成功":
            if ifoversea == 1:
                print("中转卡车费用推送fms成功！！！", request_data)
            elif ifoversea == 2:
                print("发货中转费用推送fms成功！！！", request_data)
            return request_data["car_number"]
        else:
            if ifoversea == 1:
                print("中转卡车费用推送fms失败")
            elif ifoversea == 2:
                print("发货中转费用推送fms失败")
        return car_number

def request_fahuo_fee(org_code,destination,box,waybill_number,charge_weight,customerCode,bill_count,servercode,transfertype,source,iffahuo):
    car_data = request_fahuo(servercode,box,bill_count,charge_weight,org_code,destination,source,iffahuo,waybill_number,customerCode,transfertype)
    fee_to_zhuanyun(Car_Number=car_data[0]["car_number"],Waybill_Code=car_data[0]["departure_number"],Server_Code=servercode,source=source,Charge_Weight=charge_weight,Start_Place=org_code,end_Place=destination,BusinessTime=now_T())
    return car_data[0]["car_number"]
def add_airlading(bag_list,bag_number,yt_number,servercode,source):
    # 需要空运的起飞时间做结算
    request_data = data_airlading(lading_number=random.randint(1000, 9999), bag_count=bag_number,
                                  count_number=bag_number * yt_number,
                                  servercode=servercode, source=source)
    if source == 2:
        print("WT提单-----------------------------------")
        # customerCode = "100001"  # 100001  C02672
        request_data["customer_code"] = customerCode
        request_data["customer_name"] = "WT客户名称_脚本"
        request_data["productCode"] = "WT_Productcode"
    request_data["lading_items"] = bag_list
    lading_number = request_data["lading_number"]
    print("休眠2s")
    time.sleep(2)
    request_url = url.fms + "api/AirTransport/CreateAircost"
    data = requests.post(url=request_url, json=request_data).text
    print(request_url)
    if eval(data)["message"] == "成功":
        print("提单推送fms成功！！！")
        print(request_data, lading_number)
    else:
        print("提单推送fms失败:", data, request_data)
def shipper_yingshou_fee(Waybill_Code,customerCode,Product_Code,fee_code):
    request_data = []
    for fee in fee_code:
        fee_data = {
        "Waybill_Code": Waybill_Code,
        "Customer_Code": customerCode,
        "express_sallerid": "",
        "business_ownership": "WWW",
        "Product_Code": Product_Code,
        "Product_Name": "美国快线GR美西（默认都是这个）",
        "Fee_Code": fee,
        "Fee_Name": "速递运费",
        "Arrival_Date": now_T(),
        "Fee_Expense_Time": now_T(),
        "Zone_Code": "US",
        "Zone_Name": "邮编分区",
        "Price_Value": random.randint(10, 99),
        "Price_Total_Value": random.randint(10, 99),
        "Currency": "RMB",
        "system_source": "YT",
        "Fk_type": "N",
        "calculate_unit": "kg",
        "note": "",
        "income_type": "PS"
        }
        request_data.append(fee_data)
    request_url = url.fms + "/api/BillIncomeFee/CreateBillIncomeFee"
    print(request_url)
    data = requests.post(url=request_url, json=request_data).text
    if eval(data)["message"] == "成功":
        print("应收费用推送fms成功！！！", request_data)
        return Waybill_Code
    else:
        print("应收费用推送fms失败", request_url, data, request_data)
def fahuo_with_bag(bag_list,server_code, bill_count, charge_weight, org_code, destination, source):
    data_fahuo1 = {
        "departure_number": "virtual_number",
        "car_number": "car_number",
        "delivery_day": now(),
        "bagItems": bag_list,
        "source_id": source
    }
    request_data = data_fahuo(server_code, len(bag_list), bill_count, charge_weight, org_code, destination, source)
    request_url = url.fms + "/api/TransitTransport/CreateTransitTransport"
    data_fahuo1["departure_number"]=request_data["departure_number"]
    data_fahuo1["car_number"] = request_data["car_number"]
    print(request_url)
    data = requests.post(url=request_url, json=request_data).text
    if eval(data)["message"] == "成功":
        print("发货中转信息推送fms成功！！！", request_data)
        data = requests.post(url=url.fms + "api/TransitTransport/CreateCarBag", data=data_fahuo1).text
        print(data_fahuo1)
        if eval(data)["message"] == "成功":
            print("发货中转和袋子关系推送fms成功！！！")
            return data_fahuo1
        else:
            print("发货中转和袋子关系推送fms失败")
def wt_bushou_data(dzbm,shipper_code,bsn_type,server_code,customer_code,currency_code,source):
    customer = get_customer_all(customer_code, source)
    request_data ={
        "rec_number": dzbm,
        "rec_approve_time": now(),
        "bsn_number": shipper_code,
        "bsn_type": bsn_type,#对账类型 N 末端 A 空运 Q 清关 T 中转
        "rec_tag": random.choice(["D","B"]),#对账结果 D 协议处理（服务商金额大于应收金额） B服务商为准
        "server_code": server_code,
        "refe_code": "KEHU"+shipper_code,
        "server_charge_weight": random.randint(100,999),
        "customer_code": customer_code,
        "og_id": customer["og_id"],
        "body_id": customer["customer_bodyid"],
        "saller_id": customer["express_sallerid"],
        "push_time":  now(),
        "system_id": source,
        "serverplace_code": "",
        "country_code": "US",
        "fee_values": []
    }
    if bsn_type=="N":
        fee_code_list = ["E1", "QQ", "H5", "E2"]
    if bsn_type=="A":
        fee_code_list = ["A8","A4","F9"]
    if bsn_type=="Q":
        fee_code_list = ["F9", "D4", "P8","BF","B7"]
    if bsn_type=="T":
        fee_code_list = ["TT","A4","B7","tp","P4"]
    else:
        fee_code_list = ["E1", "QQ", "H5", "E2"]
    fee_values_list = []
    for fee_code in fee_code_list:
        fee_data ={
                "fk_code": fee_code,
                "unit": "KG",
                "amount": random.randint(10,99),
                "currency_code": currency_code
            }
        fee_values_list.append(fee_data)
    request_data["fee_values"]=fee_values_list
    request_url = url.fms + "/api/BsnReconcile/Create"
    print(request_url)
    data = requests.post(url=request_url, json=request_data).text
    if eval(data)["message"] == "成功":
        print("补收费用信息推送fms成功！！！", request_data,data)
        return shipper_code
    else:
        print("补收费用信息推送fms失败",request_data)
def fms_lipei_tiaozhang_fee():
    def get_bill_data(customerCode):
        customer = get_customer_all(customerCode,source)
        ctmReceiptEntity = {
            "system_Id": 1,
            "CustomerId": customer["customer_id"],
            "AdjustmentCode": "PC"+ymd()+str(random.randint(10000,99999)),
            "FkCode": "CD",
            "Amount": random.randint(10,99),
            "CurrencyCode": "RMB",
            "Unit": "BS",
            "Remark": "运单号：脚本理赔调账",
            "CreateBy": 1,
            "SallerId": customer["express_sallerid"],
            "AccountType": None,
        }
        print(ctmReceiptEntity)
        return ctmReceiptEntity
    customer = get_bill_data(customerCode)
    url = "http://192.168.88.140:5001/FmsAPIServicesForHttpDelegate/mex,http://192.168.88.140:5004/FmsAPIServicesForHttpDelegate,AddFmsAdjustment"
    #data_get = 'WayBillNumber = "YT1819301009000005",SysSource = ""'
    # data_post = 'adjustmentInfo={"AdjustmentCode" :"","Amount" :1234,"CreateBy" : 1,"CurrencyCode" : "RMB","CustomerId" :21,"FkCode" :"CD","Remark" : "理赔测试","Unit" :"BS",}'
    #data_post = 'conditionList={"BaId": "0","BillDate": "2020-09-01T10:43:45.355394+08:00","CreateBy": "0","CustomerBodyId": "0","CustomerId": "0","OgId": "0","SallerType": "0","SystemId": "0"}'
    data_post1 = 'adjustmentInfo='+str(customer)
    print(data_post1)
    re_data = request.request_wcf(url=url, data=data_post1)
    print(re_data)
def fms_lipei_kanwu_fee(ShipperCode):
    def get_bill_data(customerCode):
        customer = get_customer_all(customerCode,source)
        ctmReceiptEntity = {
            "CustomerId": customer["customer_id"],
            "AdjustmentCode": "PC"+ymd()+str(random.randint(10000,99999)),
            "ShipperCode": ShipperCode,
            "FkCode": "CD",
            "Amount": random.randint(10,99),
            "CurrencyCode": "RMB",
            "Unit": "BS",
            "Remark": "理赔:不想要",
            "CreateBy": 1,
            "system_Id": 1,
            "BsnType": "N"
        }
        print(ctmReceiptEntity)
        return ctmReceiptEntity
    customer = get_bill_data(customerCode)
    url = "http://192.168.88.140:5001/FmsAPIServicesForHttpDelegate/mex,http://192.168.88.140:5004/FmsAPIServicesForHttpDelegate,AddFmsCostCorrect"
    #data_get = 'WayBillNumber = "YT1819301009000005",SysSource = ""'
    # data_post = 'adjustmentInfo={"AdjustmentCode" :"","Amount" :1234,"CreateBy" : 1,"CurrencyCode" : "RMB","CustomerId" :21,"FkCode" :"CD","Remark" : "理赔测试","Unit" :"BS",}'
    #data_post = 'conditionList={"BaId": "0","BillDate": "2020-09-01T10:43:45.355394+08:00","CreateBy": "0","CustomerBodyId": "0","CustomerId": "0","OgId": "0","SallerType": "0","SystemId": "0"}'
    data_post1 = 'costCorrigInfo='+str(customer)
    print(data_post1)
    re_data = request.request_wcf(url=url, data=data_post1)
    print(re_data)
def fms_kanwu_fee():
    def get_bill_data(customerCode, bill_time):
        customer = get_customer_all(customerCode,source)
        ctmReceiptEntity = {
            "AccountType": "RMB",
            "Amount": "998",
            # "AuditBy": "",
            # "AuditOn": "2018/9/12",
            "BodyId": "12",
            "CreateBy": "651",
            # "CreateOn": "2019/8/12",
            "CurrencyCode": "HKD",
            "CustomerId": "1445",
            "HandlingFee": "100",
            "HandlingRates": "10",
            # "LastOperationBy": "",
            # "LastOperationOn": "2019/8/12",
            "OgId": "4",
            "Pay": "",
            "PayAccounts": "",
            "PayMode": "1000",
            "Rate": "0.789",
            "Rece": "坂田",
            "ReceAccounts": "laidongyun@yunexpress.com",
            "ReceOgId": "4",
            "ReceSite": "74",
            # "ReceTime": "2019/8/12",
            "ReceiptIdentif": "F",
            "ReceiptType": "1",
            "Remark": "接口测试",
            # "RtId": "0",
            "SallerGroup": "140",
            "SallerId": "1558",
            "SettlementMode": "EE",
            # "State":"false",
            "TranMode": "I",
            "TransactionMode": "2",
            "TransactionNo": "",
            "VerificationAmount": "0"
        }
        print(ctmReceiptEntity)
        return ctmReceiptEntity
    customer = get_bill_data(customerCode,now())
    url = "http://192.168.88.140:5001/FmsAPIServicesForHttpDelegate/mex,http://192.168.88.140:5004/FmsAPIServicesForHttpDelegate,CreateShipperBill"
    #data_get = 'WayBillNumber = "YT1819301009000005",SysSource = ""'
    # data_post = 'adjustmentInfo={"AdjustmentCode" :"","Amount" :1234,"CreateBy" : 1,"CurrencyCode" : "RMB","CustomerId" :21,"FkCode" :"CD","Remark" : "理赔测试","Unit" :"BS",}'
    #data_post = 'conditionList={"BaId": "0","BillDate": "2020-09-01T10:43:45.355394+08:00","CreateBy": "0","CustomerBodyId": "0","CustomerId": "0","OgId": "0","SallerType": "0","SystemId": "0"}'

    data_post1 = 'conditionList='+str(customer)
    print(data_post1)
    re_data = request.request_wcf(url=url, data=data_post1)
    print(re_data)

if __name__ == "__main__":
    lading_index =lading_generate() #xxx-2040xxxx 提单序列号，避免重复
    waybill_number = random.randint(10000000,99999999) #运单序列号
    bag_number = 2 #袋子数量
    Charge_Weight = 1.188 #空运提单重量
    fee_number = 3 #空运提单费用个数  末端费用项个数
    yt_number = 5#袋子的运单数量
    transfertype = 1 #不等于1 则随机状态 运单的转运状态
    ifotherfee = 1 #空运提单费用是否需要其他费用项
    car_number = 10 #卡车序列号
    diaobo_number = random.randint(100000,999999)
    ifoversea = 2 #1海外中转，2发货中港
    operation_type_code = ["ST", "CL", "CI", "CO", "PU"]
    operation_type_code = random.choice(operation_type_code)
    transport_type_code = "KC"  #运输方式(KC卡车、AN航空、WL快递)
    server_list = ["yif"]#,"TEST008""AB123","yif" #"5555555"发货中转
    chongpai_server = "TEST007"
    #servercode =random.choice(server_list)
    CountryCode="MD"
    transit_country="MX"
    org_code="43"
    destination="CC"
    qg_servercode="YIFQG" #YIFQG YS
    fh_servercode = "5555555"  # YIFQG YS
    customerCode = "C00223"  # "C00223","C00144","C00126","C00350","C00261" #客户代码-运单使用
    wt_customerCode ="C02672"#wt客户C02672 100001 C02621
    source = 1  # 系统来源 1 YT 2 WT
    bill_count=1
    currency="RMB"
    data_list=[]
    for i in range(1):
        print("第%s个提单："%(i+1))
        lading_index = lading_generate()
        servercode = random.choice(server_list)
        print(servercode)
        #fms_lipei_tiaozhang_fee()
        #data = request_yt(waybill_number, customerCode, transfertype, servercode, 0, source)
        # fms_lipei_kanwu_fee(ShipperCode=data)
        #公用袋号——运单
        bags,shippers,bag_shipper_list = data_bag_shipper_list(bag_number, waybill_number, customerCode, yt_number, servercode, transfertype, source)
        # # #空运提单费用
        lading_number = request_airlading_withbag_fee(lading_number=str(lading_index+i), bag_list=bags, shipper_list=shippers, customerCode=customerCode, servercode=servercode, Charge_Weight=Charge_Weight,currency=currency,fee_number=fee_number, source=source)
        # # # 清关提单费用
        #request_customer_withbag_fee(lading_number=lading_number, bag_list=bags, shipper_list=shippers, qg_servercode=qg_servercode, customerCode=customerCode, if_vat=0, source=1)
        # # # 清关VAT费用
        #request_customer_withbag_fee(lading_number=lading_number, bag_list=bags, shipper_list=shippers,qg_servercode=qg_servercode, customerCode=customerCode,Charge_Weight=Charge_Weight, Currency=currency, if_vat=1, source=1)
        # # # 重派费用-不经过报价                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        #海外重派-不经过报价
        #request_chongpai_withbag_fee(shipper_list=shippers, customerCode=customerCode, servercode=servercode, if_pqm=0, source=source)
        # # # 理赔费用
        # #request_lipei_with_bag(shipper_list=shippers, servercode=servercode, source=source)
        # # # 中转费用-不经过报价
        #request_car_with_bag_fee(data=car_number, CountryCode=CountryCode, transit_country=transit_country, bag_list=bags, customerCode=customerCode, source=source,servercode=servercode, if_pqm=0, iffahuo=1)
        # # # 调拨-费用-不经过报价0 经过报价1
        #request_diaobo_withbag_fee(bag_list=bag_shipper_list, shipper_list=shippers, diaobo_number=diaobo_number,transport_type_code=transport_type_code,servercode=servercode, if_pqm=1, source=source)
        # # # 发货中转费用 -经过报价
        #request_fahuo_withbag_fee(bag_list=bags, org_code=org_code, destination=destination, charge_weight=Charge_Weight, shipper_list=shippers, servercode=fh_servercode, if_pqm=1,source=source)
        # # #request_airlading(str(lading_index),bag_number=3)
        #request_bag(source=1)
        #request_bag_yt(waybill_number+i,customerCode,yt_number,transfertype,source)
        #request_customer(str(lading_index), bag_number=3,source=1)
        #request_car(str(lading_index), bag_number=3,source=1)
        #data = request_yt(waybill_number+i,customerCode,transfertype,servercode,0,source)
        #YT 末端
        #data = request_yt(waybill_number, customerCode, transfertype, servercode, 0, source)
        #WT 末端
        #data = request_yt(waybill_number + i, customerCode=wt_customerCode, transfertype=transfertype, servercode=servercode,if_pqm=1, source=2)
        # WT 补收
        #wt_bushou_data(dzbm="KYDZ0001", shipper_code=data, bsn_type="N", server_code=servercode,customer_code=wt_customerCode, currency_code=currency, source=2)
        # #WT 空运
        #data = request_airlading_fee_withoutbag(lading_index = str(lading_index+i), customerCode=wt_customerCode, Charge_Weight=Charge_Weight, servercode=servercode,if_pqm=1, source=2)
        #wt_bushou_data(dzbm="KYDZ0002", shipper_code=data, bsn_type="A", server_code=servercode,customer_code=wt_customerCode, currency_code=currency, source=2)
        # # WT 清关
        data = request_customer_fee_withoutbag(lading_index = str(lading_index+i),servercode=servercode,qg_servercode=qg_servercode, customerCode=wt_customerCode, Charge_Weight=Charge_Weight,if_pqm=1, source = 2)
        wt_bushou_data(dzbm="KYDZ0003", shipper_code=data, bsn_type="Q", server_code=servercode,customer_code=wt_customerCode, currency_code=currency, source=2)
        # # WT 中转
        #data = request_car_fee_withoutbag(car_number+i, CountryCode, transit_country, wt_customerCode, servercode,if_pqm=1, source=2)
        #wt_bushou_data(dzbm="KYDZ0004", shipper_code=data, bsn_type="T", server_code=servercode,customer_code=wt_customerCode, currency_code=currency, source=2)

        # data = request_airlading_fee(lading_index=str(lading_index),bag_number=bag_number,
        #                      waybill_number=waybill_number,customerCode=customerCode,
        #                      Charge_Weight=Charge_Weight,yt_number=yt_number,
        #                     fee_number=fee_number,transfertype=transfertype,
        #                      ifotherfee=ifotherfee,servercode=servercode,source=source)

        #data_customer_fee(lading_number="100-202009r11")
        #清关提单费用
        # data=request_customer_fee(lading_index=str(lading_index+i),bag_number=bag_number,
        #                        waybill_number=waybill_number,customerCode=customerCode,
        #                        Charge_Weight=Charge_Weight,yt_number=yt_number,
        #                       fee_number=fee_number,transfertype=transfertype,
        #                        ifotherfee=ifotherfee,servercode=servercode,source=source,qg_servercode=qg_servercode)
        #清关提单有vat费用
        # data=request_customer_fee(lading_index=str(lading_index+i),bag_number=bag_number,
        #                       waybill_number=waybill_number,customerCode=customerCode,
        #                       Charge_Weight=Charge_Weight,yt_number=yt_number,
        #                       fee_number=fee_number,transfertype=transfertype,
        #                       ifotherfee=ifotherfee,servercode=servercode,source=source,qg_servercode=qg_servercode,if_vat=1)
        #request_lipei(waybill_number, customerCode, transfertype, source)
        #request_chongpai(waybill_number,customerCode,transfertype,servercode,source)

        #data = request_chongpai_fee(waybill_number+i, customerCode, transfertype, servercode, source)
        #data = request_yt(waybill_number+i,customerCode,transfertype,servercode,source)


        #data = request_lipei(waybill_number,customerCode,transfertype,servercode,source)
        #data_yd_fee(waybill_number, fee_number, source)
        #request_yd_fee(waybill_number, fee_number, customerCode, transfertype, source)

        #data = request_car_fee(car_number+i,CountryCode,transit_country,bag_number,waybill_number,customerCode,yt_number,servercode,transfertype,source,iffahuo=1)
        #data_fandian(shipperCode="10000", source=1)
        #data = request_fandian(waybill_number, fee_number, customerCode, transfertype,servercode, source)#应收返点
        #data = request_data_fandian_income(waybill_number,customerCode,transfertype,servercode,source) #应付返点

        #data = request_data_fandian_all(waybill_number, customerCode, transfertype, servercode, source)#应付/应收返点

        #request_diaobo(bag_number,waybill_number,customerCode,yt_number,transfertype,transport_type_code,source)
        #request_diaobo_kunei(waybill_number, customerCode, transfertype,operation_type_code, source)

        #request_kunei_fee2(waybill_number, customerCode, yt_number, transfertype, source)
        #request_diaobo(bag_number, waybill_number, customerCode, yt_number, transfertype, source)

        #data= request_diaobo_fee(bag_number, waybill_number+i, customerCode, yt_number, transfertype,transport_type_code,servercode,if_pqm, source)
        #data = request_kunei_fee2(waybill_number,customerCode,yt_number,servercode,transfertype,source)
        # request_fahuo(server_code=servercode, box=bag_number, bill_count=yt_number, charge_weight=Charge_Weight, org_code=org_code, destination=org_code, source=source, iffahuo=iffahuo,
        #               waybill_number=waybill_number, customerCode=customerCode, transfertype=transfertype)
        #发货中转费用
        # data=request_fahuo_fee(servercode=fh_servercode, box=bag_number, bill_count=yt_number, charge_weight=Charge_Weight, org_code=org_code, destination=destination, source=source, iffahuo=2,
        #             waybill_number=waybill_number, customerCode=customerCode, transfertype=transfertype)
        # re_data = {"waybill_code":"YF219177651710363494","weight":24.000,"ServerPlace_Code":None,"Country":"CN","system_source":"YT"}
        # re_data["waybill_code"]=data
        #data_list.append(data)
        #data_list.append(data)
        #fahuo_with_bag(bag_list=["111"], server_code="yif", box=1, bill_count=1, charge_weight=3.3, org_code="33", destination="44", source=1)
    #print(data_list)
    for i in data_list:
        print(i)