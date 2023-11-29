import os
import re
import pandas as pd
from tkinter import filedialog


def get_file_path():
    while True:
        file_path = filedialog.askopenfilename(
            title="Select a file",
            filetypes=[("Python files", "*.py")]
        )

        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            continue

        return file_path


def make_csv(file_path, output_file_path=None):
    with open(file_path, 'r') as file:
        data = file.read()

    # Extract the exhibit mapping (assuming it's a dictionary)
    exhibit_mapping_pattern = r"exhibit_mapping\s*=\s*{(.*?)}\n"
    exhibit_mapping_str = re.search(exhibit_mapping_pattern, data, re.DOTALL)
    exhibit_mapping = {}
    if exhibit_mapping_str:
        exhibit_mapping_str = exhibit_mapping_str.group(1).strip()
        for item in exhibit_mapping_str.split(","):
            key, value = item.split(":")
            exhibit_mapping[key.strip()] = value.strip()

    # Extract the imports
    imports = re.findall(r"import\s+(.+?)\n", data)

    # Create a CSV representation of the file
    csv_rows = []
    header = ["name", "type", "value", "line_number", "placeholder"]
    for exhibit_name, exhibit_code in exhibit_mapping.items():
        placeholder = None
        for line_number, line in enumerate(data.split("\n")):
            if line.startswith(f"def {exhibit_name}()\n"):
                if line_number + 1 < len(data.split("\n")):
                    if data.split("\n")[line_number + 1].strip() == "pass":
                        placeholder = line_number + 2
                break

        csv_row = [
            exhibit_name,
            "function",
            exhibit_code,
            data.find(f"def {exhibit_name}()\n") + 1,
            placeholder
        ]

        csv_rows.append(csv_row)

    df = pd.DataFrame(csv_rows, columns=header)

    if output_file_path:
        df.to_csv(output_file_path, index=False)

    return df, imports, header


def get_code_smells(df, imports, header):
    placeholder_functions = df[df["type"] == "function"]
    placeholder_functions = placeholder_functions[placeholder_functions["value"].str.contains("pass")]

    liposuctioned_functions = df[df["type"] == "function"]
    liposuctioned_functions = liposuctioned_functions[liposuctioned_functions["value"].str.startswith("#")]

    doppelganger_functions = df[df["type"] == "function"].groupby(["name"])["value"].filter(lambda x: len(x) > 1)

    redundant_imports = [import_name for import_name in imports if import_name not in header]

    doppelganger_functions_no_comment = doppelganger_functions[~doppelganger_functions["value"].str.startswith("#")]

    return (
        placeholder_functions,
        liposuctioned_functions,
        doppelganger_functions_no_comment,
        redundant_imports
    )


def prioritize_codes(df, placeholder_functions, liposuctioned_functions, doppelganger_functions_no_comment, redundant_imports):
    df["priority"] = 0

    for code_smells in (placeholder_functions, liposuctioned_functions, doppelganger_functions_no_comment, redundant_imports):
        for code_smell in code_smells:
            df.loc[df["name"] == code_smell, "priority"] += 10

    return df


def main():
    file_path = get_file_path()

    df, imports, header = make_csv(file_path)

    placeholder_functions, liposuctioned_functions, doppelganger_functions_no_comment, redundant_imports = get_code_smells(df, imports, header)

    df = prioritize_codes(df, placeholder_functions, liposuctioned_functions, doppelganger_functions_no_comment, redundant_imports)
    print(df)


if __name__ == "__main__":
    main()

