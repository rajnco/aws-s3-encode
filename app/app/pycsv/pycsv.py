import csv
import json
import os
import yaml

class PYCSV:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.csv_reader = csv.DictReader(open(self.file_path))
        self.data = [row for row in self.csv_reader]

    def to_json(self, json_file_path: str):
        print(f"file name {json_file_path}")
        json.dump(self.data, open(json_file_path, "w"), indent=4)

    def to_yaml(self, yaml_file_path: str):
        print(f"file name {yaml_file_path}")
        yaml.safe_dump(self.data, open(yaml_file_path, "w"), indent=4, width=4)





def main():
    """ """
    input_dir = "app/in/"
    output_dir = "app/out/"

    files = os.listdir(input_dir)
    current_directory = os.getcwd()
    for file_name in files:
        file_in_path = os.path.join(current_directory, input_dir, file_name)
        csv = PYCSV(file_in_path)
        file_out_name = file_name.replace("csv", "json")
        file_out_path = os.path.join(current_directory, output_dir, file_out_name)
        csv.to_json(file_out_path)      
        file_out_name2 = file_name.replace("csv", "yaml")
        file_out_path2 = os.path.join(current_directory, output_dir, file_out_name2)
        csv.to_yaml(file_out_path2)      
    


if __name__ == "__main__":
    main()
