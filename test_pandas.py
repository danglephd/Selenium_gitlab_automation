import pandas as pd
import csv

class Test_Pandas():

    def read_file(self):

        # Read the CSV file
        # airbnb_data = pd.read_csv("CSV/lanew-5.csv", on_bad_lines='skip')
        # airbnb_data = pd.read_csv("CSV/lanew-5-ANSI.csv", encoding='ANSI')
        airbnb_data = pd.read_csv("CSV/lanew-5-ANSI.csv", on_bad_lines='skip')
        # airbnb_data = pd.read_csv("CSV/ABCD.csv", encoding = "utf-8")

        # View the first 5 rows
        print(airbnb_data.head())


    def test_read_file_csv(self):
        with open('CSV/lanew-5.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            index = 0
            for row in reader:
                if index > 0:
                    print(row)
                else:
                    print('>>>>>This is Header!!!!! ', row)
                    column_count = row.count('|')
                index += 1



