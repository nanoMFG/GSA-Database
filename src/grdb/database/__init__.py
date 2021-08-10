"""
Package init for grdb.database.  Currently all models are imported here to
provide implicit import support.

Examples:
    $ from grdb.database import sample

Todo:
    * Move to explicit imports eg:
    $ from grdb.database.model import sample_id
    * Possibly make model a Package.
"""
import typing
import re
from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm.exc import DetachedInstanceError

class_registry = {}


class Base(object):
    """Augmented Declarative Base class

    * Automatic camel_case tables names based on ClassName
    * Automatic integer "id" column as primary key
     
    """

    @declared_attr
    def __tablename__(cls):
        return re.sub(r"(?<!^)(?=[A-Z])", "_", cls.__name__).lower()

    def __repr__(self) -> str:
        return self._repr(id=self.id)

    def _repr(self, **fields: typing.Dict[str, typing.Any]) -> str:
        """
        Helper for __repr__
        """
        field_strings = []
        at_least_one_attached_attribute = False
        for key, field in fields.items():
            try:
                field_strings.append(f"{key}={field!r}")
            except DetachedInstanceError:
                field_strings.append(f"{key}=DetachedInstanceError")
            else:
                at_least_one_attached_attribute = True
        if at_least_one_attached_attribute:
            return f"<{self.__class__.__name__}({','.join(field_strings)})>"
        return f"<{self.__class__.__name__} {id(self)}>"


# Base = declarative_base(cls=Base)
"""
sqlalchemy.ext.declarative.declarative_base:  The declarative_base class instance
to be used by all models and DataAccessLayer connections.
"""
Base = declarative_base(cls=Base, class_registry=class_registry)

from .dal import dal
