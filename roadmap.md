# Roadmap for swiftexport

## Data check rule description file

Using excel file as data check rule description file

Each check rule has a logical express with composed by a lot of atom check functions, and a error code


### Data position rule

Error check will be executed on the data user provided, we provide a object position rule to get the data we need to check.

### Atom check function

ACF on message, block, segment, 99field, 999field, it performs the base check on a object of message, block, segment, 99field, 999field.  the ACF will return True or False

### Logical express

The Logical express composed by ACF and 'and', 'or', '(',')'

## web app to arrow user to upload

## online swift message unpack

## online swift message pack


