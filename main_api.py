from fastapi import FastAPI
from pydantic import BaseModel
from connect_mysql import auto_add_bags
from ramdom_sequence import save_bag_record
app = FastAPI()

class Item(BaseModel):
    name:str
    price:float
    is_offer:bool = None

@app.get("/")
def read_root():
    return {"hello":"World"}

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
    auto_data = save_bag_record(input_yd_number=yd_number,input_bag_numer=bag_num)
    # yd_number = 1000
    # bag_num = 50
    if auto_data[0]:
        ydstring = auto_data[1]
        bag_code = auto_data[2]
        A = auto_add_bags(yd_number=yd_number, ydstring=ydstring, bag_num=bag_num, bag_code=bag_code,customerID=customer)
        for i in A:
            print(i)
        return {"bag_list":A}
    else:
        return {"error":"遇到错误,请重新请求生成数据"}