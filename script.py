import cv2
import numpy as np
import av
import math
grayscaleColors = 8
# 16 colors would have "grayscaleColors" as 16
# 32 colors would have "grayscaleColors" as 8
# 64 colors would have "grayscaleColors" as 4
# 128 colors would have "grayscaleColors" as 2
# 256 colors would have "grayscaleColors" as 1
# 8 (32 grayscale colors) is recommended. Any higher any you just get less artifacts in the video.

import os
os.system('cls') # Clear console

def remove_duplicates(input_string):
    # This is a very simple type of video compression. This groups pixels together that are the same colors
    # For example, Here are 3 pixels: `3 3 2`
    # Each value inbetween the space is the grayscale color value.

    # This is what the function does to those pixels: `3 #1 2`
    # The "#1" means that the value before it repeats 1 more time.
    # This saves a lot of space is there are many repeated pixels.
    values = input_string.split()
    compressed_values = []

    current_value = values[0]
    count = 1

    for i in range(1, len(values)):
        if values[i] == current_value:
            count += 1
        else:
            if count > 1:
                compressed_values.append(f"{current_value}#{count - 1}")
            else: 
                compressed_values.append(f"{current_value}")
            current_value = values[i]
            count = 1

    compressed_values.append(f"{current_value}#{count - 1}" if count > 1 else current_value)

    compressed_string = ' '.join(compressed_values)
    return compressed_string

videoPath = input("What is the video name? (example: funnyvideo.mp4): ")

############################################################################################################## VIDEO DATA!

# Load the video file
cap = cv2.VideoCapture(videoPath)
if not cap.isOpened(): exit(print("Unable to open"))

# Get some basic video data
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
frameNumber = 0

# Make a place for the converted grayscale video to be saved
grayscale_video_path = 'grayscale.mp4'
out = cv2.VideoWriter(grayscale_video_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height), isColor=False)

############################################################################################################## MAKE VIDEO GRAYSCALE

print("Converting video to grayscale")
while True:
    ret, frame = cap.read()
    frameNumber += 1

    print("\rFRAME: " + str(frameNumber), end='', flush=True)

    if not ret: break # if ret is true then the video is playing, hasnt reached the end

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # convert the frame to grayscale
    out.write(gray_frame) # write the grayscale frame to the output file

cap, out.release()
cv2.destroyAllWindows()
print("\nDone!")

############################################################################################################## MAKE VIDEO COLOR MAP

print("Creating a color map for video")

container = av.open(grayscale_video_path)
total_frames = container.streams.video[0].frames
pixelsCache = ""

with open("colors.txt", "w") as f:
    f.write("") # Remove everything
    f.write(f"{str(width)} {str(height)} {str(fps)}\n") # Header of the text file
    for i, frame in enumerate(container.decode(video=0)): # For every frame
        pixel_array = np.array(frame.to_image()) # Get the numpy array of the frame's pixels
        pixelNumber = 0

        for row in pixel_array: # For each row of pixels (Every pixel across the x axis)
            for pixel in row: # For every pixel
                pixelNumber += 1
                color = math.floor(pixel[2] / grayscaleColors) # New grayscale color, with quantization

                if pixelNumber == 1:
                    pixelsCache += str(color)
                else:
                    pixelsCache += " " + str(color)
        
        f.write(remove_duplicates(pixelsCache) + "\n")
        pixelsCache = ""
        print("\rFRAME: " + str(i) + " / " + str(total_frames), end='', flush=True)

print("\nDone!")