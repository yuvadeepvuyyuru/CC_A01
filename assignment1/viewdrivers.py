import webapp2
import jinja2
import os

from google.appengine.ext import ndb
from device import DeviceModel

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
                                       extensions=["jinja2.ext.autoescape"],
                                       autoescape=True)


class MainHandler(webapp2.RequestHandler):

    def get(self):
        self.response.headers["Content-Type"] = "text/html"

        listdriver_query = DeviceModel.query()
        if self.request.GET.get("search_driver") == "Search":

            geometry_shader = bool(self.request.GET.get("radio_geometry"))
            tesselation_shader = bool(self.request.GET.get("radio_tesselation_shader"))
            shader = bool(self.request.GET.get("radio_shader_int"))
            sparse_binding = bool(self.request.GET.get("radio_sparse_blinding"))
            texture_compression = bool(self.request.GET.get("radio_texture"))
            vertex_pipeline = bool(self.request.GET.get("radio_vertex"))

            listdriver_query = DeviceModel.query(ndb.OR(DeviceModel.geometry_shader == geometry_shader)).fetch()

        else:

            geometry_shader = False
            tesselation_shader = False
            shader = False
            sparse_binding = False
            texture_compression = False
            vertex_pipeline = False
            listdriver_query = DeviceModel.query().fetch()

        template_values = {
            "list_drivers": listdriver_query,
            "radio_geometry" : geometry_shader,
            "radio_tesselation_shader": tesselation_shader,
            "radio_shader_int": shader,
            "radio_sparse_blinding": sparse_binding,
            "radio_texture": texture_compression,
            "radio_vertex" : vertex_pipeline
        }

        template = JINJA_ENVIRONMENT.get_template("viewdrivers.html")
        self.response.write(template.render(template_values))