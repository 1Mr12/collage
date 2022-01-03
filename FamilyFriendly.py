#!/usr/bin/env python

from os import times


try:
	import cv2
	import subprocess
	import nude
	import argparse
except:
	print("You have to install requerments - pip3 install --upgrade nudepy opencv-python argparse ")
	exit()


class Video2Frames:

	def __init__(self, videoPath=None) -> None:
		self.VideoPath = videoPath


	def extractFrames(self):
		# Opens the Video file
		videoFile = cv2.VideoCapture(self.VideoPath)
		print("Done Reading ",self.VideoPath)
		counter=0
		try:
			subprocess.run("mkdir Frames")
		except:
			print("Found Frames Foldar")

		while(videoFile.isOpened()):
			ret, frame = videoFile.read()
			if ret == False:
				break
			cv2.imwrite('Frames/Frame-'+str(counter)+'.jpg',frame)
			print("\b"*2,end=' ')
			print(counter)
			counter+=1
		videoFile.release()
		print("Done")


class FamilyFriendly(Video2Frames):
	# Linux Command to Find the total number of frames in the video
	command = "ffprobe -v error -select_streams v:0 -count_packets -show_entries stream=nb_read_packets -of csv=p=0 {path}"
	
	def __init__(self, videoPath=None) -> None:
		self.BadFrames = []
		self.VideoPath = videoPath
		self._name = 'FamilyFriendly-{x}'.format(x=self.VideoPath.replace("/",''))
		self._fourcc = cv2.VideoWriter_fourcc(*'MP4V')
		self._out = cv2.VideoWriter(self._name, self._fourcc, 30.0, (1920,1080))
		self.videoFramesNumber=0
		self.timeToFinish=0

	def findFramesNumber(self):
		numberOfFrames = subprocess.run(self.command.format(path=self.VideoPath),capture_output=True,shell=True).stdout.decode("utf-8").strip()
		self.videoFramesNumber=numberOfFrames

	def estematedTime(self):
		self.timeToFinish = ( int(self.videoFramesNumber) * 6 ) / 3600


	def writeFrame(self,frame):
		self._out.write(frame)
		
	def vision(self,frame):
		cv2.imwrite('Frame.jpg',frame)
		print("d1")
		result = nude.is_nude('Frame.jpg')
		print("d2")
		return result


	def Good(self, frame):
		VisonResult = self.vision(frame)
		if VisonResult:
			print("UnSafe",end=' ')
			return False
		else:
			print("Safe", end=' ')
			return True

	def processFrame(self,frame,counter):
		if self.Good(frame):
			self.writeFrame(frame)
			print("Writing Frame Number: ",counter)
		else:
			print("Delete Frame number",counter)
			cv2.imwrite('Bad/Frame-'+str(counter)+'.jpg',frame)

	def deleteBadFrames(self):
		videoFile = cv2.VideoCapture(self.VideoPath)
		counter=0
        
		while(videoFile.isOpened()):
			ret, frame = videoFile.read()
			if ret == False:
				break
			else:
				self.processFrame(frame,counter)
			counter+=1
		
		videoFile.release()
	
	def clean(self):
		self._out.release()





if __name__=='__main__':
	parser = argparse.ArgumentParser(description="argument")
	parser.add_argument('-i','--input',help="input video name",type=str)
	parser.add_argument('-v','--v',help="print help",type=str)

	args = parser.parse_args()
	if args.v:
		print("-i input video name\n-t type of algorithm low, medium, high\n-h print help")
		exit()
	else:
		print("processing ",args.input)
		if args.input:
			video = FamilyFriendly(videoPath=args.input)
			video.findFramesNumber()
			video.estematedTime()
			x = input("start processing:{fpv} will take {time} Hour [yes]: ".format(fpv=video.videoFramesNumber, time=video.timeToFinish))
			if x == "yes":
				video.deleteBadFrames()
			else:
				print("done")