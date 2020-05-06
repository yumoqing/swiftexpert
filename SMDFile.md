# SWIFT消息描述文件(SMDF)使用指南

## 对象类型

在SWIFTEXPERT中,使用以下对象类型:

* 'message'代表一个SWIFT报文对象

* 'block'代表报文对象中的一个报文块

* 'segment'代表报文段对象

* '99field'代表标签值在10-99之间的报文域对象

* '999field'代表标签值100以上的报文域对象

* 'endblock'代表报文块对象描述结束

* 'endsegment'代表报文段对象结束

## SMDF 文件规则

* 每行从A列开始,A列填写字段类型

* 'block'和'endblock'必须成对出现，'block'在前，

* 'segment'和'endsegment'必须成对出现，并且必须在'block’和'endblock’之间出现

* 不是以对象类型开始的行会被忽略

* 


