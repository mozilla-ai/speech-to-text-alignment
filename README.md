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
[![Docs](https://github.com/mozilla-ai/blueprint-template/actions/workflows/docs.yaml/badge.svg)](https://github.com/mozilla-ai/blueprint-template/actions/workflows/docs.yaml/)
[![Tests](https://github.com/mozilla-ai/blueprint-template/actions/workflows/tests.yaml/badge.svg)](https://github.com/mozilla-ai/blueprint-template/actions/workflows/tests.yaml/)
[![Ruff](https://github.com/mozilla-ai/blueprint-template/actions/workflows/lint.yaml/badge.svg?label=Ruff)](https://github.com/mozilla-ai/blueprint-template/actions/workflows/lint.yaml/)

[Blueprints Hub](https://developer-hub.mozilla.ai/)
| [Documentation](https://mozilla-ai.github.io/Blueprint-template/)
| [Getting Started](https://mozilla-ai.github.io/Blueprint-template/getting-started)
| [Contributing](CONTRIBUTING.md)

</div>

# Blueprint title

This blueprint guides you to ...



## Quick-start

Create a virtual environment and install the dependencies:

``` sh
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install 'whisper-bidec @ https://github.com/OHF-Voice/whisper-bidec/archive/refs/tags/v0.0.1.tar.gz'
```

Download an example WAV file:

``` sh
wget "https://github.com/OHF-Voice/whisper-bidec/raw/refs/heads/main/tests/wav/what's%20the%20temperature%20of%20the%20EcoBee.wav"
```

Test transcribing the WAV file without any bias:

``` sh
python3 -m whisper_bidec "what's the temperature of the EcoBee.wav"
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
python3 -m whisper_bidec --text example_sentences.txt "what's the temperature of the EcoBee.wav"
what's the temperature of the EcoBee.wav|What's the temperature of the incubi?|What's the temperature of the EcoBee?
```

The bias can be adjusted with `--bias-towards-lm <BIAS>` which defaults to 0.5. Increasing this value will bias Whisper more towards the example sentences.

## How it Works


## Pre-requisites

- **System requirements**:
  - OS: Windows, macOS, or Linux
  - Python 3.10 or higher
  - Minimum RAM:
  - Disk space:

- **Dependencies**:
  - Dependencies listed in `pyproject.toml`


## Troubleshooting


## License

This project is licensed under the Apache 2.0 License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! To get started, you can check out the [CONTRIBUTING.md](CONTRIBUTING.md) file.
