import cherrypy
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence
import youtube_dl, os

r = sr.Recognizer()
ydl_opts = {"format": "bestaudio/best","outtmpl": "output.%(ext)s","postprocessors": [{"key": "FFmpegExtractAudio","preferredcodec": "wav",}],}
error = ""

def transcription(path, jezyk):
    sound = AudioSegment.from_wav(path)
    chunks = split_on_silence(
        sound,
        min_silence_len=500,
        silence_thresh=sound.dBFS - 14,
        keep_silence=500,
    )
    folder_name = "audio-chunks"
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    for i, audio_chunk in enumerate(chunks, start=1):
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            try:
                text = r.recognize_google(audio_listened, language=jezyk)
            except sr.UnknownValueError as e:
                pass
            else:
                text = f"{text.capitalize()}. "
                pass
                whole_text += text
    return whole_text

with open("main.html", encoding="utf-8") as template:
    template = template.read()

class main(object):
    @cherrypy.expose
    def index(self):
        return template


    @cherrypy.expose
    def submit(self, link, jezyk):
        global error
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            url = str(link)
            try:
                ydl.download([url])
                tekst = transcription("output.wav", jezyk)
            except: 
                tekst = f"Podałeś nieprawidłowy link."
            

            return template.replace('<textarea></textarea>' ,f'<textarea>{tekst}</textarea>')


        
cherrypy.config.update({'server.socket_port': 25565,
                        'engine.autoreload_on': True})

cherrypy.server.socket_host = '0.0.0.0'

cherrypy.quickstart(main())

#todo
# ładowanie css
# tłuamczenie
# dezaktywowanie przycisku
# przycisk do kopiowajnia
#ładne wyswietlanie błędow







