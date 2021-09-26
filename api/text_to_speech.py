import torch
from scipy.io.wavfile import write
from os import mkdir
import pathlib

REPO_OR_DIR = 'NVIDIA/DeepLearningExamples:torchhub'


def _load_model_from_torch_hub(model: str, load_state_dict_from_url: str = '', remove_weightnorm: bool = False):
    model = torch.hub.load(repo_or_dir=REPO_OR_DIR, model=model, model_math='fp16', pretrained=False)

    if load_state_dict_from_url != '':
        checkpoint = torch.hub.load_state_dict_from_url(url=load_state_dict_from_url, model_dir='model_checkpoints', map_location="cpu")
        state_dict = {key.replace("module.", ""): value for key, value in checkpoint["state_dict"].items()}
        model.load_state_dict(state_dict)

    if remove_weightnorm:
        model = model.remove_weightnorm(model)
    # model = model.to('cuda')
    return model.eval()


class TextToAudio:

    def __init__(self, output_path: str = '', output_name: str = 'audio.wav', rate: int = 22050):
        self._output_path = output_path
        self._output_name = output_name
        self._rate = rate
        self._tactotron2 = _load_model_from_torch_hub(
            model='nvidia_tacotron2',
            load_state_dict_from_url='https://api.ngc.nvidia.com/v2/models/nvidia/tacotron2pyt_fp32/versions/1/files/nvidia_tacotron2pyt_fp32_20190306.pth'
        )
        self._waveglow = _load_model_from_torch_hub(
            model='nvidia_waveglow',
            load_state_dict_from_url='https://api.ngc.nvidia.com/v2/models/nvidia/waveglowpyt_fp16/versions/2/files/nvidia_waveglowpyt_fp16_20190427',
            remove_weightnorm=True
        )
        self._utils = torch.hub.load(repo_or_dir=REPO_OR_DIR, model='nvidia_tts_utils')

    def parse_text(self, text_to_convert: str):
        sequences, lengths = self._utils.prepare_input_sequence([text_to_convert], True)
        with torch.no_grad():
            mel, _, _ = self._tactotron2.infer(sequences, lengths)
            audio = self._waveglow.infer(mel)
        audio_numpy = audio[0].data.cpu().numpy()
        cwd = pathlib.Path().resolve()
        output_path = f'{str(cwd)}/{self._output_path}'
        mkdir(output_path)
        output_path = f'{output_path}/{self._output_name}'
        write(output_path, self._rate, audio_numpy)
        return output_path


if __name__ == '__main__':
    text_to_audio = TextToAudio()
    text_to_audio.parse_text(text_to_convert='Today is Saturday and the sun is shining.')
