import cv2
import numpy as np
import pyautogui
import time
import os
import subprocess

def check_and_click_templates(template_paths, threshold=0.8):
    # 截图并转换为灰度图
    screenshot = pyautogui.screenshot()
    screenshot_gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

    for template_path in template_paths:
        # 读取模板图像
        template = cv2.imread(template_path, 0)
        if template is None:
            print(f"未找到模板图像：{template_path}")
            continue

        w, h = template.shape[::-1]
        result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(result >= threshold)

        if len(loc[0]) > 0:
            for pt in zip(*loc[::-1]):
                center_x = pt[0] + w // 2
                center_y = pt[1] + h // 2
                print(f"匹配成功：{os.path.basename(template_path)}，点击位置：({center_x}, {center_y})")
                pyautogui.moveTo(center_x, center_y)
                pyautogui.click()

                # 如果点击的是 a6，启动另一个脚本,提前启动一点，加载需要时间
                if os.path.basename(template_path) == "a6.png":
                    print("正在启动躲避导弹...")
                    subprocess.Popen(['python', 'control.py'])

                return True  # 成功点击后退出函数
    print("本轮未匹配到任何图像")
    return False

# ========== 主程序循环 ==========
template_dir = 'templates'  # 存放模板图像的文件夹
template_paths = [
    os.path.join(template_dir, 'start_button.png'),
    os.path.join(template_dir, 'a6.png'),
    os.path.join(template_dir, 'confirm.png'),
    os.path.join(template_dir, 'hao.png'),
    os.path.join(template_dir, 'done.png'),
    os.path.join(template_dir, 'a1.png'),
    os.path.join(template_dir, 'a2.png'),
    os.path.join(template_dir, 'a3.png'),
    os.path.join(template_dir, 'a4.png'),
    os.path.join(template_dir, 'a5.png'),
    os.path.join(template_dir, 'a7.png'),
]

interval = 2  # 每隔2秒检测一次

print("自动程序启动 3秒后开始...")
time.sleep(3)

try:
    while True:
        check_and_click_templates(template_paths)
        time.sleep(interval)
except KeyboardInterrupt:
    print("已停止程序。")

