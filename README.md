<p align="center">
  <picture>
    <!-- When the user prefers dark mode, show the white logo -->
    <source media="(prefers-color-scheme: dark)" srcset="./images/Blueprint-logo-white.png">
    <!-- When the user prefers light mode, show the black logo -->
    <source media="(prefers-color-scheme: light)" srcset="./images/Blueprint-logo-black.png">
    <!-- Fallback: default to the black logo -->
    <img src="./images/Blueprint-logo-black.png" width="35%" alt="Project logo"/>
  </picture>
</p>


<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![](https://dcbadge.limes.pink/api/server/YuMNeuKStr?style=flat)](https://discord.gg/YuMNeuKStr) <br>


</div>

# Whisper BiDec: a Blueprint by Mozilla.ai for aligning text transcriptions in Speech-to-Text applications

[Whisper BiDec](https://github.com/OHF-Voice/whisper-bidec) enables the user to "re-adjust" OpenAI's Whisper models to user predefined texts, leading to improved transcription accuracy for specific terms, names, or phrases. This is particularly useful in domains with specialized vocabulary or when dealing with uncommon names or smaller Whisper models. 

## Example Results


Whisper tiny before and after biasing with the text: "Dileesh Pothan":

| Without Bias | With Bias |
|--------------|------------------------|
| The rich potent as an Indian film director from Kerala who works in the Malayalam film industry.       | Dileesh Pothan is an Indian film director from Kerala who works in the Malayalam film industry.                 |

## Quick-start

Get started now with one of the following options:

### Try it on our Hugging Face Space

[![Try on Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Try%20on-Spaces-blue)](https://huggingface.co/spaces/mozilla-ai/speech-to-text-alignment)

### Try it locally

You can also install and use BiDec locally, either via the command line or through a graphical interface app.

First, install the necessary dependencies:

``` sh
git clone git@github.com:mozilla-ai/speech-to-text-alignment.git
cd speech-to-text-alignment
pip instal -r requirements.txt
```

### Graphical Interface App

Start the graphical interface app by running:

``` sh
python demo/app.py
```

### Command Line Interface


Run `python -m whisper_bidec --text <text_file> <wav_file> [<wav_file>...]` to transcribe WAV files and get CSV output like:

```
path_to_1.wav|text 1 without bias|text 1 with bias
path_to_2.wav|text 2 without bias|text 2 with bias
...
```

The text file should contain a list of sentences that you want to bias Whisper towards. These need to have the correct casing and punctuation. You can add multiple `--text` files.

Increase `--bias-towards-lm` to get transcripts more like the example sentences (default: 0.5).

Increase `--unk-logprob` to allow more words outside the example sentences (default: -5, must be less than 0) or decrease it to restrict words to example sentences (e.g., -10).



### Usage Example

Test transcribing the WAV file without any bias:

``` sh
python3 -m whisper_bidec example_data/ecobee.wav
```

This outputs CSV with the format `wav file|text without bias|text with bias` like:

``` csv
what's the temperature of the EcoBee.wav|What's the temperature of the incubi?|What's the temperature of the incubi?
```

Without bias, the WAV file is incorrectly transcribed as "What's the temperature of the **incubi**?"

Let's add a few example sentences that will bias Whisper towards the "EcoBee" device:

``` sh
cat > example_sentences.txt <<EOF
What's the temperature of the EcoBee?
What is the temperature of the EcoBee?
EOF
```

Now we can see the corrected transcript:

``` sh
python3 -m whisper_bidec --text ecobee_example.txt example_data/ecobee.wav
what's the temperature of the EcoBee.wav|What's the temperature of the incubi?|What's the temperature of the EcoBee?
```

The bias can be adjusted with `--bias-towards-lm <BIAS>` which defaults to 0.5. Increasing this value will bias Whisper more towards the example sentences.


### Troubleshooting

If you run into issues, check our Troubleshooting section before opening a new issue.

## License

This project is licensed under the Apache 2.0 License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! To get started, you can check out the [CONTRIBUTING.md](CONTRIBUTING.md) file.

