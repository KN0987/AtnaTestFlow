valid_part_number = ["9356", "9357", "9551", "9371", "9375", "9376", "9377", "9396", "9501", "9504", "9505", "9507"]

map_test_program_to_part = {
    "S:\\ets\\apps\\ATNA_8_0_x8_VS15_SCONLY": ["9356", "9357", "9551", "9396", "9505", "9504"],
    "E:\\ets\\apps\\ATNA_ENG_7_1_1_x8_VS15": ["9501"],
    "E:\\ets\\apps\\ATNA_ENG_7_5_x8_VS15": ["9371", "9375", "9376", "9377"],
    "S:\\ets\\apps\\ATNA_10_0_x8_VS15_ENG_Final_C_QUAD": ["9507"]
}

map_pds_to_part = {
    "jg2": ["9356", "9357", "9371", "9375", "9376", "9377", "9396", "9505"],
    "jg1": ["9551", "9501"],
    "jg0": ["9507"]
}


map_material_to_part = {
    "9375A": ["9356", "9357", "9371", "9375", "9376", "9377", "9396"],
    "9375B": ["9356", "9357", "9371", "9375", "9376", "9377", "9396", "9505", "9504", "9507"],
    "9501A": ["9501", "9551"], 
     "9501B": ["9501", "9551"]
}


endura_part_numbers = ["9356", "9357", "9551"]
automative_part_numbers = ["9396", "9397", "9398"]
test_steps = ["FT0", "Helium Bake", "Post HE", "Saunders", "QA"]

def check_valid_part_number(part_number):
    if part_number[0:3] != 'SIT':
        return False
    return part_number[3:7] in valid_part_number

def get_material_version(part_number):
    output = set()
    for material, parts in map_material_to_part.items():
        if part_number in parts:
             output.add(material)
    if len(output) >= 1:
        return output
    return "Can't Read Part Number"

def get_material_size(part_number):
    map_size = { 'P': '2016', 'A' : 2520, 'B' : 3225}
    for i in range(len(part_number)):
        char = part_number[i]
        if char.isalpha():
            if char == 'A' or char == 'B' or char == 'P':
                return map_size[char]
    return 'Unknown Size'

def get_test_program_path(part_number):
    for path, parts in map_test_program_to_part.items():
        if part_number in parts:
            return path
    return "Unknown Part Number"

def get_test_steps(part_number):
    temp = test_steps.copy()
    if part_number in endura_part_numbers:
        return temp
    elif part_number in automative_part_numbers:
        temp.remove("Saunders")
        return temp
    else:
        temp.remove("Helium Bake")
        temp.remove("Post HE")
        temp.remove("Saunders")
        return temp
    
def get_pds(part_number):
    for pds, parts in map_pds_to_part.items():
        if part_number in parts:
            return pds
    return "Unknown Part Number"

def isPartAutomative(part_number):
    return part_number in automative_part_numbers
    
