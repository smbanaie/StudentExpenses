import tornado.web
import tornado

class TestHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):

        self.render('home.aspx_files.html')

    def post(self, *args, **kwargs):

        name = self.get_argument('name_name')

        print "************************"+name
