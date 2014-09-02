#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import codecs
from lxml import etree
import re
import time

f = codecs.open("../data/AMICUS_sample_128.xml", "r", "utf-8")

#file = open(fname)
#filecontents = file.read()
#filecontents = filecontents.decode("utf-8")

root = etree.fromstring(f.read())
#root = etree.parse("data/AMICUS_sample_128.xml")

iso_time = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())
print "======================================================================"
print "= LAC :: Sample metadata :: "+iso_time+" ======================"
print "======================================================================"
print "==== (M)   Mandatory ================================================="
print "==== (M/a) Mandatory if Applicable ==================================="
print "==== (O)   Optional==================================================="
print "==== (M-C) Mandatory, CKAN generated ================================="
print "======================================================================"

for record in root.iter('record'):

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

# MES 1
	r = record.xpath("identifier[@type='canadiana']")
	if(len(r)):
		MES_1_metadata_identifier = r[0].text.strip()

# MES 2
	r = record.xpath("titleInfo[not(@type)]/title")
	if(len(r)):
		MES_2_title = []
		for title in r:
			MES_2_title.append(title.text.strip())

# MES 3
	r = record.xpath("name[@type='corporate']/namePart")
	if(len(r)):
		MES_3_GC_Department_or_Agency = []
		for namePart in r:
			MES_3_GC_Department_or_Agency.append(namePart.text.strip())

# MES 4
	r = record.xpath("name[@type='corporate']/namePart")
	if(len(r)):
		MES_4_author = []
		for namePart in r:
			MES_4_author.append(namePart.text.strip())
	r = record.xpath("name[@type='personal']/namePart")
	if(len(r)):
		MES_4_author[0] == '(M/a) CONFIRM MES element 4'
		for namePart in r:
			MES_4_author.append(namePart.text.strip())

# MES 5
	r = record.xpath("note[@type='Physical Description']")
	if(len(r)):
		MES_5_description = r[0].text.strip()
	# patterm match # r = record.xpath("note[starts-with(@type,'Local Note - ')]")
	r = record.xpath("note[@type='Local note - English summary']")
	if(len(r)):
		if( MES_5_description == '(M/a) CONFIRM MES element 5' ):
			MES_5_description = ''
		for name, value in sorted(r[0].items()):
			MES_5_description += "\n"+value

# MES 6
	rvm  = []
	lcsh = []
	csh  = []
	r = record.xpath("subject[@authority='rvm']/topic")
	if(len(r)):
		for subject in r:
			rvm.append(subject.text.strip())
	r = record.xpath("subject[@authority='lcsh']/topic")
	if(len(r)):
		for subject in r:
			lcsh.append(subject.text.strip())
	r = record.xpath("subject[@authority='csh']/topic")
	if(len(r)):
		for subject in r:
			csh.append(subject.text.strip())

	if(len(rvm) or len(lcsh) or len(csh)):
		MES_6_subject = []
		MES_6_subject.extend(rvm)
		MES_6_subject.extend(lcsh)
		MES_6_subject.extend(csh)

# MES 7
	# MISSING IN THE LAC MAPPING

# MES 8
	bits = []
	r = record.xpath("originInfo/dateIssued[@encoding='marc']")
	if(len(r)):
		bits.append("monograph:"+r[0].text.strip())
	r = record.xpath("extension/searchDate[@point='start']")
	if(len(r)):
		bits.append("serial-start:"+r[0].text.strip())
	r = record.xpath("extension/searchDate[@point='end']")
	if(len(r)):
		bits.append("serial-end:"+r[0].text.strip())

	if(len(bits)):
		MES_8_date_resource_published = ','.join(bits)

# MES 9
	# CKAN Produced

# MES 10
	r = record.xpath("recordInformation/recordCreationDate[@encoding='marc']")
	if(len(r)):
		yymmdd_datestring = r[0].text.strip()
		yy = yymmdd_datestring[:2]
		if(yy > 15):
			yy = '19'+yy
		else:
			yy = '20'+yy
		MES_10_modification_Date = yy+'-'+yymmdd_datestring[2:-2]+'-'+yymmdd_datestring[-2:]
	r = record.xpath("recordInformation/recordChangeDate[@encoding='iso8601']")
	if(len(r)):
		yymmdd_datestring = r[0].text.strip()
		MES_10_modification_Date = yymmdd_datestring[:4]+'-'+yymmdd_datestring[4:6]+'-'+yymmdd_datestring[6:8]

# MES 11
	# NOT AVAILABLE FROM LAC

# MES 12
	r = record.xpath("identifier[@type='isbn']")
	if(len(r)):
		MES_12_ISBN = []
		for title in r:
			MES_12_ISBN.append(title.text.strip())

# MES 13
	r = record.xpath("identifier[@type='issn']")
	if(len(r)):
		MES_13_ISSN = []
		for title in r:
			MES_13_ISSN.append(title.text.strip())

# MES 14
	r = record.xpath("identifier[@type='govt']")
	if(len(r)):
		MES_14_gc_catalogue_number = r[0].text.strip()

# MES 15
	# LAC does not record

# MES 16
	r = record.xpath("note[@type='General Note']")
	if(len(r)):
		MES_16_weekly_checklist_number = r[0].text.strip()
	
# MES 17
	# GC DOCS N/A
# MES 18
	# Docs Number N/A

# MES 19
	MES_19_LAC_identifier = MES_1_metadata_identifier

# MES 20
	r = record.xpath("recordInformation/recordIdentifier[@userView='1']")
	if(len(r)):
		MES_20_amicus_identifier = r[0].text.strip()

# MES 21
	# PWGSC Identifier N/A
# MES 22
	# DOI N/A

# MES 23 & 24
	r = record.xpath("titleInfo[@type='series']/title")
	if(len(r)):
		for title in r:
			MES_23_series_title.append(title.text.strip())
	r = record.xpath("note[@type='Series Traced in 8XX']")
	if(len(r)):
		for title in r:
			#print "::"+title.text.strip()
			title_no = title.text.strip().split(';')
			MES_23_series_title.append(title_no[0].strip())
			if(len(title_no) > 1):
				MES_24_series_number.append(title_no[1].strip())

# MES 25
	r = record.xpath("note[@type='Current Publication Frequency']")
	if(len(r)):
		MES_25_frequency_of_serial = r[0].text.strip()

# MES 26
	r = record.xpath("note[@type='Former Frequency']")
	if(len(r)):
		for title in r:
			MES_26_former_frequency.append(title.text.strip())

# MES 27
	r = record.xpath("note[@type='Dates of Publication and/or Volume Designation - Formatted style']")
	if(len(r)):
		for title in r:
			MES_27_num_and_chrono_des.append(title.text.strip())
	r = record.xpath("note[@type='Dates of Publication and/or Volume Designation-Unformatted note']")
	if(len(r)):
		for title in r:
			MES_27_num_and_chrono_des.append(title.text.strip())

# MES 28
	r = record.xpath("note[@type='Type of Computer File or Data Note - Information not provided']")
	if(len(r)):
		MES_28_file_type = r[0].text.strip()

# MES 29
	r = record.xpath("language/languageTerm[@type='code' and @authority='iso639-2b']")
	if(len(r)):
		MES_29_language = []
		for language in r:
			MES_29_language.append(language.text.strip())

# MES 30
	# NA
# MES 31
	# TBD
# MES 32
	# Automatically generated, match with Controlled List
# MES 33
	# NA 
# MES 34
	# NA 

# MES 35
	r = record.xpath("note[@type='HTTP-Resource']")
	if(len(r)):
		MES_35_access_url = []
		for name, value in sorted(r[0].items()):
			if(name == '{http://www.w3.org/1999/xlink}simpleLink'):
				MES_35_access_url.append(value)


	## Uncomment to display missing Canadiana numbers
	#if(MES_1_metadata_identifier == 'ERROR MES element 1'):
	#	print MES_1_metadata_identifier+"\n"+MES_2_title+"\n\n"

	## Uncomment to only display valid Canadiana numbers quoted to show spacing
	#if(MES_1_metadata_identifier != 'ERROR MES element 1'):
	#	print '"'+MES_1_metadata_identifier+'"'#+"\n"+MES_2_title+"\n\n"

	#if MES_6_subject[0] != 'ERROR MES element 6':
	#	continue

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

