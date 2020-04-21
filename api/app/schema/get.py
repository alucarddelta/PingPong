from .misc import BaseSchema, _includeprops
from marshmallow import validates_schema, ValidationError, fields
from app import models, db, ma

class Core(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = models.Core

        stuff = fields.Nested('app.schema.get.Core',
                          many=True,
                          dump_only=True)


class Request(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = models.Request

        stuff = fields.Nested('app.schema.get.Request',
                          many=True,
                          dump_only=True)

    request_result = fields.Nested('app.schema.get.Request_Result', exclude=['xid'],
                          many=True,
                          dump_only=True)

class Heartbeat_Send(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = models.Heartbeat_Send

        stuff = fields.Nested('app.schema.get.Heartbeat_Send',
                          many=True,
                          dump_only=True)

class Heartbeat_Receive(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = models.Heartbeat_Receive

        stuff = fields.Nested('app.schema.get.Heartbeat_Receive',
                          many=True,
                          dump_only=True)

class Request_Result(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = models.Request_Result

        stuff = fields.Nested('app.schema.get.Request_Result',
                          many=False,
                          dump_only=True)
