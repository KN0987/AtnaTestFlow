import AtnaTestFlow as testflow

def main():
    part_number = input("Enter part number:")
    print("Part Number:", part_number[3:7])

    test_program_path = testflow.get_test_program_path(part_number[3:7])
    print("Test Program Path:", test_program_path)

    test_steps = testflow.get_test_steps(part_number[3:7])
    print("Test Steps:", test_steps)

    pds_type = testflow.get_pds(part_number[3:7])
    print("PDS:", pds_type)

    pds_file = []
    is_automative = testflow.isPartAutomative(part_number[3:7])
    
    has_saunders = False
    if "Saunders" in test_steps:
        has_saunders = True

    if is_automative:
        for step in test_steps:
            if step == "FT0":
                pds_file.append(f"{pds_type}_ft_auto.pds")
            elif step == "Post HE":
                pds_file.append(f"{pds_type}_posthe_auto.pds")
            elif step == "QA":
                if has_saunders:
                    pds_file.append(f"{pds_type}_rsc_auto.pds")
                else:
                    pds_file.append(f"{pds_type}_qa_auto.pds")
    else:
        for step in test_steps:
            if step == "FT0":
                pds_file.append(f"{pds_type}_ft.pds")
            elif step == "Post HE":
                pds_file.append(f"{pds_type}_posthe.pds")
            elif step == "QA":
                if has_saunders:
                    pds_file.append(f"{pds_type}_rsc.pds")
                else:
                    pds_file.append(f"{pds_type}_qa.pds")
    
    print("PDS Files:", pds_file)


if __name__ == "__main__":
    main()