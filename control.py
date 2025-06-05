import cv2
import numpy as np
import pyautogui
import time
from PIL import ImageGrab
from ultralytics import YOLO
import random

# YOLO 模型路径
MODEL_PATH = 'D:/大学/py/pythonProject2/ltzj/yolo/runs/detect/train4/weights/best.pt'
model = YOLO(MODEL_PATH)

# 屏幕区域
SCREEN_REGION = (961, 152, 1606, 1375)  # (left, top, right, bottom)
WIDTH = SCREEN_REGION[2] - SCREEN_REGION[0]
HEIGHT = SCREEN_REGION[3] - SCREEN_REGION[1]

# 标签名
JET_CLASS_NAME = 'jet'
BULLET_CLASS_NAME = 'bullet'

# 截图
def screenshot():
    img = ImageGrab.grab(bbox=SCREEN_REGION)
    img_np = np.array(img)
    return cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

# 拖动飞机左右移动
def drag_plane(cx, cy, offset=40):
    screen_x = SCREEN_REGION[0] + int(cx)
    screen_y = SCREEN_REGION[1] + int(cy)

    # 随机选择向左（-offset）或向右（+offset）
    direction = random.choice([-1, 1])
    target_x = screen_x + direction * offset

    direction_str = "左" if direction == -1 else "右"
    print(f"🚀 避开子弹，从 ({screen_x}, {screen_y}) 向{direction_str} 移动")

    pyautogui.moveTo(screen_x, screen_y)
    pyautogui.mouseDown()
    pyautogui.moveTo(target_x, screen_y, duration=0.2)
    pyautogui.mouseUp()
    time.sleep(0.2)
# 主程序
def main():
    print("3 秒后开始监控飞机与子弹...")
    time.sleep(3)

    while True:
        frame = screenshot()
        results = model(frame, conf=0.05)[0]

        jet_box = None
        bullets = []

        for box in results.boxes:
            cls_id = int(box.cls[0])
            label = model.names[cls_id]
            x1, y1, x2, y2 = box.xyxy[0]

            if label == JET_CLASS_NAME:
                jet_box = (x1, y1, x2, y2)
            elif label == BULLET_CLASS_NAME:
                bullets.append((x1, y1, x2, y2))

        if jet_box:
            jx1, jy1, jx2, jy2 = jet_box
            jet_cx = (jx1 + jx2) / 2
            jet_cy = (jy1 + jy2) / 2
            danger = False

            for bx1, by1, bx2, by2 in bullets:
                bullet_cx = (bx1 + bx2) / 2

                # 判断 bullet 横坐标是否在 jet 范围内（允许 ±10 容差）
                if jx1 - 10 <= bullet_cx <= jx2 + 10:
                    danger = True
                    print("⚠️ 检测到子弹可能命中，开始移动躲避")
                    break

            if danger:
                drag_plane(jet_cx, jet_cy)
            else:
                print("✅ 安全，没有子弹命中风险")
        else:
            print("❌ 未检测到飞机")

        time.sleep(0.5)

if __name__ == '__main__':
    main()
