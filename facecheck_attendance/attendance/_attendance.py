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
COLUMN_NAME = "Name"
CHECKED_IN = "Check-In"
ABSENT = "Absent"

########
# Main #
###############################################################################

@staticmethod
def attend_excel(
        folder_excel_path: str = FOLDER_EXCEL_PATH,
        text_file: str = TEXT_FILE,
        column_name: str = COLUMN_NAME,
        checked_in: str = CHECKED_IN,
        absent: str = ABSENT,
) -> None:

    """
    Reads an Excel file, processes check-in status,
    and saves it as a new Excel file.

    This function reads an Excel file containing student information,
    processes the check-in status of students based on
    detected names in a text file,
    and saves the updated information in a new Excel file.

    Parameters
    ----------
    folder_excel_path : str
        The path to the folder containing the Excel file.

    text_file : str
        The name of the text file containing detected names.

    column_name : str
        The name of the column in
        the Excel file that contains student names.
        Defaults to COLUMN_NAME.

    checked_in : str
        The status to mark a student as checked in.
        Default is "Check-In."

    absent : str
        The status to mark a student as absent.
        Default is "Absent."

    Returns
    -------
    None
        This function does not return a value
        but saves the updated information to a new Excel file.

    Example
    -------
    Consider an Excel file that contains student information
    with a column named "Name." The function reads this file,
    checks if the names in the "Name" column match
    the names detected in the specified text file.
    For students whose names are detected in the text file,
    it marks their attendance as "Check-In."
    For students whose names are not detected,
    it marks their attendance as "Absent."
    The updated information is then saved to a new Excel file.

    attend_excel(
        folder_excel_path=os.path.join("excel/mockup_student.xlsx"),
        text_file=os.path.join("resources/unique_detected_face_names.txt"),
        
        checked_in="Check-in",
        absent="Absent",
    )

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
    excel_dataframe[today_date] = excel_dataframe[column_name].apply(
        lambda name: checked_in if name in detected_names else absent
    )

    # Save the DataFrame to an Excel file
    excel_dataframe.to_excel(folder_excel_path, index=False)

    #######################################################################
