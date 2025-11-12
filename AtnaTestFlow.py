map_test_program_to_part = {
    "S:\\ets\\apps\\ATNA_8_0_x8_VS15_SCONLY": ["9356", "9357", "9551", "9396", "9501", "9505"],
    "E:\\ets\\apps\\ATNA_ENG_7_5_x8_VS15": ["9371", "9375", "9376", "9377"],
    "S:\\ets\\apps\\ATNA_10_0_x8_VS15_ENG_Final_B": ["9507"]
}

map_pds_to_part = {
    "jg2": ["9356", "9357", "9371", "9375", "9376", "9377", "9396", "9505"],
    "jg1": ["9551", "9501"],
    "jg0": ["9507"]
}


endura_part_numbers = ["9356", "9357", "9551"]
automative_part_numbers = ["9396", "9397", "9398"]
test_steps = ["FT0", "Helium Bake", "Post HE", "Saunders", "QA"]


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
    
