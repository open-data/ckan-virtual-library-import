#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import codecs
from lxml import etree
import re
import time
import json
import os
import csv

# Sanity checking and short cycle testing
# 0 = unlimited, any other number is a maximum tollerance
fuse = 0
valid_file_formats = ['.doc','.htm','.html','.epub','.jpg','.odt','.pdf','.ppt','.rtf','.txt','.wpd']

linkcheck_status = {}

with open('PWGSCLINKS.csv', 'r') as csvfile:
	spamreader = csv.reader(csvfile)
	for row in spamreader:
		if row[0] == '':
			continue
		#print ', '.join(row)
		#print row
		linkcheck_status[row[1]] = row[0]

# Split tasks, same blocks of logic per MES
output_human		= False
output_linkerrors 	= False
output_json  		= True
if len(sys.argv):
	output_json  		= False
	if 'report' in sys.argv:
		output_human	= True
	elif 'linkerrors' in sys.argv:
		output_human	= True
	else:
		output_json 	= True

# Report Header
iso_time = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())
if output_human:
	print "======================================================================"
	print "= PWGSC :: "+iso_time+" ======================================="
	print "======================================================================"
	print "==== (M)   Mandatory ================================================="
	print "==== (M/a) Mandatory if Applicable ==================================="
	print "==== (O)   Optional==================================================="
	print "==== (M-C) Mandatory, CKAN generated ================================="
	print "======================================================================"

json_output = []
input_files = ['monographs-monographies.xml', 'periodicals-periodiques.xml', 'series-series.xml']
#input_files = ['series-series.xml']

global_json = {}

for input_file in input_files:

	# Report import file marker
	if output_human:
		print "======================================================================"
		print "===== "+input_file
		print "======================================================================"

	f = codecs.open("../data/"+input_file, "r", "utf-8")

	root = etree.fromstring(f.read())

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
		MES_31_type                    = ['(M/a) CONFIRM MES element 31']
		MES_32_format                  = ['(M-C) ERROR MES element 32']
		MES_33_size                    = ['(O) BLANK MES element 33']
		MES_34_number_of_pages         = ['(M/a) CONFIRM MES element 34']
		MES_35_access_url              = ['(M) ERROR MES element 35']
		MES_36_licence                 = '(M-C) ERROR MES element 36'

		iso_conversion = { 'Miscellaneous languages' : 'mis','Inuinnaqtun' : 'mis','Inuvialuqtun' : 'mis','Albanian' : 'alb','Amharic' : 'amh','Arabic' : 'ara','Bengali' : 'ben','Catalan' : 'cat','Chinese' : 'chi','Chipewyan' : 'chp','Cree' : 'cre','Creoles and pidgins' : 'crp','Croatian' : 'hrv','Dutch' : 'dut','English' : 'eng','French' : 'fra','Galician' : 'glg','German' : 'ger','Greek, Modern (1453-)' : 'gre','Gujarati' : 'guj','Hindi' : 'hin','Hungarian' : 'hun','Indonesian' : 'ind','Inuktitut' : 'iku','Italian' : 'ita','Japanese' : 'jpn','Korean' : 'kor','North American Indian' : 'nai','Ojibwa' : 'oji','Persian' : 'per','Punjabi' : 'pan','Philippine (Other)' : 'phi','Polish' : 'pol','Portuguese' : 'por','Romanian' : 'rum','Russian' : 'rus','Serbian' : 'srp','Somali' : 'som','Spanish; Castilian' : 'spa','Swahili' : 'swa','Tagalog' : 'tgl','Tamil' : 'tam','Turkish' : 'tur','Urdu' : 'urd','Vietnamese' : 'vie' }

		json_record = {}
		json_record['resources'] = [{}]
		json_record['type'] ='doc'
		json_record['license_id'] = 'ca-ogl-lgo'

		record_about = record.attrib['{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about']

## MES 29

		r = record.xpath("dc:language[@xml:lang='en']", namespaces=record.nsmap)
		#r = record.xpath("name[@type='corporate']/namePart")
		if(len(r)):
			MES_29_language = []
			for namePart in r:
				lang_test = namePart.text.strip()
				if lang_test == 'fre':
					lang_test = 'fra'
				#print "LANGO:["+MES_1_metadata_identifier+"]:"+namePart.text.strip()
				MES_29_language.append(iso_conversion[lang_test])
		json_record['resources'][0]['languages'] = ','.join(MES_29_language)

## MES 1
		#r = record.xpath("dc:identifier[@xml:lang='en']", namespaces=record.nsmap)
		r = record.xpath("dc:identifier", namespaces=record.nsmap)
		if(len(r)):
			for cn in r:
				m = re.search('{System ID}\s+(.*)', cn.text.strip())
				if m:
					MES_1_metadata_identifier = m.group(1).strip() 
				else:
					m = re.search("{ID système}\s+(.*)", cn.text.strip())
					if m:
						MES_1_metadata_identifier = m.group(1).strip() 
		json_record['name'] = 'publications-'+MES_1_metadata_identifier 

## MES 2
		bits = []
		bits_en = []
		bits_fr = []
		json_record['title_ml'] = {}
		r = record.xpath("dc:title[@xml:lang='en']", namespaces=record.nsmap)
		if(len(r)):
			for title in r:
				bits.append(title.text.strip())
				bits_en.append(title.text.strip())
		r = record.xpath("dc:title[@xml:lang='fr']", namespaces=record.nsmap)
		if(len(r)):
			for title in r:
				bits.append(title.text.strip())
				bits_fr.append(title.text.strip())
		if(len(bits)):
			MES_2_title = bits
		if(len(bits_en)):
			json_record['title_ml']['en'] = ','.join(bits_en)
		if(len(bits_fr)):
			json_record['title_ml']['fr'] = ','.join(bits_fr)
		#if(len(json_record['title_ml']) < 1):
		#	del json_record['title_ml']


		joined_title = ''
		if 'en' in json_record['title_ml']:
			joined_title = joined_title+json_record['title_ml']['en']
		if 'fr' in json_record['title_ml']:
			joined_title = joined_title+json_record['title_ml']['fr']

		if 'en' in json_record['title_ml'] and 'fr' in json_record['title_ml']:
			json_record['title'] = json_record['title_ml']['en'] + ' | ' + json_record['title_ml']['fr']

		elif 'en' in json_record['title_ml']:
			json_record['title'] = json_record['title_ml']['en']
		elif 'fr' in json_record['title_ml']:
			json_record['title'] = json_record['title_ml']['fr']
		else:
			json_record['title'] = 'ERROR TITLE MISSING'

		if json_record['title'] == '':
			json_record['title'] = 'ERROR BLANK TITLE'

#		else:		
#			for lang in MES_29_language:
#				if lang == 'eng':
#					if 'en' not in json_record['title_ml']:
#						json_record['title'] = json_record['title_ml']['fr']
#			#else:
#			#	print "y : Not english or french [ "+lang+" ] : "+MES_1_metadata_identifier

## MES 3
		bits = []
		bits_en = []
		bits_fr = []
		json_record['source_organizations_ml'] = {}
		r = record.xpath("dc:creator[@xml:lang='en']", namespaces=record.nsmap)
		if(len(r)):
			for namePart in r:
				bits.append(namePart.text.strip())
				bits_en.append(namePart.text.strip())
				#json_record['gc_org']['en'] = namePart.text.strip()
		r = record.xpath("dc:creator[@xml:lang='fr']", namespaces=record.nsmap)
		if(len(r)):
			for namePart in r:
				bits.append(namePart.text.strip())
				bits_fr.append(namePart.text.strip())
				#json_record['gc_org']['fr'] = namePart.text.strip()
		if(len(bits)):
			MES_3_GC_Department_or_Agency = bits
		if(len(bits_en)):
			json_record['source_organizations_ml']['en'] = ','.join(bits_en)
		if(len(bits_fr)):
			json_record['source_organizations_ml']['fr'] = ','.join(bits_fr)
		if(len(json_record['source_organizations_ml']) < 1):
			del json_record['source_organizations_ml']

## MES 4
		# NA

## MES 5
		bits = []
		bits_en = []
		bits_fr = []	
		json_record['description_ml'] = {}
		page = ''
		r = record.xpath("dc:description[@xml:lang='en']", namespaces=record.nsmap)
		if(len(r)):
			for title in r:
				#print "--title:"+title.text.strip()
				m = re.search('^[0-9]+p\.', title.text.strip())
				if m:
					page = page + title.text.strip()
				else:
					m = re.search('^{.*', title.text.strip())
					if not m:
						bits.append(title.text.strip())
						bits_en.append(title.text.strip())
		r = record.xpath("dc:description[@xml:lang='fr']", namespaces=record.nsmap)
		if(len(r)):
			for title in r:
				#print "--title:"+title.text.strip()
				m = re.search('^[0-9]+p\.', title.text.strip())
				if m:
					page = page + title.text.strip()
				else:
					m = re.search('^{.*', title.text.strip())
					if not m:
						bits.append(title.text.strip())
						bits_fr.append(title.text.strip())
		if(len(bits)):
			MES_5_description = "\n".join(bits)
			#json_record['description_ml'] = "\n".join(bits)
		if(len(bits_en)):
			json_record['description_ml']['en'] = ' '.join(bits_en)
			if page != '':
				json_record['description_ml']['en'] = json_record['description_ml']['en'] + ' ' + page
		if(len(bits_fr)):
			json_record['description_ml']['fr'] = ' '.join(bits_fr)
			if page != '':
				json_record['description_ml']['fr'] = json_record['description_ml']['fr'] + ' ' + page
		#if(len(json_record['description_ml']) < 1):
		#	del json_record['description_ml']


## MES 6
		bits = []
		bits_en = []
		bits_fr = []
		json_record['subject_ml'] = {}
		r = record.xpath("dc:subject[@xml:lang='en']", namespaces=record.nsmap)
		#r = record.xpath("name[@type='corporate']/namePart")
		if(len(r)):
			for namePart in r:
				bits.append(namePart.text.strip())
				bits_en.append(namePart.text.strip())
		r = record.xpath("dc:subject[@xml:lang='fr']", namespaces=record.nsmap)
		#r = record.xpath("name[@type='corporate']/namePart")
		if(len(r)):
			for namePart in r:
				bits.append(namePart.text.strip())
				bits_fr.append(namePart.text.strip())
		if(len(bits)):
			MES_6_subject = bits
		if(len(bits_en)):
			json_record['subject_ml']['en'] = ','.join(bits_en)
		if(len(bits_fr)):
			json_record['subject_ml']['fr'] = ','.join(bits_en)


		if(len(json_record['subject_ml']) < 1):
			for lang in MES_29_language:
				if lang == 'fra':
					json_record['subject_ml']['fr'] = 'Gouvernement et vie politique'
				else:
					json_record['subject_ml']['en'] = 'Government and Politics'


			
			#del json_record['subject_ml']



## MES 7
		# NA

## MES 8
		
		r = record.xpath("dc:date", namespaces=record.nsmap)
		if(len(r)):
			MES_8_date_resource_published = r[0].text.strip()
			#json_record['resources'][0]['date_published'] = MES_8_date_resource_published
			json_record['date_published'] = MES_8_date_resource_published

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

		if(MES_12_ISBN[0] != '(M/a) CONFIRM MES element 12'):
			json_record['isbn'] = ','.join(MES_12_ISBN)


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

		if(MES_13_ISSN[0] != '(M/a) CONFIRM MES element 13'):
			json_record['issn'] = ','.join(MES_13_ISSN)

## MES 14
		#r = record.xpath("dc:identifier[@xml:lang='en']", namespaces=record.nsmap)
		r = record.xpath("dc:identifier", namespaces=record.nsmap)
		if(len(r)):
			for cn in r:
				m = re.search('{Catalogue Numbe}\s+(.*)', cn.text.strip())
				if m:
					MES_14_gc_catalogue_number = m.group(1).strip() 
					json_record['gc_catalogue_number'] = m.group(1).strip()
				else:
					m = re.search("{Numéro de catalogue}\s+(.*)", cn.text.strip())
					if m:
						MES_14_gc_catalogue_number = m.group(1).strip()
						json_record['gc_catalogue_number'] = m.group(1).strip()

## MES 15
		r = record.xpath("dc:identifier", namespaces=record.nsmap)
		if(len(r)):
			for cn in r:
				m = re.search('{Departmental ID (en)}\s+(.*)', cn.text.strip())
				if m:
					MES_15_dept_catalogue_number = m.group(1).strip() 
				else:
					m = re.search("{ID ministérielle (en)}\s+(.*)", cn.text.strip())
					if m:
						MES_15_dept_catalogue_number = m.group(1).strip() 
					else:
						m = re.search("{Departmental ID (fr)}\s+(.*)", cn.text.strip())
						if m:
							MES_15_dept_catalogue_number = m.group(1).strip() 
						else:
							m = re.search("{ID ministérielle (fr)}\s+(.*)", cn.text.strip())
							if m:
								MES_15_dept_catalogue_number = m.group(1).strip() 

			if MES_15_dept_catalogue_number != '(M/a) CONFIRM MES element 15':
				json_record['dept_catalogue_number'] = MES_15_dept_catalogue_number

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

		#r = record.xpath("dc:identifier[@xml:lang='en']", namespaces=record.nsmap)
		r = record.xpath("dc:identifier", namespaces=record.nsmap)
		if(len(r)):
			for cn in r:
				m = re.search('{System ID}\s+(.*)', cn.text.strip())
				if m:
					MES_21_PWGSC_identifier = m.group(1).strip() 
				else:
					m = re.search("{ID système}\s+(.*)", cn.text.strip())
					if m:
						MES_21_PWGSC_identifier = m.group(1).strip() 

			json_record['catalogue_number'] = MES_21_PWGSC_identifier

## MES 22
		# DOI N/A

## MES 23

		bits = []
		bits_en = []
		bits_fr = []
		json_record['series_title_ml'] = {}
		#r = record.xpath("dc:identifier[@xml:lang='en']", namespaces=record.nsmap)
		r = record.xpath("dc:description", namespaces=record.nsmap)
		if(len(r)):
			for cn in r:
				m = re.search('{Series title}\s+(.*)', cn.text.strip())
				if m:
					bits.append(m.group(1).strip())
					bits_en.append(m.group(1).strip())
				m = re.search("{Titre de collection}\s+(.*)", cn.text.strip())
				if m:
					bits.append(m.group(1).strip())
					bits_fr.append(m.group(1).strip())
		if(len(bits)):
			MES_23_series_title = bits
		if(len(bits_en)):
			json_record['series_title_ml']['en'] = ','.join(bits_en)
		if(len(bits_fr)):
			json_record['series_title_ml']['fr'] = ','.join(bits_fr)
		if(len(json_record['series_title_ml']) < 1):
			del json_record['series_title_ml']

## MES 24

		bits = []
		bits_en = []
		bits_fr = []
		json_record['series_number_ml'] = {}
		#r = record.xpath("dc:identifier[@xml:lang='en']", namespaces=record.nsmap)
		r = record.xpath("dc:description", namespaces=record.nsmap)
		if(len(r)):
			for cn in r:
				m = re.search('{Issue}\s+(.*)', cn.text.strip())
				if m:
					bits.append(m.group(1).strip())
					bits_en.append(m.group(1).strip())
				m = re.search("{Numéro}\s+(.*)", cn.text.strip())
				if m:
					bits.append(m.group(1).strip())
					bits_fr.append(m.group(1).strip())
		if(len(bits)):
			MES_24_series_number = bits
		if(len(bits_en)):
			json_record['series_number_ml']['en'] = ','.join(bits_en)
		if(len(bits_fr)):
			json_record['series_number_ml']['fr'] = ','.join(bits_fr)
		if(len(json_record['series_number_ml']) < 1):
			del json_record['series_number_ml']

## MES 25
		# NA

## MES 26
		# NA

## MES 27
		bits = []
		bits_en = []
		bits_fr = []
		json_record['resources'][0]['numeric_designation_ml'] = {}
		#r = record.xpath("dc:identifier[@xml:lang='en']", namespaces=record.nsmap)
		r = record.xpath("dc:description", namespaces=record.nsmap)
		if(len(r)):
			for cn in r:
				m = re.search('{Issue}\s+(.*)', cn.text.strip())
				if m:
					bits.append(m.group(1).strip())
					bits_en.append(m.group(1).strip())
				m = re.search("{Numéro}\s+(.*)", cn.text.strip())
				if m:
					bits.append(m.group(1).strip())
					bits_fr.append(m.group(1).strip())

		if(len(bits)):
			MES_27_series_number = bits
		if(len(bits_en)):
			json_record['resources'][0]['numeric_designation_ml']['en'] = ','.join(bits_en)
		if(len(bits_fr)):
			json_record['resources'][0]['numeric_designation_ml']['fr'] = ','.join(bits_fr)
		if(len(json_record['resources'][0]['numeric_designation_ml']) < 1):
			del json_record['resources'][0]['numeric_designation_ml']

## MES 28

#		r = record.xpath("dc:format", namespaces=record.nsmap)
#		if(len(r)):
#			MES_28_file_type = r[0].text.strip()
#			json_record['resources'][0]['format_description_ml'] = {}
#			for lang in MES_29_language:
#				json_record['resources'][0]['format_description_ml'][lang[:-1]] = MES_28_file_type

## MES 29
#   See above

## MES 30
		bits = []
		#r = record.xpath("dc:identifier[@xml:lang='en']", namespaces=record.nsmap)
		r = record.xpath("dc:relation", namespaces=record.nsmap)
		if(len(r)):
			for cn in r:
				m = re.search('{Other Language Edition}\s+(.*)', cn.text.strip())
				if m:
					bits.append(m.group(1).strip())
				else:
					m = re.search("{Édition dans une autre langue}\s+(.*)", cn.text.strip())
					if m:
						bits.append(m.group(1).strip())
		if(len(bits)):
			MES_30_language_other = bits
			json_record['other_language_url'] = ','.join(MES_30_language_other)			
			#json_record['other_language_url'] = langist(bits)

## MES 31

		json_record['resources'][0]['nature_genre_ml'] = {}

		if input_file == 'monographs-monographies.xml':
			for lang in MES_29_language:
				if lang == 'eng':
					json_record['resources'][0]['nature_genre_ml']['en'] = 'monograph'
				if lang == 'fra':
					json_record['resources'][0]['nature_genre_ml']['fr'] = 'monographie'
		if input_file == 'periodicals-periodiques.xml':
			for lang in MES_29_language:
				if lang == 'eng':
					json_record['resources'][0]['nature_genre_ml']['en'] = 'periodical'
				if lang == 'fra':
					json_record['resources'][0]['nature_genre_ml']['fr'] = 'periodique'
		if input_file == 'series-series.xml':
			for lang in MES_29_language:
				if lang == 'eng':
					json_record['resources'][0]['nature_genre_ml']['en'] = 'series'
				if lang == 'fra':
					json_record['resources'][0]['nature_genre_ml']['fr'] = 'serie'

		
# CONFIRM with Alannah
#
#		bits_en = []
#		bits_fr = []	
#		json_record['resources'][0]['nature_genre_ml'] = {}
#
#		r = record.xpath("dc:type[@xml:lang='en']", namespaces=record.nsmap)
#		if(len(r)):
#			MES_31_type = []
#			for cn in r:
#				MES_31_type.append(cn.text.strip())
#				bits_en.append(cn.text.strip())
#		r = record.xpath("dc:type[@xml:lang='fr']", namespaces=record.nsmap)
#		if(len(r)):
#			if(MES_31_type[0] == '(M) ERROR MES element 31'):
#				MES_31_type = []
#			for cn in r:
#				MES_31_type.append(cn.text.strip())
#				bits_fr.append(cn.text.strip())
#
#		if(len(bits_en)):
#			json_record['resources'][0]['nature_genre_ml']['en'] = ','.join(bits_en)
#		if(len(bits_fr)):
#			json_record['resources'][0]['nature_genre_ml']['fr'] = ','.join(bits_fr)
#
# ####################

## MES 32

#		r = record.xpath("dc:format", namespaces=record.nsmap)
#		if(len(r)):
#			MES_32_format = []
#			for cn in r:
#				MES_32_format.append(cn.text.strip())

## MES 33
		# NA 

## MES 34

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

		if(MES_35_access_url[0] != '(M) ERROR MES element 35'):
			base_resource = json_record['resources'][0]
			json_record['resources'] = []
			distinct_urls = []
			distinct_formats = []
			for url in MES_35_access_url:
				distinct_urls.append(url)
				
			distinct_urls = list(set(distinct_urls))
			for distinct_url in distinct_urls:

				if distinct_url not in linkcheck_status:
					#print "not in"
#				continue
					pass
				elif linkcheck_status[distinct_url][:3] != '200':
					#print linkcheck_status[distinct_url]
					continue

				new_resource = dict(base_resource)
				new_resource['url'] = distinct_url

				interim_format = os.path.splitext(distinct_url)[1].lower()
				if interim_format in valid_file_formats:
					distinct_formats.append(interim_format)
					new_resource['format'] = interim_format
					#print interim_format
				#else:
				#	print "["+MES_1_metadata_identifier+"] FORMAT:"+interim_format
				#	print distinct_url

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

		if MES_32_format[0]						== '(M-C) ERROR MES element 32':#  or ''.join(MES_35_access_url) == '':
			continue

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
			print "GC CATALOGUE NO       ::"+MES_14_gc_catalogue_number
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

		if output_linkerrors:
				for url35 in set(MES_35_access_url):
					if url35 not in linkcheck_status:
						print '"NO LINK CHECK",'+MES_1_metadata_identifier+',"'+url35.encode('utf-8')+'"'
					elif linkcheck_status[url35] == '200 no error':
						continue
					elif linkcheck_status[url35] == "200 no error < 302 found":
						continue
					elif linkcheck_status[url35] == "200 no error < 301 moved permanently":
						continue

					else:
						print '"'+linkcheck_status[url35]+'","'+MES_1_metadata_identifier+'","'+url35.encode('utf-8')+'"'

		if output_json:
			global_json[record_about] = json_record
			#global_json[] json.dumps(json_record)
			#print json.dumps(json_record, sort_keys=True, indent=4, separators=(',', ': '))

		# Sanity checking and short cycle testing
		# print fuse
		if fuse == 1:
			break
		fuse -= 1

#for key, value in global_json.iteritems() :
#    if 'other_language_url' in value:
#    	urls = value['other_language_url'].split(',')
#    	display_ole = ''
#    	for url in urls:
#    		if url in global_json:
#    			display_ole = display_ole +  '<br><a href="'+global_json[url]['name']+'">'+global_json[url]['name']+'</a>'
#    	if display_ole != '':
#    		global_json[key]['other_language_url'] = 'Other Language Edition / Édition dans une autre langue :'+display_ole
#
for key, value in global_json.iteritems() :
	#global_json[] json.dumps(json_record)
	#print json.dumps(json_record, sort_keys=True, indent=4, separators=(',', ': '))
	print json.dumps(value)






