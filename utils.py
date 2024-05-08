from azure.cognitiveservices.speech import ResultReason

done = False


async def run_recognition(speech_recognizer):
    # Starts speech recognition, and returns after a single utterance is recognized.
    speech_recognition_result = speech_recognizer.recognize_once_async().get()
    return (
        speech_recognition_result.text
        if speech_recognition_result.reason == ResultReason.RecognizedSpeech
        else "Could not recognize speech"
    )
