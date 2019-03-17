import webapp2
import jinja2
import os

from google.appengine.api import users
from google.appengine.ext import ndb

from adddriver import AddEditDriver
from device import DeviceModel
from comparedrivers import CompareDrivers
from myuser import MyUser

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
                                       extensions=["jinja2.ext.autoescape"],
                                       autoescape=True)


class MainPage(webapp2.RequestHandler):

    def get(self):
        self.response.headers["Content-Type"] = "text/html"

        url = ""
        geometry_shader = False
        tesselation_shader = False
        shader = False
        sparse_binding = False
        texture_compression = False
        vertex_pipeline = False
        user = users.get_current_user()

        if user:
            url = users.create_logout_url(self.request.uri)
            myuser_key = ndb.Key("MyUser", user.user_id())
            myuser = myuser_key.get()

            if myuser == None:
                myuser = MyUser(id=user.user_id())
                myuser.put()

            if self.request.GET.get("search_driver") == "Search":

                geometry_shader = bool(self.request.GET.get("radio_geometry"))
                tesselation_shader = bool(self.request.GET.get("radio_tesselation_shader"))
                shader = bool(self.request.GET.get("radio_shader_int"))
                sparse_binding = bool(self.request.GET.get("radio_sparse_blinding"))
                texture_compression = bool(self.request.GET.get("radio_texture"))
                vertex_pipeline = bool(self.request.GET.get("radio_vertex"))

                listdriver = DeviceModel.query()

                if geometry_shader == True:
                    listdriver = listdriver.filter(DeviceModel.geometry_shader == True)
                if tesselation_shader == True:
                    listdriver = listdriver.filter(DeviceModel.tesselation_shader == True)
                if shader == True:
                    listdriver = listdriver.filter(DeviceModel.shader == True)
                if sparse_binding == True:
                    listdriver = listdriver.filter(DeviceModel.sparse_binding == True)
                if texture_compression == True:
                    listdriver = listdriver.filter(DeviceModel.texture_compression == True)
                if vertex_pipeline == True:
                    listdriver = listdriver.filter(DeviceModel.vertex_pipeline == True)

                listdriver_query = listdriver.fetch()

            else:
                listdriver_query = DeviceModel.query().fetch()


        else:

            url = users.create_login_url(self.request.uri)
            listdriver_query = None

        template_values = {
            "url": url,
            "user": user,
            "list_drivers": listdriver_query,
            "radio_geometry" : geometry_shader,
            "radio_tesselation_shader": tesselation_shader,
            "radio_shader_int": shader,
            "radio_sparse_blinding": sparse_binding,
            "radio_texture": texture_compression,
            "radio_vertex" : vertex_pipeline
        }

        template = JINJA_ENVIRONMENT.get_template("main.html")
        self.response.write(template.render(template_values))

    def post(self):
            self.response.headers["Content-Type"] = "text/html"


app = webapp2.WSGIApplication([
    ("/", MainPage),
    ("/adddriver",AddEditDriver),
    ("/comparedrivers",CompareDrivers)
], debug=True)

