import re


class Model:
    def __new__(cls, *args, **kwargs):
        object_name = cls.__name__
        object_fields = list()

        for _k in cls.__dict__.keys():
            if not re.search('^__.+__$', _k):
                object_fields.append({_k: cls.__dict__.get(_k)})

        meta_data = {
            'NAME': object_name.lower(),
            'FIELDS': tuple(object_fields)
        }

        return meta_data


class Field:
    def __init__(self, default, is_nullable, autoincrement, primary_key, unique):
        self.default = default
        self.is_nullable = is_nullable
        self.autoincrement = autoincrement
        self.primary_key = primary_key
        self.unique = unique

    @classmethod
    def this_class(cls):
        return cls

    @property
    def field_creation_template(self):
        template_parts = [
            '%(field_name)s',
            f'%({self.__class__.__name__})s',
        ]
        if self.primary_key and not self.unique:
            part = 'PRIMARY KEY'
            template_parts.append(part)
        elif self.unique and not self.primary_key:
            part = 'UNIQUE'
            template_parts.append(part)

        if self.autoincrement and self.primary_key:
            part = 'AUTOINCREMENT'
            template_parts.append(part)
        elif self.autoincrement and not primary_key:
            raise AttributeError("can not set autoincrement if field is not a primary key")

        if not self.is_nullable and self.default is None:
            part = 'NOT NULL'
            template_parts.append(part)
        elif not self.is_nullable and self.default is not None:
            part = 'DEFAULT {}'.format(self.default)
            template_parts.append(part)
        elif self.is_nullable and self.default is None:
            part = 'DEFAULT NULL'
            template_parts.append(part)
        else:
            raise AttributeError('error when setting a default value or setting a null value in your model field')

        template = ' '.join([part for part in template_parts])

        return template


# Numeric
class IntegerField(Field):
    def __init__(self, default=None, is_nullable=False, autoincrement=False,
                 primary_key=False, unique=False):
        super(IntegerField, self).__init__(default=default, is_nullable=is_nullable, autoincrement=autoincrement,
                                           primary_key=primary_key, unique=unique)

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
