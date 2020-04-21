# Schema
Marshmallow Schemas

#### Common Requirements
Code that is used by all HTTP request types is stored in [misc.py](misc.py) and imported into each HTTP request type module, right now this includes the baseschema object and the property selection helper def.

#### Why are there separate schema files?
Schemas have been separated into get, put, and post to allow for subtle changes in schema dependant on HTTP request type. Note that this method requires the full module path to be used for string class representations when using `fields.Nested()` - i.e. instead of `"Address"` you might need to use `"app.schema.get.Address"`. In the example that follows imagine that you have a point of presence schema that has a nested schema called address. 

##### Schemas
In the POST schema we want the name and address fields to be mandatory so we might use the following validation def:
```python
class PointOfPresence(BaseSchema):
    """
    New Point of Presence (HTTP POST) schema
    """
    class Meta(BaseSchema.Meta):
        model = models.PointOfPresence
        fields = _includeprops(model,
                               only=['name',
                                     'address'])
    """
    Required fields
    """
    name = fields.Str(required=True)
    address = fields.Nested("app.schema.post.Address",
                            exclude=("pointofpresence",),
                            required=True)

    @validates('name')
    def _validate_schema_name(self, value: str) -> None:
        """
        Checks that the specified pointofpresence name is available
        Args:
            value(str): point of presence name

        Raises:
            ValidationError: If the specified PointOfPresence name is not available
        """
        if db.session.query(models.PointOfPresence).filter(models.PointOfPresence.name == value).count() == 1:
            raise ValidationError("PointOfPresence with Name '{}' already exists".format(value))
```

We check that the name does not already exist and we enforce the presence of an address key, whose data will be validated by a nested address field schema.

However, when we update a pointofpresence we don't always need to update an address, maybe we made a typo in the name that needs fixing. We cannot use the POST schema because it enforces the requirement for the address so we use a new PUT schema:

```python
class PointOfPresence(BaseSchema):
    """
    Update Point of Presence (HTTP PUT) schema
    """
    class Meta(BaseSchema.Meta):
        model = models.PointOfPresence
        fields = _includeprops(model,
                               only=['name',
                                     'address'])

    address = fields.Nested("app.schema.put.Address",
                            exclude=("pointofpresence",),)

    @validates('name')
    def _validate_schema_name(self, value):
        """
        Validates the name field

        Args:
            value: Point of Presence name

        Raises:
            ValidationError: if a PointOfPresence with the specified name already exists

        """
        if db.session.query(models.PointOfPresence).filter(models.PointOfPresence.name == value).count() == 1:
            raise ValidationError("PointOfPresence with Name '{}' already exists".format(value))
```

The change is small in the example (removal of `required=True` from the address field) but in more complicated use cases the separation will be useful. You may also have noticed the field selection for each of these schemas has an `only` list specified. This instructs the `_includeprops` def to only return properties that match the names in the `only` list, which will make marshmallow prevent attempts to fields that we might want to be read only. We could also achieve this using `dump_only=True` on a single point of presence schema but we would sacrifice our `@validation_schema` differentiation.

Finally here's the GET schema for point of presence:

```python
class PointOfPresence(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = models.PointOfPresence
        fields = _includeprops(model)

    href = ma.URLFor('route_pointofpresence', xid='<xid>', _external=True)
    address = fields.Nested("app.schema.get.Address",
                            exclude=("pointofpresence",),
                            dump_only=True)
    racks = fields.Nested("app.schema.get.Racks",
                          exclude=("pointofpresence",),
                          many=True,
                          dump_only=True)
    devices = fields.Nested("app.schema.get.Devices",
                            many=True,
                            dump_only=True)
    regions = fields.Nested("app.schema.get.Region",
                            exclude=("pointsofpresence",
                                     "devices"),
                            many=True,
                            dump_only=True)
```

Note that we have not specified an `only` list in the fields, and we have setup all relationships that a point of presence has with other Ambry models. We've also excluded `pointofpresence` and `devices` relationships where appropriate to prevent excessive recursion. The separate schema method also allows us to use `address` as a nested schema in GET while using it as a foreign key in PUT and POST.

##### Usage
Finally here's an example of how the PUT version is used. Note that the schema init file and import has been written to permit schema.<http request type>.<schema name> usage. Other imports are not included for the sake of brevity.

```python
import app.schema as schema


@app.route('/pointofpresence/<int:xid>', methods=['PUT'])
def route_pointofpresence_put(xid: int) -> Tuple[str, int]:
    if xid:
        data = request.get_json()
        if data:
            pointofpresence = db.session.query(models.PointOfPresence).get(int(xid))
            if pointofpresence:
                try:
                    pointofpresence = schema.put.PointOfPresence().load(data,
                                                                        instance=pointofpresence)
                    db.session.add(pointofpresence)
                    db.session.commit()
                    return return_result(schema.get.PointOfPresence().dump(pointofpresence))
                except ValidationError as err:
                    return jsonify({"error": err.messages,
                                    "data": None}), 422
            else:
                return jsonify({"error": "PointOfPresence id '{}' not found".format(xid),
                                "data": None}), 404

        return jsonify({"error": "No JSON data received",
                        "data": None}), 422

    return jsonify({"error": "pointofpresence 'xid' required",
                    "data": None}), 422
```

#### Are there other ways to do this?
Probably! This method does double up on some code - you might be able to inspect the HTTP request type and modify the validation definition such that it only performs address checks for POST for example. However you may run into difficulty preventing changes to foreign keys that you might need to modify for POST but disallow for PUT.


#### Bonus round - cross validation of fields
What do you do if you need to validate one field against data from another? Simple, instead of using a validation rule against a single field; we validate the schema instead. Here's a brief example of a decorated def:

```python
class EVCCircuitInterfaceVLAN(Schema):
    vlan = fields.List(fields.String(), default=[], required=True)
    tpid = fields.List(fields.String(), default=[], required=False, validate=validate.ContainsOnly(documentation.swagger_template["definitions"]["EVCCircuitInterfaceVLAN"]["properties"]["tpid"]["items"]["enum"]))
    native = fields.String(required=False, default="")
    limits = fields.Nested(EVCCircuitInterfaceVLANLimits, required=False)

    @validates_schema
    def _validate_evccircuitinterfacevlan(self, data):
        """
        Validates vlan and tpid fields. Def documentation inline with each function
        :param data: parsed schema data
        :return:
        """
        """
        check vlan is in the accepted vlan id list
        """
        for v in data["vlan"]:
            if v not in documentation.swagger_template["definitions"]["EVCCircuitInterfaceVLAN"]["properties"]["vlan"]["items"]["enum"]:
                raise ValidationError("vlan id {} is not valid".format(v), "vlan")
        """
        if limits are set ensure the outer vlan conforms
        """
        if "limits" in data.keys() and len(data["vlan"]) > 0:
            if data["vlan"][0] != "?":
                if "min" in data["limits"].keys() and "max" in data["limits"].keys():
                    l = [str(i) for i in range(data["limits"]["min"], data["limits"]["max"]+1)]
                    if data["vlan"][0] not in l:
                        raise ValidationError("vlan id {} not in specified limits: {}-{}".format(data["vlan"][0],
                                                                                                 data["limits"]["min"],
                                                                                                 data["limits"]["max"]))
                elif "min" in data["limits"].keys():
                    if int(data["vlan"][0]) < data["limits"]["min"]:
                        raise ValidationError("vlan id {} not in specified limits: >= {}".format(data["vlan"][0],
                                                                                                 data["limits"]["min"]))
                elif "max" in data["limits"].keys():
                    if int(data["vlan"][0]) > data["limits"]["max"]:
                        raise ValidationError("vlan id {} not in specified limits: <= {}".format(data["vlan"][0],
                                                                                                 data["limits"]["max"]))

        """
        if inner vlan is specified, outer vlan cannot be "next available"
        """
        if len(data["vlan"]) > 1:
            if data["vlan"][0] == "?":
                raise ValidationError("Cannot use next available outer vlan where inner vlan is specified", "vlan")

        """
        if tpid list exists it must be the same length as the vlan list
        """
        if "tpid" in data.keys():
            if isinstance(data["tpid"], list):
                if len(data["tpid"]) != len(data["vlan"]) and len(data["tpid"]) > 0:
                    raise ValidationError("tpid list length must be the same as vlan list length if supplied", "tpid")

        """
        if native is specified it must only be specified with a single vlan and it must match that vlan
        """
        if "native" in data.keys():
            if len(data["native"]) > 0 and len(data["vlan"]) > 1:
                raise ValidationError("cannot set native vlan when number of vlans > 1", "native")
            elif len(data["native"]) > 0 and len(data["vlan"]) == 1:
                if data["native"] != data["vlan"][0]:
                    raise ValidationError("native vlan must match outer vlan", "native")
```

by using `@validates_schema` we can get access to the complete data dictionary rather than the value of an individual field. This allows for data from one field to be compared with another. Any `ValidationError` raises will be raised against the entire schema itself rather than an individual field, unless you specify the optional field value in the raise: 
`raise ValidationError(message: str, fieldname: str)`.