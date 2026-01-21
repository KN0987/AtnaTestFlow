import threading
import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
import os

import AtnaTestFlow as testflow


class TemplateGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Atna Test Flow")
        self.geometry("700x450")
        
        # Set window icon if it exists
        icon_path = os.path.join(os.path.dirname(__file__), 'icon.ico')
        if os.path.exists(icon_path):
            try:
                self.iconbitmap(icon_path)
            except Exception:
                pass  # Icon not available, continue without it

        # Part number input
        frame = tk.Frame(self)
        frame.pack(fill="x", padx=10, pady=8)

        tk.Label(frame, text="Part Number:").pack(side="left")
        self.part_entry = tk.Entry(frame, width=30)
        self.part_entry.pack(side="left", padx=(6, 10))

        self.generate_btn = tk.Button(frame, text="Generate", command=self.on_generate)
        self.generate_btn.pack(side="left")

        self.clear_btn = tk.Button(frame, text="Clear", command=self.clear_log)
        self.clear_btn.pack(side="left", padx=(6, 0))

        # Results area
        results_frame = tk.Frame(self)
        results_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        tk.Label(results_frame, text="Output:").pack(anchor="w")
        self.log = scrolledtext.ScrolledText(results_frame, state="normal", wrap="word")
        self.log.pack(fill="both", expand=True)

        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status = tk.Label(self, textvariable=self.status_var, anchor="w")
        status.pack(fill="x", side="bottom")

    def append_log(self, text):
        self.log.configure(state="normal")
        self.log.insert("end", text + "\n")
        self.log.see("end")
        self.log.configure(state="disabled")

    def clear_log(self):
        self.log.configure(state="normal")
        self.log.delete("1.0", "end")
        self.log.configure(state="disabled")

    def on_generate(self):
        part = self.part_entry.get().strip()
        if not part or len(part) < 7:
            messagebox.showerror("Input error", "Please enter a valid part number (at least 7 chars). Example: 'XXX9356YYY'")
            return

        # disable UI while running
        self.generate_btn.config(state="disabled")

        short_part = part[3:7]
        

        def worker():
            try:
                test_program_path = testflow.get_test_program_path(short_part)
                test_steps = testflow.get_test_steps(short_part)
                pds_type = testflow.get_pds(short_part)
                is_automative = testflow.isPartAutomative(short_part)
                material_version = testflow.get_material_version(short_part)
                
                part_to_find_size = part[part.find('-'):]
                material_size = testflow.get_material_size(part_to_find_size)
                
                material_code = []
                map_material_size = {'2016': 'P', '2520': 'A', '3225': 'B'}
                for material in material_version:
                    suffix = map_material_size.get(str(material_size))
                    if not suffix:
                        raise ValueError(f"Unknown material size: {material_size}")
                    material_code.append(f"{material}-{suffix}")
                
                has_saunders = False
                if "Saunders" in test_steps:
                    has_saunders = True

                pds_file = []
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

                results = {
                    "test_program_path": test_program_path,
                    "test_steps": test_steps,
                    "pds_type": pds_type,
                    "is_automative": is_automative,
                    "pds_file": pds_file,
                    "material_code": material_code,
                    "material_size": material_size
                }
            except Exception as e:
                results = {"error": str(e)}

            # update UI from main thread
            self.after(0, lambda: self.show_results(results))

        threading.Thread(target=worker, daemon=True).start()

    def show_results(self, results):
        self.generate_btn.config(state="normal")
        self.clear_log()
        
        if "error" in results:
            self.append_log("Error: " + results["error"])
            self.status_var.set("Error")
            return

        self.append_log("Material Code: " + str(results['material_code']))
        self.append_log("Socket Size: " + str(results['material_size']))
        self.append_log(f"Test Program Path: {results['test_program_path']}")
        self.append_log(f"PDS: {results['pds_type']}")
        self.show_test_steps(results['test_steps'], results['pds_file'])
             
        self.status_var.set("Ready")
    
    def show_test_steps(self, steps, pds_files):
        def step_seperator():
            self.append_log("|")
            self.append_log("V")
        self.append_log("")
        self.append_log("===================================")
        self.append_log("")
        self.append_log("Test Steps:")
        self.append_log("")
        j = 0
        for i in range(len(steps)):
            if steps[i] != "Saunders" and steps[i] != "Helium Bake":
                self.append_log(f"Step {i+1} - {steps[i]} ({pds_files[j]})")
                j += 1
            elif steps[i] == "Saunders":
                self.append_log(f"Step {i+1} - {steps[i]} - (Master Branch)")
            elif steps[i] == "Helium Bake":
                self.append_log(f"Step {i+1} - {steps[i]} - (16 Hours, 45 PSI)")
            if i != len(steps) - 1:
                step_seperator()