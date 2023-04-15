
import json
import os
import glob
import pandas as pd


def createSheetFromJson():
    # Create the sheet directory if it doesn't exist
    sheetDir = "sheet"
    if not os.path.exists(sheetDir):
        os.makedirs(sheetDir)

    # Define the folder path where the JSON files are located
    folder_path = 'json/'

    # Get a list of all JSON files in the folder
    json_files = glob.glob(folder_path + '*.json')

    # Create a Pandas ExcelWriter object with the filename as "Indeed Daily Job Posts.xlsx"
    writer = pd.ExcelWriter(os.path.join(sheetDir, "Indeed Daily Job Posts.xlsx"), engine="xlsxwriter")

    # Loop through each JSON file and create an Excel sheet with the tab name as the filename (without extension)
    for json_file in json_files:
        # Load the JSON file into a Pandas DataFrame
        data = pd.read_json(json_file)

        # Extract the filename without the extension to use as the sheet name
        filename = os.path.splitext(os.path.basename(json_file))[0]

        # Convert the Pandas DataFrame into an Excel sheet with the tab name as the filename
        data.to_excel(writer, index=False, sheet_name=filename)

    # Save the Excel sheet
    writer._save()

    print("Final Excel sheets created from processed JSON file...")






    