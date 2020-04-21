from .misc import BaseSchema, _includeprops
from marshmallow import ValidationError, fields, validates
from app import models, db


class Request(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = models.Request
        fields = _includeprops(model=model)
