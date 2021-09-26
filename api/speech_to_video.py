from Wav2Lip.inference import inference


class SpeechToVideo:

    def __init__(self, output_path: str = '', output_name: str = 'output_video.mp4'):
        self._output_path = "assets/videos/" + output_name

    def generate_video(self, model_path, video_path, audio_path):
        print(
            f'Generating video with: "{model_path}" based on the speaker: "{video_path}" and the following speech: {audio_path} and save it to "{self._output_path}".')

        # Run model
        inference(output_path=self._output_path, checkpoint_path=model_path, input_video=video_path, input_audio=audio_path)

        return self._output_path
