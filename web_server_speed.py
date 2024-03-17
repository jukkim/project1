from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# 파일에서 애니메이션 속도를 읽는 함수
def read_speed_setting():
    try:
        if os.path.exists("speed_setting.txt"):
            with open("speed_setting.txt", 'r') as file:
                speed_level = int(file.read().strip())
                return speed_level
        return None
    except Exception as e:
        return str(e)

# 속도 설정을 파일에 저장하는 함수
def update_speed_setting(speed_level):
    try:
        with open("speed_setting.txt", 'w') as file:
            file.write(str(speed_level))
            return True
    except Exception as e:
        return str(e)

@app.route('/speed', methods=['GET'])
def speed():
    new_speed = request.args.get('set')
    if new_speed:
        try:
            new_speed = int(new_speed)
            if 1 <= new_speed <= 10:
                result = update_speed_setting(new_speed)
                if result is True:
                    return jsonify({'success': True, 'speed': new_speed})
                else:
                    return jsonify({'success': False, 'error': result}), 500
            else:
                return jsonify({'success': False, 'error': 'Invalid speed value. Must be between 1 and 10.'}), 400
        except ValueError:
            return jsonify({'success': False, 'error': 'Invalid input. Speed must be an integer.'}), 400
    else:
        # 현재 속도 값 조회
        current_speed = read_speed_setting()
        if current_speed is not None:
            return jsonify({'success': True, 'speed': current_speed})
        else:
            return jsonify({'success': False, 'error': 'Speed setting not found or error reading file.'}), 404

if __name__ == '__main__':
    app.run(debug=True)
