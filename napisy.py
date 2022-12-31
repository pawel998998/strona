from youtube_transcript_api import YouTubeTranscriptApi
import translators as ts

def napisy(link, jezyk):
	przetulaczony_text = ""
	lista_napisy = []
	gotowy_text = ""
	srt = YouTubeTranscriptApi.get_transcript(link)
	for i in range(len(srt)):
		lista_napisy.append(srt[i]["text"] + " ")
	for i in range(len(lista_napisy)):
		gotowy_text += lista_napisy[i]

	n = 1000
	res = [gotowy_text[i:i + n] for i in range(0, len(gotowy_text), n)]
	for i in res:
		przetulaczony_text += (ts.google(i, to_language="pl"))
	return przetulaczony_text