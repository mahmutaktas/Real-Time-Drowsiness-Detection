import dlib
from flask import Flask, Response
import cv2
from flask_socketio import SocketIO, send, emit
from landmark_detection import dlib_detect, process_video, get_global_variable
from time import sleep

app = Flask(__name__)
socketIo = SocketIO(app, cors_allowed_origins="*")

app.host = 'http://127.0.0.1'

video = cv2.VideoCapture(0)

dlib_detector = dlib.get_frontal_face_detector()
dlib_predictor = dlib.shape_predictor("input/shape_predictor_68_face_landmarks.dat")

@app.route('/')
def index():
    return "Default Message"
def gen(vs):

    dlib_detect(vs)

    # while True:
    #     success, image = vs.read()
    #
    #
    #
    #     ret, jpeg = cv2.imencode('.jpg', image)
    #     frame = jpeg.tobytes()
    #     yield (b'--frame\r\n'
    #            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
@app.route('/video_feed')
def video_feed():
    global video
    return Response(process_video(vs=video, detector=dlib_detector, predictor=dlib_predictor, ear_th=0.21, consec_th=3),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@socketIo.on('message')
def handle_json(json):

    print(json)

    while 1:

        dict = get_global_variable()

        print(dict)

        sleep(0.2)

        send(dict, broadcast=True)

    return None

if __name__ == '__main__':
    socketIo.run(app)