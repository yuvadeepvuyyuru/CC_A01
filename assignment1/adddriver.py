import webapp2
import os
import jinja2

from google.appengine.ext import ndb

from datetime import datetime
from device import DeviceModel


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=["jinja2.ext.autoescape"],
    autoescape=True)

class AddEditDriver(webapp2.RedirectHandler):

    def get(self):

        self.response.headers["Content-Type"] = "text/html"
        button_action = "Add Driver"

        selected_name = self.request.GET.get("driver_name")

        if selected_name == None:
            selected_name = ""
            selected_driver = DeviceModel(device_name="",
                                          manufacturer_name="",
                                          date=None,
                                          geometry_shader=False,
                                          tesselation_shader=False,
                                          shader=False,
                                          sparse_binding=False,
                                          texture_compression=False,
                                          vertex_pipeline=False)

        else:
            button_action = "Update Driver"
            selected_driver_key = ndb.Key("DeviceModel", selected_name)
            selected_driver = selected_driver_key.get()

        template_values = {
            "selected_driver": selected_driver,
            "button_action" : button_action,
            "driver_name" : selected_name
        }

        template = JINJA_ENVIRONMENT.get_template("adddriver.html")
        self.response.write(template.render(template_values))

    def post(self):

        self.response.headers["Content-Type"] = "text/html"

        if self.request.get("add_driver") == "Add Driver":

            device_name =  self.request.get("device_name")

            if self.request.get("date") == "" or device_name == "":
                self.redirect("/adddriver")
                return

            listdriver_query = DeviceModel.query(DeviceModel.device_name == device_name).fetch()

            if len(listdriver_query) > 0:

                self.redirect("/adddriver")
                return

            manufacturer_name = self.request.get("manufacturer_name")
            date = datetime.strptime(self.request.get("date"), '%Y-%m-%d')
            geometry_shader = bool(self.request.get("radio_geometry"))
            tesselation_shader = bool(self.request.get("radio_tesselation_shader"))
            shader = bool(self.request.get("radio_shader_int"))
            sparse_binding = bool(self.request.get("radio_sparse_blinding"))
            texture_compression = bool(self.request.get("radio_texture"))
            vertex_pipeline = bool(self.request.get("radio_vertex"))

            new_device = DeviceModel(id = device_name,
                                     device_name=device_name,
                                     manufacturer_name=manufacturer_name,
                                     date=date,
                                     geometry_shader=geometry_shader,
                                     tesselation_shader=tesselation_shader,
                                     shader=shader,
                                     sparse_binding=sparse_binding,
                                     texture_compression=texture_compression,
                                     vertex_pipeline=vertex_pipeline)

            new_device.put()
            self.redirect("/")

        elif self.request.get("add_driver") == "Update Driver":

            selected_name = self.request.get("driver_name")
            selected_driver_key = ndb.Key("DeviceModel", selected_name)
            selected_driver = selected_driver_key.get()

            device_name = self.request.get("device_name")
            manufacturer_name = self.request.get("manufacturer_name")
            date = datetime.strptime(self.request.get("date"),'%Y-%m-%d')

            geometry_shader = bool(self.request.get("radio_geometry"))
            tesselation_shader = bool(self.request.get("radio_tesselation_shader"))
            shader = bool(self.request.get("radio_shader_int"))
            sparse_binding = bool(self.request.get("radio_sparse_blinding"))
            texture_compression = bool(self.request.get("radio_texture"))
            vertex_pipeline = bool(self.request.get("radio_vertex"))

            selected_driver.device_name =  device_name
            selected_driver.manufacturer_name = manufacturer_name
            selected_driver.date = date
            selected_driver.geometry_shader = geometry_shader
            selected_driver.tesselation_shader = tesselation_shader
            selected_driver.shader = shader
            selected_driver.sparse_binding = sparse_binding
            selected_driver.texture_compression = texture_compression
            selected_driver.vertex_pipeline = vertex_pipeline

            selected_driver.put()
            self.redirect("/")

        if self.request.get("cancel"):

            self.redirect("/")