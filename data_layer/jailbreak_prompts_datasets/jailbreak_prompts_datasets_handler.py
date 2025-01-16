import csv


def format_csv_to_two_columns(existing_csv_path: str, new_csv_path: str) -> None:
    """
    The function takes an existing CSV file, extracts the Name and prompt columns,
    and generates a new CSV file containing only these two columns.
    :param existing_csv_path: path of exiting csv file
    :param new_csv_path: path of new csv file to be created
    :return: None
    """
    # Open the original CSV file and the new CSV file with UTF-8 encoding
    with open(existing_csv_path, mode='r', newline='', encoding='utf-8') as infile, \
         open(new_csv_path, mode='w', newline='', encoding='utf-8-sig') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Get the header row and strip BOM from the first column
        header = next(reader)
        header[0] = header[0].lstrip('\ufeff').strip()  # Remove BOM and any extra spaces
        # print(header[0])
        # Find indices of 'Name' and 'Prompt' columns (case-insensitive)
        # name_index = header[0].index("Name")
        prompt_index = header.index("Prompt")

        # Write the new header with only 'Name' and 'Prompt'
        writer.writerow(["Name", "Prompt"])

        # Write rows with only 'Name' and 'Prompt' columns
        for row in reader:
            # writer.writerow([row[name_index], row[prompt_index]])
            writer.writerow([row[0], row[prompt_index]])


def create_list_of_pairs_names_and_prompts_from_csv(csv_file_path: str) -> list:
    """
    The function iterates through all records in the CSV file, formats each as a pair of strings (Name, Prompt),
    and stores the pairs in a list.
    :param csv_file_path: csv file path
    :return: list of pairs (Name, Prompt)
    """
    pairs = []

    with open(csv_file_path, mode='r', newline='', encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)

        # Skip the header row
        next(reader, None)  # Skip the first row (header)

        # Iterate over each remaining row in the CSV
        for row in reader:
            if len(row) > 1:  # Ensure the second column exists
                name = row[0]
                prompt = row[1]
                formatted_prompt = f""" {prompt} """
                pairs.append((name, formatted_prompt))
        return pairs


# if __name__ == '__main__':
#     format_csv_to_two_columns('dataset.csv',
#                               'first_dataset.csv')
#     prompts = create_list_of_prompts_from_csv('jailbreak_prompts_datasets/first_dataset.csv')
