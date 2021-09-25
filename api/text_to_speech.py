import torch
from scipy.io.wavfile import write


def _load_model_from_torch_hub(repo: str, model: str, model_math: str = '', remove_weightnorm: bool = False):
    if model_math == '':
        model = torch.hub.load(repo_or_dir=repo, model=model)
    else:
        model = torch.hub.load(repo_or_dir=repo, model=model, model_math=model_math)

    if remove_weightnorm:
        model = model.remove_weightnorm(model)
    model = model.to('cuda')
    return model.eval()


class TextToAudio:

    def __init__(self, output_path: str = '', output_name: str = 'audio.wav', rate: int = 22050):
        self._output_path = output_path + output_name
        self._rate = rate
        self._tactotron2 = _load_model_from_torch_hub(
            repo='NVIDIA/DeepLearningExamples:torchhub',
            model='nvidia_tacotron2',
            model_math='fp16'
        )
        self._waveglow = _load_model_from_torch_hub(
            repo='NVIDIA/DeepLearningExamples:torchhub',
            model='nvidia_waveglow',
            model_math='fp16'
        )
        self._utils = torch.hub.load('NVIDIA/DeepLearningExamples:torchhub', 'nvidia_tts_utils')

    def parse_text(self, text_to_convert: str):
        print(f'Converting "{text_to_convert}" into audio with rate {self._rate} and save it to "{self._output_path}".')
        sequences, lengths = self._utils.prepare_input_sequence([text_to_convert])
        with torch.no_grad():
            mel, _, _ = self._tactotron2.infer(sequences, lengths)
            audio = self._waveglow.infer(mel)
        audio_numpy = audio[0].data.cpu().numpy()
        write(self._output_path, self._rate, audio_numpy)
        return self._output_path


if __name__ == '__main__':
    text_to_audio = TextToAudio()
    text_to_audio.parse_text(text_to_convert='Today is Saturday and the sun is shining.')
