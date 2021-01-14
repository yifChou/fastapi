class url:
    #fms ="http://fmsapi.yunexpress.com/"#线上
    fms = "http://192.168.88.140/" #开发环境
    #fms = "http://fmsapi.uat.yunexpress.com/" #UAT
    crm_url = "http://crmservice.dev.yunexpress.com" #本地 "http://10.168.95.114:5000" 开发环境 http://10.168.95.192:5000 #http://crmservice.dev.yunexpress.com
    pqm_url = "http://pqm.dev.yunexpress.com"#"http://192.168.88.116:5000/" #开发环境
    #ProductCode=["ABC"] #["PK0461","ZH20207","USZMTK","XYLXB","1103"] 产品代码
    ProductCode=["CNUPSB"]#"PK0442","PK0461","ZH20207","USZMTK","1103","ABC","XYLXB","EUB-SZ",
    # 中转结算产品 "001003"
    # 理赔 "DE-TEST"
    # 海外重派 发货中转 "PK0442"
    # 末端-明细 1103
    # 清关 1103
    # 库内费用 PK0002
    # 中转 	001256
    # 末端-提单 01
    # 空运 DHLSG5  PK0054 3303
    # 调拨运输 ATZXR
    # 仓租 CNUPSB
    # 陈青连 ZH20207
    # 江佳 20087
    # 曹嘉 DHLSG5
    # 林思虹 PK0461
    # 刘文均 1103
    wt_ProductCode=["DHL-NL","FDXGR-CA"]
    yifserverchannelcode = [ "GJY","TEST007", "SHQ","GZYJ"]#"GZYJ","SPLUSZ"#末端服务渠道"TEST007", "SHQ", "GJY", "CNDHL"   "GZYJ","SPLUSZ",
    AB123serverchannelcode=["HERMES","ABCZ"]
    fiveserverchannelcode=["TEST007", "SHQ", "GJY", "CNDHL"]
class sys_data:
    severCode = "kenny_code" #服务商代码"MIAEND", "BJYWW", , "A1109"
#!/user/bin/env python
#coding:utf-8

# def data_dir(data='data',fileName=None):
#     '''查找文件的路径'''
#     return os.path.join(os.path.dirname(os.path.dirname(__file__)),data,fileName)
"""
读取配置文件。
"""
import os
import xlrd
from xlutils.copy import copy


# 配置绝对路径。
BASE_PATH = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
CONFIG_FILE = os.path.join(BASE_PATH, 'config', 'config.yml')
DATA_PATH = os.path.join(BASE_PATH, 'data')
#DRIVER_PATH = os.path.join(BASE_PATH, 'drivers')
LOG_PATH = os.path.join(BASE_PATH, 'log')
REPORT_PATH = os.path.join(BASE_PATH, 'report')
TESTS_PATH = os.path.join(BASE_PATH,'tests')

class Config:
    def __init__(self):
        pass
    def get_case(self,filename, sheetnum):
        case_dir = DATA_PATH + filename + '.xls'
        datas = xlrd.open_workbook(case_dir)
        table = datas.sheets()[sheetnum]
        nor = table.nrows
        nol = table.ncols

        return nor, table

    def write_file(self,filename,sheetnum):

        case_dir = DATA_PATH + filename + '.xls'
        datas = xlrd.open_workbook(case_dir)
        #rb = open_workbook('m:\\1.xls')

        # 通过sheet_by_index()获取的sheet没有write()方法
        rs = datas.sheet_by_index(sheetnum)

        wb = copy(rs)

        # 通过get_sheet()获取的sheet有write()方法
        ws = wb.get_sheet(sheetnum)
