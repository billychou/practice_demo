#!/usr/bin/env python


class ObjectCreator(object):
    pass


class Foo(object):
    bar = 'bip'


class Bar(object):
    pass


class UpperAttrMeta(type):
    def __new__(upperattr_metaclass, future_class_name,
                future_class_parents, future_class_attr):
        attrs = ((name, value) for name,value in future_class_attr.items() if not name.startswith('__'))
        uppercase_attr = dict((name.upper(), value) for name, value in attrs)
        return type(future_class_name, future_class_parents, uppercase_attr )


def choose_class(name):
    if name == 'foo':
        class Foo(object):
            pass
        return Foo
    else:
        class Bar(object):
            pass
        return Bar


def upper_attr(future_class_name, future_class_parents, future_class_attr):
    attrs = ((name, value) for name, value in future_class_attr.items()
            if not name.startswith('__'))
    uppercase_attr = dict((name.upper(), value) for name,value in attrs)
    return type(future_class_name, future_class_parents, uppercase_attr)

__metaclass__ = upper_attr

def echo(o):
    print(o)

if __name__ == "__main__":
    my_object = ObjectCreator()
    print(my_object)
    echo(ObjectCreator)
    ObjectCreator.new_attribute = 'foo'
    if hasattr(ObjectCreator, 'new_attribute'):
        print(True)
    else:
        print(False)
    ObjectCreatorMirror = ObjectCreator
    print(ObjectCreatorMirror())
    dir(ObjectCreator)

    myclass = choose_class('foo')
    print("myclass:", myclass)
    barclass = choose_class("bar")
    print("barclass", barclass)