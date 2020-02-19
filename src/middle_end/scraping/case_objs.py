import json

class crim_case(object):
    def __init__(self, case_info, charge_info, dispo_info, court):
        self.case_number = case_info[0]
        self.filed_date = case_info[1]
        self.locality = case_info[2]
        self.name = case_info[3]
        self.status = case_info[4]
        self.defense_attorney = case_info[5]
        self.address = case_info[6]
        self.aka1 = case_info[7]
        self.aka2 = case_info[8]
        self.gender = case_info[9]
        self.race = case_info[10]
        self.date_of_birth = case_info[11]

        self.charge = charge_info[0]
        self.code_section = charge_info[1]
        self.case_type = charge_info[2]
        self.crim_class = charge_info[3]
        self.offense_date = charge_info[4]
        self.arrest_date = charge_info[5]
        self.complainant = charge_info[6]
        self.amended_charge = charge_info[7]
        self.amended_code = charge_info[8]
        self.amended_case_type = charge_info[9]

        self.final_disposition = dispo_info[0]
        self.sentence_time = dispo_info[1]
        self.sentence_suspended_time = dispo_info[2]
        self.probation_type = dispo_info[3]
        self.probation_time = dispo_info[4]
        self.probation_starts = dispo_info[5]
        self.operator_license_suspension_time = dispo_info[6]
        self.operator_license_suspension_effective_date = dispo_info[7]
        self.operator_license_restriction_codes = dispo_info[8]
        self.fine = dispo_info[9]
        self.costs = dispo_info[10]
        self.fine_costs_due = dispo_info[11]
        self.fine_costs_paid = dispo_info[12]
        self.fine_costs_paid_date = dispo_info[13]
        self.vasap = dispo_info[14]
        
        self.court = court
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)