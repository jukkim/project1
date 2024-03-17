import tkinter as tk
import os
import time

# 파일에서 애니메이션 속도를 읽는 함수
def read_speed_setting():
    try:
        with open("speed_setting.txt", 'r') as file:
            speed_level = int(file.read().strip())
            # 속도 레벨을 밀리초 단위로 변환
            return max(1, min(10, speed_level)) * 100
    except Exception:
        return 1000  # 파일 읽기 실패 시 기본값 1초 (1000ms)

# 파일의 마지막 수정 시간을 체크하는 함수
def check_file_update(last_check):
    try:
        # 파일의 마지막 수정 시간을 가져옴
        mtime = os.path.getmtime("speed_setting.txt")
        if mtime > last_check:
            return mtime, True
    except Exception as e:
        print(f"Error checking file update: {e}")
    return last_check, False

# 애니메이션 업데이트 함수
def update_animation(last_check):
    global x_pos, speed
    # 파일 변경 확인
    last_check, updated = check_file_update(last_check)
    if updated:
        speed = read_speed_setting()
        speed_label.config(text=f"Current Speed: {speed // 100} level")
    # 애니메이션 로직
    x_pos += 10
    if x_pos > canvas.winfo_width():
        x_pos = 0
    canvas.coords(rectangle, x_pos, 10, x_pos+50, 60)
    # 다음 업데이트 예약
    root.after(speed, lambda: update_animation(last_check))

# 메인 윈도우 설정
root = tk.Tk()
root.title("Simple Animation Program")

# 캔버스 생성
canvas = tk.Canvas(root, width=400, height=200)
canvas.pack()

# 캔버스에 사각형 그리기
x_pos = 10
rectangle = canvas.create_rectangle(x_pos, 10, 50, 60, fill="blue")

# 초기 속도 설정
speed = read_speed_setting()

# 현재 속도 표시
speed_label = tk.Label(root, text=f"Current Speed: {speed // 100} level")
speed_label.pack()

# 애니메이션 시작 및 파일 변경 감지 시작
initial_check_time = os.path.getmtime("speed_setting.txt")
update_animation(initial_check_time)

root.mainloop()
