import argparse
import subprocess
import sys
from pathlib import Path


def separate_speech(input_wav: str, output_wav: str):
    """
    Separates speech from background music/effects
    and outputs speech-dominant audio.
    """

    input_wav = Path(input_wav)
    output_wav = Path(output_wav)

    if not input_wav.exists():
        raise FileNotFoundError(f"Input WAV not found: {input_wav}")

    output_wav.parent.mkdir(parents=True, exist_ok=True)

    print(f"[INFO] Separating speech from: {input_wav.name}")
    print(f"[INFO] Output speech file: {output_wav}")

    # Using Demucs (pretrained) for speech/music separation
    # This command extracts the 'vocals' (speech-dominant) stem

    command = [
        "demucs",
        "--two-stems",
        "vocals",
        "--out",
        str(output_wav.parent),
        str(input_wav),
    ]

    try:
        subprocess.run(
            command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
    except subprocess.CalledProcessError as e:
        print("[ERROR] Speech separation failed")
        print(e.stderr.decode())
        sys.exit(1)

    # Demucs outputs files in a subfolder named after the model
    # We will standardize filenames later (Day 2 refinement)

    print("[SUCCESS] Speech separation completed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Separate speech from background music/effects"
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to extracted WAV (e.g., data/extracted_audio/movie.wav)",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Path to output speech WAV (e.g., data/speech_only/movie_speech.wav)",
    )

    args = parser.parse_args()

    separate_speech(input_wav=args.input, output_wav=args.output)
