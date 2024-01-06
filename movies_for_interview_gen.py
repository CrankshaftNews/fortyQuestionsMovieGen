# Author: Shyamal Suhana Chandra
# Date: December 2, 2023 @ 3:32 PM
# Function: To create 40 questions and answers with TTS from different topic prompts for Crankshaft News.

#!/usr/local/bin/python3.11

import pyaudio
import os
import sys
import subprocess
import asyncio
from pyffmpeg import FFmpeg
import subprocess
import re
import wave
import time

def main():
	
	with open(str(sys.argv[1]), 'r') as f:
	    contents = f.read()

	tokens = contents.splitlines()	

	#print(tokens)

	filelist = []
	counter = False
	number = 0
	secondsInt = ''
	for token in tokens:
		if counter == True:
			print("TRUE")
			os.system("say -o question.aiff -v \"Matilda (Premium)\" -r 150 \""+ str(token) +"\"")
			print("say done!")
			with open('question.txt', 'w') as f:
				f.write(str(token))
			os.system("marp --image png question.txt -o question.png")
			print("marp done!")
			os.system("ffprobe -i question.aiff -show_entries format=duration -v quiet -of csv='p=0' >> seconds.txt")
			with open("seconds.txt", 'r') as seconds:
				secondInt = seconds.read()
				print(str(secondInt.replace('\n', '')))
			open("seconds.txt", 'w').close()				
			os.system("ffmpeg -loglevel quiet -y -loop 1 -i question.png -c:v libx264 -t `echo " + str(secondInt.replace('\n', '')) + " | perl -nl -MPOSIX -e 'print ceil($_);'` -pix_fmt yuv420p -vf scale=1920:1080 question_" + str(number) + ".mp4")
			os.system("ffmpeg -loglevel quiet -y -i question_" + str(number) + ".mp4 -i question.aiff -t `echo " + str(secondInt.replace('\n', '')) + " | perl -nl -MPOSIX -e 'print ceil($_);'` question" + str(number) + ".mp4")
			print("ffmpeg done!")
			filelist.append(str("file question" + str(number) + ".mp4"))
			counter = False
		elif counter == False:
			print("FALSE")
			os.system("say -o answer.aiff -v \"Zoe (Premium)\" -r 150 \""+ str(token) +"\"")
			print("say done!")
			with open('answer.txt', 'w') as f:
				f.write(str(token))
			open("seconds.txt", 'w').close()				
			os.system("marp --image png answer.txt -o answer.png")
			print("marp done!")		
			os.system("ffprobe -i answer.aiff -show_entries format=duration -v quiet -of csv='p=0' >> seconds.txt")
			with open("seconds.txt", 'r') as seconds:
				secondInt = seconds.read()					
				print(str(secondsInt.replace('\n', '')))
			open("seconds.txt", 'w').close()														
			os.system("ffmpeg -loglevel quiet -y -loop 1 -i answer.png -c:v libx264 -t `echo " + str(secondInt.replace('\n', '')) + " | perl -nl -MPOSIX -e 'print ceil($_);'` -pix_fmt yuv420p -vf scale=1920:1080 answer_" + str(number) + ".mp4")
			os.system("ffmpeg -loglevel quiet -y -i answer_" + str(number) + ".mp4 -i answer.aiff -t `echo " + str(secondInt.replace('\n', '')) + " | perl -nl -MPOSIX -e 'print ceil($_);'` answer" + str(number) + ".mp4")
			print("ffmpeg done!")			
			filelist.append(str("file answer" + str(number) + ".mp4"))
			counter = True
			number = number + 1
	print("END OF CONVERSATION!")
	filefinallist = "\n".join(filelist)
	with open('filelist.txt', 'w') as f:
		f.write(str(filefinallist))
	os.system("ffmpeg -loglevel quiet -threads 8 -f concat -i filelist.txt -c copy " + str(sys.argv[2]) + "")
	print("final ffmpeg done!")
if __name__ == "__main__":
	main()
