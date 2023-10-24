###########
# Imports #
###############################################################################

from datetime import datetime
import logging
import os
import signal
from typing import List

import cv2
import face_recognition
import numpy as np
from PIL import ImageGrab

#############
# Constants #
###############################################################################

THRESHOLD = 0.6
IMAGE_FOLDER = "data"

#########
# Class #
###############################################################################

class FaceRecognitionProcessor():
    """
    Class for face recognition processing.

    Attributes:
        known_face_encodings (list): List of known face encodings.
        known_face_names (list): List of known face names.
        logger (Logger): Logger for the class.

    """
    #############
    # Functions #
    #######################################################################

    def __init__(self):

        """
        Initialize the FaceRecognitionProcessor class.

        Initializes the known_face_encodings and known_face_names lists.

        """

        # Initialize your known_face_encodings and known_face_names lists

        self.known_face_encodings = []
        self.known_face_names = []
        self.detected_face_names = []
        self.logger = self.setup_logger()
        
        self.output_file = "resources"
        self.file_name = "unique_detected_face_names.txt"

        signal.signal(signal.SIGINT, self.handle_exit)

    #######################################################################

    @staticmethod
    def setup_logger():

        """
        Set up the logger for the class.

        Returns:
            Logger: The logger instance.

        """

        logger = logging.getLogger("FaceRecognition")
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        return logger

    #######################################################################

    def load_data(self, image_folder: str = IMAGE_FOLDER) -> None:

        """
        Load known face data from image files.

        Args:
            image_folder (str): Path to the folder containing image files.

        """

        self.known_face_encodings = []
        self.known_face_names = []

        for filename in os.listdir(image_folder):
            if filename.endswith(".jpg"):
                # Extract the name from
                # the image filename without the extension
                name = os.path.splitext(filename)[0]

                # Load a sample picture and learn how to recognize it.
                image = face_recognition.load_image_file(
                    os.path.join(image_folder, filename)
                )
                face_encoding = face_recognition.face_encodings(image)[0]

                # Append the face encoding and name to the lists
                self.known_face_encodings.append(face_encoding)
                self.known_face_names.append(name)

    #######################################################################

    def process_faces(self, detected_face_encodings,):

        """
        Process detected faces and return their names.

        Args:
            detected_face_encodings (list): List of detected face encodings.

        Returns:
            list: List of names corresponding to the detected faces.

        """

        face_names = []

        for face_encoding in detected_face_encodings:
            name = "Unknown"
            if self.known_face_encodings:
                face_distances = face_recognition.face_distance(
                    self.known_face_encodings,
                    face_encoding
                )
                best_match_index = np.argmin(face_distances)

                if face_distances[best_match_index] < THRESHOLD:
                    name = self.known_face_names[best_match_index]
            
            if name not in self.detected_face_names:
                self.detected_face_names.append(name)  # Collect unique face names

            face_names.append(name)

        return face_names

    #######################################################################

    def screenshot_record(
            self,
            record: bool = True,
            output_folder: str = None,
    ) -> None:

        """
        Record the screen and perform face recognition.

        Args:
            record (bool): Whether to continue recording.
            output_folder (str): Path to the output folder for frames.

        """

        if output_folder is None:

            output_folder = os.path.join(
                "Result",
                "Output_Frames_" + datetime.now().strftime('%Y%m%d_%H%M%S')
            )

        os.makedirs(output_folder, exist_ok=True)

        frame_count = 0

        while record:

            # Initialize some variables
            face_locations: List[tuple] = []
            face_encodings: List[np.ndarray] = []
            face_names: List[str] = []

            printscreen = np.array(ImageGrab.grab())

            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(
                cv2.cvtColor(printscreen, cv2.COLOR_BGR2RGB)
            )
            face_encodings = face_recognition.face_encodings(
                cv2.cvtColor(printscreen, cv2.COLOR_BGR2RGB),
                face_locations
                )

            face_names = self.process_faces(face_encodings)
            print(face_names)

            for (top, right, bottom, left), name in zip(face_locations, face_names):
                cv2.rectangle(
                    printscreen,
                    (left, top),
                    (right, bottom),
                    (0, 0, 255),
                    2
                )
                cv2.rectangle(
                    printscreen,
                    (left, bottom - 35),
                    (right, bottom),
                    (0, 0, 255),
                    cv2.FILLED
                )

                font = cv2.FONT_HERSHEY_DUPLEX

                cv2.putText(
                    printscreen,
                    name,
                    (left + 6, bottom - 6),
                    font,
                    1.0,
                    (255, 255, 255),
                    1
                )

            frame_count += 1
            frame_filename = os.path.join(
                output_folder,
                f"frame_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            )
            cv2.imwrite(
                frame_filename,
                cv2.cvtColor(printscreen, cv2.COLOR_BGR2RGB)
            )

    #######################################################################

    def save_detected_face_names(self):

        os.makedirs(self.output_file, exist_ok=True)

        filtered_names = [
            name for name in self.detected_face_names if name != "Unknown"
        ]
        # Use "a" to append to the file, not overwrite it
        with open(os.path.join(self.output_file, self.file_name), "w") as file:
            file.write(", ".join(filtered_names))  # Save names with commas

    #######################################################################

    def handle_exit(self, signum, frame):
        # Handle program exit (e.g., Ctrl+C) by saving the data
        self.save_detected_face_names()
        exit(0)

    #######################################################################
