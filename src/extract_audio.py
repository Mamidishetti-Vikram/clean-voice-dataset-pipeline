import subprocess
import argparse
import os
import sys
from pathlib import Path


def extract_audio(video_path: str, output_path: str, sample_rate: int = 44100):
    """
    Extracts and standardizes audio from a video file using ffmpeg.

    Output format:
    - WAV
    - Mono
    - 24-bit PCM
    - Fixed sample rate
    """

    video_path = Path(video_path)
    output_path = Path(output_path)

    # 1. Validate input
    if not video_path.exists():
        raise FileNotFoundError(f"Input video not found: {video_path}")

    # 2. Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"[INFO] Extracting audio from: {video_path.name}")
    print(f"[INFO] Output WAV will be saved to: {output_path}")
    print(f"[INFO] Target sample rate: {sample_rate} Hz")
    print("[INFO] Audio format: mono, 24-bit PCM WAV")

    # 3. Build FFmpeg command (EXPLICIT — NO DEFAULTS)
    ffmpeg_command = [
        "ffmpeg",
        "-y",  # overwrite output if exists (safe: output dir only)
        "-i",
        str(video_path),  # input video
        "-vn",  # no video
        "-ac",
        "1",  # mono
        "-ar",
        str(sample_rate),  # sample rate
        "-sample_fmt",
        "s32",  # internal high-precision processing
        "-c:a",
        "pcm_s24le",  # 24-bit PCM WAV
        str(output_path),
    ]

    # 4. Execute FFmpeg
    try:
        result = subprocess.run(
            ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True
        )
    except subprocess.CalledProcessError as e:
        print("[ERROR] FFmpeg extraction failed")
        print(e.stderr.decode())
        sys.exit(1)

    print("[SUCCESS] Audio extraction completed successfully")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extract and standardize audio from a video file"
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to input video file (e.g., data/raw_movies/movie.mp4)",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Path to output WAV file (e.g., data/extracted_audio/movie.wav)",
    )
    parser.add_argument(
        "--sample_rate",
        type=int,
        default=44100,
        help="Target sample rate (default: 44100 Hz)",
    )

    args = parser.parse_args()

    extract_audio(
        video_path=args.input, output_path=args.output, sample_rate=args.sample_rate
    )
