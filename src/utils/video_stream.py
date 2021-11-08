import cv2
import numpy as np 
import pickle
import struct
import datetime

class VideoStream:
    FRAME_HEADER_LENGTH = 5
    DEFAULT_IMAGE_SHAPE = (512, 512) #(380, 280)
    VIDEO_LENGTH = np.inf
    DEFAULT_FPS = 25

    # if it's present at the end of chunk,
    # it's the last chunk for current jpeg (end of frame)
    JPEG_EOF = b'\xff\xd9'

    def __init__(self, file_path: str):
        # Read the video file here
        self.vid = cv2.VideoCapture(0)

        # frame number is zero-indexed
        # after first frame is sent, this is set to zero
        self.current_frame_number = -1

    def close(self):
        # After the loop release the cap object
        self.vid.release()
        
        # Destroy all the windows
        cv2.destroyAllWindows()

    def get_next_frame(self) -> bytes:
        
        while True:
            self.ret, self.frame = self.vid.read()

            timestamp = datetime.datetime.now()
            cv2.putText(self.frame, timestamp.strftime(
                "%I:%M:%S.%f"), (10, self.frame.shape[0] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

            cv2.putText(self.frame, 'frame: '+str(self.current_frame_number), (10, self.frame.shape[0] - 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

            # Display the resulting frame
            cv2.imshow('frame', self.frame)

            ret, buf = cv2.imencode(".jpg", self.frame)
            
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

            self.current_frame_number += 1
        
            return  bytes(buf) #bytearray(buf)