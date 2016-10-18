#!/usr/bin/env python
# -*- coding: utf-8  -*-
"""
borm ,业务对象映射 ，处理业务对象的声明和json互转，borm旨在降低数据在业务逻辑之间流转的成本，统一声明校验数据

适合场景：
    1. 需要在很多复杂的业务逻辑里传递业务对象时，封装一个统一的Model
    2. 发起第三方请求时声明model对象，可以简化对象构造，参数校验的成本，也更容易维护
    3. 校验api的参数，构造请求字典

class Base(borm.BOModel):
    channel = borm.StringField(required=True)

class User(Base):
    name = borm.StringField(required=True)
    age = borm.IntegerField(default=18)

user = User(name='jack',age='25',channel='china')
user.todict()

{
    channel: 'china',
    name: 'jack',
    age: 25
}

可以提供一个校验器类：

class _FormValidator(object):
    def validate_name(self, model, value, field_obj):
        if not value:
            raise borm.ValidateError('param:name must be given.')

class User(Base):
    __validator__ = _FormValidator()
    name = borm.StringField(required=True)
    age = borm.IntegerField(default=18)

user.validate(quiet=True) #quite 控制是否引发校验失败的异常，不引发，则会返回异常的exec对象列表

通过orm和校验可以实现在业务层级任何地方对业务对象进行有效值校验，object-json转换等。
"""
import json
import weakref
from misc import safeunicode, safestr


class BormError(Exception):
    def __init__(self, reason):
        self.reason = reason
        super(BormError, self).__init__(reason)


class FieldError(BormError):
    """ field error"""


class RequiredError(BormError):
    """require error"""


class ValidateError(BormError):
    def __init__(self, reason, field=None):
        self.field = field
        super(ValidateError, self).__init__(reason)


class Field(object):
    def __init__(self, **kw):
        self.__datatype = kw.get('datatype', None)
        self.__default = kw.get('default', None)
        self.__required = kw.get('required', False)
        self.__info = kw.get('info', '')
        self._name = None
        self._model = None

    @property
    def default(self):
        d = self.__default
        return d() if callable(d) else d

    @property
    def value(self):
        if self._model:
            return self._model[self._name]

    @property
    def info(self):
        return self.__info

    @property
    def datatype(self):
        return self.__datatype

    @property
    def required(self):
        return self.__required

    def __str__(self):
        return '<%s:%s>' % (self.__class__.__name__, str(self.datatype),)

    def check(self, value):
        raise NotImplementedError

    def clean(self):
        self._model[self._name] = self.default


class BuildinTypeField(Field):
    def __init__(self, convert_args=None, **kw):
        self.__convert_args = convert_args

        super(BuildinTypeField, self).__init__(**kw)

    @property
    def convert_args(self):
        return self.__convert_args


    def check(self, value):
        if value is not None:
            if not isinstance(value, self.datatype):
                try:
                    if self.convert_args:
                        return self.datatype(value, **self.convert_args)
                    return self.datatype(value)
                except:
                    raise FieldError('invalid check %s,need %s.' % (type(value), str(self.datatype),))

            else:
                return value

        else:
            return self.default


class BOField(Field):
    def __init__(self, **kw):
        datatype = kw.pop("datatype", '')
        if not issubclass(datatype, BOModel):
            raise FieldError('invalid check %s,need %s.' % (str(datatype), str(BOModel),))

        super(BOField, self).__init__(datatype=datatype, **kw)

    def check(self, value):
        if value is not None:
            if not isinstance(value, self.datatype):
                raise FieldError('invalid check %s,need %s.' % (type(value), str(self.datatype),))
            else:
                return value
        else:
            return self.default


class StringField(BuildinTypeField):
    def __init__(self, encoding='utf8', blank=False, **kw):
        self.__encoding = encoding
        self._init(encoding, blank, **kw)

    def _init(self, encoding, blank=False, **kw):
        default = kw.pop("default", '' if blank else None)
        super(StringField, self).__init__(default=default, datatype=str, **kw)

    @property
    def encoding(self):
        return self.__encoding

    def check(self, value):
        if value is not None:
            return safestr(safeunicode(value), encoding=self.encoding)
        else:
            return self.default


class UnicodeField(StringField):
    def _init(self, encoding, blank=False, **kw):
        default = kw.pop("default", u'' if blank else None)
        super(StringField, self).__init__(default=default, datatype=unicode, **kw)

    def check(self, value):
        if value is not None:
            return safeunicode(value, encoding=self.encoding)
        else:
            return self.default


class _BOList(list):
    def todict(self, ignore_null=False, ignore_default=False):
        return [l if not hasattr(l, 'todict') else l.todict(ignore_null=ignore_null, ignore_default=ignore_default) for
                l in self]


class _BODict(dict):
    def todict(self, ignore_null=False, ignore_default=False):
        return {k: v if not hasattr(v, 'todict') else v.todict(ignore_null=ignore_null, ignore_default=ignore_default) \
                for k, v in self.iteritems()}


class ListField(BuildinTypeField):
    def __init__(self, generictype=None, ruleout=True, **kw):
        default = kw.pop("default", [])
        self.__generictype = generictype
        self.__ruleout = ruleout
        super(ListField, self).__init__(default=default, datatype=_BOList, **kw)

    def check(self, value):
        value = super(ListField, self).check(value)
        if value:
            if self.__generictype and self.__ruleout:
                return _BOList([v for v in value if isinstance(v, self.__generictype)])
            else:
                return value


class DictField(BuildinTypeField):
    def __init__(self, generictype=None, ruleout=True, **kw):
        default = kw.pop("default", {})
        self.__generictype = generictype
        self.__ruleout = ruleout
        super(DictField, self).__init__(default=default, datatype=_BODict, **kw)

    def check(self, value):
        value = super(DictField, self).check(value)
        if value:
            if self.__generictype and self.__ruleout:

                return _BODict({k: v for k, v in value.iteritems() if isinstance(v, self.__generictype)})
            else:
                return value


class FloatField(BuildinTypeField):
    def __init__(self, **kw):
        default = kw.pop("default", 0.0)
        super(FloatField, self).__init__(default=default, datatype=float, **kw)


class IntegerField(BuildinTypeField):
    def __init__(self, **kw):
        default = kw.pop("default", 0)
        super(IntegerField, self).__init__(default=default, datatype=int, **kw)


class BoolField(BuildinTypeField):
    def __init__(self, **kw):
        default = kw.pop("default", False)
        super(BoolField, self).__init__(default=default, datatype=bool, **kw)

    def check(self, value):
        if isinstance(value, basestring):
            val = value.lower()
            if val in ('false', 'null', 'none', '0',):
                value = False

        super(BoolField, self).check(value)


class BOMetaclass(type):
    def __new__(mcs, name, bases, attrs):
        if name == 'BOModel':
            return type.__new__(mcs, name, bases, attrs)

        mappings = {}
        validator = []

        for base in bases:
            base_mappings = getattr(base, '__mappings__', {})
            mappings.update(base_mappings)

            base_validate = getattr(base, '__validator__', None)
            if base_validate:
                if isinstance(base_validate, list):
                    validator += base_validate
                else:
                    validator.append(base_validate)

        for k, v in attrs.iteritems():
            if isinstance(v, Field):
                mappings[k] = v

        [attrs.pop(k) for k in mappings.iterkeys() if k in attrs]

        attrs['__mappings__'] = mappings
        if attrs.get('__validator__', None):
            validator.append(attrs['__validator__'])
        else:
            attrs['__validator__'] = None
        attrs['__validator__'] = validator

        return type.__new__(mcs, name, bases, attrs)


class BOModel(dict):
    __metaclass__ = BOMetaclass

    def __init__(self, **kwargs):
        kw = {}
        for k, v in self.__mappings__.iteritems():

            if isinstance(v, Field):
                v._model = weakref.proxy(self)
                v._name = k
                if k in kwargs:
                    kw[k] = v.check(kwargs.pop(k))
                else:
                    kw[k] = v.check(v.default)

        kw.update(kwargs)

        super(BOModel, self).__init__(**kw)

    def clean_all(self):
        for k, v in self.__mappings__.iteritems():
            self[k] = v.check(v.default)

    def validate(self, quiet=False):
        errors = []

        def vald_(key, val):
            validator_method = None
            for valid in self.__validator__[::-1]:
                validator_method = getattr(valid, 'validate_%s' % key, None)
                if validator_method:
                    break
            try:
                validator_method and validator_method(self, self[key], val)
            except ValidateError as e:
                e.field = key
                if not quiet:
                    raise e
                else:
                    errors.append(e)

        for k, v in self.__mappings__.iteritems():
            if v.required and self[k] is None and v.default is None:
                require_error = RequiredError('"%s" is a required field.' % k)
                if quiet:
                    errors.append(require_error)
                else:
                    raise RequiredError('"%s" is a required field.' % k)
            if self.__validator__:
                vald_(k, v)

        return errors

    def __getattr__(self, key):
        try:
            if key.endswith('__field') and key.rstrip('__field') in self.__mappings__:
                return self.__mappings__.get(key.rstrip('__field'), None)

            return self[key]

        except KeyError:
            raise AttributeError(r"'BaseBO' object has no attribute '%s'" % key)

    def __set(self, key, value):
        if key in self.__mappings__:
            value = self.__mappings__[key].check(value)

        self[key] = value

    def __setattr__(self, key, value):
        self.__set(key, value)

    def __repr__(self):
        return '<%s ' % self.__class__.__name__ + dict.__repr__(self) + '>'

    def update(self, kwargs):
        if not kwargs: kwargs = {}
        for k, v in kwargs.iteritems():
            self.__set(k, v)

    def todict(self, exclude=None, include=None, ignore_null=False, ignore_default=False):
        if not exclude:
            exclude = []
        if not include:
            include = self.__mappings__.keys()

        def v_tolist_(k, field):
            v = getattr(self, k)
            if field.required and v is None and field.default is None:
                raise RequiredError('"%s" is a required field.' % k)

            if v:
                return v.todict(ignore_null=ignore_null, ignore_default=ignore_default) if hasattr(v, 'todict') else v
            else:
                return v

        def ignoreit_(k, field):
            val = getattr(self, k)
            if ignore_null:
                if val is None:
                    return True
            if ignore_default:
                if val == field.default:
                    return True

            return False

        if exclude:
            return {k: v_tolist_(k, v) for k, v in self.__mappings__.iteritems()
                    if k not in exclude and not ignoreit_(k, v)}
        else:
            return {k: v_tolist_(k, v) for k, v in self.__mappings__.iteritems()
                    if k in include and not ignoreit_(k, v)}

    def dumps(self, dicts=None, exclude=None, include=None, **kwargs):
        dict = dicts or self.todict(exclude=exclude, include=include)
        return json.dumps(dict, **kwargs)

    @classmethod
    def parse_list(cls, lists, exclude=None, include=None, ignore_null=False, ignore_default=False):
        if not lists: lists = []

        def _(l):
            if hasattr(l, 'todict'):
                return l.todict(exclude=exclude, include=include, ignore_null=ignore_null,
                                ignore_default=ignore_default)
            else:
                return l

        return [_(l) for l in lists]


    @classmethod
    def parse_dict(cls, dicts, ignore_null=False, ignore_default=False):
        if not dicts: dicts = {}

        def _(l):
            if hasattr(l, 'todict'):
                return l.todict(ignore_null=ignore_null,
                                ignore_default=ignore_default)
            else:
                return l

        return {k: _(obj) for k, obj in dicts.iteritems()}
