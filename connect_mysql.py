import pymysql
import random
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
            host="IT-100",
            port=3308,
            user="mysql",
            password="a135246A",
            database=database_name,
            charset="utf8")
        print(conn)
        cursor = conn.cursor()
        return cursor, conn
    except Exception as e:
        print(e)

# sql = "select pm_id from bil_payment where  pm_id <5000"
#
# sum = cursor.execute(sql)
# result = cursor.fetchall()
# print(type(result))
# cursor.close()
# conn.close()
#db, conn = connect_sql(database_name="tms")
#fms_db, fms_conn = connect_it_100(database_name="fms_db")
def excute_sql(db,conn,sql):
    try:
        print("执行前：",sql)
        success = db.execute(sql)
        conn.commit()
        print(sql,"\n","成功",success,"条")
    except Exception as e:
        conn.rollback()
        print(e)
def add_bussiness(yd,number,customerID):
    '''插入运单数据，
    yd填写1916400912120000
    number为要插入多少个运单'''
    pass
    last_bsid = "select bs_id from bsn_expressexport order by bs_id desc limit 1;"
    excute_sql(db,conn,last_bsid)
    start_bsid = db.fetchall()[0][0]+1
    print(start_bsid)
    add_bsid = "INSERT INTO `tms`.`bsn_expressexport` (bs_id, `shipper_hawbcode`, `serve_hawbcode`, `refer_hawbcode`, `channel_hawbcode`, `original_invoicesign`, `invoice_referencesign`, `sender_account`, `payer_account`, `third_partyaccount`, `label_printtimes`, `lastselect_id`, `invoice_printdate`, `oda_sign`, `booking_code`, `booking_sign`, `manifest_sign`, `seekcargo_sign`, `battery_code`, `tariffno`, `printformat_sign`, `buyer_id`, `collectcharge_confirmsign`, `document_change_sign`, `last_update_time`, `routing_code`, `serviceremark`, `shippingcabinet_hawbcode`, `aviation_hawbcode`) select pm_id-1+%s, CONCAT('YIF',%s+pm_id), '', %s+pm_id-1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'U', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'N', NOW(), NULL, NULL, NULL, NULL from bil_payment WHERE pm_id BETWEEN 1 AND %s"%(start_bsid,yd,start_bsid,number)
    excute_sql(db, conn, add_bsid)
    '''tms插入应付费用'''
    last_icid = "select IcId from bil_income order by IcId desc limit 1;"
    excute_sql(fms_db, fms_conn, last_icid)
    start_icid = fms_db.fetchall()[0][0] + 1
    print(start_icid)
    tms_imcome = "INSERT INTO `tms`.`bil_income` ( `ic_id`, `customer_id`, `bs_id`, `fk_code`, `unit_code`, `ic_amount`, `currency_code`, `ic_currencyrate`, `customer_bill_id`, `ic_createdate`, `st_id_creator`, `ic_balancesign`, `ic_writeoffsign`, `last_update_time`) select  pm_id-1+%s,'%s', pm_id-1+%s, 'E1', 'KG', '4.00', 'RMB', '0.6000', NULL, NOW(), '0', 'N', 'N', NOW() from bil_payment WHERE pm_id BETWEEN 1 AND %s"%(start_icid,customerID,start_bsid,number)
    excute_sql(db, conn, tms_imcome)
    '''财务系统数据库
    运单表
    应收费用表
    应付费用表
    未出账单表
    '''
    fms_bsid = "INSERT INTO `fms_db`.`bsn_receivablebusiness` (`BsId`, `ShipperCode`, `ReferCode`, `ServerCode`, `ProductCode`, `CountryCode`, `ShipperChargeWeight`, `ShipperOgId`, `ArrivalDate`, `Saller`, `CustomerId`, `ServerChannelCode`, `TransferstatusType`, `PostCode`, `ServerChargeWeight`, `IsHold`, `IsResetCharge`, `CheckOutOn`, `SourceSystem`, `SourceId`, `OperationStatus`, `SyncId`, `ReturnRemark`, `ReturnType`, `ReturnDate`, `IsVirtual`, `IssueKindCode`, `ShipperWeight`, `ServerWeight`) select id-1+%s, CONCAT('YIF',%s+id), CONCAT('refercode',%s+id), '202005121005', 'PK0351', 'AF', '1.500', '74', NOW(), '794', '%s', 'TEST007', 'S', '69988-5566', '1.500', 'Y', 'N', NOW(), '1', '1000', 'O', '220097565', '', 'S', NULL, 'N', '', '00000001.500', '00000001.500' from test_tmp WHERE id BETWEEN 1 AND %s"%(start_bsid,yd,start_bsid,number,customerID)    #print(add_bsid)
    excute_sql(fms_db, fms_conn, fms_bsid)
    # last_IcId = "select IcId from bil_income order by IcId desc limit 1;"
    # excute_sql(fms_db, fms_conn, last_IcId)
    # start_IcId = fms_db.fetchall()[0][0] + 1
    # print(start_IcId)
    fms_income = "INSERT INTO `fms_db`.`bil_income` (`IcId`,`CustomerId`, `BsId`, `FkCode`, `PirceType`, `Unit`, `Amount`, `CurrencyCode`, `Rate`, `CreateBy`, `CreateOn`, `Remark`, `OccurType`, `OccurDate`) select %s+id-1,'%s', id-1+%s, 'E1', 'RMB', 'KG', '4.00', 'RMB', '0.6000', '0', NOW(), '测试脚本数据', 'N', NOW() from test_tmp WHERE id BETWEEN 1 AND %s"%(start_icid,customerID,start_bsid,number)
    excute_sql(fms_db, fms_conn, fms_income)
    fms_not_income ="INSERT INTO `fms_db`.`bil_incomebill` (`IcId`, `CreateOn`, `CustomerId`) select id-1+%s, NOW(), '%s' from test_tmp WHERE id BETWEEN 1 AND %s"%(start_icid,customerID,number)
    excute_sql(fms_db, fms_conn, fms_not_income)
    fms_payment = "INSERT INTO `fms_db`.`bil_payment` ( `bs_id`, `server_id`, `fk_code`, `unit_code`, `pm_amount`, `currency_code`, `pm_currencyrate`, `pm_createdate`, `st_id_creator`, `pm_writeoffsign`, `pm_occurdate`, `pm_zone`, `pm_note`) select id-1+%s, '481', 'E1', 'KG', '100.00', 'RMB', '1.0000', NOW(), '0', 'N', NOW(), '0', '测试脚本数据' from test_tmp WHERE id BETWEEN 1 AND %s"%(start_bsid,number)
    excute_sql(fms_db, fms_conn, fms_payment)
    '''签入签出'''
    check_sql="INSERT INTO `tms`.`bsn_business_operator` (`bs_id`, `checkin_date`, `checkin_st_id`, `entry_date`, `entry_st_id`, `checkout_date`, `checkout_st_id`, `last_track_code`, `last_track_date`, `last_track_location`, `last_track_comment`, `last_comment`, `st_id_comment`, `last_comment_date`, `last_documentary`, `st_id_documentary`, `last_documentary_date`, `check_weight_st_id`, `last_update_time`) select bs_id, NOW(), '1', NULL, NULL, NOW(), '1', 'DF', NOW(), 'SHENZHEN - CHINA', '快件操作完成', '签出成功。', '1', NOW(), NULL, NULL, NULL, NULL, NOW()from bsn_expressexport where bs_id BETWEEN %s and  %s;" %(start_bsid,start_bsid+number-1)
    #print(check_sql)
    excute_sql(db,conn,check_sql)
    '''签入签出状态表'''
    check_staus = "INSERT INTO `tms`.`bsn_business` (`tms_id`, `bs_id`, `arrivalbatch_id`, `checkin_og_id`, `datasource_code`, `transferstatus_code`, `returnstatus_code`, `operation_status`, `documentarystatus_code`, `customer_id`, `customer_channelid`, `arrival_date`, `product_code`, `checkin_cargotype`, `paymentmode_code`, `destination_countrycode`, `destination_cityid`, `destination_postcode`, `shipper_weight`, `checkin_grossweight`, `checkin_volumeweight`, `shipper_chargeweight`, `estimate_chargeweight`, `server_chargeweight`, `shipper_pieces`, `server_channelid`, `checkout_cargotype`, `departure_date`, `prealert_date`, `return_sign`, `lastoperate_og_id`, `transaction_id`, `warehouse_code`, `seller_id`, `departbatch_id`, `checkout_grossweight`, `checkout_volumeweight`, `mail_cargo_type`, `serve_weight_checksign`, `invoice_totalcharge`, `manual_shipper_chargeweight`, `manual_server_chargeweight`, `virtual_business`, `unit_code`, `return_time`, `return_note`, `sysn_state`, `input_mode`, `manual_return_fee_sign`, `manual_return_fee_date`, `sync_fba`, `points_bubble_ratio`, `manual_return_fee_Accrued_sign`, `return_status_audit_state`, `volume_coefficient`, `volume_state`, `package_weight`, `last_update_time`, `back_to_side`, `operation_notes`) select '1', bs_id, '7570', '74', 'O', 'S', NULL, 'O', 'N', '%s', NULL, NOW(), 'PK0351', 'W', 'P', 'AF', NULL, NULL, '8', round(RAND()*10)*10+10, '10', '99', '100', '999', '7', '12', 'W', NULL, NULL, 'N', '74', NULL, NULL, '1558', NULL, '1000', '9999', '6', 'N', NULL, NULL, NULL, 'N', NULL, NULL, NULL, 'N', '4', 'N', NULL, 'N', NULL, 'N', 'N', '1000', '0', '0.00', NOW(), NULL, NULL from bsn_expressexport where bs_id BETWEEN %s and  %s;" %(customerID,start_bsid,start_bsid+number-1)
    #print(check_staus)
    excute_sql(db,conn,check_staus)
    '''业务计费表'''

    '''申报价值'''
    invoice_sql = "INSERT INTO `tms`.`bsn_invoice` ( `bs_id`, `name_prefix`, `invoice_cnname`, `invoice_enname`, `unit_code`, `invoice_weight`, `invoice_quantity`, `invoice_totalcharge`, `invoice_currencycode`, `invoice_totalWeight`, `textile_sign`, `hs_code`, `import_licenseid`, `export_licenseid`, `invoice_createrid`, `invoice_createdate`, `invoice_modifydate`, `invoice_modifyrid`, `invoice_url`, `sku`, `asin`, `type_code`, `last_update_time`, `invoice_note`, `sku_audit_status`, `CertificateRemark`, `HSTaxrate`, `box_no`, `txture_code`, `note`) select bs_id, NULL, 'test', '摩托车护目镜', 'PCE', '1.000', '1', round(RAND()*10)*10+10, 'USD', '1.000', NULL, 'xx22', NULL, NULL, '1', NOW(), NOW(), NULL, '', 'xx22', NULL, '', NOW(), 'test', '', '', '0.00000', NULL, NULL, NULL from bsn_expressexport where bs_id BETWEEN %s and  %s;" %(start_bsid,start_bsid+number-1)
    excute_sql(db,conn,invoice_sql)
    return start_bsid,start_bsid+number-1
def add_bag(bag,start,end,server_channel=0):
    '''插入袋子数据，start为袋子起始运单，end为最后运单id bag=SV91020121206
    bag填写当天月日+流水 如121201
    server_channel=0则有服务渠道，不为0则没有服务渠道
    '''
    '''新建袋子'''
    bag = "BAG033"+str(bag)
    if server_channel==0:
        bag_sql = "INSERT INTO `tms`.`bsn_departbatch_bag` (`tms_id`, `bag_labelcode`, `bag_additionalvalue`, `bag_maxweight`, `bag_grossweight`, `bag_countpieces`, `server_id`, `server_channelid`, `departbatch_createdate`, `departbatch_createrid`, `departbatch_note`, `bag_code`, `operating_point`, `country_code`, `bag_state`, `bag_prediction`, `departurebatch_id`, `bag_pakcet`, `bagrule_code`, `bag_number`, `zone_code`, `country_type`, `bag_zone_number`, `last_update_time`, `bag_server_code`, `bag_label_url`, `bag_mainfest_url`, `bag_shipper`, `LowerLimitWeight`, `LicenseNumber`, `bagcode_serialno`, `check_status`, `check_time`, `check_user`, `check_remarks`, `ShipmentsWeight`) VALUES ('1',  '%s', %s, '10000.00', '0.512', '1', '481', '523', NOW(), '1', '', NULL, '74', 'AF', 'D', 'D', '4654', NULL, 'YDLYZ', '20', NULL, '2', NULL, NOW(), '', '', '', NULL, '0.00', NULL, NULL, 'S', NULL, NULL, NULL, NULL);" %(bag,bag)
    else:
        bag_sql = "INSERT INTO `tms`.`bsn_departbatch_bag` (`tms_id`, `bag_labelcode`, `bag_additionalvalue`, `bag_maxweight`, `bag_grossweight`, `bag_countpieces`, `server_id`, `server_channelid`, `departbatch_createdate`, `departbatch_createrid`, `departbatch_note`, `bag_code`, `operating_point`, `country_code`, `bag_state`, `bag_prediction`, `departurebatch_id`, `bag_pakcet`, `bagrule_code`, `bag_number`, `zone_code`, `country_type`, `bag_zone_number`, `last_update_time`, `bag_server_code`, `bag_label_url`, `bag_mainfest_url`, `bag_shipper`, `LowerLimitWeight`, `LicenseNumber`, `bagcode_serialno`, `check_status`, `check_time`, `check_user`, `check_remarks`, `ShipmentsWeight`) VALUES ('1',  '%s', NULL, '10000.00', '0.512', '1', '481', NULL, NOW(), '1', '', NULL, '74', 'AF', 'D', 'D', '4654', NULL, 'YDLYZ', '20', NULL, '2', NULL, NOW(), '', '', '', NULL, '0.00', NULL, NULL, 'S', NULL, NULL, NULL, NULL);" %(bag)
    excute_sql(db,conn,bag_sql)
    '''袋子关联运单'''
    search_bag = "select bag_id,departurebatch_id from bsn_departbatch_bag where bag_labelcode = '%s';"%(bag)
    excute_sql(db,conn,search_bag)
    bag_id,depart = db.fetchone()
    print(bag_id,depart)
    bag_bs_sql = "INSERT INTO `tms`.`bsn_departbatch_express` (`bs_id`, `departbatch_id`, `bag_id`, `last_update_time`) select  bs_id, %s, %s, now() from bsn_expressexport where bs_id BETWEEN %s and  %s;"%(depart,bag_id,start,end)
    excute_sql(db,conn,bag_bs_sql)
    '''袋子长宽高'''
    bag_weight = "INSERT INTO `tms`.`bsn_departbatch_bag_size` (`bag_id`, `bsc_id`, `length`, `width`, `height`, `weight`, `unit`, `setup_length`, `setup_width`, `setup_height`, `setup_weight`, `creater_id`, `create_time`, `updater_id`, `update_time`) VALUES (%s, NULL, round(RAND()*10,0), round(RAND()*10,0), round(RAND()*10,0), '100', NULL, NULL, NULL, NULL, NULL, '1', NOW(), NULL, NULL);"%(bag_id)
    excute_sql(db,conn,bag_weight)
    return bag
def add_transit_info(title,flag,bag_all):
    '''

    :param flag: 卡车号前缀
    :param bag_all: 卡车要关联的袋子号，list
    :return:
    '''
    transit =  title+str(flag)
    sql = "INSERT INTO `tms`.`fms_transit_info` (`state`, `related_bags`, `is_revoke`, `is_push`, `car_number`, `transit_weight`, `transit_volume`, `transit_plates`, `service_code`, `transitcost_id`, `departure_time`, `arrival_time`, `isfee`, `remark`, `createdon`, `createdby`, `updateon`, `updateby`) VALUES ('T', '1', '0', '0', %s, '200', '0.000', '0', 'PENG', '132', NOW(), NOW()+1, 'N', 'SQL插入数据', NOW(), '1', NULL, NULL)" %(transit);
    excute_sql(db,conn,sql)
    '''查询卡车ID'''
    search_car = "select transitinfo_id from fms_transit_info where car_number='%s';"%(transit)
    excute_sql(db,conn,search_car)
    car_id = db.fetchone()
    print(car_id[0])
    for bag in bag_all:
        car_bag_combine = "INSERT INTO `tms`.`fms_transit_bag_detail` ( `transitinfo_id`, `bag_number`, `createdby`, `createdon`) VALUES( %s, '%s', '1', NOW()) " % (car_id[0],bag)
        print(car_bag_combine)
        excute_sql(db,conn,car_bag_combine)
def cut_number(loop,min,max):
    list_all=[]
    list_in = []
    l_need = []
    for i in range(loop+1):
        start = random.randint(min,max) #每个袋子最少10 least
        list_in.append(start)
    list_in[0]=min
    list_in[-1]=max
    list_all = list(set(list_in))
    list_all.sort()
    print(list_all)
    for k in range(len(list_all)-1):
        if k==0:
            l = [list_all[k],list_all[k+1]]
        else:
            l = [list_all[k]+1, list_all[k + 1]]

        l_need.append(l)
    print(l_need)
    return l_need
def auto_add_bags(yd_number,ydstring,bag_num,bag_code,customerID):
    '''
    :param yd_number: 运单数量
    ydstring=1916400912120100
    bag_num 袋子数量
    bag_code 袋子编码
    :return:
    '''
    start, end = add_bussiness(yd=ydstring, number=yd_number,customerID=customerID)
    '''运单分几个袋子装
        sum为运单总数量
        loop为多少个袋子'''
    bags = cut_number(min=start, max=end, loop=bag_num)
    i = 0
    bag_list = []
    #bags = [[1, 3], [4, 4], [5, 9], [10, 10]]
    for bag in bags:
        print(bag[0], bag[1])
        bagone = add_bag(bag_code + i, bag[0], bag[1],server_channel=1)
        i = i + 1
        bag_list.append(bagone)
    print(bag_list)
    return bag_list
if __name__=="__main__":
    ''':param
    yd_number: 运单数量
    ydstring = 1916400912120100
    bag_num  必须运单号足够多，袋子才会更接近
    袋子数量
    bag_code
    袋子编码
    :return:'''
    ydstring = 4916402008194000
    bag_code =2081940
    yd_number= 5
    bag_num= 1
    A = auto_add_bags(yd_number=yd_number,ydstring=ydstring,bag_num=bag_num,bag_code=bag_code,customerID=15)
    for i in A:
        print(i)
    # sql = "SELECT * FROM bsn_receivablebusiness WHERE ShipperCode='YT2013311101000001';"
    # excute_sql(fms_db,fms_conn,sql)
    # data = fms_db.fetchall()
    # print(data)