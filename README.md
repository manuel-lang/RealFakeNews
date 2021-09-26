# DeepFakeNews

Generate realistic news videos solely by providing your transcript. We summarize your news and generate a video of a speaker announcing your news.

## Features
- [x] Text Summarization
- [ ] Text Translation
- [x] Speech Synthesis
- [x] Video Generation
- [x] Lip Synchronization
- [ ] Multiple Language Support
- [ ] Make Your Own Speaker

## How does it work

We use [HuggingFace Transformers](https://huggingface.co/transformers/index.html) for Natural Language Understanding tasks and then generate audio with [NVIDIA's tacotron2](https://github.com/NVIDIA/tacotron2). We use the audio on predefined video material and adjust the speakers' lips using [Wav2Lip](https://github.com/Rudrabha/Wav2Lip).

The processing pipeline is integrated in FastAPI and gets accessed by a small React frontend. The entire application can be started using docker-compose.

## Run the application

In order to run the application, you need to have CUDA set up.

`docker-compose up`
