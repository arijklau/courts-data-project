#### search url for alexandria court cases
# criminal:  https://ajis.alexandriava.gov/CriminalCaseList.aspx?lastName=&firstName=&from=&thru=&fileNo=&businessName=
# civil: https://ajis.alexandriava.gov/CivilCaseList.aspx?court=Alexandria%20Circuit%20Court&casetype=&from=&thru=&fileNo=&status=&actionFrom=&actionThru=

import urllib
import urllib.parse
import urllib.request

criminal = "https://ajis.alexandriava.gov/CriminalCaseList.aspx?"
civil = "https://ajis.alexandriava.gov/CivilCaseList.aspx?"

crim_vals = {
	'lastName':'',
	'firstName':'',
	'from':'',
	'thru':'',
	'fileNo':'',
	'businessName':''
}

civ_vals = {
	'court':'Alexandria',
	'Circuit Court':'',
	'casetype':'',
	'from':'',
	'thru':'',
	'fileNo':'',
	'actionFrom':'',
	'actionThru':''
}

class crim_case_obj(object):
	def __init__(self, case):
		self.name = case[0][2:]
		self.file_num = case[1]
		self.court = case[2]
		self.id_num = case[3]
		self.age = case[4]
		self.charge = case[5]
		self.sex = case[6]
		self.race = case[7]
		self.initiated = case[8]
		self.offense_date = case[9]

criminal_url = criminal + urllib.parse.urlencode(crim_vals)
civil_url = civil + urllib.parse.urlencode(civ_vals)

crim_req = urllib.request.Request(criminal_url)
civ_req = urllib.request.Request(civil_url)

crim_req = "https://ajis.alexandriava.gov/CriminalCaseList.aspx?lastName=%20&firstName=&from=&thru=&fileNo=&businessName=University%20of%20Virginia"

with urllib.request.urlopen(crim_req) as response:
	the_page = response.read().strip(b'\t')
	ind1, ind2 = the_page.find(b'table'), the_page.find(b'/table') # RM: find the start end of the table
	the_page = the_page[ind1:ind2].split(b'\r\n') # RM: subset the data into between the indices and split 
	new_page = []
	case_objs = []
	for line in the_page:
		try: 
			new_line = line.split(b"</td><td>") # split by table markers
			if len(new_line) > 1: new_page.append([p.strip() for p in new_line][1:]) # if the length of the newly splitted line is greater than 1 (meaning it is in the table), include it
		except:
			continue
	for case in new_page:
		case = [i.decode("utf-8") for i in case]
		temp_case = crim_case_obj(case)
		case_objs.append(temp_case)

# FOR NOW IN OUR SCHEMA: case objects can serve as our default schema but we will probably need to add more info such as civ vs crim, region, etc.
		
