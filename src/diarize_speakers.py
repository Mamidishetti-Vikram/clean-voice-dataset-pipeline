import argparse
import json
import subprocess
from pathlib import Path
from typing import List, Dict


# -------------------------------------------------------------------
# 1. SPEAKER DIARIZATION (MOCK — MATCHES ~218s AUDIO)
# -------------------------------------------------------------------


def diarize_audio(input_wav: Path) -> List[Dict]:
    """
    Mock speaker diarization for ~3:38 (218 seconds) audio.

    This simulates realistic alternating speakers so the
    pipeline can be tested end-to-end before real models.
    """

    print("[INFO] Running mock speaker diarization (218s audio)")

    segments = [
        {"speaker": "speaker_0", "start": 0.0, "end": 14.2, "overlap": False},
        {"speaker": "speaker_1", "start": 14.2, "end": 31.6, "overlap": False},
        {"speaker": "speaker_0", "start": 31.6, "end": 49.8, "overlap": False},
        {"speaker": "speaker_1", "start": 49.8, "end": 67.4, "overlap": False},
        {"speaker": "speaker_0", "start": 67.4, "end": 86.1, "overlap": False},
        {"speaker": "speaker_1", "start": 86.1, "end": 104.9, "overlap": False},
        {"speaker": "speaker_0", "start": 104.9, "end": 123.5, "overlap": False},
        {"speaker": "speaker_1", "start": 123.5, "end": 142.7, "overlap": False},
        {"speaker": "speaker_0", "start": 142.7, "end": 161.8, "overlap": False},
        {"speaker": "speaker_1", "start": 161.8, "end": 180.4, "overlap": False},
        {"speaker": "speaker_0", "start": 180.4, "end": 198.6, "overlap": False},
        {"speaker": "speaker_1", "start": 198.6, "end": 218.0, "overlap": False},
    ]

    return segments


# -------------------------------------------------------------------
# 2. SAVE DIARIZATION METADATA
# -------------------------------------------------------------------


def save_metadata(segments: List[Dict], output_path: Path):
    """
    Saves diarization metadata to JSON.
    """

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        json.dump(segments, f, indent=2)

    print(f"[INFO] Diarization metadata saved to: {output_path}")


# -------------------------------------------------------------------
# 3. EXPORT SPEAKER-WISE AUDIO SEGMENTS
# -------------------------------------------------------------------


def export_segments(input_wav: Path, segments: List[Dict], output_dir: Path):
    """
    Cuts audio into speaker-wise WAV clips using FFmpeg.
    """

    print("[INFO] Exporting speaker segments")

    for idx, seg in enumerate(segments):
        speaker = seg["speaker"]
        start = seg["start"]
        end = seg["end"]
        duration = end - start

        speaker_dir = output_dir / speaker
        speaker_dir.mkdir(parents=True, exist_ok=True)

        output_clip = speaker_dir / f"clip_{idx:04d}.wav"

        command = [
            "ffmpeg",
            "-y",
            "-i",
            str(input_wav),
            "-ss",
            str(start),
            "-t",
            str(duration),
            "-ac",
            "1",
            "-ar",
            "16000",
            "-c:a",
            "pcm_s16le",
            str(output_clip),
        ]

        subprocess.run(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True
        )

        print(f"[INFO] Saved: {output_clip}")

    print("[SUCCESS] All speaker segments exported")


# -------------------------------------------------------------------
# 4. MAIN PIPELINE
# -------------------------------------------------------------------


def main(input_wav: Path, output_dir: Path):
    if not input_wav.exists():
        raise FileNotFoundError(f"Input WAV not found: {input_wav}")

    output_dir.mkdir(parents=True, exist_ok=True)

    # Step 1: Diarization
    segments = diarize_audio(input_wav)

    # Step 2: Save metadata
    metadata_path = output_dir / "diarization.json"
    save_metadata(segments, metadata_path)

    # Step 3: Export audio clips
    export_segments(input_wav, segments, output_dir)


# -------------------------------------------------------------------
# ENTRY POINT
# -------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Speaker diarization and segment export pipeline"
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Path to speech-only WAV (e.g. data/speech_only/vocals.wav)",
    )

    parser.add_argument(
        "--output", required=True, help="Output directory for speaker segments"
    )

    args = parser.parse_args()

    main(input_wav=Path(args.input), output_dir=Path(args.output))
