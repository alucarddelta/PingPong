import inspect
from sqlalchemy.inspection import inspect as sainspect
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.ext.associationproxy import ColumnAssociationProxyInstance
from app import ma, db, models
from typing import List, Optional, Union, Type


def _includeprops(model: Type[models.Base],
                  custom: Optional[Union[List[str], None]] = None,
                  exclude: Optional[Union[List[str], None]] = None,
                  include: Optional[Union[List[str], None]] = None,
                  only: Optional[Union[List[str], None]] = None,
                  excludefk: bool = True) -> List[str]:
    """ returns a string list of sqlalchemy model property, InstrumentedAttribute, and ColumnAssociationProxyInstance field names based on
    passed exclude, include, and only lists and an exclude foreign keys boolean.

    Args:
        model (:obj:`models.Base`): SqlAlchemy Model Base or BaseDeployable instance
        custom (:obj:`list` of :obj:`str`, optional): custom schema fields to include (e.g. href)
        exclude (:obj:`list` of :obj:`str`, optional): specifically exclude these property names
        include (:obj:`list` of :obj:`str`, optional): specifically include these property names - overrides exclude
        only (:obj:`list` of :obj:`str`, optional): only include these property names - overrides exclude and include
        excludefk (bool): exclude properties whose name ends in '_xid'

    Returns:
        List[str]: List of property names to be included in schema view

    """
    r = list()
    i = list()
    e = list()
    o = list()
    if isinstance(exclude, list):
        e.extend(exclude)
    if isinstance(include, list):
        i.extend(include)
    if isinstance(only, list):
        o.extend(only)
    if isinstance(custom, list):
        r.extend(custom)

    for prop in inspect.getmembers(inspect.getmembers(sainspect(eval('models.{}()'.format(model.__name__))))[2][1]['class_']):
        if isinstance(prop[1], property) or isinstance(prop[1], InstrumentedAttribute) or isinstance(prop[1], ColumnAssociationProxyInstance):
            if o:
                if prop[0] in o:
                    if prop[0] not in r:
                        r.append(prop[0])
            elif (prop[0][0] != "_" and prop[0] not in r) and prop[0] not in e:
                if excludefk and prop[0][-4:] == "_xid" and prop[0] not in i:
                    continue
                r.append(prop[0])

    return r


class BaseSchema(ma.ModelSchema):
    """ Base Marshmallow Schema inherited from Flask-Marshmallow instance. Implements default sqla_session and post dump def
    that ignores first level keys with no value set

    """
    class Meta:
        """ setup base schema meta data """
        sqla_session = db.session
