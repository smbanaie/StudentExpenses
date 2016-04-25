#!/usr/bin/env python
# -*- coding: utf-8 -*-
from peewee import fn
import tornado.web
import tornado
from models import *
from index_handler import TornadoRequestBase
from index_handler import authentication
from pycket.session import SessionManager
import uuid, os

import jdatetime


class UploadImageUserHandler(TornadoRequestBase):
    @authentication()
    def post(self, *args, **kwargs):
        picture_address = self.user['picture_address']
        file = self.request.files['file'][0]
        file2 = "static/upload/user_images/"
        if not os.path.exists(file2): os.makedirs(file2)
        output_file = open("static/upload/user_images/" + picture_address, 'wb')
        output_file.write(file['body'])


class admin_Handler(TornadoRequestBase):
    @authentication()
    def get(self, *args, **kwargs):
        date = str(jdatetime.datetime.now())
        date = date.split('.')[0]

        self.render('admin/admin.html', date=date, user=self.user)

    def post(self, *args, **kwargs):
        return


class payments_Handler(TornadoRequestBase):
    @authentication()
    def get(self):

        date = str(jdatetime.datetime.now())
        date = date.split('.')[0]
        all_user = User().select().where(User.User == self.user['id_admin'])

        self.render('admin/payments.html', date=date, user=self.user, all_user=all_user)

    def post(self, *args, **kwargs):
        amount = self.get_argument('amount')
        date = self.get_argument('date')
        payer_id = self.get_argument('payer')
        type = self.get_argument('type')

        admin_id = self.user['id_admin']
        if type == "recive":
            type1 = True
        else:
            type1 = False
        bool_accept = False
        for i in self.request.arguments:
            if self.get_argument(i, None) == "":
                self.write(" لطفا همه فیلدها را پر کنید. ")
                bool_accept = True
                return
        if not bool_accept:
            Payment.create(
                amount=amount,
                type=type1,
                payer_id=payer_id,
                date=date,
                User=admin_id
            )
            self.write('success')


class add_buy_Handler(TornadoRequestBase):
    @authentication()
    def get(self):

        date = str(jdatetime.datetime.now())
        date = date.split('.')[0]
        id_admin = self.user['id_admin']

        all_user = User().select().where(User.User == id_admin)
        self.render('admin/add_buy.html', date=date, user=self.user, all_user=all_user)

    def post(self, *args, **kwargs):

        payer_id = self.get_argument('payer')
        amount = self.get_argument('amount')
        concern = self.get_argument('concern')
        partners = self.get_arguments('partners')
        count = len(partners)
        per_share = int(amount)/count
        id_admin = self.user['id_admin']
        date = self.get_argument('date')
        bool_accept = False

        for i in self.request.arguments:
            if self.get_argument(i, None) == "":
                self.write(" لطفا همه فیلدها را پر کنید. ")
                bool_accept = True
                return

        if not bool_accept:
            buy = Buy.create(
                amount=amount,
                concern=concern,
                date=date,
                payer_id=payer_id,
                per_share=per_share
            )
            for i in partners:
                User_has_buy.create(
                    User=i,
                    Buy=buy.id
                )

            for i in partners:
                try:
                    find_user = User.select().where(User.User == id_admin, User.id == i).get()
                    find_user = find_user.account
                except:
                    find_user = False
                account2 = per_share + int(find_user)
                update_account = User.update(account=account2).where(User.User == id_admin, User.id == i)
                update_account.execute()

        self.write('success')

class subscribers_Handler(TornadoRequestBase):
    @authentication()
    def get(self):
        admin_id = self.session.get('id_admin')
        all_user = User().select().where(User.User == admin_id)

        # id = self.session.get('id')
        # user = User.select().where(User.id == id).get()
        #

        date = str(jdatetime.datetime.now())
        date = date.split('.')[0]

        self.render('admin/subscribers.html', date=date, all_user=all_user, user=self.user)


class delsubscribers_Handler(TornadoRequestBase):
    @authentication()
    def post(self, *args, **kwargs):
        user_id = self.get_argument('user_id')

        try:
            find2 = User_has_buy.select().where(User_has_buy.User == user_id).get()
        except:
            find2 = False
        if not find2:
            User().select().where(User.id == user_id).get().delete_instance()
            self.write("success")
        else:
            self.write("این کاربر در خریدهای قبلی وجود دارد حذف ان امکان ندارد.")
            # os.remove("F:\python\Projhe(payandore)\TornadoD3\static\upload\user_images\\" + User.picture_address)


class changestatus_Handler(TornadoRequestBase):
    @authentication()
    def post(self, *args, **kwargs):
        user_id = self.get_argument('user_id')
        status = self.get_argument('status')
        if status == "1":
            status = 0
        else:
            status = 1

        try:
            find = User().select().where(User.id == user_id, User.type == False).get()
        except:
            find = False

        if find:
            User.update(status=status).where(User.id == user_id).execute()
            self.write('success')
        else:
            self.write("مدیر همیشه فعال می باشد.")


class modir_Handler(TornadoRequestBase):
    @authentication()
    def get(self, *args, **kwargs):
        date = str(jdatetime.datetime.now())
        date = date.split('.')[0]
        admin = Admin().select().get()
        admin = admin.name
        print(admin)
        self.render('modir/modir.html', date=date, name=admin)


class user_Handler(TornadoRequestBase):
    @authentication()
    def get(self, *args, **kwargs):
        date = str(jdatetime.datetime.now())
        date = date.split('.')[0]
        self.render('user/user.html', date=date, user=self.user)


class logout_Handler(TornadoRequestBase):
    def get(self):
        for i in self.session.keys():
            self.session.delete(i)
        self.redirect('/')


class bill_Handler(TornadoRequestBase):
    @authentication()
    def get(self, *args, **kwargs):

        date = str(jdatetime.datetime.now())
        date = date.split('.')[0]
        all_user = User().select().where(User.User == self.user['id_admin'])

        self.render('admin/bill.html', date=date, user=self.user, all_user=all_user)

    def post(self, *args, **kwargs):

        user_id = self.get_argument('user_id')
        try:
            user = User().select().where(User.id == user_id).get()
        except:
            user = False
        pic = user.picture_address
        payment = \
            Payment.select(fn.sum(Payment.amount)).where(Payment.payer_id == user_id, Payment.type == True).dicts()[0][
                'sum(`t1`.`amount`)']
        if not payment:
            payment = 0
        recive = \
            Payment.select(fn.sum(Payment.amount)).where(Payment.payer_id == user_id, Payment.type == False).dicts()[0][
                'sum(`t1`.`amount`)']
        if not recive:
            recive = 0
        spent = Buy.select(fn.sum(Buy.amount)).where(Buy.payer_id == user_id).dicts()[0]['sum(`t1`.`amount`)']
        if not spent:
            spent = 0
        try:
            account_user = User.select().where(User.id == user_id).get()
            account_user = account_user.account
        except:
            account_user = False

        sum = int(payment) + int(spent) - int(recive) - int(account_user)
        if sum > 0:
            status = "بستانکار"
        elif sum < 0:
            status = "بدهکار"
        else:
            status = "تسویه"
        dict = {'picture_address': pic, 'payment': payment, 'recive': recive, 'spent': spent,
                'account_user': account_user, 'sum': sum, 'status': status}
        self.write(dict)


class tinyconsumption_Handler(TornadoRequestBase):
    @authentication()
    def get(self, *args, **kwargs):
        date = str(jdatetime.datetime.now())
        date = date.split('.')[0]
        try:
            page = int(args[0]) - 1 if args[0] else 0
        except:
            page = 0

        find = Buy.select(
            Buy.id.alias('buy_id'),
            Buy.amount,
            Buy.concern,
            Buy.date,
            Buy.payer_id,
            User.name, User.id).join(User_has_buy).switch(
            User_has_buy).join(User).where(User.User == self.user['id_admin'])

        list_id_buy = []
        list_all_buy = find.dicts()

        for i in list_all_buy:
            if i['buy_id'] not in list_id_buy:
                list_id_buy.append(i['buy_id'])

        last_list_buy = []

        for i in list_id_buy:
            list_user = []
            amount = ""
            concern = ""
            date = ""
            for j in range(0, list_all_buy.count()):
                if i == list_all_buy[j]['buy_id']:
                    list_user.append(list_all_buy[j]['name'])
                    amount = list_all_buy[j]['amount']
                    concern = list_all_buy[j]['concern']
                    date = list_all_buy[j]['date']

            last_list_buy.append(
                dict(
                    {
                        'list_user': list_user,
                        'id': i,
                        'amount': amount,
                        'concern': concern,
                        'date': date,
                    }
                )
            )
            continue
        type_user = self.session.get('type_user')

        pagination = dict(
            have_next=False,
            have_prev=True,
            next=page + 1,
            prev=page - 1,
            total=len(last_list_buy),
            current_page=page
        )

        if len(last_list_buy) > 5:
            pagination['have_next'] = True

        if page == 0:
            pagination['have_prev'] = False

        last_list_buy = last_list_buy[page * 5: (page + 1) * 5]

        if type_user:
            self.render('admin/tinyconsumption.html', date=date, user=self.user, list_buy=last_list_buy, pagination=pagination)
        else:
            self.render('user/tinyconsumption.html', date=date, user=self.user, list_buy=last_list_buy, pagination=pagination)


class profile_Handler(TornadoRequestBase):
    @authentication()
    def get(self, *args, **kwargs):
        date = str(jdatetime.datetime.now())
        date = date.split('.')[0]
        user = self.user
        if user['type_user'] == True:
            self.render('admin/profile.html', date=date, user=user)
        else:
            self.render('user/profile.html', date=date, user=user)


class user_bill_Handler(TornadoRequestBase):
    @authentication()
    def get(self, *args, **kwargs):
        date = str(jdatetime.datetime.now())
        date = date.split('.')[0]

        all_user = User().select().where(User.User == self.user['id_admin'])
        self.render('user/bill.html', date=date, user=self.user, all_user=all_user)


class message_Handler(TornadoRequestBase):
    @authentication()
    def get(self, *args, **kwargs):
        date = str(jdatetime.datetime.now())
        date = date.split('.')[0]
        user = self.user
        message = Message().select(User.name, Message).join(User).where(Message.id_reciver == self.user['id']).dicts()

        self.render('admin/message.html', date=date, user=self.user, message=message)


class registerbuy_Handler(TornadoRequestBase):
    @authentication()
    def get(self, *args, **kwargs):
        date = str(jdatetime.datetime.now())
        date = date.split('.')[0]
        self.render('user/add_buy.html', date=date, user=self.user)


    def post(self, *args, **kwargs):
        bool_accept = False
        description = self.get_argument('buy')
        date_buy = self.get_argument('date')
        for i in self.request.arguments:
            if self.get_argument(i, None) == "":
                self.write(" لطفا همه فیلدها را پر کنید. ")
                bool_accept = True
                break
        uer_id = self.session['id']
        id_admin = self.session['id_admin']
        date = str(jdatetime.datetime.now())
        date = date.split('.')[0][0:10]
        if not bool_accept:
            Message.create(
                description=description,
                date_buy=date_buy,
                date=date,
                id_reciver=id_admin,
                User=uer_id,
                status=True

            )
            self.write("success")


class status_message_Handler(TornadoRequestBase):
    @authentication()
    def post(self, *args, **kwargs):
        id_message = self.get_argument('id_message')
        Message().update(status=False).where(Message.id == id_message).execute()
        count = int(self.session.get('count_message')) - 1
        self.session.set('count_message', count)
        message = self.session.get('message')
        new_message = []
        for i in message:
            if i['id'] != int(id_message):
                new_message.append(i)
        self.session.set('message', new_message)


class del_message_Handler(TornadoRequestBase):
    @authentication()
    def post(self, *args, **kwargs):
        id_message = self.get_argument('id_message')

        try:
            msg = Message().select().where(Message.id == id_message).get()
            msg = msg.status
        except:
            msg = False
        if msg:
            Message().select().where(Message.id == id_message).get().delete_instance()
            message = self.session.get('message')
            new_message = []
            for i in message:
                if i['id'] != int(id_message):
                    new_message.append(i)
            self.session.set('message', new_message)
            count = int(self.session.get('count_message')) - 1
            self.session.set('count_message', count)
            self.write("reduce")
        else:
            Message().select().where(Message.id == id_message).get().delete_instance()
            message = self.session.get('message')
            new_message = []
            for i in message:
                if i['id'] != int(id_message):
                    new_message.append(i)
            self.session.set('message', new_message)
            self.write("no_reduce")


class note_Handler(TornadoRequestBase):
    @authentication()
    def get(self, *args, **kwargs):
        date = str(jdatetime.datetime.now())
        date = date.split('.')[0]
        note = Note().select().where(Note.User == self.session.get('id'))
        type_user = self.session.get('type_user')
        if type_user:
            self.render('admin/note.html', date=date, user=self.user, note=note)
        else:
            self.render('user/note.html', date=date, user=self.user, note=note)

    def post(self, *args, **kwargs):
        title = self.get_argument('title')
        body = self.get_argument('body')
        date_alert = self.get_argument('date')
        user_id = self.session.get('id')
        bool_accept = False
        dict_data = {}
        for i in self.request.arguments:
            if self.get_argument(i, None) == "":
                bool_accept = True
                dict_data = {"msg": 'همه فیلد ها را پر کنید.'}
                self.write(dict_data)
                return
        if not bool_accept:
            note = Note.create(
                title=title,
                text=body,
                date=date_alert,
                User=user_id
            )
            dict_data = {
                "msg": 'success',
                "title": note.title,
                "text": note.text,
                "date": note.date,
                "id": note.id
            }
            self.write(dict_data)


class delnote_Handler(TornadoRequestBase):
    @authentication()
    def post(self, *args, **kwargs):
        note_id = self.get_argument('note_id')
        Note().select().where(Note.id == note_id).get().delete_instance()
        self.write("success")


class delbuy_Handler(TornadoRequestBase):
    @authentication()
    def post(self, *args, **kwargs):
        buy_id = self.get_argument('buy_id')
        try:
            per_share = Buy().select().where(Buy.id == buy_id).get()
            per_share = per_share.per_share
        except:
            per_share = False
        buys = User_has_buy().select().where(User_has_buy.Buy == buy_id).dicts()
        for i in buys:
            User_has_buy().select().where(User_has_buy.Buy == buy_id).get().delete_instance()
        Buy().select().where(Buy.id == buy_id).get().delete_instance()

        find_user = User().select().where(User.User == self.session.get('id_admin')).dicts()
        for i in find_user:
                # try:
                #     find_user1 = User.select().where(User.User == self.session.get('id_admin'), User.account == i['account']).get()
                #     find_user1 = find_user1.account
                # except:
                #     find_user1 = False
                account2 = i['account'] - per_share
                User.update(account=account2).where(User.User == self.session.get('id_admin'), User.account == i['account']).execute()


