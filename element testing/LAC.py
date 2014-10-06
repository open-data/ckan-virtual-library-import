#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import codecs
from lxml import etree
import re
import time
import json
import os
# Sanity checking and short cycle testing
# 0 = unlimited, any other number is a maximum tollerance
fuse = 0
valid_file_formats = ['.doc','.htm','.html','.epub','.jpg','.odt','.pdf','.ppt','.rtf','.txt']

# Split tasks, same blocks of logic per MES
output_human = False
output_json  = True
if len(sys.argv):
	if 'report' in sys.argv:
		output_human = True
		output_json  = False
	if 'debug' in sys.argv:
		output_human = False
		output_json  = False

f = codecs.open("../data/LAC_records_complete.xml", "r", "utf-8")
root = etree.fromstring(f.read())

# Report Header
iso_time = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())
if output_human:
	print "======================================================================"
	print "= LAC :: =============== :: "+iso_time+" ======================"
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
	MES_31_type                    = ['(M/a) CONFIRM MES element 31']
	MES_32_format                  = ['(M-C) ERROR MES element 32']
	MES_33_size                    = ['(O) BLANK MES element 33']
	MES_34_number_of_pages         = ['(M/a) CONFIRM MES element 34']
	MES_35_access_url              = ['(M) ERROR MES element 35']
	MES_36_licence                 = '(M-C) ERROR MES element 36'

	json_record = {}
	json_record['resources'] = [{}]
	json_record['type'] ='doc'
	json_record['license_id'] = 'ca-ogl-lgo'

# MES 29
	r = record.xpath("language/languageTerm[@type='code' and @authority='iso639-2b']")
	if(len(r)):
		MES_29_language = []
		for language in r:
			MES_29_language.append(language.text.strip())
	if MES_29_language[0] == '(M) ERROR MES element 29':
		json_record['resources'][0]['languages'] = 'eng'
	else:		
		json_record['resources'][0]['languages'] = ','.join(MES_29_language)
	
	effective_language = 'en'
	if MES_29_language[0] == 'fre' or MES_29_language[0] == 'fra':
		effective_language = 'fr'

# MES 1
	# VERIFY THAT YOU ARE DOING WHAT THEY ASKED YOU TO
	r = record.xpath("identifier[@type='canadiana']")
	if(len(r)):
		cleanup = r[0].text.strip()
		cleanup = cleanup.split(' ', 1)[0].lower()
		MES_1_metadata_identifier = cleanup

	json_record['name'] = 'collections-'+cleanup

# MES 2
	r = record.xpath("titleInfo[not(@type)]/title")
	if(len(r)):
		MES_2_title = []
		for title in r:
			MES_2_title.append(title.text.strip())

	json_record['title'] = ' | '.join(MES_2_title)

	if json_record['title'] == '':
		json_record['title'] = 'ERROR BLANK TITLE'

# MES 3
	json_record['source_organizations_ml'] = {}

	r = record.xpath("name[@type='corporate']/namePart")
	if(len(r)):
		MES_3_GC_Department_or_Agency = []
		for namePart in r:
			MES_3_GC_Department_or_Agency.append(namePart.text.strip())

	if(MES_3_GC_Department_or_Agency[0] != '(M) ERROR MES element 3'):
		json_record['source_organizations_ml'][effective_language] = ','.join(MES_3_GC_Department_or_Agency)

# MES 4
	json_record['author'] = {}	

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

	if(MES_4_author[0] != "(M/a) CONFIRM MES element 4"):
		json_record['author'] = ','.join(MES_4_author)

# MES 5
	json_record['description_ml'] = {}	

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

	if MES_5_description != '(M/a) CONFIRM MES element 5':
		json_record['description_ml'][effective_language] = MES_5_description

# MES 6
	json_record['subject_ml'] = {}

	rvm  = []
	lcsh = []
	csh  = []
	r = record.xpath("subject[@authority='rvm']/topic")
	if(len(r)):
		for subject in r:
			rvm.append(subject.text.strip())
	r = record.xpath("subject[@authority='rvm']/name[@type='corporate']")
	if(len(r)):
		for subject in r:
			rvm.append(subject.text.strip())
	r = record.xpath("subject[@authority='lcsh']/topic")
	if(len(r)):
		for subject in r:
			lcsh.append(subject.text.strip())
	r = record.xpath("subject[@authority='lcsh']/name[@type='corporate']")
	if(len(r)):
		for subject in r:
			lcsh.append(subject.text.strip())
	r = record.xpath("subject[@authority='csh']/topic")
	if(len(r)):
		for subject in r:
			csh.append(subject.text.strip())
	r = record.xpath("subject[@authority='csh']/name[@type='corporate']")
	if(len(r)):
		for subject in r:
			csh.append(subject.text.strip())

	if(len(rvm) or len(lcsh) or len(csh)):
		MES_6_subject = []
		MES_6_subject.extend(rvm)
		MES_6_subject.extend(lcsh)
		MES_6_subject.extend(csh)

	if(MES_6_subject[0] != '(M) ERROR MES element 6'):
		json_record['subject_ml'][effective_language] = ','.join(MES_6_subject)


# MES 7
	# MISSING IN THE LAC MAPPING

# MES 8
	bits = []
	daterange = ''
	match_range = ''
	r = record.xpath("originInfo/dateIssued[@encoding='marc']")
	if(len(r)):
		year = r[0].text.strip()[:4]
		#print "Ya"+year
		m = re.match(r"([0-9]{3})u", year)			
		if m:
			match_range = m.group(1)+'0-'+m.group(1)+'9'
		m = re.search('^[0-9]+$', year)
		if m:
		#	print "INSTANCE:"
			if int(year) < int(iso_time[:4]):
		#		print "--a"
				daterange = r[0].text.strip()
				bits.append(r[0].text.strip())
		else:
			pass
			#print '['+MES_1_metadata_identifier +'] '+r[0].text.strip()
	r = record.xpath("extension/searchDate[@point='start']")
	if(len(r)):
		year = r[0].text.strip()[:4]
		#print "Yb"+year
		m = re.match(r"([0-9]{3})u", year)			
		if m:
			match_range = m.group(1)+'0-'+m.group(1)+'9'
		m = re.search('^[0-9]+$', year)
		if m:
		#	print "INSTANCE:"
			if int(year) < int(iso_time[:4]):
		#		print "--b"
				daterange = r[0].text.strip()
				bits.append(r[0].text.strip())
		else:
			pass
			#print '['+MES_1_metadata_identifier +'] '+r[0].text.strip()
	r = record.xpath("extension/searchDate[@point='end']")
	if(len(r)):
		year = r[0].text.strip()[:4]
		#print "Yc"+year
		m = re.match(r"([0-9]{3})u", year)			
		if m:
			match_range = m.group(1)+'0-'+m.group(1)+'9'
		m = re.search('^[0-9]+$', year)
		if m:
		#	print "INSTANCE:"
			if int(year) < int(iso_time[:4]):
		#		print "--c"
				daterange = daterange+'-'+r[0].text.strip()
				bits.append(r[0].text.strip())
		else:
			pass
			#print '['+MES_1_metadata_identifier +'] '+r[0].text.strip()


	#if match_range != '':
	#	print "1111-RANGE:"+match_range+' ('+(','.join(bits))+')'

	if(len(bits)):
		MES_8_date_resource_published = ','.join(bits)
	elif match_range != '':
		#print "SUPERRANGE:"+match_range
		MES_8_date_resource_published = match_range
		daterange = match_range

	if MES_8_date_resource_published != "(M) ERROR MES element 8":
		MES_8_date_resource_published = MES_8_date_resource_published + ' ( '+daterange+' }'
		json_record['date_published'] = daterange
		#json_record['resources'][0]['date_published'] = MES_8_date_resource_published

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

	json_record['date_modified'] = MES_10_modification_Date
	#json_record['resources'][0]['date_modified'] = MES_10_modification_Date

# MES 11
	# NOT AVAILABLE FROM LAC

# MES 12
	r = record.xpath("identifier[@type='isbn']")
	if(len(r)):
		MES_12_ISBN = []
		for title in r:
			MES_12_ISBN.append(title.text.strip())

	if(MES_12_ISBN[0] != '(M/a) CONFIRM MES element 12'):
		json_record['isbn'] = ','.join(MES_12_ISBN)

# MES 13
	r = record.xpath("identifier[@type='issn']")
	if(len(r)):
		MES_13_ISSN = []
		for title in r:
			MES_13_ISSN.append(title.text.strip())

	if(MES_13_ISSN[0] != '(M/a) CONFIRM MES element 13'):
		json_record['issn'] = ','.join(MES_13_ISSN)

# MES 14
	r = record.xpath("identifier[@type='govt']")
	if(len(r)):
		MES_14_gc_catalogue_number = r[0].text.strip()

	if '(M/a) CONFIRM MES element 14' != '(M/a) CONFIRM MES element 14':
		json_record['gc_catalogue_number'] = MES_14_gc_catalogue_number

# MES 15
	# LAC does not record

# MES 16
	r = record.xpath("note[@type='General Note']")
	if(len(r)):
		MES_16_weekly_checklist_number = r[0].text.strip()

	if '(M/a) CONFIRM MES element 16' != '(M/a) CONFIRM MES element 16':
		json_record['weekly_checklist_number'] = MES_16_weekly_checklist_number
	
# MES 17
	# GC DOCS N/A
# MES 18
	# Docs Number N/A

# MES 19
	MES_19_LAC_identifier = MES_1_metadata_identifier

	json_record['lac_identifier'] = MES_19_LAC_identifier

# MES 20
	r = record.xpath("recordInformation/recordIdentifier[@userView='1']")
	if(len(r)):
		MES_20_amicus_identifier = r[0].text.strip()

	json_record['amicus_identifier'] = MES_19_LAC_identifier

# MES 21
	# PWGSC Identifier N/A
# MES 22
	# DOI N/A

# MES 23 & 24
	json_record['series_title_ml'] = {}
	json_record['series_number_ml'] = {}

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

	if(MES_23_series_title[0] != "(M/a) CONFIRM MES element 23"):
		json_record['series_title_ml'][effective_language] = ','.join(MES_23_series_title)
	if(MES_24_series_number[0] != "(M/a) CONFIRM MES element 24"):
		json_record['series_number_ml'][effective_language] = ','.join(MES_24_series_number)

# MES 25
	r = record.xpath("note[@type='Current Publication Frequency']")
	if(len(r)):
		MES_25_frequency_of_serial = r[0].text.strip()

	if MES_25_frequency_of_serial != "(M/a) CONFIRM MES element 25":
		json_record['frequency'] = MES_25_frequency_of_serial

# MES 26
	r = record.xpath("note[@type='Former Frequency']")
	if(len(r)):
		for title in r:
			MES_26_former_frequency.append(title.text.strip())

	if MES_26_former_frequency[0] != "(M/a) CONFIRM MES element 26":
		json_record['former_frequency'] = ','.join(MES_26_former_frequency)

# MES 27
	json_record['resources'][0]['numeric_designation_ml'] = {}
	r = record.xpath("note[@type='Dates of Publication and/or Volume Designation - Formatted style']")
	if(len(r)):
		for title in r:
			MES_27_num_and_chrono_des.append(title.text.strip())
	r = record.xpath("note[@type='Dates of Publication and/or Volume Designation-Unformatted note']")
	if(len(r)):
		for title in r:
			MES_27_num_and_chrono_des.append(title.text.strip())


	

	if( MES_27_num_and_chrono_des[0] != '(M/a) CONFIRM MES element 27' ):
		json_record['resources'][0]['numeric_designation_ml'][effective_language] = ','.join(MES_27_num_and_chrono_des)


# MES 28
	json_record['resources'][0]['format_description_ml'] = {}
	
	r = record.xpath("note[@type='Type of Computer File or Data Note - Information not provided']")
	if(len(r)):
		MES_28_file_type = r[0].text.strip()

	if MES_28_file_type != '(M/a) CONFIRM MES element 28':
		json_record['resources'][0]['format_description_ml'][effective_language] = MES_28_file_type

# MES 30
	# NA
# MES 31
	# TBD
# MES 33
	# NA 
# MES 34
	# NA 

# MES 35
	bits = []
	r = record.xpath("note[@type='HTTP-Resource']")
	if(len(r)):
		for name, value in sorted(r[0].items()):
			#print 'NAME:1:'+name
			if(name == '{http://www.w3.org/1999/xlink}simpleLink'):
				#print '   V:1:'+value
				bits.append(value)

	r = record.xpath("note[@type='HTTP-No information provided']")
	if(len(r)):
		for name, value in sorted(r[0].items()):
			#print 'NAME:2:'+name
			if(name == '{http://www.w3.org/1999/xlink}simpleLink'):
				bits.append(value)

#-<note type="HTTP-Version of Resource" xlink:simpleLink="http://data2.collectionscanada.gc.ca/080074/jhc_1930_vol67.pdf">
	r = record.xpath("note[@type='HTTP-Version of Resource']")
	if(len(r)):
		for name, value in sorted(r[0].items()):
			#print 'NAME:3:'+name
			if(name == '{http://www.w3.org/1999/xlink}simpleLink'):
				bits.append(value)

#-<note type="HTTP-Resource">http://epe.lac-bac.gc.ca/100/200/301/inac-ainc/jurisdictional_responsibilities-e/bk3_yk/b3yk.pdf
	r = record.xpath("note[@type='HTTP-Resource']")
	if(len(r)):
		for url in r:
			#print 'NAME:4:'+name
			bits.append(url.text.strip())

	r = record.xpath("note[@type='Resource']")
	if(len(r)):
		for url in r:
			#print 'NAME:5:'+name
			bits.append(url.text.strip())

#-<note type="HTTP-No information provided">http://www.cic.gc.ca/english/immigr/adopt_e.html
	r = record.xpath("note[@type='HTTP-No information provided']")
	if(len(r)):
		for url in r:
			#print 'NAME:6:'+name
			bits.append(url.text.strip())

	if(len(bits)):
		MES_35_access_url = bits

	if(MES_35_access_url[0] != '(M) ERROR MES element 35'):
		base_resource = json_record['resources'][0]
		json_record['resources'] = []
		distinct_urls = []
		distinct_formats = []
		for url in MES_35_access_url:
			if url != '':
				#distinct_urls.append(url)
				#print "STRING:\n"+url
				for match in re.finditer('(https?://[^\s?#@]+)', url, re.S):
					distinct_urls.append(match.group(1))

		distinct_urls = list(set(distinct_urls))
		for distinct_url in distinct_urls:
			new_resource = dict(base_resource)
			new_resource['url'] = distinct_url

			interim_format = os.path.splitext(distinct_url)[1].lower()
			if interim_format in valid_file_formats:
				distinct_formats.append(interim_format)
				new_resource['format'] = interim_format
			#else:
			#	print "FORMAT:"+interim_format
			#	pass
				#print interim_format

			json_record['resources'].append(new_resource)

		if len(distinct_urls):
			MES_35_access_url = list(distinct_urls)
		else:
			MES_35_access_url = ['(M) ERROR MES element 35']
		if len(distinct_formats):
			MES_32_format = list(distinct_formats)
		else:
			MES_32_format = ['(M-C) ERROR MES element 32']

	#continue
	


#M [20117014656][2] http://epe.lac-bac.gc.ca/100/200/301/hrsdc-rhdcc/ http://epe.lac-bac.gc.ca/100/200/301/hrsdc-rhdcc/essential_skills_apprenticeship/what_are_essential_trades/HS18-9-1-2009-fra.pdf
#M [20137039581][2] http://publications.gc.ca/collections/collection_2013/ec/CW69-5-525A-eng.pdf ; http://publications.gc.ca/collections/collection_2013/ec/CW69-5-525B-eng.pdf
#M [2013703959X][2] http://publications.gc.ca/collections/collection_2013/ec/CW69-5-525A-fra.pdf ; http://publications.gc.ca/collections/collection_2013/ec/CW69-5-525B-fra.pdf

#	if(MES_35_access_url[0] != '(M) ERROR MES element 35'):
#		json_record['resources'][0]['url'] = ','.join(MES_35_access_url)

	## Uncomment to display missing Canadiana numbers
	#if(MES_1_metadata_identifier == 'ERROR MES element 1'):
	#	print MES_1_metadata_identifier+"\n"+MES_2_title+"\n\n"

	## Uncomment to only display valid Canadiana numbers quoted to show spacing
	#if(MES_1_metadata_identifier != 'ERROR MES element 1'):
	#	print '"'+MES_1_metadata_identifier+'"'#+"\n"+MES_2_title+"\n\n"

	#if MES_6_subject[0] != 'ERROR MES element 6':
	#	continue



	if MES_1_metadata_identifier 	        == '(M-C) ERROR MES element 1':# or  MES_1_metadata_identifier == '':
		continue
	if MES_2_title[0] 						== '(M) ERROR MES element 2':#   or  ''.join(MES_2_title) == '':
		continue
	if MES_3_GC_Department_or_Agency[0]		== '(M) ERROR MES element 3':#   or  ''.join(MES_3_GC_Department_or_Agency) == '':
		continue
##	#if MES_6_subject[0] 					== '(M) ERROR MES element 6'   or  MES_6_subject == '':
	if MES_8_date_resource_published  		== '(M) ERROR MES element 8':#   or  MES_8_date_resource_published == '':
		continue
	if MES_29_language[0]                	== '(M) ERROR MES element 29':#  or ''.join(MES_29_language) == '':
		continue
	if MES_32_format[0]						== '(M-C) ERROR MES element 32':#  or ''.join(MES_35_access_url) == '':
		continue
	if MES_35_access_url[0]              	== '(M) ERROR MES element 35':#  or ''.join(MES_35_access_url) == '':
		continue

#	if MES_1_metadata_identifier 	        != '(M-C) ERROR MES element 1' and  MES_1_metadata_identifier != '':
#		continue
#	if MES_2_title[0] 						!= '(M) ERROR MES element 2'   and  ''.join(MES_2_title) != '':
#		continue
#	if MES_3_GC_Department_or_Agency[0]		!= '(M) ERROR MES element 3'   and  ''.join(MES_3_GC_Department_or_Agency) != '':
#		continue
#	#if MES_6_subject[0] 					!= '(M) ERROR MES element 6'   and  MES_6_subject != '':
#	if MES_8_date_resource_published  		!= '(M) ERROR MES element 8'   and  MES_8_date_resource_published != '':
#		continue
#	if MES_29_language[0]                	!= '(M) ERROR MES element 29'  and ''.join(MES_29_language) != '':
#		continue
#	if MES_35_access_url[0]              	!= '(M) ERROR MES element 35':  and ''.join(MES_35_access_url) != '':
#		continue
#	if MES_35_access_url[0]              	!= '(M) ERROR MES element 35':#  and ''.join(MES_35_access_url) != '':
#		continue

#	if "Pyroxasulfone, le 28 juillet 2014" != ''.join(set(MES_2_title)).encode('utf-8'):
#		continue

	#print json.dumps(json_record)
#	print json.dumps(json_record, sort_keys=True, indent=4, separators=(',', ': '))

#	print MES_1_metadata_identifier.encode('utf-8')
#	
	if output_human:
		print "ID                    ::"+MES_1_metadata_identifier.encode('utf-8')
		print "TITLE                 ::"+("\nTITLE                 ::".join(set(MES_2_title))).encode('utf-8')
		print "GCDEP                 ::"+("\nGCDEP                 ::".join(set(MES_3_GC_Department_or_Agency))).encode('utf-8')
		print "AUTHOR                ::"+("\nAUTHOR                ::".join(set(MES_4_author))).encode('utf-8')
		print "DESC                  ::"+MES_5_description.encode('utf-8')
		print "SUBJECT               ::"+("\nSUBJECT               ::".join(set(MES_6_subject))).encode('utf-8')
		print "KEYWORDS              ::"+("\nKEYWORDS              ::".join(set(MES_7_keywords))).encode('utf-8')
		print "D PUBLISHED           ::"+MES_8_date_resource_published.encode('utf-8')
		print "D CONTRIB             ::"+MES_9_date_contributed.encode('utf-8')
		print "D MODIFIED            ::"+MES_10_modification_Date.encode('utf-8')
		print "D CREATED             ::"+MES_11_data_resource_created.encode('utf-8')
		print "ISBN                  ::"+("\ISBN                   ::".join(set(MES_12_ISBN))).encode('utf-8')
		print "ISSN                  ::"+("\ISSN                   ::".join(set(MES_13_ISSN))).encode('utf-8')
		print "GC CATALOGUE NO       ::"+MES_14_gc_catalogue_number.encode('utf-8')
		print "DEPT. CATALOGUE NO    ::"+MES_15_dept_catalogue_number.encode('utf-8')
		print "WEEK CHECKLIST NO     ::"+MES_16_weekly_checklist_number.encode('utf-8')
		print "FILE CODE             ::"+MES_17_file_code.encode('utf-8')
		print "GC DOCS NO            ::"+MES_18_gc_docs_number.encode('utf-8')
		print "LAC_IDENT             ::"+MES_19_LAC_identifier.encode('utf-8')
		print "AMICUS NO             ::"+MES_20_amicus_identifier.encode('utf-8')
		print "CATALOGUE SYSTEM NO   ::"+MES_21_PWGSC_identifier.encode('utf-8')
		print "DOI                   ::"+("\nDOI                   ::".join(set(MES_22_DOI))).encode('utf-8')
		print "Series Title          ::"+("\nSeries Title          ::".join(set(MES_23_series_title))).encode('utf-8')
		print "Series Number         ::"+("\nSeries Number         ::".join(set(MES_24_series_number))).encode('utf-8')
		print "FREQUENCY             ::"+MES_25_frequency_of_serial.encode('utf-8')
		print "FORMER FREQUENCY      ::"+("\nFORMER FREQUENCY      ::".join(set(MES_26_former_frequency))).encode('utf-8')
		print "NUM & CHRONO          ::"+("\nNUM & CHRONO          ::".join(set(MES_27_num_and_chrono_des))).encode('utf-8')
		print "FILETYPE              ::"+MES_28_file_type.encode('utf-8')
		print "LANGUAGE              ::"+("\nLANGUAGE              ::".join(set(MES_29_language))).encode('utf-8')
		print "OTHER LANGUAGE        ::"+("\nOTHER LANGUAGE        ::".join(set(MES_30_language_other))).encode('utf-8')
		print "TYPE                  ::"+("\nTYPE                  ::".join(set(MES_31_type))).encode('utf-8')
		print "FORMAT                ::"+("\nFORMAT                ::".join(set(MES_32_format))).encode('utf-8')
		print "SIZE                  ::"+("\SIZE                   ::".join(set(MES_33_size))).encode('utf-8')
		print "PAGES                 ::"+("\nPAGES                 ::".join(set(MES_34_number_of_pages))).encode('utf-8')
		print "ACCESS URL            ::"+("\nACCESS URL            ::".join(set(MES_35_access_url))).encode('utf-8')
		print "LICENSE               ::"+MES_36_licence.encode('utf-8')
		print "======================================================================"

	if output_json:
		print json.dumps(json_record)
		#print json.dumps(json_record, sort_keys=True, indent=4, separators=(',', ': '))

	# Sanity checking and short cycle testing
	if fuse == 1:
		break
	fuse -= 1

#	print "[ "+MES_1_metadata_identifier+" ]ACCESS URL            ::"+(" | ".join(set(MES_35_access_url))).encode('utf-8')





