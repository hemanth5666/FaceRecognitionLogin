from flask import Flask, render_template, request, jsonify
import cv2
import face_recognition
import os

app = Flask(__name__)

# Define the path to the authorized user image
authorized_image_path = "D:/project/face/authorized_user.jpg"

# Check if the authorized user image exists
if os.path.exists(authorized_image_path):
    # Load the sample image of the authorized user
    try:
        authorized_image = face_recognition.load_image_file(authorized_image_path)
        authorized_encoding = face_recognition.face_encodings(authorized_image)[0]
    except Exception as e:
        raise RuntimeError("Error loading authorized user image: " + str(e))
else:
    raise FileNotFoundError("Authorized user image not found. Please check the file path.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    try:
        # Capture frame from webcam
        video_capture = cv2.VideoCapture(0)
        ret, frame = video_capture.read()
        video_capture.release()

        if not ret:
            raise RuntimeError("Failed to capture frame from webcam.")

        # Convert the image from BGR color (OpenCV) to RGB color (face_recognition)
        rgb_frame = frame[:, :, ::-1]

        # Perform face recognition
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        # Compare face encoding with authorized user's encoding
        if len(face_encodings) > 0:
            match = face_recognition.compare_faces([authorized_encoding], face_encodings[0])
            if match[0]:
                return jsonify({'success': True})
            else:
                return jsonify({'success': False, 'message': 'Face recognition failed. Face not recognized.'})
        else:
            return jsonify({'success': False, 'message': 'No face detected in the image.'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
