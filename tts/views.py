import json
import requests
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

def home(request):
    return render(request, "tts/index.html")

@csrf_exempt
def tts_generate(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    try:
        payload = json.loads(request.body.decode("utf-8"))
        text = (payload.get("text") or "").strip()
        if not text:
            return JsonResponse({"error": "text is required"}, status=400)
    except Exception:
        return JsonResponse({"error": "invalid json"}, status=400)

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{settings.ELEVEN_VOICE_ID}"
    headers = {
        "xi-api-key": settings.ELEVEN_API_KEY,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg",
    }
    data = {
        "text": text,
        "model_id": settings.ELEVEN_MODEL_ID,
        "voice_settings": {
            "stability": 0.38,
            "similarity_boost": 0.85,
            "style": 0.80,
            "use_speaker_boost": True
        }
    }

    r = requests.post(url, headers=headers, json=data, timeout=60)
    if r.status_code != 200:
        return JsonResponse({"error": "elevenlabs failed", "detail": r.text}, status=r.status_code)

    resp = HttpResponse(r.content, content_type="audio/mpeg")
    resp["Content-Disposition"] = 'inline; filename="speech.mp3"'
    return resp
