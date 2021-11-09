import re


class Model:
    def __new__(cls, *args, **kwargs):
        object_name = cls.__name__
        object_fields = list()

        for _k in cls.__dict__.keys():
            if not re.search('^__.+__$', _k):
                object_fields.append({_k: cls.__dict__.get(_k)})

        meta_data = {
            'NAME': object_name,
            'FIELDS': tuple(object_fields)
        }

        return meta_data


class Field:
    def __init__(self, field_name, default, is_nullable, autoincrement):
        self.humanized_name = field_name
        self.default = default
        self.__meta_data = None

    @property
    def meta_data(self) -> tuple:
        if self.__meta_data is not None:
            return self.__meta_data
        else:
            raise AttributeError('field Undefined.')

    @meta_data.setter
    def meta_data(self, value):
        if isinstance(value, (list, tuple)):
            if isinstance(value, tuple):
                self.__meta_data = value
            else:
                self.__meta_data = tuple(value)
        else:
            params = {'type': type(value)}
            raise ValueError('value type %(type)s is invalid.\n\
                              value must to be a list or tuple.' % params)


# Numeric
class IntegerField(Field):
    def __init__(self, field_name=None, default='__non_use_default__', is_nullable=False, autoincrement=False):
        super(IntegerField, self).__init__(field_name=field_name, default=default, is_nullable=is_nullable,
                                           autoincrement=autoincrement)

    def __str__(self):
        return self.__class__.__name__

    def __repr__(self):
        return f'<{self.__str__()}>'

    def new(self, value):
        """
        Return a new meta data, but used for insert values in database.
        """
        try:
            value = "'%s'" % value
        except TypeError:
            if self.default != '__non_use_default__' and isinstance(value, int):
                value = 'null' if self.default is None else "'%s'" % self.default
            else:
                raise ValueError('value of %s is invalid' % self.__class__.__name__)
        return value


class RealField(Field):
    pass


class BooleanField(Field):
    pass


# Date/Time
class DateField(Field):
    pass


class TimeField(Field):
    pass


class DateTimeField(Field):
    pass


# Literal
class CharacterField(Field):
    pass


class TextField(Field):
    pass


class EnumField(Field):
    pass


class SetField(Field):
    pass
