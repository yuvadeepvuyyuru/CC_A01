from google.appengine.ext import ndb


class DeviceModel(ndb.Model):

        device_name = ndb.StringProperty()
        manufacturer_name = ndb.StringProperty()
        date = ndb.DateProperty()

        geometry_shader = ndb.BooleanProperty()
        tesselation_shader = ndb.BooleanProperty()
        shader = ndb.BooleanProperty()
        sparse_binding = ndb.BooleanProperty()
        texture_compression = ndb.BooleanProperty()
        vertex_pipeline = ndb.BooleanProperty()