from .misc import BaseSchema, _includeprops
from marshmallow import validates_schema, ValidationError, fields
from app import models, db

class Core(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = models.Core
        fields = _includeprops(model=model)

class Request(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = models.Request
        fields = _includeprops(model=model)

class Request_Result(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = models.Request_Result
        fields = _includeprops(model=model)

class Heartbeat_Receive(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = models.Heartbeat_Receive
        fields = _includeprops(model=model)