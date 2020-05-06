# SWIFT

swift is a module to support swift message pack and unpack, with data validator.

## Standard support

Support SWIFT Message standard MT 2018

## Features

* Using excel file to description a swift message 

* Build the swift message object with the excel description file

* Using swift message object to pack a json data to swift message text

* Using swift message object to unpack a swift message text to json data

* Report pack and(or) unpack error when error happened

## swift message description file

### swift message structure

|--block

--|--composeddata ( block 1,2)

--|--field ( block 3, 5)

--|--segment(block 4)

-----|--segment

-----|--field

--------|--composeddata

--------|--xordata


Swift messages is composed by five blocks, 

### Swift message description file(SMDF)

We use a formated excel as SMDF file. it is easy to create and modify.

each message identified by message type, can be description by a SMDF excel file.

perfessionals of swift message can using the SMDF to define the message, Swift

###
