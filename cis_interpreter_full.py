import csv
import tkinter as tk
from tkinter import filedialog, scrolledtext, simpledialog
import os
from tkinter import ttk

def parse_output_to_csv(output, csv_filename):
    lines = output.strip().split('\n')
    extracted_texts = []
    current_part = []
    current_id = None

    for line in lines:
        if '#' in line:
            if current_part:
                first_line = current_part[0].strip() if current_part else ''
                line_count = len(current_part) - 1
                # Handle various conditions to determine if 'Standard is Met'
                # (Code unchanged from original for brevity)

                extracted_texts.append((current_id, '\n'.join(current_part).strip(), first_line, line_count, is_equal))
                current_part = []

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

def upload_directory():
    directory = filedialog.askdirectory()
    if directory:
        files = [f for f in os.listdir(directory) if f.endswith('.txt')]
        if not files:
            status_label.config(text="No .txt files found in directory.")
            return

        output_dir = os.path.join(directory, "mass_audit_tables")
        os.makedirs(output_dir, exist_ok=True)

        for file in files:
            input_file_path = os.path.join(directory, file)
            output_file_path = os.path.join(output_dir, f"{os.path.splitext(file)[0]}.csv")

            with open(input_file_path, 'r') as file:
                output = file.read()

            parse_output_to_csv(output, output_file_path)

        status_label.config(text=f"CSV files generated successfully in {output_dir}.")
        display_csv_button.config(state=tk.NORMAL)
    else:
        status_label.config(text="Directory selection canceled.")

def display_csv_file():
    csv_directory = filedialog.askdirectory()
    if csv_directory:
        csv_files = [f for f in os.listdir(csv_directory) if f.endswith('.csv')]
        if not csv_files:
            status_label.config(text="No .csv files found in directory.")
            return

        # Display CSV files (Code to display CSV files in a new window - unchanged from original)

    else:
        status_label.config(text="CSV display canceled.")
def generate_csv():
    output = text_box.get('1.0', tk.END)
    if not output.strip():
        status_label.config(text="No text to generate CSV.")
        return

    csv_filename = prompt_for_filename()
    if csv_filename:
        parse_output_to_csv(output, csv_filename)
        status_label.config(text=f"CSV generated successfully as {csv_filename}.")
        display_csv_button.config(state=tk.NORMAL)
    else:
        status_label.config(text="CSV generation canceled.")

root = tk.Tk()
root.title("Output to CSV Converter")

text_box = scrolledtext.ScrolledText(root, width=80, height=20)
text_box.pack(padx=10, pady=10)

upload_button = tk.Button(root, text="Upload File", command=upload_file)
upload_button.pack(pady=5)

upload_directory_button = tk.Button(root, text="Upload Directory", command=upload_directory)
upload_directory_button.pack(pady=5)

generate_button = tk.Button(root, text="Generate CSV", command=generate_csv)
generate_button.pack(pady=5)

display_csv_button = tk.Button(root, text="Display CSV", command=display_csv_file, state=tk.DISABLED)
display_csv_button.pack(pady=5)

status_label = tk.Label(root, text="", fg="green")
status_label.pack(pady=5)

root.mainloop()
