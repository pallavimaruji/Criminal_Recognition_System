import cv2
import sqlite3
import smtplib
cap = cv2.VideoCapture(0)

# Create the haar cascade
faceCascade = cv2.CascadeClassifier("myfacehaarcascade.xml")
rec=cv2.face.LBPHFaceRecognizer_create()
rec.read("recognizer/trainer.yml")
font=cv2.FONT_HERSHEY_DUPLEX
path="dataSet"

def getProfile(id):
	con=sqlite3.connect("database")
	cmd="SELECT * FROM test WHERE ID="+str(id)
	cursor=con.execute(cmd)
	profile=None
	for row in cursor:
		profile=row
	con.close()
	return profile
while(True):
	# Capture frame-by-frame
	ret, frame = cap.read()

	# Our operations on the frame come here
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# Detect faces in the image
	faces = faceCascade.detectMultiScale(gray,scaleFactor=1.3,minNeighbors=5,minSize=(30, 30))
		#flags = cv2.CV_HAAR_SCALE_IMAGE)

	print("Found {0} faces!".format(len(faces)))

	# Draw a rectangle around the faces
	flag=0
	i=""
	for (x, y, w, h) in faces:
		cv2.rectangle(frame, (x ,y), (x+w, y+h), (223, 200, 31), 2)
		id,config=rec.predict(gray[y:y+h,x:x+w])
		if config<85:
			profile=getProfile(id)
		else:
			id=0
			profile=getProfile(id)
		if profile!=None:
			cv2.rectangle(frame, (x ,y), (x+w, y+h), (223, 200, 31), 2)
			cv2.putText(frame,str(profile[1]),(x,y+h),font,1,(0,255,0))
			cv2.putText(frame,str(profile[2]),(x,y+h+30),font,1,(0,255,0))
			cv2.putText(frame,str(profile[3]),(x,y+h+60),font,1,(0,255,0))
			cv2.putText(frame,str(profile[4]),(x,y+h+90),font,1,(0,255,0))
			if str(profile[4])=='YES':
				flag=1
				i=profile[1]

				
		
		

	# Display the resulting frame
	cv2.imshow('Detection Required', frame)
	if flag==1 or cv2.waitKey(10) == 27:
		# When everything done, release the capture
		cap.release()
		cv2.destroyAllWindows()
		
	if flag==1:
		content=i+" (Name of Criminal) \nLocation: Latitude=26.7810587,Longitude=75.8175107"
		mail=smtplib.SMTP('smtp.gmail.com',587)
		mail.ehlo()
		mail.starttls()
		mail.login('nakulswims@gmail.com','bajrangbali1')
		mail.sendmail('nakulswims@gmail.com','nakul12.joshi@gmail.com',content)
		mail.close()
	
