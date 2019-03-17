import webapp2
import jinja2
import os

from google.appengine.ext import ndb

from device import DeviceModel


JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
                                       extensions=["jinja2.ext.autoescape"],
                                       autoescape=True)

class CompareDrivers(webapp2.RequestHandler):

    def get(self):
        self.response.headers["Content-Type"] = "text/html"

        selected_device_name = self.request.GET.get("selected_device")
        current_device_name = self.request.GET.get("current_device")

        if selected_device_name != None and current_device_name != None:

            selected_device_key = ndb.Key("DeviceModel", selected_device_name)
            selected_device = selected_device_key.get()

            current_device_key = ndb.Key("DeviceModel", current_device_name)
            current_device = current_device_key.get()

            listdriver_query = DeviceModel.query(ndb.OR(DeviceModel.device_name == selected_device_name,
                                             DeviceModel.device_name == current_device_name)).fetch()

        else:
            listdriver_query = DeviceModel.query().fetch()

        template_values = {
            "list_drivers": listdriver_query
        }

        if self.request.get("cancel"):
            self.redirect("/")

        template = JINJA_ENVIRONMENT.get_template("comparedrivers.html")
        self.response.write(template.render(template_values))


