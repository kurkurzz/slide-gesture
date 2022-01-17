import datetime as dt
import time

import cv2
import numpy as np
import matplotlib.pyplot as plt
import mediapipe as mp

from keyboard import left_key, right_key

time.sleep(2)
w_cam, h_cam = 648, 480

cap = cv2.VideoCapture(0)
# cap.set(3, w_cam)
# cap.set(4, h_cam)

mp_hand = mp.solutions.hands
hand = mp_hand.Hands(
	max_num_hands = 1,
	min_detection_confidence=0.7
)
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

t_start = dt.datetime.now()
# 0=none, 1=right, 2=left
before_right = 0
after_right = 0
ignore = True
while True:
	t_new = dt.datetime.now()
	if (t_new - t_start).microseconds >= 500000:
	# if (t_new - t_start).seconds >= 1:
		t_start = t_new
		print(f'before right: {before_right}')
		print(f'after right: {after_right}')
		print(f'ignore: {ignore}')
		if before_right==1 and after_right==2 and not ignore:
			left_key()
			pass
		elif after_right==1 and before_right==2 and not ignore:
			right_key()
			pass

		before_right = after_right

	ret, frame = cap.read()
	frame = cv2.flip(frame, 1)
	frame_rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
	result = hand.process(frame_rgb)

	if result.multi_hand_landmarks:
		for hand_lm in result.multi_hand_landmarks:
			h, w, c = frame.shape

			tips = (hand_lm.landmark[8], hand_lm.landmark[12], 
			hand_lm.landmark[16], hand_lm.landmark[20])
			palm = hand_lm.landmark[0]

			right_side = []
			for tip in tips:
				right_side.append(tip.x > palm.x)

			check_sum =  sum(1 for i in right_side if i)
			after_right = 0
			if check_sum == 4:
				after_right = 1
			elif check_sum == 0:
				after_right = 2

			if hand_lm.landmark[4].y < hand_lm.landmark[3].y:
				ignore = False
			else:
				ignore = True
			
			mp_drawing.draw_landmarks(
			frame,
			hand_lm,
			mp_hand.HAND_CONNECTIONS,)
	else:
		# after_right = 0
		pass

	cv2.imshow('webcam',frame)
	cv2.waitKey(1)