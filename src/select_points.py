"""
Run this script OUTSIDE Jupyter to select corresponding points on c1 and c2.
    uv run python src/select_points.py

An OpenCV window opens for each image.
Click 6 landmarks in the SAME order on both images.
Points are saved to data/selected_points.npz for the notebook to load.
"""
import cv2 as cv
import numpy as np

N = 6
p1 = np.empty((N, 2))
p2 = np.empty((N, 2))
n  = 0

def draw_circle(event, x, y, flags, param):
    global n
    p = param[0]
    if event == cv.EVENT_LBUTTONDOWN:
        cv.circle(param[1], (x, y), 5, (0, 0, 255), -1)
        cv.putText(param[1], str(n + 1), (x + 8, y - 8),
                   cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        p[n] = (x, y)
        n += 1
        print('  Point %d: (%d, %d)' % (n, x, y))

im1 = cv.imread('data/c1.jpg', cv.IMREAD_REDUCED_COLOR_4)
im2 = cv.imread('data/c2.jpg', cv.IMREAD_REDUCED_COLOR_4)
im1copy = im1.copy()
im2copy = im2.copy()

# --- Image 1 ---
print('=== Click %d points on Image 1 (c1) ===' % N)
n = 0
cv.namedWindow('Image 1 — click %d points' % N, cv.WINDOW_AUTOSIZE)
param = [p1, im1copy]
cv.setMouseCallback('Image 1 — click %d points' % N, draw_circle, param)

while True:
    cv.imshow('Image 1 — click %d points' % N, im1copy)
    if n >= N:
        break
    if cv.waitKey(20) & 0xFF == 27:
        break
cv.destroyAllWindows()

# --- Image 2 ---
print('=== Click %d MATCHING points on Image 2 (c2) in the same order ===' % N)
n = 0
cv.namedWindow('Image 2 — click %d points' % N, cv.WINDOW_AUTOSIZE)
param = [p2, im2copy]
cv.setMouseCallback('Image 2 — click %d points' % N, draw_circle, param)

while True:
    cv.imshow('Image 2 — click %d points' % N, im2copy)
    if n >= N:
        break
    if cv.waitKey(20) & 0xFF == 27:
        break
cv.destroyAllWindows()

print('\np1 (reduced coords):\n', p1)
print('p2 (reduced coords):\n', p2)

# Scale up to full resolution (IMREAD_REDUCED_COLOR_4 = 1/4 size)
np.savez('data/selected_points.npz', p1=p1, p2=p2, reduce_factor=4)
print('\nSaved to data/selected_points.npz')
