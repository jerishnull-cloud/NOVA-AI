import cv2
from PySide6.QtCore import QThread, Signal


class HandTrackingWorker(QThread):

    movement = Signal(float, float)
    status = Signal(str)

    def __init__(self):
        super().__init__()
        self.running = True

    def stop(self):
        self.running = False

    def run(self):

        camera = None

        try:

            self.status.emit("● STARTING CAMERA")

            camera = cv2.VideoCapture(
                0,
                cv2.CAP_DSHOW
            )

            if not camera.isOpened():

                self.status.emit(
                    "○ CAMERA NOT AVAILABLE"
                )

                return

            # Try MediaPipe
            try:

                import mediapipe as mp

                mp_hands = mp.solutions.hands

                hands = mp_hands.Hands(
                    static_image_mode=False,
                    max_num_hands=1,
                    min_detection_confidence=0.5,
                    min_tracking_confidence=0.5
                )

                self.status.emit(
                    "● HAND TRACKING ACTIVE"
                )

                previous_x = None
                previous_y = None

                while self.running:

                    success, frame = camera.read()

                    if not success:
                        continue

                    frame = cv2.flip(
                        frame,
                        1
                    )

                    rgb = cv2.cvtColor(
                        frame,
                        cv2.COLOR_BGR2RGB
                    )

                    results = hands.process(
                        rgb
                    )

                    if results.multi_hand_landmarks:

                        hand = (
                            results.multi_hand_landmarks[0]
                        )

                        wrist = hand.landmark[
                            mp_hands.HandLandmark.WRIST
                        ]

                        x = wrist.x
                        y = wrist.y

                        if previous_x is not None:

                            dx = x - previous_x
                            dy = y - previous_y

                            if (
                                abs(dx) > 0.006
                                or abs(dy) > 0.006
                            ):

                                self.movement.emit(
                                    dx,
                                    dy
                                )

                        previous_x = x
                        previous_y = y

                    else:

                        previous_x = None
                        previous_y = None

                hands.close()

            except Exception as mediapipe_error:

                self.status.emit(
                    "○ CAMERA READY / HAND AI UNAVAILABLE"
                )

                # Keep camera alive instead of crashing NOVA
                while self.running:

                    success, _ = camera.read()

                    if not success:
                        break

        except Exception as error:

            self.status.emit(
                "○ MOTION SYSTEM OFFLINE"
            )

        finally:

            if camera is not None:
                camera.release()

            self.status.emit(
                "○ MOTION CONTROL STANDBY"
            )