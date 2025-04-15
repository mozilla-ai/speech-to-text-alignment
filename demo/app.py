from typing import Tuple

import gradio as gr
from transformers import WhisperProcessor, WhisperForConditionalGeneration
from whisper_bidec import decode_wav, get_logits_processor, load_corpus_from_sentences


def transcribe(processor_name: str, audio: str, bias_text: str | None) -> Tuple[str, str]:
    processor = WhisperProcessor.from_pretrained(processor_name)
    model = WhisperForConditionalGeneration.from_pretrained(processor_name)

    text_with_bias = ""
    if bias_text.strip():
        corpus = load_corpus_from_sentences(bias_text.splitlines(), processor)
        logits_processor = get_logits_processor(
            corpus=corpus, processor=processor, bias_towards_lm=0.5
        )
        text_with_bias = decode_wav(model, processor, audio, logits_processor=logits_processor)
    text_no_bias = decode_wav(model, processor, audio, logits_processor=None)

    return text_no_bias, text_with_bias


def setup_gradio_demo():
    with gr.Blocks() as demo:
        gr.Markdown("Whisper Bidec Demo")

        processor = gr.Textbox(value="openai/whisper-tiny.en", label="Whisper Model from Hugging Face"),
        audio_clip = gr.Audio(type="filepath", label="Upload WAV"),
        bias_text = gr.Textbox(lines=3, placeholder="Optional bias lines")

        transcribe_button = gr.Button("Transcribe")

        output = gr.Text(label="Output")
        biased_output = gr.Text(label="Biased output")

        transcribe_button.click(
            fn=transcribe,
            inputs=[
                processor,
                audio_clip,
                bias_text,
            ],
            outputs=[output, biased_output],
        )
    demo.launch()


if __name__ == "__main__":
    setup_gradio_demo()