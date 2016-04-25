#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functools
import tornado
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import string
import os.path
import uuid
import jdatetime
from pycket.session import SessionManager
from models import *
import random


def authentication():
    def f(func):
        @functools.wraps(func)
        def func_wrapper(self, *args, **kwargs):
            if not self.current_user:
                self.redirect('/')
                return

            return func(self, *args, **kwargs)

        return func_wrapper

    return f


class TornadoRequestBase(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        super(TornadoRequestBase, self).__init__(application, request, **kwargs)

        self.session = SessionManager(self)

        self.user = {
            "name": self.session.get('name', None),
            "user": self.session.get('user', None),
            "id": self.session.get('id', None),
            "picture_address": self.session.get('picture_address', None),
            "id_admin": self.session.get('id_admin', None),
            "type_user": self.session.get('type_user', None),
            "online": self.session.get('online', None),
            "password": self.session.get('password', None),
            "email": self.session.get('email', None),
            "message": self.session.get('message', None),
            "count_message": self.session.get('count_message', None)


        }

    def get_current_user(self):
        return self.session.get('online')


class index_Handler(TornadoRequestBase):
    def get(self):
        self.render('home/index.html')

    def post(self, *args, **kwargs):
        username = self.get_argument('user')
        password = self.get_argument('password')
        # try:
        #     admin = Admin().select().where(Admin.user == username,Admin.password == password).get()
        # except:
        #     admin = False
        try:
            find_user = User().select().where((User.user == username) & (User.password == password) & ((User.status == 3) | (User.status==1))).get()
        except:
            find_user = False

        if find_user:
            try:
                message = Message().select().where(Message.id_reciver == find_user.id, Message.status == True)
                count_message = message.count()
                message_list = []
                m_dict = {}
                for item in message:
                    user = User().select().where(User.id == item.User).get()
                    m_dict = {'id':item.id,'description': item.description, 'status': item.status, 'name': user.name,
                              'picture_address': user.picture_address, 'date': str(item.date),"id":item.id}
                    message_list.append(m_dict)
            except:
                count_message = 0
                message_list = []

            self.session.set('name', find_user.name)
            self.session.set('id', find_user.id)
            self.session.set('id_admin', find_user.User)
            self.session.set('picture_address', find_user.picture_address)
            self.session.set('type_user', find_user.type)
            self.session.set('online', True)
            self.session.set('user', find_user.user)
            self.session.set('email', find_user.email)
            self.session.set('password', find_user.password)
            self.session.set('count_message', count_message)
            self.session.set('message', message_list)

            if find_user.type == True:
                self.write("admin-user")
            else:
                self.write('user')
        # elif admin:
        #     self.write("admin")
        else:
            self.write("نام کاربری یا پسورد اشتباه می باشد.یا اکانت شما فعال نیست.")


class register_Handler(TornadoRequestBase):
    def get(self):
        self.render('home/register.html')

    def post(self, *args, **kwargs):

        update_check = False
        if 'update' in self.request.arguments.keys():
            update_check = True
            id_update = self.get_argument('id_user')

        name = self.get_argument('name')
        email = self.get_argument('email')
        user = self.get_argument('user')
        password = self.get_argument('password')

        bool_acept = False
        for i in self.request.arguments:
            if self.get_argument(i, None) == "":
                dict_u = {"msg":'همه فیلد ها را پر کنید.' }
                self.write(dict_u)
                bool_acept = True
                return
        if not update_check:
            try:
                find_user = User().select().where(User.user == user).get()
            except:
                find_user = False

            if find_user:
                bool_acept = True
                dict_u = {"msg":'نام کاربری تکراری است.' }
                self.write(dict_u)
                return
            try:
                file = self.request.files['image'][0]
                original_fname = file['filename']
                type_image = original_fname.split(".")[-1]
                address_image = str(uuid.uuid4()) + ".jpg"
                file2 = "static/upload/user_images/"
                if not os.path.exists(file2): os.makedirs(file2)
                output_file = open("static/upload/user_images/" + address_image, 'wb')
                output_file.write(file['body'])
            except:
                bool_acept = True
                dict_u = {"msg":'تصویر انتخاب نشده.'}
                self.write(dict_u)
                return


        if len(password) < 5:
            bool_acept = True
            dict_u = {"msg":'پسودرد حداقل باید 6 کاراکتر باشد.' }
            self.write(dict_u)
            return
        if not update_check:
            repeat_password = self.get_argument('repeat_Pass')
            if password != repeat_password:
                dict_u = {"msg":'پسورد با تکرارش مطابقت ندارد.'}
                self.write(dict_u)
                bool_acept = True
                return
        id_user = 0
        while (True):
            id_user = random.randint(100, 10000000)
            try:
                find = User.select().where(User.id == id_user).get()
            except:
                find = False

            if not find:
                break
            else:
                continue

        if 'type_user' in self.session.keys():
            if self.session.get('type_user'):
                type_user = False
                id_admin = self.session.get('id')
                status = 1

            else:
                status = 3
                type_user = True
                id_admin = id_user

        else:
            type_user = True
            id_admin = id_user
            status = 3

        if not bool_acept and not update_check:
            user = User.create(
                id=id_user,
                name=name,
                user=user,
                email=email,
                password=password,
                picture_address=address_image,
                account=0,
                type=type_user,
                User=id_admin,
                status=status

            )
            dict_u = {
                "msg": "success",
                "name": user.name,
                "user": user.user,
                "picture_address": user.picture_address,
                "id": user.id
            }
            self.write(dict_u)

        elif not bool_acept and update_check:
            User.update(
                name=name,
                user=user,
                email=email,
                password=password,
            ).where(User.id == id_update)
            self.session.set('name', name)
            self.session.set('user', user)
            self.write("success")


class ForgetpassHandler(TornadoRequestBase):
    def get(self):
        self.render('home/forget_pass.html')




