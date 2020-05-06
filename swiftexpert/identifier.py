from appPublic.dictObject import DictObject

"""
Option A 	[/1!a][/34x]
4!a2!a2!c[3!c] 	(Party Identifier)
(Identifier Code)
Option J 	5*40x 	(Party Identification)
"""
fund_beneficiary_customer_method = {
	"A":["[/1!a][/34x]\r\n4!a2!a2!c[3!c]",["code","identifier","","bank","country","location","branch"]],
	"J":["5*40x",["party_identification"]],
}

identifier_method = {
	"":["[/34x]\r\n4*35x",["account","","name_address"]],
	"A":["[/1a][/34x]\r\n4!a2!a2!c[3!c]",["","identifier","","bank","country","location","branch"]],
	"B":["[/1a][/34x]\r\n[35x]",["one","identifier","","location"]],
	"C":["/34x",["","account"]],
	"D":["[/1a][/34x]\r\n4*35x",["one","identifier","","name_address"]],
	"F":["[35x]\r\n4*35x",["identifier","","name_address"]],
	"G":["/34x\r\n4!a2!a2!c[3!c]",["","account","","bank","country","location","branch"]],
	"H":["/34x\r\n4*35x",["","account","name_address"]],
	"J":["5*40x",["narrative"]],
	"K":["[/34x]\r\n4*35x",["account","","name_address"]],
	"L":["35x", ["narrative"]],
	"P":[":4!c//4!a2!a2!c[3!c]", ["","qualifier","","bank","country","location","branch"]],
	"Q":[":4!c//4*35x", ["","qualifier","","name_address" ]],
	"R":[":4!c/8c/34x", ["","qualifier","","dss","","proproetary_code"]],
	"S":[":4!c/[8c]/4!c/2!a/30x", ["","qualifier","dss","","id_type","","country","","alternate_id"]],
	"T":[":4!c//2*35x", [ "","qualifier","","name"]],
	"U":[":4!c//3*35x", ["","qualifier","name"]],
}

payment_method = {
	"A":["6!n3!a15d",["date","currency","amount"]],
	"B":["3!a15d",["currency","amount"]],
	"P":["6!n3!a15d",["date","currency","amount"]],
	"R":["6!n3!a15d",["date","currency","amount"]],
}

date_method = {
	"A":[":4!c//8!n",['','qualifier','','date']],
	"B":[":4!c/[8c]/4!c",['','qualifier','','dss','','date_code']],
	"C":[":4!c//8!n6!n",['','qualifier','','date','time']],
	"E":[":4!c//8!n6!n[,3n]\r\n[/[N]2!n[2!n]]",['','qualifier','','date','time','','decimal','','utc_indictor']],
	"F":["8!n",["date"]],
	"J":["1!a3!n",["code","days"]],
}

currency_method = {
	"R":["3!a",["currency"]],
	"S":["3!a",["currency"]],
}

numberIdentification_method = {
	"A":[":4!c//3!c",["","qualifier","","num_id" ]],
	"B":[":4!c/[8c]/30x",["","qualifier","","dss","","number"]],
	"J":[":4!c//5!c",["","qualifier","","extended_number_id"]],
	"K":[":4!c//3!c/15d",["","qualifier","","number_id","","quantity"]],
}

price_method = {
	"A":[":4!c//4!c/[N]15d",["","qualifier","","percentage_type_code","","sign","price"]],
	"B":[":4!c//4!c/3!a15d",["","qualifier","","amount_type_code","","currency_code","price"]],
	"E":[":4!c//4!c",["","qualifier","","proce_code"]],
}

place_method = {
	"B":[":4!c/[8c]/4!c[/30x]",["","qualifier","","dss","","place_code","","narrative"]],
	"C":[":4!c//2!a",["","qualifier","","country" ]],
	"D":[":4!c//[2!a]/35x",["","qualifier","","country","","place" ]],
	"F":[":4!c//4!c/4!a2!a2!c[3!c]",["","qualifier","","place_code","",
				"bank","country","location","branch"]],
	"H":[":4!c//4!a2!a2!c[3!c]",["","qualifier","bank","country","location","branch"]],
	"L":[":4!c//18!c2!n",["","qualifier","","legal_entity_identifier","x"]],
}

indicator_method = {
	"F":[":4!c/[8c]/4!c",["","qualifier","","dss","indicator"]],
	"H":[":4!c//4!c",["","qualifier","","indicator"]],
}

account_method = {
	"A":[":4!c//35x",["","qualifier","","account_number"]],
	"B":[":4!c/[8c]/4!c/35x",["","qualifier","","dss","",
			"account_type_code","","account_number"]],
	"E":[":4!c//34x",["","qualifier","","ib_account_number"]],
}

narrative_method = {
	"C":[":4!c//4*35x",["","qualifier","","narrative"]],
	"D":[":4!c//6*35x",["","qualifier","","narrative"]],
	"E":[":4!c//10*35x",["","qualifier","","narrative"]],
}

financialInstrumentType_method = {
	"A":[":4!c/[8c]/30x",["","qualifier","","dss","","instrument_code"]],
	"B":[":4!c/[8c]/4!c",["","qualifier","","dss","","instrument_code"]],
	"C":[":4!c//6!c",["","qualifier","","cfi_code"]],
}

rate_method = {
	"A":[":4!c//[N]15d",["","qualifier","","sign","rate"]],
	"C":[":4!c/[8c]/24x",["","qualifier","","dss","","rate_name"]]
}

"""
balance:
Option B 	:4!c/[8c]/4!c/[N]15d 	(Qualifier)(Data Source Scheme)(Quantity Type Code)(Sign)(Balance)
Option C 	:4!c//4!c/4!c/[N]15d 	(Qualifier)(Quantity Type Code)(Balance Type Code)(Sign)(Balance)
"""
balance_method = {
	"B":[":4!c/[8c]/4!c/[N]15d",["","qualifier","","dss","","quantity_type_code","","sign","balance"]],
	"C":[":4!c/4!c/4!c/[N]15d",["","qualifier","","quantity_type_code","","balance_type_code","","sign","balance"]],
}
reference_method = {
	"C":["4!c//16x",["qualifier","","reference"]],
	"U":["4!c//52x",["qualifier","","reference"]],
}

tag_methods={
	"11a":currency_method,
	"12a":financialInstrumentType_method,
	"13a":numberIdentification_method,
	"20a":reference_method,
	"22a":indicator_method,
	"30a":date_method,
	"32a":payment_method,
	"33a":payment_method,
	"34a":payment_method,
	"42a":identifier_method,
	"50a":identifier_method,
	"51a":identifier_method,
	"52a":identifier_method,
	"53a":identifier_method,
	"54a":identifier_method,
	"55a":identifier_method,
	"56a":identifier_method,
	"57a":identifier_method,
	"58a":identifier_method,
	"59a":identifier_method,
	"70a":narrative_method,
	"81a":identifier_method,
	"82a":identifier_method,
	"83a":fund_beneficiary_customer_method,
	"84a":identifier_method,
	"85a":identifier_method,
	"86a":identifier_method,
	"87a":identifier_method,
	"88a":identifier_method,
	"89a":identifier_method,
	"90a":price_method,
	"91a":identifier_method,
	"92a":rate_method,
	"93a":balance_method,
	"94a":place_method,
	"95a":identifier_method,
	"96a":identifier_method,
	"97a":account_method,
	"98a":date_method,
}

def tag_xor(tag,opts,pack_name=""):
	fmtdic={}
	method = tag_methods.get(tag,None)
	if method is None:
		raise Exception("tag(%s) has not methods" % tag)
	keys=[i for i in opts if i<='Z' and i>='A'] 
	# print(opts,'-----keys=',keys,'----')
	keys = [i if i in method.keys() else '' for i in keys ]
	# print('-----keys=',keys,'----')
	[fmtdic.update({i:method.get(i)}) for i in keys ]
	d = DictObject(name="party",
		object="xor",
		kwargs=DictObject(
			name="party_n",
			fmtdic=fmtdic
		)
	)
	return d
