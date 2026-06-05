import cv2
import numpy as np
import os

os.makedirs("images", exist_ok=True)

def create_good_gear(filename):
    img = np.zeros((400, 400), dtype=np.uint8)
    # Draw perfect gear - center circle
    cv2.circle(img, (200, 200), 150, 255, -1)
    cv2.circle(img, (200, 200), 80, 0, -1)
    # Draw perfect teeth all around
    for angle in range(0, 360, 20):
        rad = np.radians(angle)
        x = int(200 + 165 * np.cos(rad))
        y = int(200 + 165 * np.sin(rad))
        cv2.circle(img, (x, y), 18, 255, -1)
    cv2.imwrite(f"images/{filename}", img)
    print(f"Created: {filename}")

def create_defective_gear(filename):
    img = np.zeros((400, 400), dtype=np.uint8)
    # Draw gear with missing tooth (defect)
    cv2.circle(img, (200, 200), 150, 255, -1)
    cv2.circle(img, (200, 200), 80, 0, -1)
    # Draw teeth but SKIP one to create defect
    for angle in range(0, 360, 20):
        if angle == 40:  # missing tooth here
            continue
        rad = np.radians(angle)
        x = int(200 + 165 * np.cos(rad))
        y = int(200 + 165 * np.sin(rad))
        cv2.circle(img, (x, y), 18, 255, -1)
    cv2.imwrite(f"images/{filename}", img)
    print(f"Created: {filename}")

# Create 10 good gears
for i in range(1, 11):
    create_good_gear(f"good_gear_{i}.png")

# Create 10 defective gears
for i in range(1, 11):
    create_defective_gear(f"defective_gear_{i}.png")

print("\nAll 20 test images created in images/ folder!")