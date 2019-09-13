import librosa
filename='/home/dell/highlights/powerplay.wav'
x,sr=librosa.load(filename,sr=16000)

int(librosa.get_duration(x, sr)/60)#getting entire duration in minutes.

max_slice=5 
window_length = max_slice * sr

import IPython.display as ipd

a=x[1*window_length:2*window_length] 
ipd.Audio(a, rate=sr)#listening one of the audio

energy = sum(abs(a**2))
#print(energy)#energy of chunk

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

fig=plt.figure(figsize=(14,8))
ax1=fig.add_subplot(2,1,1)
ax1.set_xlabel('Time')
ax1.set_ylabel('Energy')
plt.plot(a)
plt.savefig('energy.png')

import numpy as np
energy=np.array([sum(abs(x[i:i+window_length]**2)) for i in range(0,len(x),window_length)])

#plt.hist(energy)
#plt.savefig("histogram.png")

import pandas as pd
df=pd.DataFrame(columns=['energy','start','end'])
thresh=12000
row_index=0
for i in range(len(energy)):
	value=energy[i]
	if(value>=thresh):
		i=np.where(energy==value)[0]
		df.loc[row_index,'energy']=value
		df.loc[row_index,'start']=i[0]*5
		df.loc[row_index,'end']=(i[0]+1)*5
		row_index+=1
'''
temp=[]
i=0
j=0
n=len(df)-2
m=len(df)-1
while(i<=n):
	j=i+1
	while(j<=m):
		if(df['end'][i]==df['start'][j]):
			df.loc[i,'end']=df.loc[j,'end']
			temp.append(j)
			j=j+1
		else:
			i=j
			break
'''
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import *
start=np.array(df['start'])
end=np.array(df['end'])
k=0
for i in range(len(df)):
	if(i!=0):
		start_lim=start[i]-5
	else:
		start_lim = start[i] 
 	end_lim   = end[i]
 	filename="highlight" + str(i+1) + ".mp4"
 	ffmpeg_extract_subclip("powerplay.mp4",start_lim,end_lim,targetname=filename) 
 	if(i==0):
 		final_clip=VideoFileClip(filename)
 	else:
 		clip=VideoFileClip(filename)
 		final_clip=concatenate_videoclips([final_clip,clip])

final_clip.write_videofile("my_concatenation.mp4")		
 						
				

