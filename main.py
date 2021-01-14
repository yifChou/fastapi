from fastapi import FastAPI ,UploadFile,File
from pydantic import BaseModel
from connect_mysql import auto_add_bags
from ramdom_sequence import save_bag_record
from request_dts import dts_batch_get,dts_batch_baglist_get
from fms.request_fms import *
import time
from starlette.responses import FileResponse
app = FastAPI()

class Item(BaseModel):
    name:str
    price:float
    is_offer:bool = None
class dts_batch(BaseModel):
    bag_number:int
    yd_number: int
    batch_number:int
    url:str
class dts_batch_list(BaseModel):
    bag_list:list
    yd_number: int
    url:str
class fms_lading_fee(BaseModel):
    bag_number:int
    yd_number: int
    customerCode:str
    servercode:str
    source:int
    Charge_Weight:float
    currency:str
    ProductCode:list
@app.post("/fms/air_lading_fee")
def get_fms_lading_fee(data:fms_lading_fee):
    waybill_number = random.randint(10000000, 99999999)
    lading_number=lading_generate()
    customerCode=data.customerCode
    servercode=data.servercode
    source=data.source
    yt_number=data.yd_number
    Charge_Weight=data.Charge_Weight
    fee_number=random.randint(1,3)
    currency=data.currency
    url.ProductCode=random.choice(data.ProductCode)
    if data.bag_number >= 1 and data.yd_number >= 1 :
        # 公用袋号——运单
        bags, shippers, bag_shipper_list = data_bag_shipper_list(bag_number=data.bag_number, waybill_number=waybill_number, customerCode=customerCode,yt_number=yt_number,
                                                                 servercode=servercode, transfertype=1, source=source)
        # # #空运提单费用
        lading_number = request_airlading_withbag_fee(lading_number=lading_number, bag_list=bags,
                                                      shipper_list=shippers, customerCode=customerCode,
                                                      servercode=servercode, Charge_Weight=Charge_Weight,
                                                      currency=currency, fee_number=fee_number, source=source)

        return lading_number
    else:
        return {"error": "袋子/运单数量必须大于1"}
@app.post("/dts/batch")
def get_dts_batch(data:dts_batch):
    if "http://" not in data.url or "https://" not in data.url:
        if data.bag_number >= 1 and data.yd_number >= 1 and data.batch_number >= 1:
            flag = dts_batch_get(url=data.url,bag_number=data.bag_number,waybills=data.yd_number,patch_number=data.batch_number)
            return flag
        else:
            return {"error": "袋子/运单/批次数量必须大于1"}
    else:
        return {"error": "url地址填写有误"}
@app.post("/dts/batch_list")
def get_dts_batch_list(data:dts_batch_list):
    if "http://" not in data.url or "https://" not in data.url:
        if len(data.bag_list) >= 1 and data.yd_number >= 1:
            flag = dts_batch_baglist_get(url=data.url,bag_list=data.bag_list,waybills=data.yd_number)
            return flag
        else:
            return {"error": "袋子/运单数量必须大于1"}
    else:
        return {"error": "url地址填写有误"}

@app.get("/")
def read_root():

    return {"hello":"World1"}

@app.get("/hello")
def read_root():
    return {"hello":"World2"}

@app.get("/items/{item_id}")
def read_item(item_id: int,q: str = None):
    return {"item_id":item_id,"q":q}

@app.get("/tms/get_bag/{customer}")
def get_tms_bag(yd_number:int,bag_num:int,customer:int):
    '''
    :param yd: 运单起始编号，防止重复
    :param bag_code: 袋子起始编号，防止重复
    :param yd_number: 运单数量
    :param bag_num: 袋子数量
    :return:
    '''
    # ydstring = 4916402008171000
    # bag_code = 2081710
    # yd_number = 1000
    # bag_num = 50
    auto_data = save_bag_record(input_yd_number=yd_number,input_bag_numer=bag_num)#自动生成ydstring,bag_code
    if auto_data[0]:
        ydstring = auto_data[1]
        bag_code = auto_data[2]
        A = auto_add_bags(yd_number=yd_number, ydstring=ydstring, bag_num=bag_num, bag_code=bag_code,customerID=customer)
        for i in A:
            print(i)
        return {"bag_list":A}
    else:
        return {"error":"遇到错误,请重新请求生成数据"}
@app.post("/file_upload")
async def file_upload(file: UploadFile = File(...)):
    start = time.time()
    try:
        res = await file.read()
        with open(file.filename, "wb") as f:
            f.write(res)
        return {"message": "success", 'time': time.time() - start, 'filename': file.filename}
    except Exception as e:
        return {"message": str(e), 'time': time.time() - start, 'filename': file.filename}
@app.get("/file")
def file():
    return FileResponse('./ATS-TP-BC2020048.mm', filename='ATS-TP-BC2020048.mm')
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app,host='0.0.0.0',port=8080)