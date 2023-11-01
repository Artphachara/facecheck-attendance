from datetime import datetime
import os
import pandas as pd
import timeit

FOLDER_EXCEL_PATH = os.path.join("excel", "mockup_student.xlsx")
TEXT_FILE = os.path.join("resources", "unique_detected_face_names.txt")
CHECKED_IN = "Check-In"
ABSENT = "Absent"

def attend_excel(
        folder_excel_path: str = FOLDER_EXCEL_PATH,
        text_file: str = TEXT_FILE,
        checked_in: str = CHECKED_IN,
        absent: str = ABSENT,
) -> None:

    # Create the full path to the Excel file
    excel_file_path = os.path.join(folder_excel_path)

    # Read the Excel file into a pandas DataFrame
    excel_dataframe = pd.read_excel(excel_file_path)

    # Read the text file and split names
    with open(text_file, "r") as file:
        detected_names = file.read().split(", ")

    today_date = datetime.today().strftime("%d %b %Y")

    # Define a function for the check-in status using a custom function
    def determine_check_in_status_custom(row):
        if row["Name"] in detected_names:
            return checked_in
        else:
            return absent

    # Add a new column for check-in status using the custom function
    excel_dataframe[today_date] = excel_dataframe.apply(
        determine_check_in_status_custom,
        axis=1
    )

    # Save the DataFrame to an Excel file
    excel_dataframe.to_excel(folder_excel_path, index=False)

    # Define a function for the lambda-based check-in status
    def lambda_check_in_status():
        excel_dataframe[today_date] = excel_dataframe["Name"].apply(
            lambda name: checked_in if name in detected_names else absent
        )

    # Measure the execution time of applying the custom function
    custom_function_time = timeit.timeit(
        lambda: excel_dataframe.apply(determine_check_in_status_custom, axis=1),
        number=1000
    )

    # Measure the execution time of applying the lambda function
    lambda_function_time = timeit.timeit(lambda_check_in_status, number=1000)

    print(f"Custom function time taken: {custom_function_time} seconds")
    print(f"Lambda function time taken: {lambda_function_time} seconds")
    print(f"Difference (Custom - Lambda): {lambda_function_time - custom_function_time} seconds")

attend_excel()
