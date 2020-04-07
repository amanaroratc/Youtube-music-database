import pandas as pd
import csv
import time

timestr = time.strftime("%Y%m%d-%H%M%S")
print('Current timestamp is: ', timestr)

askname=input("Enter your filename (without.txt): ") #the text file should be in the same directory as this Python file

text_file = open("%s.txt" %askname) #text file generated manually by using ctrl-A ctrl-V on the liked songs page on browser
lines = text_file.readlines()

text_file.close()

lines=lines[11:] #Deleting unncessary information obtained from webpage

#check if a string is in time format. Used to separate one song data from another
def isTimeFormat(input):
    try:
        time.strptime(input, '%H:%M')
        return True
    except ValueError:
        return False

#print(isTimeFormat('3:01')) #test statement

for i in range(len(lines)): #Remove trailing newline
    lines[i]=lines[i].rstrip() 

time_index=[]

#here we identify the indices for all the timestamps, i.e., duration of the song
for i in range(len(lines)):
    if isTimeFormat(lines[i])==True:
        time_index.append(i)

#print(time_index) #test statement

#Create a new empty dataframe
data = pd.DataFrame(columns=['Track name', 'Artist','Album','Duration'])

#The data for a song can sometime have more than one artist, and/or it may have no album name.
#The code below handles all such cases to add the songs to the dataframe rows using the timestamp, i.e., the duration as a separator
for i in range(len(time_index)):
    if i==0:
        data=data.append({'Duration': lines[time_index[i]],'Track name': lines[0], 'Artist': lines[1], 'Album': lines[2]}, ignore_index=True)
    else:
        data=data.append({'Duration': lines[time_index[i]],'Track name': lines[time_index[i-1]+2], 'Artist': lines[time_index[i-1]+3], 'Album': lines[time_index[i]-2]}, ignore_index=True)

#This is the final database of all liked songs from YouTube Music
data.to_csv('ytmusic_liked_database_%s.csv' %timestr)
print(data.head())

#This generates another text file used to download the songs using spotdl
#Not a necessary step, can simply convert to a Spotify playlist and download thereafter using spotdl
dataconv=data.drop(['Album','Duration'],axis=1)
print(dataconv.head())

dataconv.to_csv(r'%s.txt' %timestr, header=None, index=None, sep=' ', mode='a')
