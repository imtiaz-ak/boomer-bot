import json
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from pytube import YouTube
from pymessenger.bot import Bot


ACCESS_TOKEN = 'ACCESS_TOKEN'
VERIFY_TOKEN = 'VERIFY_TOKEN'

bot = Bot(ACCESS_TOKEN)


def get_message(link):

    video = YouTube(link)
    video = video.streams.filter(only_audio=True).first()

    destination = settings.MEDIA_ROOT
    out_file = video.download(output_path=destination)

    reply = "I have downloaded the video"
    return reply


# uses PyMessenger to send response to user
def send_message(recipient_id, response):
    # sends user the text message provided via input response parameter
    print("I AM ABOUT TO SEND A TEXT MESSAGE")
    bot.send_text_message(recipient_id, response)


@csrf_exempt
def messenger_download_bot(request):
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook."""

        token_sent = request.GET["hub.verify_token"]
        challenge = request.GET["hub.challenge"]
        if token_sent == VERIFY_TOKEN:
            return HttpResponse(challenge)
        else:
            return HttpResponse('Invalid verification token')

    elif request.method == 'POST':
        print("I HAVE RECEIVED A POST REQUEST")
        output = json.loads(request.body)
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                if message.get('message'):
                    print("I GOT ALL THE INFO")
                    print("THE TEXT IS {}".format(
                        message['message'].get('text')))
                    print("THE USER IS {}".format(message['sender']['id']))
                    # Facebook Messenger ID for user so we know where to send response back to
                    recipient_id = message['sender']['id']

                    if message['message'].get('text'):
                        response_sent_text = get_message(
                            message['message'].get('text'))
                        send_message(recipient_id, response_sent_text)

        return HttpResponse(status=200)
