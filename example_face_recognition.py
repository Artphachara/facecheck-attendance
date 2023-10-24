###########
# Imports #
###############################################################################

from facecheck_attendance.detect_face import FaceRecognitionProcessor

########
# Main #
###############################################################################

if __name__ == "__main__":
    
    face_processor = FaceRecognitionProcessor()
    face_processor.load_data()

    try:
        face_processor.screenshot_record()
    except KeyboardInterrupt:
        pass  # Handle Ctrl+C gracefully

    # Save the data before exiting
    face_processor.save_detected_face_names()

###############################################################################
