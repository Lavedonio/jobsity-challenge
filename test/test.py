import csv
import requests
from copy import deepcopy


TEST_FILE = "trips.csv"


def read_csv(filename: str) -> dict:
    """
        Reads a CSV an returns a list of dictionaries
    """
    data = []
    data_dict = {}
    with open(TEST_FILE) as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=",")

        # Parsing columns
        columns = next(csv_reader)
        for key in columns:
            if key == "datetime":
                key = "date_time"
            data_dict[key] = ""

        # Adding rows
        for row in csv_reader:
            data_model = deepcopy(data_dict)

            for key, value in zip(columns, row):
                if key == "datetime":
                    data_model["date_time"] = value.replace(" ", "T")
                    print(value)
                else:
                    data_model[key] = value

            data.append(data_model)

    return data


def main():
    print("Reading CSV...")
    data = read_csv(TEST_FILE)
    number_of_rows = len(data)
    print(f"{number_of_rows} row retrieved.")

    url = "http://localhost:8000/api/trip/"
    print("Adding data to API...")
    for index, datapoint in enumerate(data, start=1):
        response = requests.post(url, data=datapoint)
        if response.status_code in [200, 201]:
            print(f"({index} / {number_of_rows}) Datapoint added.")
        else:
            print(
                f"({index} / {number_of_rows}) Error! Status code {response.status_code} | Datapoint discarded.")

    print("Done.")


if __name__ == "__main__":
    main()
