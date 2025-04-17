import csv
import os
import tempfile
from typing import Tuple

import gradio as gr
from transformers import WhisperProcessor, WhisperForConditionalGeneration
from whisper_bidec import decode_wav, get_logits_processor, load_corpus_from_sentences
from pydub import AudioSegment


def _parse_file(file_path: str) -> list[str]:
    """Parse .txt / .md / .csv and return its content as a list of strings by splitting per new line or row."""

    if file_path.endswith(".csv"):
        sentences = []
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                sentences.append(row)
    else:
        with open(file_path, "r") as f:
            sentences = f.readlines()
    return sentences


def _convert_audio(input_audio_path: str) -> str:
    """Whisper decoder expects wav files with 16kHz sample rate and mono channel.
    Convert the audio file to this format, save it in a tmp file and return the path.
    """
    fd, tmp_path = tempfile.mkstemp(suffix=".wav")
    os.close(fd)  # Close file descriptor

    audio = AudioSegment.from_file(input_audio_path)
    audio = audio.set_channels(1).set_frame_rate(16000)
    audio.export(tmp_path, format="wav")
    return tmp_path


def transcribe(
    processor_name: str,
    audio_path: str,
    bias_strength: float,
    bias_text: str | None,
    bias_text_file: str | None,
) -> Tuple[str, str]:
    processor = WhisperProcessor.from_pretrained(processor_name)
    model = WhisperForConditionalGeneration.from_pretrained(processor_name)

    sentences = ""

    if bias_text:
        sentences = bias_text.split(",")
    elif bias_text_file:
        sentences = _parse_file(bias_text_file)

    converted_audio_path = _convert_audio(audio_path)

    if sentences:
        corpus = load_corpus_from_sentences(sentences, processor)
        logits_processor = get_logits_processor(
            corpus=corpus, processor=processor, bias_towards_lm=bias_strength
        )
        text_with_bias = decode_wav(
            model, processor, converted_audio_path, logits_processor=logits_processor
        )
    else:
        text_with_bias = ""

    text_no_bias = decode_wav(
        model, processor, converted_audio_path, logits_processor=None
    )

    return text_no_bias, text_with_bias


def setup_gradio_demo():
    css = """
    #centered-column {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column; 
        text-align: center;
    }
    """
    with gr.Blocks(css=css) as demo:
        gr.Markdown("# Whisper Bidec Demo")

        gr.Markdown("## Step 1: Select a Whisper model")
        processor = gr.Textbox(
            value="openai/whisper-tiny.en", label="Whisper Model from Hugging Face"
        )

        gr.Markdown("## Step 2: Upload your audio file")
        audio_clip = gr.Audio(type="filepath", label="Upload a WAV file")

        gr.Markdown("## Step 3: Set your biasing text")
        with gr.Row():
            with gr.Column(scale=20):
                gr.Markdown(
                    "You can add multiple possible sentences by separating them with a comma <,>."
                )
                bias_text = gr.Textbox(label="Write your biasing text here")
            with gr.Column(scale=1, elem_id="centered-column"):
                gr.Markdown("## OR")
            with gr.Column(scale=20):
                gr.Markdown(
                    "Note that each new line (.txt / .md) or row (.csv) will be treated as a separate sentence to bias towards to."
                )
                bias_text_file = gr.File(
                    label="Upload a file with multiple lines of text",
                    file_types=[".txt", ".md", ".csv"],
                )

        gr.Markdown("## Step 4: Set how much you want to bias towards the LM")
        bias_amount = gr.Slider(
            minimum=0.0,
            maximum=1.0,
            value=0.5,
            step=0.1,
            label="Bias strength",
            interactive=True,
        )

        gr.Markdown("## Step 5: Get your transcription before and after biasing")
        transcribe_button = gr.Button("Transcribe")

        with gr.Row():
            with gr.Column():
                output = gr.Text(label="Output")
            with gr.Column():
                biased_output = gr.Text(label="Biased output")

        transcribe_button.click(
            fn=transcribe,
            inputs=[
                processor,
                audio_clip,
                bias_amount,
                bias_text,
                bias_text_file,
            ],
            outputs=[output, biased_output],
        )
    demo.launch()


if __name__ == "__main__":
    setup_gradio_demo()
