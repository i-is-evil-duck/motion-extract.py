import cv2
import os

def subtractive_motion_tracking(input_path, output_path):
    cap = cv2.VideoCapture(input_path)

    if not cap.isOpened():
        print(f"cant open vid: {input_path}")
        return

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height), isColor=True)
    backSub = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=50, detectShadows=False)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        fg_mask = backSub.apply(gray)
        highlight = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        highlight[fg_mask > 0] = [0, 0, 255]
        out.write(highlight)

    cap.release()
    out.release()
    print(f"saved: {output_path}")

if __name__ == "__main__":
    input_path = input("path to input: ").strip()

    if not os.path.exists(input_path):
        print("file not found")
    else:
        base, ext = os.path.splitext(input_path)
        output_path = base + "_motion.mp4"

        subtractive_motion_tracking(input_path, output_path)
