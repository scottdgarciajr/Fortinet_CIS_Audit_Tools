import csv 

import tkinter as tk 

from tkinter import filedialog, scrolledtext 

  

# Global variables for file paths 

documentation_file = "" 

commands_csv_file_path = "" 

  

# Function to handle file upload for documentation CSV 

def upload_documentation_file(): 

    global documentation_file 

    documentation_file = filedialog.askopenfilename() 

    output_text.insert(tk.END, f"Documentation File Path: {documentation_file}\n") 

  

# Function to handle file upload for commands CSV 

def upload_commands_file(): 

    global commands_csv_file_path 

    commands_csv_file_path = filedialog.askopenfilename() 

    output_text.insert(tk.END, f"Commands CSV File Path: {commands_csv_file_path}\n") 

  

# Function to process documentation CSV and generate output 

def process_documentation_csv(output_file): 

    global documentation_file 

    if documentation_file: 

        with open(documentation_file, mode='r') as file: 

            reader = csv.reader(file) 

            data = list(reader) 

  

        with open(output_file, mode='a') as output: 

            for row in data: 

                if len(row) >= 2: 

                    standard = row[0] 

                    documentation = row[1] 

                    output.write("config system alias\n") 

                    output.write(f"edit {standard}doc\n") 

                    output.write('set command "\n') 

                    output.write(f"#{standard} ;{documentation}\n") 

                    output.write('"\n') 

                    output.write("end\n\n") 

  

                    output_text.insert(tk.END, f"Processed standard: {standard}\n") 

  

# Placeholder function to collect standards from the CSV 

def collect_standards_from_csv(csv_file): 

    standards = [] 

    with open(csv_file, newline='') as csvfile: 

        reader = csv.DictReader(csvfile) 

        for row in reader: 

            standards.append(row["Standard Number"]) 

    return standards 

  

# Placeholder function to prepend alias to standards 

def prepend_alias_to_standards(standards): 

    return [f"alias {standard}" for standard in standards] 

  

# Function to chunk a list by length 

def chunk_list_by_length(lst, max_length): 

    chunks = [] 

    current_chunk = [] 

    current_length = 0 

  

    for item in lst: 

        item_length = len(item) 

        if current_length + item_length > max_length: 

            chunks.append(current_chunk) 

            current_chunk = [item] 

            current_length = item_length 

        else: 

            current_chunk.append(item) 

            current_length += item_length 

  

    if current_chunk: 

        chunks.append(current_chunk) 

  

    return chunks 

  

# Function to process commands CSV and generate output commands 

def process_commands_csv(output_file): 

    global commands_csv_file_path 

    if commands_csv_file_path: 

        def print_commands_from_csv(csv_file, output):
            with open(csv_file, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    standard_number = row["Standard Number"]
                    commands = row["Commands"].strip() if "Commands" in row else ""

                    output.write("config system alias\n")
                    output.write(f"edit {standard_number}\n")
                    output.write('set command "\n')
                    output.write(f"show system alias {standard_number}doc | grep -i #{standard_number}\n")
                    if commands:
                        output.write(commands + "\n")
                    output.write('"\n')
                    output.write("end\n\n")
                    
                    output_text.insert(tk.END, f"Processed commands for standard: {standard_number}\n")


  

        standards = collect_standards_from_csv(commands_csv_file_path) 

        prefixed_standards = prepend_alias_to_standards(standards) 

  

        with open(output_file, mode='a') as output: 

            print_commands_from_csv(commands_csv_file_path, output) 

  

            max_length = 200 

            chunks = chunk_list_by_length(prefixed_standards, max_length) 

  

            num_chunks = 0 

            for num_chunks, chunk in enumerate(chunks, start=1): 

                output.write("config system alias\n") 

                output.write(f"edit a{num_chunks}\n") 

                output.write('set command "\n') 

                output.write("\n".join(chunk) + "\n") 

                output.write('"\n') 

                output.write("end\n\n") 

  

            output.write("config system alias\n") 

            output.write("edit cis_audit\n") 

            output.write('set command "\n') 

            for i in range(1, num_chunks + 1): 

                output.write(f"alias a{i}\n") 

            output.write('"\n') 

            output.write("end\n") 

  

            output_text.insert(tk.END, "Finished processing commands CSV\n") 

  

# GUI setup 

root = tk.Tk() 

root.title("Upload Files") 

  

# Title label 

title_label = tk.Label(root, text="Fortinet CIS Auditing Script Generator", font=("Helvetica", 16, "bold")) 

title_label.pack(pady=10) 

  

# Description label 

description_label = tk.Label(root, text="Upload your documentation and commands CSV files to generate a Fortinet CIS auditing script.", font=("Helvetica", 12)) 

description_label.pack(pady=5) 

  

# Buttons for file uploads 

btn_documentation = tk.Button(root, text="Upload Documentation CSV", command=upload_documentation_file) 

btn_documentation.pack(pady=10) 

  

btn_commands = tk.Button(root, text="Upload Commands CSV", command=upload_commands_file) 

btn_commands.pack(pady=10) 

  

# Text widget for displaying output 

output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20) 

output_text.pack(pady=10) 

  

# Text widget for displaying generated script 

generated_text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20) 

generated_text_area.pack(pady=10) 

  

# Function to process files 

def process_files(): 

    output_file_name = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")]) 

    if output_file_name: 

        process_documentation_csv(output_file_name) 

        process_commands_csv(output_file_name) 

        with open(output_file_name, 'r') as file: 

            generated_text = file.read() 

            generated_text_area.delete('1.0', tk.END)  # Clear previous content 

            generated_text_area.insert(tk.END, generated_text) 

        output_text.insert(tk.END, "Done!\n") 

  

btn_process = tk.Button(root, text="Process Files", command=process_files) 

btn_process.pack(pady=20) 

  

root.mainloop() 
