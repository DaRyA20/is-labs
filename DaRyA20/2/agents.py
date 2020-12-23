from pade.misc.utility import display_message, start_loop, call_later
from pade.core.agent import Agent
from pade.acl.messages import ACLMessage
from pade.acl.aid import AID
from sys import argv
import pickle

class PriceMessage():
    def __init__(self):
        self.step = 0
        self.my_price = 0
        self.is_final = False


# Класс продавца
class Seller(Agent):
    def __init__(self, aid, start_price, min_sell_price):
        super(Seller, self).__init__(aid=aid, debug=False)
        # задается начальная стоимость товара
        self.start_price = start_price
        # минимальная цена для продажи
        self.min_sell_price = min_sell_price
        # уровень на котором сейчас идет торг
        self.current_price = start_price
        # как долго готов торговать
        self.max_steps = 10

    def on_start(self):
        super(Seller, self).on_start()
        display_message(self.aid.localname, 'I am Seller, ')
        call_later(8.0, self.sending_start_message)

    # отправка предложения о покупке
    def sending_start_message(self):
        price_message = PriceMessage()
        price_message.my_price = self.start_price
        message = ACLMessage(ACLMessage.INFORM)
        message.add_receiver(AID('buyer'))
        message.set_content(pickle.dumps(price_message))
        display_message(self.aid.localname, 'Would you like to buy this for {}'.format(price_message.my_price))
        self.send(message)

    def react(self, message):
        super(Seller, self).react(message)
        # фильтруем сообщения полученные не от покупателя
        if message.sender.name[0:3] == 'ams':
            return
        price_message = pickle.loads(message.content)
        # реагируем на последнее сообщение покупателя
        if price_message.is_final == True:
            if price_message.my_price >=  self.min_sell_price:
                display_message(self.aid.localname, 'I am agree on this {}'.format(price_message.my_price))
            else:
                display_message(self.aid.localname, 'I am disagree on this {}'.format(price_message.my_price))
        # если торг идет слишком долго
        elif price_message.step >= self.max_steps:
            price_message.step += 1
            price_message.is_final = True
            # соглашаемся если нас устраивает последнее предложение
            if price_message.my_price >= self.min_sell_price:
                message = ACLMessage(ACLMessage.INFORM)
                message.add_receiver(AID('buyer'))
                message.set_content(pickle.dumps(price_message))
                self.send(message)
                display_message(self.aid.localname, 'I am agree on this {}'.format(price_message.my_price))
            # делаем финальное предложение
            else:
                price_message.my_price = self.min_sell_price
                self.current_price = price_message.my_price
                message = ACLMessage(ACLMessage.INFORM)
                message.add_receiver(AID('buyer'))
                message.set_content(pickle.dumps(price_message))
                self.send(message)
                display_message(self.aid.localname, 'My last proposal is {}'.format(price_message.my_price))
        # торг
        else:
            price_message.step += 1
            price_message.my_price = (price_message.my_price + self.current_price) / 2
            self.current_price = price_message.my_price
            message = ACLMessage(ACLMessage.INFORM)
            message.add_receiver(AID('buyer'))
            message.set_content(pickle.dumps(price_message))
            self.send(message)
            display_message(self.aid.localname, 'My proposal is {}'.format(price_message.my_price))


# класс покупателся
class Buyer(Agent):
    def __init__(self, aid, max_buy_price):
        super(Buyer, self).__init__(aid=aid, debug=False)
        # максимальная цена которую покупатель готов отдать
        self.max_buy_price = max_buy_price
        self.current_price = 0
        self.max_steps = 6

    def react(self, message):
        super(Buyer, self).react(message)
        if message.sender.name[0:3] == 'ams':
            return
        price_message = pickle.loads(message.content)
        # делаем первое предложение по стоимости
        if price_message.step == 1:
            price_message.step += 1
            price_message.my_price = self.max_buy_price / 2
            self.current_price = price_message.my_price
            message = ACLMessage(ACLMessage.INFORM)
            message.add_receiver(AID('seller'))
            message.set_content(pickle.dumps(price_message))
            self.send(message)
            display_message(self.aid.localname, 'My proposal is {}'.format(price_message.my_price))
        # реагируем на последнее предложение
        elif price_message.is_final == True:
            if price_message.my_price <=  self.max_buy_price:
                display_message(self.aid.localname, 'I am agree on this {}'.format(price_message.my_price))
            else:
                display_message(self.aid.localname, 'I am disagree on this {}'.format(price_message.my_price))
        # если торг идет слишком долго
        elif price_message.step >= self.max_steps:
            price_message.step += 1
            price_message.is_final = True
            # если нас устраивает цена на которой сейчас идут торги
            if price_message.my_price <= self.max_buy_price:
                message = ACLMessage(ACLMessage.INFORM)
                message.add_receiver(AID('seller'))
                message.set_content(pickle.dumps(price_message))
                self.send(message)
                display_message(self.aid.localname, 'I am agree on this {}'.format(price_message.my_price))
            # если нас не устраивает цена на которой сейчас идут торги? делаем последнее предложение
            else:
                price_message.my_price = self.max_buy_price
                self.current_price = price_message.my_price
                message = ACLMessage(ACLMessage.INFORM)
                message.add_receiver(AID('seller'))
                message.set_content(pickle.dumps(price_message))
                self.send(message)
                display_message(self.aid.localname, 'My last proposal is {}'.format(price_message.my_price))
        # торг
        else:
            price_message.step += 1
            price_message.my_price = (price_message.my_price + self.current_price) / 2
            self.current_price = price_message.my_price
            message = ACLMessage(ACLMessage.INFORM)
            message.add_receiver(AID('seller'))
            message.set_content(pickle.dumps(price_message))
            self.send(message)
            display_message(self.aid.localname, 'My proposal is {}'.format(price_message.my_price))


if __name__ == '__main__':

    agents = list()
    port = int(argv[1])
    destinatario_agent = Seller(AID(name='seller@localhost:{}'.format(port)), 300, 150)
    agents.append(destinatario_agent)

    port += 1
    remetente_agent = Buyer(AID(name='buyer@localhost:{}'.format(port)), 200)
    agents.append(remetente_agent)

    start_loop(agents)


# output example
# [seller] 23/12/2020 13:16:56.186 --> Would you like to buy this for 300
# [buyer] 23/12/2020 13:16:56.191 --> My proposal is 150.0
# [seller] 23/12/2020 13:16:56.195 --> My proposal is 225.0
# [buyer] 23/12/2020 13:16:56.200 --> My proposal is 187.5
# [seller] 23/12/2020 13:16:56.204 --> My proposal is 206.25
# [buyer] 23/12/2020 13:16:56.206 --> My proposal is 196.875
# [seller] 23/12/2020 13:16:56.209 --> My proposal is 201.5625
# [buyer] 23/12/2020 13:16:56.212 --> My last proposal is 200
# [seller] 23/12/2020 13:16:56.214 --> I am agree on this 200
