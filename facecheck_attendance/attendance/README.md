# ATTEND EXCEL
The `attend_excel` Python script is designed to read an Excel file containing student data, process the check-in status based on a list of detected names, and save the updated data as a new Excel file. This can be used for keeping track of student attendance in a class or event.

## Usage
```python
from facecheck_attendance.attendance import attend_excel

attend_excel(
    folder_excel_path="input_excel_file_path",
    text_file="input_text_file_path",
)
```