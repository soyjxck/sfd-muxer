"""
CLI for the SFD muxer.

Usage:
    # Demux a SFD file into raw MPEG-1 video + CRI ADX audio
    python -m sfd_muxer demux input.sfd --video out.m1v --audio out.sfa

    # Mux MPEG-1 video + CRI ADX into a SofDec SFD
    python -m sfd_muxer mux --video in.m1v --audio in.sfa -o out.sfd

    # Show SFD file info (sector count, video/audio sizes)
    python -m sfd_muxer info input.sfd
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .container import SFD, SECTOR


def cmd_demux(args: argparse.Namespace) -> int:
    sfd = SFD.from_file(args.input)
    if args.video:
        Path(args.video).write_bytes(sfd.extract_video())
        print(f"Video: {args.video} ({len(sfd.extract_video()):,} B)")
    if args.audio:
        Path(args.audio).write_bytes(sfd.extract_audio())
        print(f"Audio: {args.audio} ({len(sfd.extract_audio()):,} B)")
    return 0


def cmd_mux(args: argparse.Namespace) -> int:
    video = Path(args.video).read_bytes()
    audio = Path(args.audio).read_bytes()
    n = SFD.mux(video, audio).to_file(args.output)
    print(f"Muxed: {args.output} ({n:,} B, {n // SECTOR} sectors)")
    return 0


def cmd_info(args: argparse.Namespace) -> int:
    data = Path(args.input).read_bytes()
    print(f"file: {args.input}")
    print(f"size: {len(data):,} B ({len(data) // SECTOR} sectors of 0x800)")
    sfd = SFD.from_bytes(data)
    print(f"video: {len(sfd.extract_video()):,} B (raw MPEG-1)")
    print(f"audio: {len(sfd.extract_audio()):,} B (CRI ADX .sfa)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(prog="sfd-muxer")
    sub = ap.add_subparsers(dest="cmd", required=True)

    d = sub.add_parser("demux", help="extract video + audio from a SFD")
    d.add_argument("input", type=Path)
    d.add_argument("--video", type=Path, help="output path for raw MPEG-1 video")
    d.add_argument("--audio", type=Path, help="output path for CRI ADX audio")
    d.set_defaults(func=cmd_demux)

    m = sub.add_parser("mux", help="mux MPEG-1 + CRI ADX into a SFD")
    m.add_argument("--video", type=Path, required=True, help="raw MPEG-1 elementary stream")
    m.add_argument("--audio", type=Path, required=True, help="CRI ADX (.sfa)")
    m.add_argument("-o", "--output", type=Path, required=True)
    m.set_defaults(func=cmd_mux)

    i = sub.add_parser("info", help="show SFD file info")
    i.add_argument("input", type=Path)
    i.set_defaults(func=cmd_info)

    args = ap.parse_args()
    ret: int = args.func(args)
    return ret


if __name__ == "__main__":
    sys.exit(main())
