python中slot使用
===

1. 说明

python新模式的类,有一个变量是__slots__,slots的作用是阻止在实例化时为实例分配dict,默认情况下每个类都会有一个dict, 
通过__dict__访问,这个__dict__维护了这个实例的所有属性。 

