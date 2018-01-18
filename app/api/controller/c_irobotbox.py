# -*- coding:utf-8 -*-

from suds.client import Client
from ..models.m_irobotbox import IrobotboxOrder, IrobotboxOrderProducts
# from app.order.models import Product
from app import db
from sqlalchemy import or_
import datetime

class GetIrobotboxOrder(object):
    def __init__(self, url, key):
        self.url = url
        self.key = key

    def get_order(self):
        client = Client(self.url)
        results = client.service.GetOrders(self.key)
        orders = results.OrderInfoList.ApiOrderInfo


        for i in range(len(orders)):
            order = IrobotboxOrder(ordercode=orders[i].OrderCode)

            check_order = order.order_exist()
            startime = (datetime.datetime.now()-datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")

            if check_order:
                check_order.OrderStatus = orders[i].OrderStatus
                check_order.OrderState = orders[i].OrderState
                check_order.TransportID = orders[i].TransportID
                check_order.WareHouseID = orders[i].WareHouseID
                check_order.TrackNumbers = orders[i].TrackNumbers

                records = IrobotboxOrderProducts.query.filter_by(order_id=orders[i].OrderCode).all()
                products = results.OrderInfoList.ApiOrderInfo[i].OrderList.ApiOrderList

                for record in records:
                    if record.SKU == None:
                        for product in products:
                            if product.SellerSKU == record.SellerSKU:
                                record.SKU = product.SKU
                                record.ClientSKU = product.ClientSKU.encode("UTF-8") if product.ClientSKU else None
                                record.GroupSKU = product.GroupSKU.encode("UTF-8") if product.GroupSKU else None
                                record.GroupProductNum = product.GroupProductNum
                                record.GroupProductPrice = product.GroupProductPrice
                                record.ProductNum = product.ProductNum
                                record.ProductPrice = product.ProductPrice
                                record.ShippingPrice = product.ShippingPrice
                                record.LastBuyPrice = product.LastBuyPrice
                                record.LastSupplierPrice = product.LastSupplierPrice
                                record.FirstLegFee = product.FirstLegFee
                                record.TariffFee = product.TariffFee
                                record.IsBuildPackage = product.IsBuildPackage
                                record.ProductWeight = product.ProductWeight
                                record.ProductLength = product.ProductLength
                                record.ProductWidth = product.ProductWidth
                                record.ProductHeight = product.ProductHeight
                                record.BusinessAdminID = product.BusinessAdminID
                                record.ProductLinks = product.ProductLinks.encode("UTF-8") if product.ProductLinks else None
                                record.ProductLatestCost = product.ProductLatestCost



                db.session.add(check_order)
                db.session.commit()

            elif len(results.OrderInfoList.ApiOrderInfo[i].OrderList) and orders[i].IsPay and orders[i].TotalPrice > 0 and orders[i].OrderStatus != 2:
                order.OrderCode = orders[i].OrderCode
                order.ClientOrderCode = orders[i].ClientOrderCode.encode("UTF-8") if orders[i].ClientOrderCode else None
                order.SalesRecordNumber = orders[i].SalesRecordNumber
                order.TransactionId = orders[i].TransactionId
                order.ClientUserAccount = orders[i].ClientUserAccount
                order.Email = orders[i].Email
                order.Telephone = orders[i].Telephone
                order.OrderSourceID = orders[i].OrderSourceID
                order.OrderSourceName = orders[i].OrderSourceName.encode("UTF-8") if orders[i].OrderSourceName else None
                order.IsPay = orders[i].IsPay
                order.PaymentMethods = orders[i].PaymentMethods
                order.OrderStatus = orders[i].OrderStatus
                order.OrderState = orders[i].OrderState
                order.PayTime = orders[i].PayTime
                order.Currency = orders[i].Currency
                order.TotalPrice = orders[i].TotalPrice
                order.PromotionDiscountAmount = orders[i].PromotionDiscountAmount
                order.TransportPay = orders[i].TransportPay
                order.Country = orders[i].Country
                order.TransportID = orders[i].TransportID
                order.IsFBAOrder = orders[i].IsFBAOrder
                order.WareHouseID = orders[i].WareHouseID
                order.ProductWeight = orders[i].ProductWeight
                order.TrackNumbers = orders[i].TrackNumbers
                order.PaypalFee = orders[i].PaypalFee
                order.RefundPaypalFee = orders[i].RefundPaypalFee
                order.PaypalTransactionFee = orders[i].PaypalTransactionFee

                order.orderproducts = []

                products = results.OrderInfoList.ApiOrderInfo[i].OrderList.ApiOrderList

                for j in range(len(products)):
                    product = IrobotboxOrderProducts()
                    product.SKU = products[j].SKU
                    product.ClientSKU = products[j].ClientSKU.encode("UTF-8") if products[j].ClientSKU else None
                    product.GroupSKU = products[j].GroupSKU.encode("UTF-8") if products[j].GroupSKU else None
                    product.GroupProductNum = products[j].GroupProductNum
                    product.GroupProductPrice = products[j].GroupProductPrice
                    product.ProductNum = products[j].ProductNum
                    product.ProductPrice = products[j].ProductPrice
                    product.ShippingPrice = products[j].ShippingPrice
                    product.LastBuyPrice = products[j].LastBuyPrice
                    product.LastSupplierPrice = products[j].LastSupplierPrice
                    product.FirstLegFee = products[j].FirstLegFee
                    product.TariffFee = products[j].TariffFee
                    product.SellerSKU = products[j].SellerSKU
                    product.OrderItemId = products[j].OrderItemId
                    product.ASIN = products[j].ASIN
                    product.ParameterValues = products[j].ParameterValues.encode("UTF-8") if products[j].ParameterValues else None
                    product.IsBuildPackage = products[j].IsBuildPackage
                    product.ProductWeight = products[j].ProductWeight
                    product.ProductLength = products[j].ProductLength
                    product.ProductWidth = products[j].ProductWidth
                    product.ProductHeight = products[j].ProductHeight
                    product.BusinessAdminID = products[j].BusinessAdminID
                    product.ProductLinks = products[j].ProductLinks.encode("UTF-8") if products[j].ProductLinks else None
                    product.ProductLatestCost = products[j].ProductLatestCost
                    product.NetWeight = products[j].NetWeight
                    product.ItemTax = products[j].ItemTax




                    order.orderproducts.append(product)

                db.session.add(order)
                db.session.commit()


        self.key['NextToken'] = results.NextToken
        return self.key




