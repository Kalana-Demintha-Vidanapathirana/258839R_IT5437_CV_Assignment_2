# IT5437 — Computer Vision · Assignment 2
**Fitting and Alignment**

> **Student:** Kalana Vidanapathirana · **Index:** 258839R  
> **Programme:** MSc in Artificial Intelligence · University of Moratuwa  
> **Course:** IT5437 Computer Vision

---

## Overview

This assignment covers three classical computer vision problems:

| # | Problem | Techniques |
|---|---------|-----------|
| 1 | Line fitting on noisy point sets | Total Least Squares (TLS), RANSAC |
| 2 | Physical size estimation from a single image | Camera/lens geometry, contour detection |
| 3 | Circuit board alignment and comparison | Homography, image differencing, SIFT |

---

## Project Structure

```
Assignment_2/
├── data/                        # Input data
│   ├── lines.csv                # 100×6 point dataset (3 line groups)
│   ├── c1.jpg, c2.jpg           # Circuit board images
│   ├── earrings.jpg             # Earrings image for size estimation
│   └── selected_points.npz      # Saved click-points for Q3 (generated)
│
├── src/                         # Solution notebooks and scripts
│   ├── problem1_line_fitting.ipynb
│   ├── problem2_camera_geometry.ipynb
│   ├── problem3_alignment.ipynb
│   ├── select_points.py         # Interactive point selector for Q3a
│   └── build_report.py          # Generates 258839R.docx
│
├── notebooks/                   # Lecture reference notebooks (a–f)
├── reference_images/            # Lecture sample images
├── output/                      # Generated figures (auto-created on run)
├── 258839R.docx                 # Submitted report
├── it5437_assignment_02.pdf     # Assignment specification
├── pyproject.toml               # uv project + dependencies
└── uv.lock                      # Reproducible lock file
```

---

## Setup

This project uses [uv](https://github.com/astral-sh/uv) for dependency management.

```bash
# Clone the repo
git clone https://github.com/Kalana-Demintha-Vidanapathirana/Assignment_2.git
cd Assignment_2

# Install all dependencies (creates .venv automatically)
uv sync

# Launch JupyterLab
uv run jupyter lab
```

**Python version:** 3.12  
**Key libraries:** `opencv-python`, `numpy`, `matplotlib`, `scipy`, `scikit-image`

---

## Running the Solutions

### Question 1 — Line Fitting
Open and run [`src/problem1_line_fitting.ipynb`](src/problem1_line_fitting.ipynb)

- **Part (a):** TLS via SVD on the first line group
- **Part (b):** Sequential RANSAC to recover all three lines from 300 mixed points

### Question 2 — Earring Size
Open and run [`src/problem2_camera_geometry.ipynb`](src/problem2_camera_geometry.ipynb)

No interaction needed — runs end-to-end automatically.

### Question 3 — Circuit Board Alignment

**Step 1:** Select corresponding points interactively (run this *outside* Jupyter — OpenCV windows don't work inside the kernel):

```bash
uv run python src/select_points.py
```

Two windows open. Click **6 landmarks in the same order** on each image. Points are saved to `data/selected_points.npz`.

**Step 2:** Open and run [`src/problem3_alignment.ipynb`](src/problem3_alignment.ipynb) top to bottom.

---

## Results Summary

### Q1 — Line Fitting

| Part | Method | Result |
|------|--------|--------|
| (a) | Total Least Squares | `a=-0.7736, b=0.6337, d=-3.7942` · residual=0.406 |
| (b) | RANSAC (3 lines) | 83 + 66 + 62 inliers · 89 unassigned (near intersections) |

TLS outperforms ordinary LS by minimising orthogonal distances — it is unaffected by which axis the error is measured along, making it the correct choice for geometric line fitting.

### Q2 — Earring Size

| Camera parameter | Value |
|-----------------|-------|
| Focal length `f` | 8 mm |
| Object distance `u` | 720 mm |
| Image distance `v` | 8.090 mm |
| Magnification `m` | 0.01124 |
| Scale | **0.1958 mm/pixel** |

| Measurement | Pixels | Real size |
|-------------|--------|-----------|
| Outer diameter | 418 px | **81.84 mm** |
| Inner diameter | 316 px | **61.87 mm** |
| Band width | 51 px | **9.99 mm** |

### Q3 — Circuit Board Alignment

> Both `c1.jpg` and `c2.jpg` are the **same board** photographed from different viewpoints (manually transformed). The ideal difference image after alignment is therefore zero.

| Part | Result |
|------|--------|
| (a) Manual H | 6 clicked points → DLT homography → warped image |
| (b) Diff image | Residual highlights manual alignment error, not board changes |
| (c) SIFT | 4172/4500 keypoints · **2641 good matches** (Lowe's ratio test, t=0.7) |
| (d) Auto H | RANSAC with 2523 inliers · mean pixel diff ≈ 0.8/255 (near-perfect) |

**Auto > Manual:** SIFT+RANSAC uses ~420× more correspondences and has built-in outlier rejection, producing a near-perfect alignment where manual clicking introduces ~20-pixel errors at full resolution.

---

## Key Observations

- **TLS vs OLS:** TLS is the correct method when both x and y have noise; OLS only minimises vertical error and gives biased results for tilted lines.
- **RANSAC robustness:** Sequential RANSAC works well when line groups are spatially separated but struggles near intersection regions — the 89 unassigned points all sit in overlap zones.
- **Camera geometry:** The large magnification ratio (u/v ≈ 89) means small pixel-measurement errors produce relatively large real-world size errors.
- **Homography accuracy:** The difference image is the clearest quantitative measure — a darker image means better alignment.

---

## Report

The 4-page report (`258839R.docx`) is included in the repository root. It covers all three questions with code snippets, result figures, and discussion.

---

## References

- Lecture notebooks: `notebooks/` (provided by course)
- OpenCV documentation: https://docs.opencv.org
- Lowe, D.G. (2004). Distinctive image features from scale-invariant keypoints. *IJCV*.
