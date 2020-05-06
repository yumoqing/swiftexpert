from swiftexpert.swift_field import SwiftXXField, SwiftXXXField

"""
x = SwiftXXField(tag='35B',name="intermediary",formatstr="[ISIN1!e12!c]\r\n[4*35x]")
x.setTextData(":56A:/Q\r\nI\r\n")
txt = x.unpack()
print(x.innerData,txt)

d = ":35B:ISIN US3135G0BA00\r\nBONDFNMA-NEW 2.375\r\n11APR16/0D/2016/04/11/2.375PCT\r\n:16R:FIA"
x = SwiftXXField(tag='35B',name="intermediary",formatstr="[ISIN1!e12!c]\r\n[4*35x]")
x.setTextData(d)
txt = x.unpack()
print(x.innerData,txt)
"""
d = "{108:02019050800001150}"
x = SwiftXXXField(tag='108',name="intermediary",formatstr="24c")
x.setTextData(d)
txt = x.unpack()
print(x.innerData,txt)
