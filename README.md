# Automated Quality Inspection System (Computer Vision)

> A computer vision pipeline that automatically inspects gear parts on a conveyor belt and detects structural defects using OpenCV and Python.

![Python](https://img.shields.io/badge/Python-3.10.11-blue?style=for-the-badge&logo=python)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green?style=for-the-badge)
![Accuracy](https://img.shields.io/badge/Accuracy-100%25-brightgreen?style=for-the-badge)
![DecodeLabs](https://img.shields.io/badge/DecodeLabs-Internship%202026-purple?style=for-the-badge)

---

## Project Overview

This project implements an **Automated Optical Inspection System** that processes images of gear parts and determines whether each part is defective or not — without any human involvement.

Traditional factory inspection relies on human workers checking parts one by one. A human inspector experiences fatigue and is highly likely to miss a 1mm structural defect after checking hundreds of parts in a single shift.

This system replaces the human inspector with a deterministic computer vision pipeline that never gets tired and never misses a defect.

---

## How It Works

The system follows a 3-phase IPO (Input-Process-Output) architecture:

```
+------------------+    +------------------+    +------------------+
|      INPUT       |--->|     PROCESS      |--->|      OUTPUT      |
| Capture & Clean  |    | Extract & Measure|    |  Decide & Act    |
|                  |    |                  |    |                  |
| - Grayscale      |    | - Find Contours  |    | - PASS / FAIL    |
| - Gaussian Blur  |    | - Convex Hull    |    | - Bounding Box   |
| - Thresholding   |    | - Solidity Check |    | - Report         |
+------------------+    +------------------+    +------------------+
```

---

## The 3 Phases Explained

### Phase 1 — Isolating the Signal (Image Cleaning)

Raw images contain noise from dust and lighting. Three steps clean the image:

```python
# Step 1: Convert to grayscale (flatten color to intensity)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Step 2: Gaussian blur (remove high-frequency noise)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Step 3: Threshold (convert to pure black and white)
_, thresh = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY)
```

### Phase 2 — Topological Analysis (Shape Measurement)

Once the image is clean, the system analyzes the geometry:

```python
# Find the outer boundary of the gear
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Calculate solidity (actual area vs convex hull area)
hull_points = cv2.convexHull(largest)
contour_area = cv2.contourArea(largest)
hull_area = cv2.contourArea(hull_points)
solidity = contour_area / hull_area
```

**What is Solidity?**

Imagine stretching a rubber band tightly around the gear:
- Perfect gear — rubber band fits perfectly — solidity close to 1.0
- Defective gear — gap between rubber band and gear — solidity lower

### Phase 3 — The Tolerance Gate (Pass/Fail Decision)

```python
if solidity < 0.8440:
    verdict = "FAIL"  # Structural defect detected
else:
    verdict = "PASS"  # Part is good
```

---

## Results

```
==================================================
   AUTOMATED QUALITY INSPECTION REPORT
   DecodeLabs Internship 2026 - Rahul Bhukal
==================================================
  defective_gear_1.png     Solidity: 0.8419   [FAIL]
  defective_gear_2.png     Solidity: 0.8419   [FAIL]
  ...
  good_gear_1.png          Solidity: 0.8460   [PASS]
  good_gear_2.png          Solidity: 0.8460   [PASS]
  ...
==================================================
  Total Parts Inspected : 20
  Passed                : 10
  Failed                : 10
  Accuracy              : 100.0%
==================================================
```

---

## Project Structure

```
decodelabs_task02/
|-- images/                      # 20 test gear images
|   |-- good_gear_1.png          # 10 perfect gears
|   |-- defective_gear_1.png     # 10 defective gears
|-- output/                      # Processed result images
|-- inspect.py                   # Main inspection pipeline
|-- create_test_images.py        # Test image generator
|-- report.py                    # Final inspection report
└-- README.md
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/rahulji0805/decodelabs_task02.git

# Navigate into the project
cd decodelabs_task02

# Install dependencies
pip install opencv-python numpy
```

### Generate Test Images

```bash
python create_test_images.py
```

### Run Inspection

```bash
python inspect.py
```

### Generate Report

```bash
python report.py
```

---

## Key Concepts Used

- **Grayscale Conversion** — reduces image complexity from 3 channels to 1
- **Gaussian Blur** — removes high-frequency noise using a mathematical kernel
- **Thresholding** — converts grayscale to binary black and white image
- **Contour Detection** — traces the outer boundary of the gear shape
- **Convex Hull** — finds the smallest convex shape enclosing the gear
- **Solidity** — ratio of actual area to convex hull area used as defect metric

---

## Why Computer Vision over Human Inspection?

| Metric | Human Inspector | This System |
|---|---|---|
| Fatigue | Gets tired after 500 parts | Never tires |
| Accuracy | Drops over time | Consistent 100% |
| Speed | Slow | Real-time |
| Cost | High (salary) | One-time setup |
| Minimum defect size | Limited by eye | Pixel-level precision |

---

## Tech Stack

- **Language:** Python 3.10.11
- **Library:** OpenCV 4.x
- **Library:** NumPy
- **IDE:** Visual Studio Code

---

## License

This project is licensed under the MIT License.

---

## Acknowledgements

- **DecodeLabs** — for providing this internship project
- **OpenCV** — for the computer vision library

---

## Author

**Rahul Bhukal**
- Robotics and Automation Intern — DecodeLabs (Batch 2026)
- GitHub: [rahulji0805](https://github.com/rahulji0805)

---

> "Your journey to becoming a professional Robotics Engineer accelerates right here, right now, with the very first bounding box you draw today."
> — DecodeLabs, Project 2