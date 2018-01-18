
# -*- coding:utf-8 -*-
from app.extensions import celery
from app import db
from app.api.controller.c_irobotbox import GetIrobotboxOrder
from app.api.i18n import irobotbox_url, irobotbox_order_api
import datetime
from app.rate.models import Rates
from flask import redirect, url_for
from app.api.models.m_irobotbox import Log,IrobotboxOrder as IBO, IrobotboxOrderProducts as IOP
from sqlalchemy import distinct
from app import db
import os 

@celery.task()
def getIrobotboxOrder():
    if int(datetime.datetime.now().strftime("%M")) < 10:
        Rates().get_rate()

    irobotbox_order_api['StartTime'] = (datetime.datetime.now()-datetime.timedelta(minutes=21)).strftime("%Y-%m-%d %H:%M:%S")
    irobotbox_order_api['EndTime'] = (datetime.datetime.now()-datetime.timedelta(minutes=10)).strftime("%Y-%m-%d %H:%M:%S")

    orders = GetIrobotboxOrder(url=irobotbox_url, key=irobotbox_order_api)
    result = orders.get_order()

    flag_arr=[]
    flag_arr.append(result['NextToken'])

    

    while result['NextToken'] != -1:
        orders = GetIrobotboxOrder(url=irobotbox_url, key=result)
        result = orders.get_order()
        flag_arr.append(result['NextToken'])

    if -1 not in flag_arr:
        flag=0
    else:
        flag=1
    log=Log(start_time=irobotbox_order_api['StartTime'],end_time=irobotbox_order_api['EndTime'],status=flag)
    db.session.add(log)

    return "爬取数据成功!"


@celery.task()
def getOrderAgain():
    notgots=Log.query.filter_by(status=0).all()
    for notgot in notgots:
        irobotbox_order_api['StartTime'] = notgot.start_time
        irobotbox_order_api['EndTime'] = notgot.end_time

        orders = GetIrobotboxOrder(url=irobotbox_url, key=irobotbox_order_api)	
        result = orders.get_order()
        flag_arr=[]
        flag_arr.append(result['NextToken'])

        while result['NextToken'] != -1:
            orders = GetIrobotboxOrder(url=irobotbox_url, key=result)
            result = orders.get_order()
            flag_arr.append(result['NextToken'])

        if -1 not in flag_arr:
            flag=0
        else:
            flag=1
            
        notgot.status=flag
        db.session.add(notgot)
    return "补充抓取成功!"





