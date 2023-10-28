# Face Recognition Processor
The `FaceRecognitionProcessor` class is a Python script designed for face recognition and processing. It uses the Face Recognition library to recognize faces in images or screen recordings and associate them with known names. The script is suitable for various applications, such as attendance tracking, security, and more.

## Usage
```python
from facecheck_attendance.detect_face import FaceRecognitionProcessor

FaceRecognitionProcessor().load_data(
    image_folder = "input_image_folder_path"
)

try:
        FaceRecognitionProcessor().screenshot_record()
    except KeyboardInterrupt:
        pass

    FaceRecognitionProcessor().save_detected_face_names()

```