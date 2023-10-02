import csv
import pandas as pd


def read_csv(path, file_name):
    try:
        # Open the CSV file in the root directory
        with open(path + file_name, "r") as csv_file:
            # Create a CSV reader
            csv_reader = csv.reader(csv_file)
            # return csv_reader

            df = pd.DataFrame(csv_reader)
            df.columns = df.iloc[0]
            df = df[1:]
            df.set_index("Date", inplace=True)
            return df

    except FileNotFoundError:
        print("File not found.")
    except PermissionError:
        print(
            "Permission denied. You may need to run the script with administrative privileges."
        )
    except Exception as e:
        print(f"An error occurred: {e}")


path = "/home/denis/backtester_files/"
file_name = "AAPL.csv"

df = read_csv(path, file_name)
print(df)
