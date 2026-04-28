"""
SFD Muxer — CRI SofDec MPEG Program Stream multiplexer/demultiplexer.

The SFD format is CRI's streaming container used for PS2 / Dreamcast /
GameCube cutscenes (Magna Carta, Burnout, etc.). It interleaves an MPEG-1
video stream with a CRI ADX audio stream in 0x800-byte sectors.

Usage:
    from sfd_muxer import SFD

    # Demux
    sfd = SFD.from_file("cutscene.sfd")
    video = sfd.extract_video()    # raw MPEG-1 elementary stream
    audio = sfd.extract_audio()    # CRI ADX (.sfa)

    # Mux
    sfd = SFD.mux(video_data, audio_data)
    sfd.to_file("out.sfd")
"""

from .container import SFD, SofdecMuxer

__version__ = "0.1.0"
__all__ = ["SFD", "SofdecMuxer"]
