import cv2
import numpy as np
import os

INPUT_FOLDER = "images"
OUTPUT_FOLDER = "output"

def inspect_part(image_path):
    img = cv2.imread(image_path)
    if img is None:
        print(f"Could not load: {image_path}")
        return

    filename = os.path.basename(image_path)
    result_img = img.copy()

    # PHASE 1 - Clean the image
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY)

    # PHASE 2 - Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        print(f"{filename} --> NO PART DETECTED")
        return

    # Get largest contour
    largest = max(contours, key=cv2.contourArea)

    # Calculate solidity (area vs convex hull area)
    hull_points = cv2.convexHull(largest)
    contour_area = cv2.contourArea(largest)
    hull_area = cv2.contourArea(hull_points)

    if hull_area == 0:
        print(f"{filename} --> ERROR")
        return

    # Solidity = how "full" the shape is
    # Perfect gear = close to 1.0
    # Defective gear = lower value (missing tooth = missing area)
    solidity = contour_area / hull_area

    print(f"{filename} --> Solidity: {solidity:.4f}", end=" --> ")

    # PHASE 3 - Verdict based on solidity
    if solidity < 0.8440:
        verdict = "FAIL"
        color = (0, 0, 255)
        print("FAIL - Structural defect detected!")
        # Draw bounding box around defect area
        x, y, w, h = cv2.boundingRect(largest)
        cv2.rectangle(result_img, (x, y), (x+w, y+h), (0, 0, 255), 2)
    else:
        verdict = "PASS"
        color = (0, 255, 0)
        print("PASS - Part is good!")

    # Write verdict on image
    cv2.putText(result_img, verdict, (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)

    # Save output
    output_path = os.path.join(OUTPUT_FOLDER, filename)
    cv2.imwrite(output_path, result_img)


# Run
print("=== Quality Inspection System Started ===\n")
for file in sorted(os.listdir(INPUT_FOLDER)):
    if file.endswith(".jpg") or file.endswith(".png"):
        inspect_part(os.path.join(INPUT_FOLDER, file))

print("\n=== Inspection Complete! Check output folder ===")