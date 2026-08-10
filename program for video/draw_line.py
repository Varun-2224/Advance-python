import cv2
import numpy as np

# Global variables to store mouse state and drawn lines
drawing = False  # True if mouse is pressed
ix, iy = -1, -1  # Initial x, y coordinates
cx, cy = -1, -1  # Current x, y coordinates
canvas = None    # Overlay canvas to store the drawn lines

def draw_line(event, x, y, flags, param):
    global ix, iy, cx, cy, drawing, canvas

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
        cx, cy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            cx, cy = x, y

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        # Draw the final line on the canvas when the mouse is released
        cv2.line(canvas, (ix, iy), (x, y), (0, 255, 0), 3)  # Green line, thickness 3

def main():
    global canvas, cx, cy, ix, iy, drawing

    # Initialize video capture (0 is usually the default built-in webcam)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    # Create a window and bind the mouse callback function to it
    window_name = 'Live Cam Feed - Draw Line'
    cv2.namedWindow(window_name)
    cv2.setMouseCallback(window_name, draw_line)

    print("Instructions:")
    print("- Click and drag with the Left Mouse Button to draw a line.")
    print("- Press 'c' to clear all drawn lines.")
    print("- Press 'q' to quit.")

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to grab frame.")
            break

        # Flip the frame horizontally for a natural mirror effect
        frame = cv2.flip(frame, 1)

        # Initialize the canvas with the same dimensions as the frame
        if canvas is None:
            canvas = np.zeros_like(frame)

        # Combine the frame and the canvas
        # Find where canvas has drawings (non-zero pixels)
        gray_canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray_canvas, 1, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)

        # Black-out the area of drawings in the frame
        frame_bg = cv2.bitwise_and(frame, frame, mask=mask_inv)
        # Take only region of drawings from canvas
        canvas_fg = cv2.bitwise_and(canvas, canvas, mask=mask)

        # Combine background and foreground
        combined_frame = cv2.add(frame_bg, canvas_fg)

        # If drawing, show a real-time preview of the line being drawn
        if drawing:
            cv2.line(combined_frame, (ix, iy), (cx, cy), (0, 0, 255), 2)  # Red preview line

        # Display the resulting frame
        cv2.imshow(window_name, combined_frame)

        # Key controls
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('c'):
            # Clear canvas
            canvas = np.zeros_like(frame)

    # When everything done, release the capture and close windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
