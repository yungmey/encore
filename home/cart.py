# from home.models import TGoods

class Cartitem:
    def __init__(self, book, amount):
        self.id = book.id
        self.bookname =book.bookname
        self.picture =book.picture
        self.price =book.price
        self.marketprice =book.marketprice
        self.totalprice =self.price
        self.amount = amount
        self.state= True

class Addcar:
    def __init__(self):
        self.cartitems = []
        self.totalprice = 0
        self.save =0
        self.amount =0

    def add(self,cartitem):
        if not self.cartitems:
            self.totalprice = cartitem.totalprice
            self.amount = 1
            self.save = cartitem.marketprice - cartitem.price
            self.cartitems.append(cartitem)
        else:
            self.totalprice +=cartitem.price
            self.amount += cartitem.amount
            self.save += (cartitem.marketprice-cartitem.price)
            for i in self.cartitems:
                if i.id == cartitem.id:
                    i.amount +=1
                    i.totalprice = cartitem.price * i.amount
                    break

            else:
                self.cartitems.append(cartitem)

    def find(self,cartitem_id):
        cartitem_id =(cartitem_id if isinstance(cartitem_id,int) else int(cartitem_id))
        for i in self.cartitems:
            if cartitem_id == i.id:
                return i
        return False

    def remove(self, info_id):
        # 移入回收站
        # self.find(info_id).state = False
        for i in self.cartitems:
            if i.id == int(info_id):
                i.state = False
                self.cartitems.remove(i)
        self.change()

    def change(self):
        # 内容变更，同步更新其相关信息
        # ddprice = 0
        totalprice = 0
        amount = 0
        save = 0
        for i in self.cartitems:
            if i.state:
                # dangdang_price += item.dangdang_price * item.amount  # 购物车当当价总计
                i.totalprice = i.price * i.amount
                totalprice += i.price * i.amount  # 原价总计
                amount += i.amount  # 数量总计
                save += (i.marketprice - i.price) * amount
            else:
                # dangdang_price += item.dangdang_price * item.amount  # 购物车当当价总计
                i.totalprice -= i.price * i.amount  # 原价总计
                i.amount -= i.amount  # 数量总计
                save -= (i.marketprice - i.price) * amount
        # self.dangdang_price = dangdang_price
        self.totalprice = totalprice
        self.amount = amount
        self.save = save

    def upc(self,cartitem_id, new_amount):
        cartitem = self.find(cartitem_id)
        cartitem.amount = new_amount
        self.change()
        return cartitem.totalprice
