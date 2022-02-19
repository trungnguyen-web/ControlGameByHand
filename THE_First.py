import mediapipe as mp
import cv2
import math


class myPose():
    def __init__(self):
        self.mp_pose = mp.solutions.pose  # khoi tao bien
        self.pose = self.mp_pose.Pose()  # khoi tao ham
        self.mp_drawing = mp.solutions.drawing_utils
        self.shoudler_line_y = 0  # luu vi tri vai nguoi dung

    def detectPose(self, image):
        # chuyen RGB
        imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # Lay ket qua dau ra model
        results = self.pose.process(imageRGB)
        if results.pose_landmarks:
            self.mp_drawing.draw_landmarks(image, landmark_list=results.pose_landmarks,
                                           connections=self.mp_pose.POSE_CONNECTIONS,
                                           landmark_drawing_spec=self.mp_drawing.DrawingSpec(color=(255,255,255),
                                                                                             thickness=3,
                                                                                             circle_radius=3),
                                           connection_drawing_spec=self.mp_drawing.DrawingSpec(color=(0, 0, 255),
                                                                                               thickness=2))
        return image, results

    # Check Dung O Dau, left, right
    def checkPose_LRC(self, image, results):
        # lay kich thuoc anh dau vao, _ nghia la kenh mau tu do
        image_height, image_width, _ = image.shape
        image_mid_width = image_width // 2
        leftShoulder_x = int(results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_SHOULDER].x * image_width)
        rightShoulder_x = int(results.pose_landmarks.landmark(self.mp_pose.PoseLandmark.RIGHT_SHOULDER).x * image_width)

        if (leftShoulder_x < image_mid_width) and (rightShoulder_x <= image_mid_width):
            LRC = "L"
        elif (leftShoulder_x > image_mid_width) and (rightShoulder_x > image_mid_width):
            LRC = "R"
        else:
            LRC = "C"
        # ve duong thang tren man hinh de kiem tra do cao cua vai
        cv2.putText(image, LRC, (5, image_height - 10), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)
        cv2.line(image, (image_mid_width, 0), (image_mid_width, image_height), (255, 255, 255), 2)
        return LRC, image

    def checkPose_JSD(self, image, results):
        image_height, image_width, _ = image.shape
        leftShoulder_y = int(results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_SHOULDER].y * image_height)
        rightShoulder_y = int(
            results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_SHOULDER].y * image_height)

        centerShoulder_y = ads(leftShoulder_y + rightShoulder_y) // 2

        jump_threshold = 30
        down_threshold = 15
        if (centerShoulder_y < self.shoudler_line_y - jump_threshold):
            JSD = "J"
        elif (centerShoulder_y > self.shoudler_line_y + down_threshold):
            JSD = "D"
        else:
            JSD = "C"
        cv2.putText(image, JSD, (5, image_height -50), cv2.FONT_HERSHEY_PLAIN, 2, (2555, 255, 123), 3)
        cv2.line(image, (0, self.shoudler_line_y), (image_width, self.shoudler_line_y), (0, 255, 255), 2)

        return image, JSD

    # HAM XAC DINH KHOANG CACH CO TAY
    def checkPose_Clap(self, image, results):
        image_height, image_width, _ = image.shape

        leftHand = (results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_WRIST].x * image_width,
                    results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_WRIST].y * image_height)

        rightHand = (results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_WRIST].x * image_width,
                     results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_WRIST].y * image_height)

        distance = int(math.hypot(leftHand[0] - rightHand[0], leftHand[1] - rightHand[1]))
        clap_threshold = 100
        if distance < clap_threshold:
            CLAP = "C"
        else:
            CLAP = "N"
        cv2.putText(image, CLAP, (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 3)
        return image, CLAP

    #ham luu location Shoulder
    def save_Shoulder_line_y(self, image,results):
        image_height, image_width = image.shape

        leftShoudler_y = int(results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_SHOULDER].y*image_height)
        rightShoudler_y = int(results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_SHOULDER].y*image_height)
        self.shoudler_line_y = ads(leftShoudler_y + rightShoudler_y) //2
        return
