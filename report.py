import cv2
import numpy as np
import os

INPUT_FOLDER = "images"
OUTPUT_FOLDER = "output"
THRESHOLD = 0.8440

pass_count = 0
fail_count = 0
total = 0

print("=" * 50)
print("   AUTOMATED QUALITY INSPECTION REPORT")
print("   DecodeLabs Internship 2026 - Rahul Bhukal")
print("=" * 50)
print()

for file in sorted(os.listdir(INPUT_FOLDER)):
    if file.endswith(".jpg") or file.endswith(".png"):
        total += 1
        image_path = os.path.join(INPUT_FOLDER, file)
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if not contours:
            continue

        largest = max(contours, key=cv2.contourArea)
        hull_points = cv2.convexHull(largest)
        contour_area = cv2.contourArea(largest)
        hull_area = cv2.contourArea(hull_points)
        solidity = contour_area / hull_area if hull_area > 0 else 0

        if solidity < THRESHOLD:
            status = "FAIL"
            fail_count += 1
        else:
            status = "PASS"
            pass_count += 1

        print(f"  {file:<30} Solidity: {solidity:.4f}   [{status}]")

print()
print("=" * 50)
print(f"  Total Parts Inspected : {total}")
print(f"  Passed                : {pass_count}")
print(f"  Failed                : {fail_count}")
accuracy = (pass_count / 10 * 100 + fail_count / 10 * 100) / 2
print(f"  Accuracy              : {accuracy:.1f}%")
print("=" * 50)