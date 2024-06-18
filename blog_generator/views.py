from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
from decouple import config
# from transformers import pipeline
import json
from pytube import YouTube
import os
import assemblyai as aai
import openai



# Create your views here.

def bloggen(request):

        return render(request, 'aiblog/blogs.html')

@csrf_exempt
def generate_blog(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            yt_link = data['link']
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({'error': 'Invalid data sent'}, status=400)


        # get yt title
        title = yt_title(yt_link)

        # get transcript
        transcription = get_transcription(yt_link)
        if not transcription:
            return JsonResponse({'error': " Failed to get transcript"}, status=500)


        # use OpenAI to generate the blog
        blog_content = generate_blog_from_transcription(transcription)
        if not blog_content:
            return JsonResponse({'error': " Failed to generate blog article"}, status=500)




        # return blog article as a response
        return JsonResponse({'content': blog_content})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    



def yt_title(link):
    yt = YouTube(link)
    title = yt.title
    return title

def download_audio(link):
    yt = YouTube(link)
    video = yt.streams.filter(only_audio=True).first()
    out_file = video.download(output_path=settings.MEDIA_ROOT)
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)
    return new_file

def get_transcription(link):
    audio_file = download_audio(link)
    aai.settings.api_key = config('AI_KEY')
    print(audio_file)
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_file)

    if transcript.error:
        print(transcript.error)
    else:
        print("\nNano tier output:")
        print(transcript.text)
    return transcript.text

# def generate_blog_from_transcription(transcription):
    
#     # generator = pipeline('text-generation', model='gpt2')
    # prompt = f"Based on the following transcript from a YouTube video, write a comprehensive blog article, write it based on the transcript, but dont make it look like a youtube video, make it look like a proper blog article:\n\n{transcription}\n\nArticle:"
    # # generated_text = generator(prompt, max_length=5000)
    # openai.api_key = config('OPEN_AI')

   

#     response = openai.Completion.create(
#     model="gpt-4",
#     prompt=prompt,
#     max_tokens=3500
#     )
#     generated_content = response.choices[0].text.strip()
#     #generated_content = generated_text[0]['generated_text']

#     return generated_content
def generate_blog_from_transcription(transcription):
    prompt = f"Based on the following transcript from a YouTube video, write a comprehensive blog article, write it based on the transcript, but dont make it look like a youtube video, make it look like a proper blog article:\n\n{transcription}\n\nArticle:"
    # generated_text = generator(prompt, max_length=5000)
    openai.api_key = config('OPEN_AI')

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=3500
    )
    print(response) 
    generated_content = response['choices'][0]['message']['content']
    return generated_content