###########
# Imports #
###############################################################################

from datetime import datetime
import os
import pandas as pd

#############
# Constants #
###############################################################################

FOLDER_EXCEL_PATH = os.path.join("excel", "mockup_student.xlsx")
TEXT_FILE = os.path.join("resources", "unique_detected_face_names.txt")

def attend_excel(
        folder_excel_path=FOLDER_EXCEL_PATH,
        text_file=TEXT_FILE,
) -> pd.DataFrame:

    """
    Read an Excel file, process check-in status, and save it as a new Excel file.

    Args:
        folder_path (str): The path to the folder containing the Excel file.
        excel_file (str): The name of the Excel file.
        txt_file (str): The name of the text file containing detected names.
        output_excel_file (str): The name of the output Excel file.

    Returns:
        pd.DataFrame: The Excel data with check-in status as a DataFrame.
    """

    # Create the full path to the Excel file
    excel_file_path = os.path.join(folder_excel_path)

    # Read the Excel file into a pandas DataFrame
    excel_dataframe = pd.read_excel(excel_file_path)

    # Read the text file and split names
    with open(text_file, "r") as file:
        detected_names = file.read().split(", ")

    today_date = datetime.today().strftime("%d %b %Y")

    # Add a new column for check-in status
    excel_dataframe[today_date] = excel_dataframe["Name"].apply(
        lambda name: "Check-In" if name in detected_names else "Not in class"
    )

    # Save the DataFrame to an Excel file
    excel_dataframe.to_excel(folder_excel_path, index=False)

    #######################################################################
