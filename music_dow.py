from pytube import YouTube 
from pytube import Playlist
from moviepy.editor import *
import eyed3
import sys

def get_data(file):
    urls = {"no_name_playlist":[]}
    with open(file, "r") as objfile:
        list_urls = objfile.readlines()
        for i in list_urls:
            if "list" in i:
                urls[Playlist(i).title] = Playlist(i).video_urls
            else:
                urls["no_name_playlist"].append(i)
    return urls

def download(url, albun, parameters):
    print(url)
    video = YouTube(url)
    autor = video.author
    file_name = video.title.replace(" ", "_") + ".mp4"
    try:
        video = video.streams.get_highest_resolution()
        video.download(filename=file_name)
    except:
        print(f"error in {video.title}; not download")
        return None
    
    if "m" in parameters:
        try:
            video = VideoFileClip(file_name)
            audio = video.audio
            audio.write_audiofile(file_name[0:-3]+"mp3")

            audio.close
            video.close

            #add albun and artist
            if albun != "no_name_playlist":
                audiofile = eyed3.load(file_name[0:-3]+"mp3")
                audiofile.tag.album = albun
                audiofile.tag.save()
            
            audiofile = eyed3.load(file_name[0:-3]+"mp3")
            audiofile.tag.artist = autor
            audiofile.tag.title = file_name[0:-4]
            audiofile.tag.save()
            
        except:
            print("error in audio")
        if "v" not in parameters:
            os.remove(file_name)


if __name__ == '__main__':
    dict_urls = get_data(sys.argv[1])
    if len(sys.argv) > 2:
        parameters = sys.argv[2]
    else:
        parameters = "v"
    for i in dict_urls:
        print(i)
        for e in dict_urls[i]:
            download(e, i, parameters)
