# DeepFakeNews

Generate realistic news videos solely by providing your transcript. We summarize your news and generate a video of a speaker announcing your news.

## Features
- [x] Text Summarization
- [x] Text Translation
- [x] Video Generation
- [ ] Multiple Language Support
- [ ] Make Your Own Speaker

## How does it work

We use [HuggingFace Transformers](https://huggingface.co/transformers/index.html) for NLP tasks and then generate audio with [NVIDIA's tacotron2](https://github.com/NVIDIA/tacotron2). We use the audio on predefined video material and adjust the speakers' lips using [Wav2Lip](https://github.com/Rudrabha/Wav2Lip).

## Run the application

`docker-compose up`
