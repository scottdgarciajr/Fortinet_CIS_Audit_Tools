import csv 

import tkinter as tk 

from tkinter import filedialog, scrolledtext, simpledialog 

import os 

from tkinter import ttk 

  

def parse_output_to_csv(output, csv_filename): 

    # Split the output by lines 

    lines = output.strip().split('\n') 

  

    # Process each part and extract text before the next "#" 

    extracted_texts = [] 

    current_part = [] 

    current_id = None 

  

    for line in lines: 

        if '#' in line: 

            if current_part: 

                # Extract first line and append to extracted_texts 

                first_line = current_part[0].strip() if current_part else '' 

                line_count = len(current_part) - 1 

  

                # Determine if first line count is a letter 

                if first_line.isdigit(): 

                    if int(first_line) == 0: 

                        is_equal = 0 

                    else: 

                        is_equal = 1 if int(first_line) <= line_count else 0 

                elif first_line == "c": 

                    internets_count = sum(1 for l in current_part if 'Internets' in l or 'omcast' in l) 

                    lines_without_internets = line_count - internets_count 

                    is_equal = 1 if internets_count - lines_without_internets == 1 else 0 

                elif first_line == "y": 

                    is_equal = 1 

                elif first_line == "n": 

                    is_equal = 0 

                elif first_line == ">2": 

                    is_equal = 1 if line_count > 2 else 0 

                elif first_line == "==1": 

                    is_equal = 1 if line_count == 1 else 0 

                elif first_line == "d": 

                    intrazone_count = sum(1 for l in current_part if 'intrazone' in l) 

                    lines_without_intrazone = line_count - intrazone_count 

                    is_equal = 1 if intrazone_count - lines_without_intrazone == 0 else 0 

                elif first_line == "i": 

                    enabled_count = sum(1 for l in current_part if 'scan-botnet-connections' in l) 

                    lines_without_enabled = line_count - enabled_count 

                    is_equal = 1 if enabled_count - lines_without_enabled == 0 else 0 

                elif first_line == "a": 

                    # Ensure the output contains " 2 " and " 6 " 

                    contains_2_and_6 = all(any(f" {num} " in l for l in current_part) for num in [" 2 ", " 6 "]) 

                    is_equal = 1 if contains_2_and_6 else 0 

                elif first_line == "p": 

                    # Ensure the output does not contain 'set category' 

                    does_not_contain_set_category = all('set category' not in l for l in current_part) 

                    is_equal = 1 if does_not_contain_set_category else 0 

                elif first_line == "m": 

                    is_equal = 'Manual; Requires Review' 

                else: 

                    is_equal = '?' 

  

                extracted_texts.append((current_id, '\n'.join(current_part).strip(), first_line, line_count, is_equal)) 

                current_part = [] 

  

            # Extract identifier and text 

            if ';' in line: 

                parts = line.split(';', 1) 

                identifier = parts[0].strip().replace('#', '') 

                current_id = identifier 

                line = parts[1] 

  

            current_part.append(line.strip()) 

        else: 

            current_part.append(line.strip()) 

  

    if current_part: 

        first_line = current_part[0].strip() if current_part else '' 

        line_count = len(current_part) - 1 

  

        if first_line.isdigit(): 

            is_equal = 1 if first_line == str(line_count) else 0 

        else: 

            is_equal = '?' 

  

        extracted_texts.append((current_id, '\n'.join(current_part).strip(), first_line, line_count, is_equal)) 

  

    # Write to CSV file 

    with open(csv_filename, 'w', newline='') as csvfile: 

        csvwriter = csv.writer(csvfile) 

        csvwriter.writerow(['Identifier', 'Text', 'First Line', 'Line Count', 'Standard is Met']) 

  

        for identifier, text, first_line, line_count, is_equal in extracted_texts: 

            csvwriter.writerow([identifier, text, first_line, line_count, is_equal]) 

  

def upload_file(): 

    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")]) 

    if file_path: 

        with open(file_path, 'r') as file: 

            content = file.read() 

            text_box.delete('1.0', tk.END) 

            text_box.insert(tk.END, content) 

  

def prompt_for_filename(): 

    # Prompt the user for a CSV file name 

    csv_filename = simpledialog.askstring("Save CSV", "Enter the CSV file name (with .csv extension):") 

    return csv_filename 

  

def generate_csv(): 

    csv_filename = prompt_for_filename() 

    if csv_filename: 

        output = text_box.get('1.0', tk.END) 

        parse_output_to_csv(output, csv_filename) 

        status_label.config(text=f"CSV generated successfully as {csv_filename}.") 

        display_csv_button.config(state=tk.NORMAL) 

    else: 

        status_label.config(text="CSV generation canceled.") 

  

def display_csv_file(): 

    csv_filename = 'cis_audit.csv' 

    if os.path.exists(csv_filename): 

        with open(csv_filename, 'r', newline='') as csvfile: 

            csvreader = csv.reader(csvfile) 

            data = list(csvreader) 

  

        # Create a new window to display CSV content 

        display_window = tk.Toplevel(root) 

        display_window.title("CSV Content") 

  

        # Create a Treeview widget with scrollbars 

        tree = ttk.Treeview(display_window, columns=data[0], show="headings") 

        tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True) 

  

        # Add scrollbars 

        vsb = ttk.Scrollbar(display_window, orient="vertical", command=tree.yview) 

        vsb.pack(side=tk.RIGHT, fill=tk.Y) 

        tree.configure(yscrollcommand=vsb.set) 

  

        # Set column headings (first row of CSV) 

        for col in data[0]: 

            tree.heading(col, text=col) 

  

        # Insert data rows into the Treeview 

        for row in data[1:]: 

            tree.insert("", tk.END, values=row) 

  

    else: 

        status_label.config(text="CSV file does not exist.") 

  

# Create the main window 

root = tk.Tk() 

root.title("Output to CSV Converter") 

  

# Create a text box for input/output 

text_box = scrolledtext.ScrolledText(root, width=80, height=20) 

text_box.pack(padx=10, pady=10) 

  

# Button to upload file 

upload_button = tk.Button(root, text="Upload File", command=upload_file) 

upload_button.pack(pady=5) 

  

# Button to generate CSV 

generate_button = tk.Button(root, text="Generate CSV", command=generate_csv) 

generate_button.pack(pady=5) 

  

# Button to display CSV 

display_csv_button = tk.Button(root, text="Display CSV", command=display_csv_file, state=tk.DISABLED) 

display_csv_button.pack(pady=5) 

  

# Status label 

status_label = tk.Label(root, text="", fg="green") 

status_label.pack(pady=5) 

  

# Start the GUI main loop 

root.mainloop() 
