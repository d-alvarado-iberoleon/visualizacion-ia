import cv2
import numpy as np
import matplotlib.pyplot as plt

COLORS = [(0,255,0),(255,0,0),(0,165,255),(0,255,255),(255,0,255)]

def canvas(img_l, img_r, pts_l, pts_r, scale):
    c = np.hstack([img_l.copy(), img_r.copy()])
    W = img_l.shape[1]
    for i, (l, r) in enumerate(zip(pts_l, pts_r)):
        col = COLORS[i % len(COLORS)]
        rc = (r[0] + W, r[1])
        cv2.circle(c, l, 10, col, -1)
        cv2.circle(c, rc, 10, col, -1)
        cv2.line(c, l, rc, col, 3)
        cv2.putText(c, str(i+1), l, cv2.FONT_HERSHEY_SIMPLEX, 1, col, 1)
    h, w = c.shape[:2]
    return cv2.resize(c, (int(w * scale), int(h * scale)))

def click(event, x, y, flags, params):
    img_l, img_r, pts_l, pts_r, scale = params
    if event != cv2.EVENT_LBUTTONDOWN: return
    ox, oy = int(x / scale), int(y / scale)
    W = img_l.shape[1]
    if len(pts_l) == len(pts_r) and ox < W:
        pts_l.append((ox, oy))
    elif len(pts_l) > len(pts_r) and ox >= W:
        pts_r.append((ox - W, oy))
    cv2.imshow("win", canvas(img_l, img_r, pts_l, pts_r, scale))

def get_correspondences():
    img_l = cv2.imread("img_izq.jpeg")
    img_r = cv2.imread("img_der.jpeg")
    pts_l, pts_r = [], []

    SCREEN_W = 1400
    scale = SCREEN_W / (img_l.shape[1] + img_r.shape[1])
    params = (img_l, img_r, pts_l, pts_r, scale)

    cv2.namedWindow("win")
    cv2.setMouseCallback("win", click, params)  # <-- params se pasa aquí
    cv2.imshow("win", canvas(*params))

    while True:
        k = cv2.waitKey(20) & 0xFF
        if k == ord('q'): break
        if k == ord('z'):
            if pts_l: pts_l.pop()
            if pts_r: pts_r.pop()
        if k == ord('s'):
            np.savetxt("pts_l.csv", pts_l, fmt="%d,%d")
            np.savetxt("pts_r.csv", pts_r, fmt="%d,%d")
        cv2.imshow("win", canvas(*params))

    cv2.destroyAllWindows()
    return np.array(pts_l), np.array(pts_r)

def find_homography(pts_l, pts_r):
    assert len(pts_l) == 4

    A = []
    for (x, y), (xp, yp) in zip(pts_l, pts_r):
        A.append([-x, -y, -1,  0,  0,  0, xp*x, xp*y, xp])
        A.append([ 0,  0,  0, -x, -y, -1, yp*x, yp*y, yp])
    
    A = np.array(A)
    A8 = A[:, :8]
    b = -A[:, 8]
    
    h = np.linalg.solve(A8, b)
    H = np.append(h, 1).reshape(3, 3)
    
    return H

def warp(img_l, img_r, H):
    h, w = img_l.shape[:2]
    canvas_h, canvas_w = h*3, w*3 
    output = np.zeros((h*3, w*3, 3), dtype=np.uint8)
    T = np.array([[1, 0, -w], [0, 1, -h], [0, 0, 1]])  # Traslación para centrar img_l
    H_inv = H@T #np.linalg.inv(T@H)

    xs, ys = np.meshgrid(np.arange(canvas_w), np.arange(canvas_h))
    ones   = np.ones_like(xs)
    pts    = np.stack([xs.ravel(), ys.ravel(), ones.ravel()]).astype(float)

    pts_src = H_inv @ pts
    pts_src /= pts_src[2]

    xs_src = pts_src[0].reshape(canvas_h, canvas_w).astype(int)
    ys_src = pts_src[1].reshape(canvas_h, canvas_w).astype(int)

    mask = (xs_src >= 0) & (xs_src < img_r.shape[1]) & \
           (ys_src >= 0) & (ys_src < img_r.shape[0])
    print("Mask")
    print(mask.shape)
    output[mask] = img_r[ys_src[mask], xs_src[mask]]

    output[h:2*h, w:2*w] = img_l  

    return output

def recortar(panorama):
    # máscara de píxeles no negros
    mask = panorama > 0

    filas = np.any(mask, axis=1)
    cols  = np.any(mask, axis=0)

    y1, y2 = np.where(filas)[0][[0, -1]]
    x1, x2 = np.where(cols)[0][[0, -1]]

    return panorama[y1:y2, x1:x2]

#pt1, pt2 = get_correspondences()
pt1 = np.loadtxt("pts_l.csv", delimiter=",", dtype=int)
pt2 = np.loadtxt("pts_r.csv", delimiter=",", dtype=int)

H = find_homography(pt1, pt2)
print("Matriz de homografía:")
print(H)

output = warp(cv2.imread("img_izq.jpeg"), cv2.imread("img_der.jpeg"), H)
output = recortar(output)
plt.imshow(cv2.cvtColor(output, cv2.COLOR_BGR2RGB))
plt.axis("off")
plt.show()
