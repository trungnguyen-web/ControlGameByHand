import cv2
import pyautogui
from THE_First import myPose
class MyGame():
    def __init__(self):
        self.pose = myPose()
        self.game_started = False
        self.x_positions =1 # 0 : Left, 1: Center, 2: Right
        self.y_positions = 1 # 0: Down, 1:Stand, 2: jump
        self.clap_duration = 0 # so frame ma nguoi dung vo taay

    def move_LRC(self,LRC):
        if LRC=="L":
            for _ in range(self.x_positions):
                pyautogui.press("left")
            self.x_positions= 0
        elif LRC=="R":
            for _ in range(2,self.x_positions,-1):
                pyautogui.press("right")
            self.x_positions=2
        else:
            if self.x_positions == 0 :
                pyautogui.press("right")
            elif self.x_positions == 2:
                pyautogui.press("left")

            self.x_positions =1
        return
    def move_JSD(self,JSD):
        if (JSD=="J") & (self.y_positions==1):
            pyautogui.press('up')
            self.y_positions=2
        elif (JSD=="D") and (self.y_positions==1):
            pyautogui.press('down')
            self.y_positions=0
        elif (JSD=="S") and (self.y_positions!=1):
            self.y_positions=1
        return
    def play_game(self):
        #khoi tao ca mera
        cap = cv2.VideoCapture(0)
        cap.set(3,1280)
        cap.set(4,960)

        while True:
            ret,image = cap.read()
            if ret:

                image= cv2.flip(image,1)
                image_hight,image_width, _ = image.shape
                image, results =self.pose.detectPose(image)

                if results.pose_landmarks:
                        #kiem tra game da chay chua
                    if self.game_started:
                        image, LRC = self.pose.checkPose_LRC(image, results)
                        self.move_LRC(LRC)

                        #kiem tra len xuong
                        image, JSD = self.pose.checkPose_JSD(image, results)
                        self.move_JSD(JSD)
                    else:
                        cv2.putText(image, "Clap your hand to play",(5,image_hight-10),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),3)
                    image, CLAP =self.pose.checkPose_Clap(image,results)
                    if CLAP == 'C':
                        self.clap_duration +=1
                        if self.clap_duration == 10:
                            if self.game_started:
                            #reset
                                self.x_positions = 1
                                self.y_positions =1
                                self.pose.shoudler_line_y(image, results)
                                pyautogui.press('space')
                            else:
                                self.game_started = True
                                self.pose.save_Shoulder_line_y(image,results)
                                pyautogui.click(x=720,y= 560, button ="left" )
                            self.clap_duration =0
                    else:
                        self.clap_duration = 0
                cv2.imshow("Game",image)
            if cv2.waitKey(1) == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
mygame= MyGame()
mygame.play_game()