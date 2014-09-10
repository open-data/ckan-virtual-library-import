#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import codecs
from lxml import etree
import re
import time

f = codecs.open("../data/monographs-monographies.xml", "r", "utf-8")
#f = codecs.open("../data/periodicals-periodiques.xml", "r", "utf-8")
#f = codecs.open("../data/series-series.xml", "r", "utf-8")

#file = open(fname)
#filecontents = file.read()
#filecontents = filecontents.decode("utf-8")

root = etree.fromstring(f.read())
#root = etree.parse("data/AMICUS_sample_128.xml")

iso_time = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())
print "======================================================================"
print "= PWGSC :: Sample metadata :: "+iso_time+" ===================="
print "======================================================================"
print "==== (M)   Mandatory ================================================="
print "==== (M/a) Mandatory if Applicable ==================================="
print "==== (O)   Optional==================================================="
print "==== (M-C) Mandatory, CKAN generated ================================="
print "======================================================================"

for record in root.xpath("/rdf:RDF/rdf:Description", namespaces={'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'}):

	MES_1_metadata_identifier 	   = '(M-C) ERROR MES element 1'
	MES_2_title 				   = ['(M) ERROR MES element 2']
	MES_3_GC_Department_or_Agency  = ['(M) ERROR MES element 3']
	MES_4_author                   = ['(M/a) CONFIRM MES element 4']
	MES_5_description              = '(M/a) CONFIRM MES element 5'
	MES_6_subject                  = ['(M) ERROR MES element 6']
	MES_7_keywords                 = ['(O) ERROR MES element 7']
	MES_8_date_resource_published  = '(M) ERROR MES element 8'
	MES_9_date_contributed         = '(M-C) ERROR MES element 9'
	MES_10_modification_Date       = '(M/a) CONFIRM MES element 10'
	MES_11_data_resource_created   = '(M/a) CONFIRM MES element 11'
	MES_12_ISBN                    = ['(M/a) CONFIRM MES element 12']
	MES_13_ISSN                    = ['(M/a) CONFIRM MES element 13']
	MES_14_gc_catalogue_number     = '(M/a) CONFIRM MES element 14'
	MES_15_dept_catalogue_number   = '(M/a) CONFIRM MES element 15'
	MES_16_weekly_checklist_number = '(M/a) CONFIRM MES element 16'
	MES_17_file_code               = '(O) BLANK MES element 17'
	MES_18_gc_docs_number          = '(M/a) CONFIRM MES element 18'
	MES_19_LAC_identifier          = '(M/a) CONFIRM MES element 19'
	MES_20_amicus_identifier       = '(M/a) CONFIRM MES element 20'
	MES_21_PWGSC_identifier        = '(M/a) CONFIRM MES element 21'
	MES_22_DOI                     = ['(O) BLANK MES element 22']
	MES_23_series_title            = ['(M/a) CONFIRM MES element 23']
	MES_24_series_number           = ['(M/a) CONFIRM MES element 24']
	MES_25_frequency_of_serial     = '(M/a) CONFIRM MES element 25'
	MES_26_former_frequency        = ['(M/a) CONFIRM MES element 26']
	MES_27_num_and_chrono_des      = ['(M/a) CONFIRM MES element 27']
	MES_28_file_type               = '(M/a) CONFIRM MES element 28'
	MES_29_language                = ['(M) ERROR MES element 29']
	MES_30_language_other          = ['(M/a) CONFIRM MES element 30']
	MES_31_type                    = ['(M) ERROR MES element 31']
	MES_32_format                  = ['(M-C) ERROR MES element 32']
	MES_33_size                    = ['(O) BLANK MES element 33']
	MES_34_number_of_pages         = ['(M/a) CONFIRM MES element 34']
	MES_35_access_url              = ['(M) ERROR MES element 35']
	MES_36_licence                 = '(M-C) ERROR MES element 36'

## MES 1
	# Can't move forward with 'NA'

## MES 2
	r = record.xpath("dc:title[@xml:lang='en']", namespaces=record.nsmap)
	if(len(r)):
		MES_2_title = []
		for title in r:
			MES_2_title.append(title.text.strip())

## MES 3
	r = record.xpath("dc:creator[@xml:lang='en']", namespaces=record.nsmap)
	#r = record.xpath("name[@type='corporate']/namePart")
	if(len(r)):
		MES_3_GC_Department_or_Agency = []
		for namePart in r:
			MES_3_GC_Department_or_Agency.append(namePart.text.strip())
#	r = record.xpath("dc:creator[@xml:lang='fr']", namespaces=record.nsmap)
#	#r = record.xpath("name[@type='corporate']/namePart")
#	if(len(r)):
#		MES_3_GC_Department_or_Agency[0] == '(M) ERROR MES element 3'
#		for namePart in r:
#			MES_3_GC_Department_or_Agency.append('fr:'+namePart.text.strip())

## MES 4
	# NA

## MES 5
#	r = record.xpath("dc:description[@xml:lang='en']", namespaces=record.nsmap)
#	if(len(r)):
#		bits = []
#		for title in r:
#			bits.append(title.text.strip())
#		MES_5_description = "\n".join(bits)

## MES 6
	r = record.xpath("dc:subject[@xml:lang='en']", namespaces=record.nsmap)
	#r = record.xpath("name[@type='corporate']/namePart")
	if(len(r)):
		MES_6_subject = []
		for namePart in r:
			MES_6_subject.append(namePart.text.strip())

## MES 7
	# NA

## MES 8
	r = record.xpath("dc:date", namespaces=record.nsmap)
	if(len(r)):
		MES_8_date_resource_published = r[0].text.strip()

## MES 9
	# CKAN Produced

## MES 10
	# NA

## MES 11
	# NA

## MES 12
	r = record.xpath("dc:identifier", namespaces=record.nsmap)
	#r = record.xpath("name[@type='corporate']/namePart")
	if(len(r)):
		for isbn in r:
			isbn_bits = isbn.text.strip().split(' ')
			if(isbn_bits[0] == '{ISBN}'):
				if(MES_12_ISBN[0] == '(M/a) CONFIRM MES element 12'):
					MES_12_ISBN = []
				MES_12_ISBN.append(isbn_bits[1].strip())

## MES 13
	r = record.xpath("dc:identifier", namespaces=record.nsmap)
	#r = record.xpath("name[@type='corporate']/namePart")
	if(len(r)):
		for issn in r:
			issn_bits = issn.text.strip().split(' ')
			if(issn_bits[0] == '{ISSN}'):
				if(MES_13_ISSN[0] == '(M/a) CONFIRM MES element 13'):
					MES_13_ISSN = []
				MES_13_ISSN.append(issn_bits[1].strip())

## MES 14
	r = record.xpath("dc:identifier[@xml:lang='en']", namespaces=record.nsmap)
	if(len(r)):
		for cn in r:
			cn_bits = cn.text.strip().split(' ')
			if(cn_bits[0] == '{Catalogue' and cn_bits[1] == 'Number}'):
				MES_14_gc_catalogue_number = cn_bits[2].strip()
#	r = record.xpath("dc:identifier[@xml:lang='fr']", namespaces=record.nsmap)
#	if(len(r)):
#		for cn in r:
#			cn_bits = cn.text.strip().split(' ')
#			if(cn_bits[0].encode('utf-8') == '{Numéro' and cn_bits[1].encode('utf-8') == 'de' and cn_bits[2].encode('utf-8') == 'catalogue}'):
#				if(MES_14_gc_catalogue_number == '(M/a) CONFIRM MES element 14'):
#					MES_14_gc_catalogue_number = ''
#				MES_14_gc_catalogue_number += "\nfr:"+cn_bits[3].strip()

## MES 15
#	r = record.xpath("dc:identifier[@xml:lang='en']", namespaces=record.nsmap)
#	if(len(r)):
#		for cn in r:
#			cn_bits = cn.text.strip().split(' ')
#			if(cn_bits[0] == '{Catalogue' and cn_bits[1] == 'Number}'):
#				MES_14_gc_catalogue_number = 'en:'+cn_bits[2].strip()

	r = record.xpath("dc:identifier[@xml:lang='en']", namespaces=record.nsmap)
	if(len(r)):
		if(re.match('{Departmental ID (en)}', title.text.strip()) or re.match('{Departmental ID (fr)}', title.text.strip()) or re.match('{ID ministérielle (en)}', title.text.strip()) or re.match('{ID ministérielle (fr)}', title.text.strip())):
			MES_15_dept_catalogue_number = r[0].text.strip()

#<dc:identifier xml:lang=""en"">{Departmental ID (en)}
#<dc:identifier xml:lang=""fr"">{ID ministérielle (en)}
#<dc:identifier xml:lang=""en"">{Departmental ID (fr)}
#<dc:identifier xml:lang=""fr"">{ID ministérielle (fr)}

## MES 16
	# NA

## MES 17
#	d = dict(record.attrib)
#	for a,b in sorted(d.items()):
#		if(a == '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about'):
#			MES_17_file_code = b

## MES 18
	# N/A

## MES 19
	# Not required "LAC"

## MES 20
	# Not required "LAC"


## MES 21

	r = record.xpath("dc:identifier[@xml:lang='en']", namespaces=record.nsmap)
	if(len(r)):
		for cn in r:
			cn_bits = cn.text.strip().split(' ')
			if(cn_bits[0] == '{System' and cn_bits[1] == 'ID}'):
				MES_21_PWGSC_identifier = cn_bits[2].strip()
#	r = record.xpath("dc:identifier[@xml:lang='fr']", namespaces=record.nsmap)
#	if(len(r)):
#		for cn in r:
#			cn_bits = cn.text.strip().split(' ')
#			if(cn_bits[0].encode('utf-8') == '{ID' and cn_bits[1].encode('utf-8') == 'système}'):
#				if(MES_21_PWGSC_identifier == '(M/a) CONFIRM MES element 21'):
#					MES_21_PWGSC_identifier = ''
#				MES_21_PWGSC_identifier += "\nfr:"+cn_bits[2].strip()

## MES 22
	# DOI N/A

## MES 23

	r = record.xpath("dc:description[@xml:lang='en']", namespaces=record.nsmap)
	if(len(r)):
		for cn in r:
			cn_bits = cn.text.strip().split(' ')
			if(len(cn_bits) > 2):
				if(cn_bits[0] == '{Series' and cn_bits[1] == 'title}'):
					if(MES_23_series_title[0] == '(M/a) CONFIRM MES element 23'):
						MES_23_series_title = []
					MES_23_series_title.append((' '.join(cn_bits[2:])).strip())

# MES 24

	r = record.xpath("dc:description[@xml:lang='en']", namespaces=record.nsmap)
	if(len(r)):
		for cn in r:
			cn_bits = cn.text.strip().split(' ')
			if(cn_bits[0] == '{Issue}'):
				if(MES_24_series_number[0] == '(M/a) CONFIRM MES element 24'):
					MES_24_series_number = []
				MES_24_series_number.append((' '.join(cn_bits[1:])).strip())

## MES 25
	# NA

## MES 26
	# NA

## MES 27

	r = record.xpath("dc:description[@xml:lang='en']", namespaces=record.nsmap)
	if(len(r)):
		for cn in r:
			cn_bits = cn.text.strip().split(' ')
			if(cn_bits[0] == '{Issue}'):
				if(MES_27_num_and_chrono_des[0] == '(M/a) CONFIRM MES element 27'):
					MES_27_num_and_chrono_des = []
				MES_27_num_and_chrono_des.append((' '.join(cn_bits[1:])).strip())

## MES 28
	r = record.xpath("dc:format", namespaces=record.nsmap)
	if(len(r)):
		MES_28_file_type = r[0].text.strip()

## MES 29
# NO SAFE WAY TO ADAPT TO NON OFFICIAL LANGUAGES

	r = record.xpath("dc:language[@xml:lang='en']", namespaces=record.nsmap)
	#r = record.xpath("name[@type='corporate']/namePart")
	if(len(r)):
		MES_29_language = []
		for namePart in r:
			if(namePart.text.strip() == 'English' or namePart.text.strip() == 'english'):
				MES_29_language.append('eng')
			else:
				MES_29_language.append('fra')

## MES 30

	r = record.xpath("dc:relation[@xml:lang='en']", namespaces=record.nsmap)
	if(len(r)):
		for cn in r:
			cn_bits = cn.text.strip().split(' ')
			if(cn_bits[0].encode('utf-8') == '{Other' and cn_bits[1].encode('utf-8') == 'Language' and cn_bits[2].encode('utf-8') == 'Edition}'):
				MES_30_language_other = []
				MES_30_language_other.append(cn_bits[3].strip())

## MES 31
#
#	r = record.xpath("dc:type[@xml:lang='en']", namespaces=record.nsmap)
#	if(len(r)):
#		MES_31_type = []
#		for cn in r:
#			MES_31_type.append(cn.text.strip())
#	r = record.xpath("dc:type[@xml:lang='fr']", namespaces=record.nsmap)
#	if(len(r)):
#		if(MES_31_type[0] == '(M) ERROR MES element 31'):
#			MES_31_type = []
#		for cn in r:
#			MES_31_type.append(cn.text.strip())

## MES 32

	r = record.xpath("dc:format", namespaces=record.nsmap)
	if(len(r)):
		MES_32_format = []
		for cn in r:
			MES_32_format.append(cn.text.strip())

## MES 33
	# NA 

## MES 34
#
#	r = record.xpath("dc:description[@xml:lang='en']", namespaces=record.nsmap)
#	if(len(r)):
#		bits = []
#		for title in r:
#			if(re.match('^[0-9]+p.', title.text.strip())):
#				bits.append(title.text.strip())
#		if(len(bits)):
#			MES_34_number_of_pages = bits
## MES 35

	r = record.xpath("dc:identifier", namespaces=record.nsmap)
	#r = record.xpath("name[@type='corporate']/namePart")
	if(len(r)):
		for url in r:
			url_bits = url.text.strip().split(' ')
			if(url_bits[0] == '{URL}'):
				if(MES_35_access_url[0] == '(M) ERROR MES element 35'):
					MES_35_access_url = []
				MES_35_access_url.append(url_bits[1].strip())

#
#	## Uncomment to display missing Canadiana numbers
#	#if(MES_1_metadata_identifier == 'ERROR MES element 1'):
#	#	print MES_1_metadata_identifier+"\n"+MES_2_title+"\n\n"
#
#	## Uncomment to only display valid Canadiana numbers quoted to show spacing
#	#if(MES_1_metadata_identifier != 'ERROR MES element 1'):
#	#	print '"'+MES_1_metadata_identifier+'"'#+"\n"+MES_2_title+"\n\n"
#
#	#if MES_6_subject[0] != 'ERROR MES element 6':
#	#	continue
#

	print "ID                    ::"+MES_1_metadata_identifier
	print "TITLE                 ::"+("\nTITLE                 ::".join(MES_2_title))
	print "GCDEP                 ::"+("\nGCDEP                 ::".join(MES_3_GC_Department_or_Agency))
	print "AUTHOR                ::"+("\nAUTHOR                ::".join(MES_4_author))
	print "DESC                  ::"+MES_5_description
	print "SUBJECT               ::"+("\nSUBJECT               ::".join(MES_6_subject))
	print "KEYWORDS              ::"+("\nKEYWORDS              ::".join(MES_7_keywords))
	print "D PUBLISHED           ::"+MES_8_date_resource_published
	print "D CONTRIB             ::"+MES_9_date_contributed
	print "D MODIFIED            ::"+MES_10_modification_Date
	print "D CREATED             ::"+MES_11_data_resource_created
	print "ISBN                  ::"+("\ISBN                   ::".join(MES_12_ISBN))
	print "ISSN                  ::"+("\ISSN                   ::".join(MES_13_ISSN))
	print "GC CATALOGUE NO       ::"+MES_14_gc_catalogue_number
	print "DEPT. CATALOGUE NO    ::"+MES_15_dept_catalogue_number
	print "WEEK CHECKLIST NO     ::"+MES_16_weekly_checklist_number
	print "FILE CODE             ::"+MES_17_file_code
	print "GC DOCS NO            ::"+MES_18_gc_docs_number
	print "LAC_IDENT             ::"+MES_19_LAC_identifier
	print "AMICUS NO             ::"+MES_20_amicus_identifier
	print "CATALOGUE SYSTEM NO   ::"+MES_21_PWGSC_identifier
	print "DOI                   ::"+("\nDOI                   ::".join(MES_22_DOI))
	print "Series Title          ::"+("\nSeries Title          ::".join(MES_23_series_title))
	print "Series Number         ::"+("\nSeries Number         ::".join(MES_24_series_number))
	print "FREQUENCY             ::"+MES_25_frequency_of_serial
	print "FORMER FREQUENCY      ::"+("\nFORMER FREQUENCY      ::".join(MES_26_former_frequency))
	print "NUM & CHRONO          ::"+("\nNUM & CHRONO          ::".join(MES_27_num_and_chrono_des))
	print "FILETYPE              ::"+MES_28_file_type
	print "LANGUAGE              ::"+("\nLANGUAGE              ::".join(MES_29_language))
	print "OTHER LANGUAGE        ::"+("\nOTHER LANGUAGE        ::".join(MES_30_language_other))
	print "TYPE                  ::"+("\nTYPE                  ::".join(MES_31_type))
	print "FORMAT                ::"+("\nFORMAT                ::".join(MES_32_format))
	print "SIZE                  ::"+("\SIZE                   ::".join(MES_33_size))
	print "PAGES                 ::"+("\nPAGES                 ::".join(MES_34_number_of_pages))
	print "ACCESS URL            ::"+("\nACCESS URL            ::".join(MES_35_access_url))
	print "LICENSE               ::"+MES_36_licence

	print "======================================================================"
