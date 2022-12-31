from pydub import AudioSegment
from pydub.silence import split_on_silence
import translators as ts
import speech_recognition as sr
import youtube_dl, os

def rozpoznaj_mowe(link2, jezyk):
	przetulaczony_text = ""
	link = f"https://www.youtube.com/watch?v={link2}"
	r = sr.Recognizer()
	ydl_opts = {"format": "bestaudio/best","outtmpl": "output.%(ext)s","postprocessors": [{"key": "FFmpegExtractAudio","preferredcodec": "wav",}],}
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		url = str(link)
		ydl.download([url])
	sound = AudioSegment.from_wav("output.wav")
	chunks = split_on_silence(sound,min_silence_len=500,silence_thresh=sound.dBFS - 14,keep_silence=500,)
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
	n = 1000
	res = [whole_text[i:i + n] for i in range(0, len(whole_text), n)]
	for i in res:
		przetulaczony_text += (ts.google(i, to_language='pl'))
	return przetulaczony_text