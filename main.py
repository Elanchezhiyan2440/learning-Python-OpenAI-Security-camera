import tkinter as tk
import cv2
import winsound
import os

class SecurityCam:
    def __init__(self):
        # Initialize the webcam capture
        self.cam = cv2.VideoCapture(0)

        # Initialize the Tkinter window
        self.root = tk.Tk()
        self.root.geometry("200x100")

        # Create a button to start the security camera
        self.start_button = tk.Button(self.root, text="Start", command=self.start)
        self.start_button.pack(pady=10)

        # Start the Tkinter main loop
        self.root.mainloop()

    def start(self):
        # Define the codec and create a VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

        # Loop through the video frames until the user quits
        while self.cam.isOpened():
            # Read two consecutive frames from the webcam
            ret, frame1 = self.cam.read()
            ret, frame2 = self.cam.read()

            # Find the difference between the two frames
            diff = cv2.absdiff(frame1, frame2)

            # Convert the difference to grayscale
            gray = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)

            # Apply Gaussian blur to the grayscale image
            blur = cv2.GaussianBlur(gray, (5, 5), 0)

            # Apply thresholding to the blurred image
            _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)

            # Dilate the thresholded image to fill in small holes
            dilated = cv2.dilate(thresh, None, iterations=3)

            # Find contours in the dilated image
            contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            # Loop through the contours and draw rectangles around moving objects
            for c in contours:
                if cv2.contourArea(c) < 5000:
                    continue
                x, y, w, h = cv2.boundingRect(c)
                cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
                winsound.PlaySound('alert.wav', winsound.SND_ASYNC)

            # Display the video stream and save the frames to a video file
            cv2.imshow('Security Cam', frame1)
            out.write(frame1)

            # Exit the loop if the user presses 'q'
            if cv2.waitKey(10) == ord('q'):
                break

        # Release the resources and destroy the windows
        self.cam.release()
        out.release()
        cv2.destroyAllWindows()

# Create an instance of the SecurityCam class and start the application
SecurityCam()
