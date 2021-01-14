import pymysql
import time
import random
from fms.config import url
import json
import requests
def now():
    return time.strftime("%Y-%m-%d %H:%M:%S")
def connect_sql(database_name):
    try:
        conn = pymysql.connect(
            host = "10.168.95.60",
            port = 3306,
            user="root",
            password="a135246A",
            database=database_name,
            charset="utf8")
        print(conn)
        cursor = conn.cursor()
        return cursor,conn
    except Exception as e:
        print(e)
def connect_it_100(database_name):
    try:
        conn = pymysql.connect(
            host = "IT-100",
            port = 3308,
            user="mysql",
            password="a135246A",
            database=database_name,
            charset="utf8")
        print(conn)
        cursor = conn.cursor()
        return cursor,conn
    except Exception as e:
        print(e)
def connect_bms(database_name):
    try:
        conn = pymysql.connect(
            host = "10.168.95.227",
            port = 3306,
            user="bms_admin",
            password="sZ5VIfyCl!MsdfeW1D",
            database=database_name,
            charset="utf8")
        print(conn)
        cursor = conn.cursor()
        return cursor,conn
    except Exception as e:
        print(e)



def excute_sql(db,conn,sql):
    try:
        success = db.execute(sql)
        conn.commit()
        print(sql,"\n","成功",success,"条")
    except Exception as e:
        conn.rollback()
        print(e)
def fee_to_air_diaobo(lading_number,Server_Code,source,Charge_Weight,Currency,bs_time):
    request_data = {
  "airChargeResultValues": [
    {
      "air_Price_Value": 1.0,
      "air_Price_TotalValue": 2.0,
      "fk_code": "A4",
      "unit_Code": "KG",
      "getPrice_Type": "1",
      "currency": Currency
    }
  ],
  "price_number": 1,
  "waybill_Code": lading_number,
  "airService_type": "2",
  "volume_Weight": 4.0,
  "charge_Weight": Charge_Weight,
  "lading_Weight": 6.0,
  "server_Code": Server_Code,
  "source_id": source,
  "Current_date":bs_time
}
    print(request_data)
    request_url = url.fms + "api/CostAirTransfer/AddBillJson"
    print(request_url)
    data = requests.post(url=request_url, json=request_data).text
    print(data)
    if '"Code":0' in data:
        print("调拨空运费用推送pqm成功！！！", request_data)
        # return request_data["shipper_hawbcode"]
    else:
        print("调拨空运费用推送pqm失败", request_url, data, request_data)
def fee_to_pqm(lading_number,Volume_Weight,Charge_Weight,AirService_type ):
    try:
        dts_db, dts_conn = connect_it_100(database_name="pqm_db")
        sql = "select * from cost_charged_json limit 1"
        #     price = ["YT004-RH-ORD-PVG-FWZF-GDZF ",
        # "YT012-OZ-ORD-TAO-CS2-Q1",
        # "YT012-OZ-ORD-TAO-CS2-Q1",
        # "YT012-OZ-ORD-TAO-CS2-Q1",
        # "YT012-OZ-ORD-TAO-CS2-Q1",
        # "YT001-00-PEK-MFM-FWF-Q1",
        # "YT001-QR-PEK-MFM-FWF-Q1",
        # "YT002-CZ-CGO-KIX-FWZF-GDZF ",
        # "YT001-BR-PEK-MFM-QW01-Y002 ",
        # "YT008-GA-ORD-SYD-FWF-XIAOXIE ",
        # "YT008-GA-ORD-SYD-FWF-XIAOXIE ",
        # "YT001-OZ-ORD-BLQ-FW01-Y001 ",
        # "YT001-OZ-ORD-BLQ-FW01-Y001 ",
        # "YT001-OZ-ORD-BLQ-FW01-Y001 ",
        # "YT024-MH-PEK-BRU-QW01-Y001 ",
        # "YT024-MH-PEK-BRU-QW01-Y001 ",
        # "YT008-KL-ORD-SYD-FW01-Y001 ",
        # "YT008-KL-ORD-SYD-FW01-Y001 ",
        # "YT008-KL-ORD-SYD-FW01-Y001 ",
        # "YT024-MH-PEK-BRU-FWF-GDZF",
        # "YT024-MH-PEK-BRU-FWF-GDZF",
        # "YT024-CA-PEK-BRU-FWZF-GDF",
        # "CSSJ-BR-ZAZ-BCN-FWZF-FDF ",
        # "CSSJ-UA-PEK-CGO-FWF-GDZF ",
        # "CSSJ-UA-PEK-CGO-FWF-GDZF ",
        # "YT024-TA-PEK-BRU-CS2-CS343 ",
        # "YT008-PO-CAN-ORD-FWZF-FDF",
        # "YT008-PO-CAN-ORD-FWZF-FDF"]
        price = "yif-YI-HKG-AMS-FWF-FDZF" #报价系统的报价成本
        data = price.split("-")
        weight = random.randint(1000, 9999)
        volume = random.randint(1000, 9999)
        fee_sql = "INSERT INTO `pqm_db`.`cost_charged_json`( `waybill_code`, `jsonstring`, `opt_state`, `create_time`, `error_count`, `error_message`, `system_source`, `md5`, `cost_type`) " \
                  "VALUES ('%s', '{\"Waybill_Code\":\"%s\",\"Volume_Weight\":%s,\"Charge_Weight\":%s,\"PV_Weight\":0.0,\"PV_Plate\":\"H1\",\"Tune_Weight\":null,\"AirServer_Code\":null,\"Server_Code\":\"%s\",\"Airline_Two_Code\":\"%s\",\"Airport_Code_Start\":\"%s\",\"Airport_Code_End\":\"%s\",\"Rule_Type\":\"ZB\",\"Server_Type\":\"%s\",\"Quo_Type\":\"%s\",\"Status\":null,\"Current_date\":\"2020-10-06T00:00:00\",\"System_Code\":\"YT\",\"OrgShortCode\":\"YT-SZ\",\"Unit_Code\":null,\"Ticket\":300,\"Box_Number\":20}', 'D', '2020-11-06 15:40:07', NULL, '', 'YT', '%s', " \
                  "'%s');" % (
                  lading_number, lading_number, Volume_Weight, Charge_Weight, data[0], data[1], data[2], data[3], data[4], data[5],
                  lading_number,AirService_type)
        print(fee_sql)
        excute_sql(dts_db, dts_conn, fee_sql)
        print("空运提单费用插入PQM成功")
    except Exception as e:
        print(e)
def fee_to_diaobo_air(lading_number, Volume_Weight, Charge_Weight):
    try:
        dts_db, dts_conn = connect_it_100(database_name="pqm_db")
        sql = "select * from cost_charged_json limit 1"
        #     price = ["YT004-RH-ORD-PVG-FWZF-GDZF ",
        # "YT012-OZ-ORD-TAO-CS2-Q1",
        # "YT012-OZ-ORD-TAO-CS2-Q1",
        # "YT012-OZ-ORD-TAO-CS2-Q1",
        # "YT012-OZ-ORD-TAO-CS2-Q1",
        # "YT001-00-PEK-MFM-FWF-Q1",
        # "YT001-QR-PEK-MFM-FWF-Q1",
        # "YT002-CZ-CGO-KIX-FWZF-GDZF ",
        # "YT001-BR-PEK-MFM-QW01-Y002 ",
        # "YT008-GA-ORD-SYD-FWF-XIAOXIE ",
        # "YT008-GA-ORD-SYD-FWF-XIAOXIE ",
        # "YT001-OZ-ORD-BLQ-FW01-Y001 ",
        # "YT001-OZ-ORD-BLQ-FW01-Y001 ",
        # "YT001-OZ-ORD-BLQ-FW01-Y001 ",
        # "YT024-MH-PEK-BRU-QW01-Y001 ",
        # "YT024-MH-PEK-BRU-QW01-Y001 ",
        # "YT008-KL-ORD-SYD-FW01-Y001 ",
        # "YT008-KL-ORD-SYD-FW01-Y001 ",
        # "YT008-KL-ORD-SYD-FW01-Y001 ",
        # "YT024-MH-PEK-BRU-FWF-GDZF",
        # "YT024-MH-PEK-BRU-FWF-GDZF",
        # "YT024-CA-PEK-BRU-FWZF-GDF",
        # "CSSJ-BR-ZAZ-BCN-FWZF-FDF ",
        # "CSSJ-UA-PEK-CGO-FWF-GDZF ",
        # "CSSJ-UA-PEK-CGO-FWF-GDZF ",
        # "YT024-TA-PEK-BRU-CS2-CS343 ",
        # "YT008-PO-CAN-ORD-FWZF-FDF",
        # "YT008-PO-CAN-ORD-FWZF-FDF"]
        price = "yif-CX-HKG-AMS-DB2-DB"  # 报价系统的报价成本
        data = price.split("-")
        weight = random.randint(1000, 9999)
        volume = random.randint(1000, 9999)
        fee_sql = "INSERT INTO `pqm_db`.`cost_charged_json`( `waybill_code`, `jsonstring`, `opt_state`, `create_time`, `error_count`, `error_message`, `system_source`, `md5`, `cost_type`, `db_type`) " \
                  "VALUES ('%s', '{\"Waybill_Code\":\"%s\",\"Volume_Weight\":%s,\"Charge_Weight\":%s,\"PV_Weight\":0.0,\"PV_Plate\":\"H1\",\"Tune_Weight\":null,\"AirServer_Code\":null,\"Server_Code\":\"%s\",\"Airline_Two_Code\":\"%s\",\"Airport_Code_Start\":\"%s\",\"Airport_Code_End\":\"%s\",\"Rule_Type\":\"ZB\",\"Server_Type\":\"%s\",\"Quo_Type\":\"%s\",\"Status\":null,\"Current_date\":\"2020-10-06T00:00:00\",\"System_Code\":\"YT\",\"OrgShortCode\":\"YT-SZ\",\"Unit_Code\":null,\"Ticket\":300,\"Box_Number\":20}', 'D', '2020-11-06 15:40:07', NULL, '', 'YT', '%s', " \
                  "'DB', 'DB-KY');" % (
                      lading_number, lading_number, Volume_Weight, Charge_Weight, data[0], data[1], data[2], data[3],
                      data[4], data[5],
                      lading_number)
        print(fee_sql)
        excute_sql(dts_db, dts_conn, fee_sql)
        print("空运调拨费用插入PQM成功")
    except Exception as e:
        print(e)
def fee_to_paisong(Waybill_Code,Server_Code,ServerPlace_Code,B_time):
    try:
        dts_db, dts_conn = connect_bms(database_name="bms_db")
        # sql = "select * from cost_charged_json limit 1"
        # weight = random.randint(1000, 9999)
        # volume = random.randint(1000, 9999)
        # fee_sql = "INSERT INTO `pqm_db`.`bil_jsoncharged_cost`(`waybill_code`, `jsonstring`, `opt_state`, `create_time`, `error_count`, `error_message`, `system_source`, `md5`) " \
        #       "VALUES ('%s', '{\"Waybill_Code\":\"%s\",\"Currency_Code\":\"YD\",\"Customer_Code\":\"\",\"Product_Code\":\"\",\"Server_Code\":\"%s\",\"Server_Type\":\"PS\",\"ServerPlace_Code\":\"%s\",\"System_Code\":\"YT\",\"Og_id_ChargeFirst\":\"YT-SZ\",\"Og_id_ChargeSecond\":\"\",\"Arrival_Date\":\"2020-10-28T09:18:16\",\"Country\":\"AR\",\"Postcode\":\"518000\",\"City\":\"005001\",\"Province\":\"005\",\"Charge_Weight\":1.852,\"Unit_Code\":\"KG\",\"Unit_Length\":\"CM\",\"Unit_Area\":null,\"Unit_Bulk\":null,\"Unit_Volume\":null,\"Pieces\":5,\"Category_Code\":\"5\",\"Declared_Value\":0.8,\"Currency\":\"RMB\",\"Tariff\":\"0.6\",\"Airline\":\"中国南方\",\"Departure_Airport\":\"宝安机场\",\"Destination_Airport\":\"伦敦机场\",\"Customs_Clearance_Port\":\"QHKA\",\"Start_Place\":\"MD\",\"end_Place\":\"MX\",\"Remark\":null,\"Ticket\":5,\"HS_Code\":5,\"Box_Number\":5,\"First_Long\":0.0,\"Two_Long\":0.0,\"Three_Long\":0.0,\"BusinessTime\":\"2020-03-11T00:00:00\",\"airline_two_code\":\"BR\",\"detailEntities\":null,\"Goods_Code\":null,\"Extra_ServicesList\":[{\"ExtraService\":\"rt\",\"ExtraService_Coefficient\":0.8},{\"ExtraService\":\"py\",\"ExtraService_Coefficient\":0.7},{\"ExtraService\":\"aa\",\"ExtraService_Coefficient\":0.6}],\"IsFinalCharge\":false,\"ChargType\":null,\"HCustomsNumber\":0.0,\"MCustomsNumber\":0.0,\"LCustomsNumber\":0.0,\"HCargoValueNumber\":0.0,\"MCargoValueNumber\":0.0,\"LCargoValueNumber\":0.0,\"Charge_Volume\":5.0,\"Truck_Number\":1,\"Tray_Number\":1,\"TimeUnti\":\"Day\",\"TimeVaule\":5,\"TrackingNumber\":\"33P\",\"StartCountry\":\"IT\",\"EndCountry\":\"DE\",\"HAWB_Number\":3,\"Start_TransferPoint\":\"MD\",\"End_TransferPoint\":\"MX\"}', 'D', '%s', 0, '', 'YT'," \
        #       " '%s')"% (Waybill_Code, Waybill_Code, Server_Code,ServerPlace_Code,B_time, Waybill_Code)
        # print(fee_sql)
        # excute_sql(dts_db, dts_conn, fee_sql)
        # print("派送费用插入PQM成功")

        sql = "INSERT INTO `bms_db`.`jsn_cost_deliver`(`waybill_code`, `server_code`, `settlement_code`, `arrival_date`, `org_short_code`, `country`, `postcode`, `charge_weight`, `weight_unit`, `opt_state`, `create_time`, `error_count`, `error_message`, `system_source`, `md5`) VALUES " \
              "('%s', '%s', '', NOW(), NULL, NULL, NULL, NULL, NULL, 'D', NOW(), 0, '', 'YT', '');"% (Waybill_Code, Server_Code)
        print(sql)
        excute_sql(dts_db, dts_conn, sql)
        select_sql = "select id from jsn_cost_deliver where waybill_code='%s';"%(Waybill_Code)
        excute_sql(dts_db, dts_conn, select_sql)
        id =dts_db.fetchall()[0][0]
        insert_sql = "INSERT INTO `bms_db`.`jsn_cost_deliver_json`(`id`, `waybill_code`, `jsonstring`) VALUES ( %s, '%s'," \
                     " '{\"Waybill_Code\":\"%s\",\"Currency_Code\":\"YD\",\"Customer_Code\":\"\",\"Product_Code\":\"\",\"Server_Code\":\"%s\",\"Server_Type\":\"PS\",\"ServerPlace_Code\":\"%s\",\"System_Code\":\"YT\",\"Og_id_ChargeFirst\":\"YT-SZ\",\"Og_id_ChargeSecond\":\"\",\"Arrival_Date\":\"2020-10-28T09:18:16\",\"Country\":\"AR\",\"Postcode\":\"518000\",\"City\":\"005001\",\"Province\":\"005\",\"Charge_Weight\":1.852,\"Unit_Code\":\"KG\",\"Unit_Length\":\"CM\",\"Unit_Area\":null,\"Unit_Bulk\":null,\"Unit_Volume\":null,\"Pieces\":5,\"Category_Code\":\"5\",\"Declared_Value\":0.8,\"Currency\":\"RMB\",\"Tariff\":\"0.6\",\"Airline\":\"中国南方\",\"Departure_Airport\":\"宝安机场\",\"Destination_Airport\":\"伦敦机场\",\"Customs_Clearance_Port\":\"QHKA\",\"Start_Place\":\"MD\",\"end_Place\":\"MX\",\"Remark\":null,\"Ticket\":5,\"HS_Code\":5,\"Box_Number\":5,\"First_Long\":0.0,\"Two_Long\":0.0,\"Three_Long\":0.0,\"BusinessTime\":\"2020-03-11T00:00:00\",\"airline_two_code\":\"BR\",\"detailEntities\":null,\"Goods_Code\":null,\"Extra_ServicesList\":[{\"ExtraService\":\"rt\",\"ExtraService_Coefficient\":0.8},{\"ExtraService\":\"py\",\"ExtraService_Coefficient\":0.7},{\"ExtraService\":\"aa\",\"ExtraService_Coefficient\":0.6}],\"IsFinalCharge\":false,\"ChargType\":null,\"HCustomsNumber\":0.0,\"MCustomsNumber\":0.0,\"LCustomsNumber\":0.0,\"HCargoValueNumber\":0.0,\"MCargoValueNumber\":0.0,\"LCargoValueNumber\":0.0,\"Charge_Volume\":5.0,\"Truck_Number\":1,\"Tray_Number\":1,\"TimeUnti\":\"Day\",\"TimeVaule\":5,\"TrackingNumber\":\"33P\",\"StartCountry\":\"IT\",\"EndCountry\":\"DE\",\"HAWB_Number\":3,\"Start_TransferPoint\":\"MD\",\"End_TransferPoint\":\"MX\"}'" \
                     ");"% (id,Waybill_Code, Waybill_Code, Server_Code,ServerPlace_Code,)
        excute_sql(dts_db, dts_conn, insert_sql)
        print("派送费用插入PQM成功")

    except Exception as e:
        print(e)
def fee_to_kunei(Waybill_Code,date_time,Procedure_Type,Og_id_ChargeFirst):

    request_data = {
    "shipper_hawbcode":Waybill_Code,
    "orig_warehouse_og_code":Og_id_ChargeFirst,
    "operation_type_code":Procedure_Type,
    "operation_time":date_time,
    "weight":"1.5",
    "weight_unit_code":"KG",
    "system_source_code":"101"
}
    print(request_data)
    request_url = url.pqm_url + "api/CostAllocate/AddBillJson"
    print(request_url)
    data = requests.post(url=request_url, json=request_data).text
    print(data)
    if '推送成功' in data:
        print("库内调拨费用插入PQM成功！！！", request_data)
        # return request_data["shipper_hawbcode"]
    else:
        print("库内调拨费用推送pqm失败", request_url, data, request_data)
    # dts_db, dts_conn = connect_bms(database_name="bms_db")#换库和表2个jsn_cost_allocate  jsn_cost_allocate_json
    # try:
    #     Waybill_Code=Waybill_Code
    #     date_time =date_time
    #     Procedure_Type=Procedure_Type
    #     Og_id_ChargeFirst=Og_id_ChargeFirst
    #     kunei_fee_sql = "INSERT INTO `pqm_db`.`cost_charged_json`( `waybill_code`, `jsonstring`, `opt_state`, `create_time`, `error_count`, `error_message`, `system_source`, `md5`, `cost_type`, `db_type`, `procedure_code`)"\
    #     "VALUES ('%s', '{\"Waybill_Code\":\"%s\",\"Charge_Date\":\"%s\",\"Charge_Weight\":12.0,\"Unit_Code\":None,\"Procedure_Type\":\"%s\",\"Og_id_ChargeFirst\":\"%s\",\"System_Code\":\"YT\"}', 'O', '%s', 0, '', 'YT', '', 'CZ', NULL, '%s');"%(Waybill_Code,Waybill_Code,date_time,Procedure_Type,Og_id_ChargeFirst,date_time,Procedure_Type)
    #     #print(kunei_fee_sql)
    #     excute_sql(dts_db, dts_conn, kunei_fee_sql)
    #     print("库内调拨费用插入PQM成功")
    #     dts_db.close()
    #     dts_conn.close()
    # except Exception as e:
    #     dts_db.close()
    #     dts_conn.close()
    #     print(e)
def fee_to_air():
    dts_db, dts_conn = connect_it_100(database_name="pqm_db")
    sql = "select * from cost_charged_json limit 1"
    #     price = ["YT004-RH-ORD-PVG-FWZF-GDZF ",
    # "YT012-OZ-ORD-TAO-CS2-Q1",
    # "YT012-OZ-ORD-TAO-CS2-Q1",
    # "YT012-OZ-ORD-TAO-CS2-Q1",
    # "YT012-OZ-ORD-TAO-CS2-Q1",
    # "YT001-00-PEK-MFM-FWF-Q1",
    # "YT001-QR-PEK-MFM-FWF-Q1",
    # "YT002-CZ-CGO-KIX-FWZF-GDZF ",
    # "YT001-BR-PEK-MFM-QW01-Y002 ",
    # "YT008-GA-ORD-SYD-FWF-XIAOXIE ",
    # "YT008-GA-ORD-SYD-FWF-XIAOXIE ",
    # "YT001-OZ-ORD-BLQ-FW01-Y001 ",
    # "YT001-OZ-ORD-BLQ-FW01-Y001 ",
    # "YT001-OZ-ORD-BLQ-FW01-Y001 ",
    # "YT024-MH-PEK-BRU-QW01-Y001 ",
    # "YT024-MH-PEK-BRU-QW01-Y001 ",
    # "YT008-KL-ORD-SYD-FW01-Y001 ",
    # "YT008-KL-ORD-SYD-FW01-Y001 ",
    # "YT008-KL-ORD-SYD-FW01-Y001 ",
    # "YT024-MH-PEK-BRU-FWF-GDZF",
    # "YT024-MH-PEK-BRU-FWF-GDZF",
    # "YT024-CA-PEK-BRU-FWZF-GDF",
    # "CSSJ-BR-ZAZ-BCN-FWZF-FDF ",
    # "CSSJ-UA-PEK-CGO-FWF-GDZF ",
    # "CSSJ-UA-PEK-CGO-FWF-GDZF ",
    # "YT024-TA-PEK-BRU-CS2-CS343 ",
    # "YT008-PO-CAN-ORD-FWZF-FDF",
    # "YT008-PO-CAN-ORD-FWZF-FDF"]
    price = "yif-YI-HKG-AMS-FWF-FDZF"
    lading_number = ["100-49970925"]
    for i in range(len(lading_number)):
        data = price.split("-")
        lading_number = lading_number[i]
        weight = random.randint(1000, 9999)
        volume = random.randint(1000, 9999)
        fee_sql = "INSERT INTO `pqm_db`.`cost_charged_json`( `waybill_code`, `jsonstring`, `opt_state`, `create_time`, `error_count`, `error_message`, `system_source`, `md5`, `cost_type`) " \
                  "VALUES ('%s', '{\"Waybill_Code\":\"%s\",\"Volume_Weight\":%s,\"Charge_Weight\":%s,\"PV_Weight\":0.0,\"PV_Plate\":\"H1\",\"Tune_Weight\":None,\"AirServer_Code\":None,\"Server_Code\":\"%s\",\"Airline_Two_Code\":\"%s\",\"Airport_Code_Start\":\"%s\",\"Airport_Code_End\":\"%s\",\"Rule_Type\":\"ZB\",\"Server_Type\":\"%s\",\"Quo_Type\":\"%s\",\"Status\":None,\"Current_date\":\"2020-07-06T00:00:00\",\"System_Code\":\"YT\",\"OrgShortCode\":\"YT-SZ\",\"Unit_Code\":None,\"Ticket\":300,\"Box_Number\":20}', 'D', '2020-07-06 15:40:07', NULL, '', 'YT', '%s', " \
                  "'KY');" % (
                  lading_number, lading_number, volume, weight, data[0], data[1], data[2], data[3], data[4], data[5],
                  lading_number)
        print(fee_sql)
        excute_sql(dts_db, dts_conn, fee_sql)
    dts_db.close()
    dts_conn.close()
def fee_to_zhuanyun(Waybill_Code,Car_Number,Server_Code,source,Charge_Weight,Start_Place,end_Place,BusinessTime):
    if source==1:
        source="YT"
    else:
        source = "WT"
    data = {"Waybill_Code":Waybill_Code,"Currency_Code":"KC","Car_Number":Car_Number,"Customer_Code":None,"Product_Code":"","Server_Code":Server_Code,"Server_Type":None,"ServerPlace_Code":None,"System_Code":source,"Og_id_ChargeFirst":"YT-SZ","Og_id_ChargeSecond":None,"Arrival_Date":BusinessTime,"Country":None,"Postcode":None,"City":None,"Province":None,"Charge_Weight":Charge_Weight,"Unit_Code":"KG","Unit_Length":None,"Unit_Area":None,"Unit_Bulk":None,"Unit_Volume":None,"ExtraService":None,"ExtraService_Coefficient":None,"Pieces":0,"Category_Code":None,"Declared_Value":0.0,"Currency":None,"Tariff":None,"Airline":None,"Departure_Airport":None,"Destination_Airport":None,"Customs_Clearance_Port":None,"Start_Place":Start_Place,"end_Place":end_Place,"Remark":None,"Ticket":0,"HS_Code":0,"Box_Number":0,"First_Long":0.0,"Two_Long":0.0,"Three_Long":0.0,"BusinessTime":BusinessTime,"airline_two_code":None,"detailEntities":None,"Goods_Code":None,"IsFinalCharge":False,"ChargType":None,"HCustomsNumber":0.0,"MCustomsNumber":0.0,"LCustomsNumber":0.0,"HCargoValueNumber":0.0,"MCargoValueNumber":0.0,"LCargoValueNumber":0.0,"Charge_Volume":2.000,"Tray_Number":0,"Truck_Number":0,"TimeUnti":None,"TimeVaule":0,"TrackingNumber":None}
    request_data = {
    "waybill_code": Waybill_Code,
    "jsonstring": json.dumps(data, ensure_ascii=False),
    "system_source": source,
    "cost_type": "ZY"
}

    print(request_data)
    request_url = url.pqm_url + "api/CostTransfer/AddBillJson"
    print(request_url)
    data = requests.post(url=request_url, json=request_data).text
    print("发货中转返回值",data)
    if '"Code":0' in data:
        print("转运费用推送pqm成功！！！", request_data)
        # return request_data["shipper_hawbcode"]
    else:
        print("转运费用推送pqm失败", request_url, data, request_data)
def fee_to_qingguan(Waybill_Code,Server_Code,ServerPlace_Code,source,Charge_Weight,Customs_Clearance_Port,Currency,BusinessTime):
    if source==1:
        source="YT"
    else:
        source = "WT"
    data = {"Waybill_Code":Waybill_Code,"Server_Code":Server_Code,"System_Code":source,"Arrival_Date":BusinessTime,"Customs_Clearance_Port": Customs_Clearance_Port,"Charge_Weight":Charge_Weight,
            "Currency":Currency,"Declared_Value":random.randint(1,9),"ServerPlace_Code":ServerPlace_Code,"Server_Type":"QG","Currency_Code":"TD","Customer_Code":None,"Product_Code":"","Og_id_ChargeFirst":None,"Og_id_ChargeSecond":None,"Country":None,"Postcode":None,"City":None,"Province":None,"Unit_Code":"KG","Unit_Length":None,"Unit_Area":None,"Unit_Bulk":None,"Unit_Volume":None,"ExtraService":None,"ExtraService_Coefficient":None,"Pieces":0,"Category_Code":None,"Tariff":None,"Airline":None,"Departure_Airport":None,"Destination_Airport":None,"Remark":None,"Ticket":0,"HS_Code":0,"Box_Number":0,"First_Long":0.0,"Two_Long":0.0,"Three_Long":0.0,"BusinessTime":BusinessTime,"airline_two_code":None,"detailEntities":None,"Goods_Code":None,"IsFinalCharge":False,"ChargType":None,"HCustomsNumber":0.0,"MCustomsNumber":0.0,"LCustomsNumber":0.0,"HCargoValueNumber":0.0,"MCargoValueNumber":0.0,"LCargoValueNumber":0.0,"Charge_Volume":2.000,"Tray_Number":0,"Truck_Number":0,"TimeUnti":None,"TimeVaule":0,"TrackingNumber":None}
    request_data = {
    "waybill_code": Waybill_Code,
    "jsonstring": json.dumps(data, ensure_ascii=False),
    "system_source": source,
    "cost_type": "QG"
}
    print(request_data)
    request_url = url.pqm_url + "api/CostClearance/AddBillJson"
    print(request_url)
    data = requests.post(url=request_url, json=request_data).text
    print(data)
    if '"Code":0' in data:
        print("清关费用推送pqm成功！！！", request_data)
        # return request_data["shipper_hawbcode"]
    else:
        print("清关费用推送pqm失败", request_url, data, request_data)
def fee_to_wt(Waybill_Code,Server_Code,Product_Code,Customer_Code,income_type,source):
    if source==1:
        source="YT"
    else:
        source = "WT"
    # data = {"Waybill_Code":Waybill_Code,"Server_Code":Server_Code,"System_Code":source,"Arrival_Date":BusinessTime,"Customs_Clearance_Port": Customs_Clearance_Port,"Charge_Weight":Charge_Weight,
    #         "Currency":Currency,"Declared_Value":random.randint(1,9),"ServerPlace_Code":ServerPlace_Code,"Server_Type":"QG","Currency_Code":"TD","Customer_Code":None,"Product_Code":"","Og_id_ChargeFirst":None,"Og_id_ChargeSecond":None,"Country":None,"Postcode":None,"City":None,"Province":None,"Unit_Code":"KG","Unit_Length":None,"Unit_Area":None,"Unit_Bulk":None,"Unit_Volume":None,"ExtraService":None,"ExtraService_Coefficient":None,"Pieces":0,"Category_Code":None,"Tariff":None,"Airline":None,"Departure_Airport":None,"Destination_Airport":None,"Remark":None,"Ticket":0,"HS_Code":0,"Box_Number":0,"First_Long":0.0,"Two_Long":0.0,"Three_Long":0.0,"BusinessTime":BusinessTime,"airline_two_code":None,"detailEntities":None,"Goods_Code":None,"IsFinalCharge":False,"ChargType":None,"HCustomsNumber":0.0,"MCustomsNumber":0.0,"LCustomsNumber":0.0,"HCargoValueNumber":0.0,"MCargoValueNumber":0.0,"LCargoValueNumber":0.0,"Charge_Volume":2.000,"Tray_Number":0,"Truck_Number":0,"TimeUnti":None,"TimeVaule":0,"TrackingNumber":None}
    data = {
        "Waybill_Code": Waybill_Code,
        "Currency_Code": "YD",
        "Customer_Code": Customer_Code,
        "Product_Code": Product_Code,#"FDXGR-CA",
        "Server_Code": Server_Code,
        "ServerPlace_Code": None,
        "System_Code": "WT",
        "Og_id_ChargeFirst": "WT-SZ",
        "Og_id_ChargeSecond": None,
        "Arrival_Date": now(),
        "Country": None,
        "Postcode": None,
        "City": None,
        "Province": None,
        "Charge_Weight": random.randint(10,99),
        "Unit_Code": "KG",
        "Unit_Length": None,
        "Unit_Area": None,
        "Unit_Bulk": None,
        "Unit_Volume": None,
        "Pieces": 0,
        "Category_Code": None,
        "Declared_Value": 17415.02,
        "Currency": "USD",
        "Tariff": None,
        "Airline": None,
        "Departure_Airport": None,
        "Destination_Airport": None,
        "Customs_Clearance_Port": "LHR",
        "Start_Place": None,
        "end_Place": None,
        "Remark": None,
        "Working_Time": now(),
        "Ticket": 4558,
        "HS_Code": 0,
        "Box_Number": 103,
        "First_Long": 0,
        "Two_Long": 0,
        "Three_Long": 0,
        "BusinessTime": None,
        "airline_two_code": "KE",
        "detailEntities": [],
        "GoodsCode": None,
        "T_Declared_Value": 0,
        "GoodsNumber": 0,
        "Extra_ServicesList": None,
        "Goods_Code": None,
        "IsFinalCharge": False,
        "ChargType": None,
        "HCustomsNumber": 0,
        "MCustomsNumber": 772,
        "LCustomsNumber": 0,
        "HCargoValueNumber": 0,
        "MCargoValueNumber": 17415.02,
        "LCargoValueNumber": 0,
        "Charge_Volume": 0,
        "Tray_Number": 0,
        "Truck_Number": 0,
        "TimeUnti": None,
        "TimeVaule": 0,
        "TrackingNumber": None,
        "StartCountry": None,
        "EndCountry": None,
        "HAWB_Number": 0,
        "Car_Number": None,
        "Start_TransferPoint": None,
        "End_TransferPoint": None,
        "Arrive_Date": None,
        "Dock_system": None,
        "Charge_Pattern": None,
        "EndServer_Code": None,
        "StartPlaceCode": None,
        "EndPlaceCode": None
    }
    if income_type=="KY":
        data["Currency_Code"]="YD"
    if income_type=="ZY":
        data["Currency_Code"]="KC"
    if income_type=="QG":
        data["Currency_Code"]="TD"
    if income_type=="QG":
        data["Currency_Code"]="TD"
    if income_type=="PS":
        data["Currency_Code"]="YD"
    request_data = {
    "waybill_code": Waybill_Code,
    "jsonstring": json.dumps(data, ensure_ascii=False),
    "system_source": source,
    "product_code": Product_Code,
    "income_type": income_type
}
    print(request_data)
    request_url = url.pqm_url + "/api/BilJsoncharged/AddBilJsoncharged"
    print(request_url)
    data = requests.post(url=request_url, json=request_data).text
    print(data)
    if '"Code":0' in data:
        if income_type=="KY":
            print("WT空运应收费用推送pqm成功！！！", request_data)
        elif income_type=="QG":
            print("WT清关应收费用推送pqm成功！！！", request_data)
        elif income_type=="ZY":
            print("WT中转应收费用推送pqm成功！！！", request_data)
        elif income_type == "PS":
            print("WT末端应收费用推送pqm成功！！！", request_data)
        # return request_data["shipper_hawbcode"]
    else:
        if income_type=="KY":
            print("WT空运应收费用推送pqm失败", request_data)
        elif income_type=="QG":
            print("WT清关应收费用推送pqm失败", request_data)
        elif income_type=="ZY":
            print("WT中转应收费用推送pqm失败", request_data)
        elif income_type == "PS":
            print("WT末端应收费用推送pqm失败", request_data)
def fee_to_diaobo(transport_hawbcode,charge_type_code,db_time):
    # if source==1:
    #     source="YT"
    # else:
    #     source = "WT"
    request_data = {
    "allocation_labelcode": transport_hawbcode["allocation_labelcode"],
    "transport_hawbcode":transport_hawbcode["transport_hawbcode"],
    "transport_server_code":transport_hawbcode["transport_server_code"],
    "bag_count":transport_hawbcode["bag_count"],
    "express_count":transport_hawbcode["bag_count"]*3,
    "transport_total_weight":transport_hawbcode["transport_total_weight"],
    "weight_unit_code":"kg",
    "orig_warehouse_code":transport_hawbcode["orig_warehouse_code"],
    "dest_warehouse_code":transport_hawbcode["dest_warehouse_code"],
    "transport_send_time":db_time,
    "transport_type_code":transport_hawbcode["transport_type_code"],
    "load_type_code":transport_hawbcode["load_type_code"],
    "transport_service_body_code":transport_hawbcode["transport_service_body_code"],
    "settlement_code":"YD",
    "transport_code":"ZY",
    "system_source_code":transport_hawbcode["system_source_code"],
    "first_billing_location_code":"YT-XM",
    "dest_country_code":"AF",
    "kc_count":"1",
    "airline_company_code":"CX",
    "take_off_code":"HKG",
    "take_ground_code":"AMS",
    "service_type_code":"DB2",
    "fare_type_code":"DB",
    "charge_type_code":"",
    "transport_receive_time":db_time
}
    if charge_type_code=="KC":
        request_data["charge_type_code"]=""
        request_data["transport_code"]="ZY"
    elif charge_type_code=="AN":
        request_data["charge_type_code"] = "KY"
        request_data["transport_code"] = ""
    elif charge_type_code=="WL":
        request_data["settlement_code"] = "WL"
        request_data["orig_warehouse_code"]= "YT-GZ"
        request_data["dest_warehouse_code"] = "YT-XM"
    print(request_data)
    request_url = url.pqm_url + "api/CostAirTransfer/AddBillJson"
    print(request_url)
    data = requests.post(url=request_url, json=request_data).text
    print(data)
    if '推送成功' in data:
        print("调拨费用推送pqm成功！！！", request_data)
        # return request_data["shipper_hawbcode"]
    else:
        print("调拨费用推送pqm失败", request_url, data, request_data)
def fee_to_chongpai(Waybill_Code,Customer_Code,ServerPlace_Code,serverCode,db_time,source):
    if source==1:
        source="YT"
    else:
        source = "WT"
    data = {
	"Waybill_Code": Waybill_Code["shipperCode"]+"-1",
	"Currency_Code": "YD",
	"Customer_Code":Customer_Code,
	"Product_Code": "",
	"Server_Code": serverCode,
	"Server_Type": "PS",
	"ServerPlace_Code": ServerPlace_Code,
	"System_Code": "YT",
	"Og_id_ChargeFirst": "YT-SZ",
	"Arrival_Date": db_time,
	"Country": Waybill_Code["countryCode"],
	"Postcode": Waybill_Code["postCode"],
	"City": "AT",
	"Charge_Weight": Waybill_Code["shipperChargeWeight"],
	"Dock_system": "RMS",
	"Charge_Pattern": "0"
}
    request_data ={
  "jsonstring": json.dumps(data,ensure_ascii=False),
  "waybill_code": Waybill_Code["shipperCode"]+"-1",
  "system_source": source,
  "cost_type":"PS"
}
    print(request_data)
    request_url = url.pqm_url + "api/CostDeliver/AddBillJson"
    print(request_url)
    data = requests.post(url=request_url, json=request_data).text
    print(data)
    if '"Code":0' in data:
        print("海外重派费用推送pqm成功！！！", request_data)
        # return request_data["shipper_hawbcode"]
    else:
        print("海外重派费用推送pqm失败", request_url, data, request_data)
def fee_to_moduan(transport_hawbcode,db_time):
    # if source==1:
    #     source="YT"
    # else:
    #     source = "WT"
    request_data = {
    "allocation_labelcode": transport_hawbcode["allocation_labelcode"],
    "transport_hawbcode":transport_hawbcode["transport_hawbcode"],
    "transport_server_code":transport_hawbcode["transport_server_code"],
    "bag_count":transport_hawbcode["bag_count"],
    "express_count":transport_hawbcode["bag_count"]*3,
    "transport_total_weight":transport_hawbcode["transport_total_weight"],
    "weight_unit_code":"kg",
    "orig_warehouse_code":transport_hawbcode["orig_warehouse_code"],
    "dest_warehouse_code":transport_hawbcode["dest_warehouse_code"],
    "transport_send_time":db_time,
    "transport_type_code":transport_hawbcode["transport_type_code"],
    "load_type_code":transport_hawbcode["load_type_code"],
    "transport_service_body_code":transport_hawbcode["transport_service_body_code"],
    "settlement_code":"YD",
    "transport_code":"ZY",
    "system_source_code":transport_hawbcode["system_source_code"],
    "first_billing_location_code":"YT-XM",
    "dest_country_code":"AF",
    "kc_count":"1",
    "airline_company_code":"",
    "take_off_code":"",
    "take_ground_code":"",
    "service_type_code":"DB",
    "fare_type_code":"GDZF",
    "charge_type_code":"",
    "transport_receive_time":db_time
}
    print(request_data)
    request_url = url.pqm_url + "api/CostChargedJson/PulshAirTransferChargeJson"
    print(request_url)
    data = requests.post(url=request_url, json=request_data).text
    print(data)
    if '推送成功' in data:
        print("调拨费用推送pqm成功！！！", request_data)
        # return request_data["shipper_hawbcode"]
    else:
        print("调拨费用推送pqm失败", request_url, data, request_data)
if  __name__ =="__main__":
    from common_util import *
    #fee_to_kunei(Waybill_Code="YF224219261010063679",date_time="2020-09-26T00:00:00",Procedure_Type="ST",Og_id_ChargeFirst="YT-SH")
    Waybill_Code="102-20201013"
    Server_Code="YIFQG"
    source=1
    Charge_Weight=1.11
    Start_Place="MD"
    end_Place="MX"
    BusinessTime=now_T()
    Customs_Clearance_Port="AMS"
    Currency="RMB"
    #fee_to_zhuanyun(Waybill_Code, Server_Code, source, Charge_Weight, Start_Place, end_Place, BusinessTime)
    #fee_to_qingguan(Waybill_Code, Server_Code, source, Charge_Weight, Customs_Clearance_Port, Currency, BusinessTime)
    #fee_to_paisong(Waybill_Code="YT9603847896421", Server_Code="BJYWW", ServerPlace_Code="TEST008")
    fee_to_diaobo_air(lading_number="100-20201030", Volume_Weight=3.33, Charge_Weight=4.44)