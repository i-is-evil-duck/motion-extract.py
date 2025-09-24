import cv2
import numpy as np
import os

def nothing(x):
    pass

def motion_preview_render():
    input_path = input("Enter the path to the input video file: ").strip()
    if not os.path.isfile(input_path):
        print("Error: File not found.")
        return

    output_path = "output.mp4"

    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps    = cap.get(cv2.CAP_PROP_FPS)

    cv2.namedWindow("Motion Extract")
    cv2.createTrackbar("Delay", "Motion Extract", 2, 150, nothing)
    cv2.createTrackbar("Alpha", "Motion Extract", 50, 100, nothing)

    buffer = []

    while True:
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            buffer.clear()
            continue

        delay = cv2.getTrackbarPos("Delay", "Motion Extract")
        alpha = cv2.getTrackbarPos("Alpha", "Motion Extract") / 100.0
        inverted = 255 - frame
        buffer.append(inverted)

        if len(buffer) > delay:
            delayed_inverted = buffer[-(delay+1)]
            blended = cv2.addWeighted(frame, 1-alpha, delayed_inverted, alpha, 0)
        else:
            blended = frame

        cv2.imshow("Motion Extract", blended)

        key = cv2.waitKey(int(1000/fps)) & 0xFF

        if key == 27:
            break
        elif key == ord('r'):  #render
            print(f"Rendering to {output_path} with delay={delay} frames and alpha={alpha}")
            render_video(input_path, output_path, delay, alpha)

    cap.release()
    cv2.destroyAllWindows()

def render_video(input_path, output_path, delay, alpha):
    cap = cv2.VideoCapture(input_path)
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps    = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    buffer = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        inverted = 255 - frame
        buffer.append(inverted)

        if len(buffer) > delay:
            delayed_inverted = buffer[-(delay+1)]
            blended = cv2.addWeighted(frame, 1-alpha, delayed_inverted, alpha, 0)
        else:
            blended = frame

        out.write(blended)

    cap.release()
    out.release()
    print("Rendering complete.")

if __name__ == "__main__":
    motion_preview_render()
