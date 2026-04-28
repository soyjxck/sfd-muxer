# SFD Muxer

Multiplexer/demultiplexer for the CRI SofDec PS2 cutscene container (`.sfd`).

If this helped you, consider [buying me a coffee](https://ko-fi.com/soyjack)

CRI SofDec is the streaming format used for video cutscenes in many PS2 / Dreamcast / GameCube games. It interleaves MPEG-1 video with CRI ADX audio in 0x800-byte sectors. Examples of games shipping `.sfd` cutscenes:

- Magna Carta: Tears of Blood
- Burnout, Burnout 2/3
- Various Sega and CRI-licensed PS2/Dreamcast titles

Python port of [nebulas-star/SFD_Muxer](https://github.com/nebulas-star/SFD_Muxer) (C, 2021), restricted to the case of exactly 1 MPEG-1 video stream + 1 stereo CRI ADX audio (SofDec v1). Validated byte-equivalent to the reference C build for the cutscenes used in the Magna Carta undub.

## Install

```bash
pip install sfd-muxer
```

## Usage

### Command Line

```bash
# Extract video and audio from a SFD file
sfd-muxer demux cutscene.sfd --video out.m1v --audio out.sfa

# Create a new SFD from video + audio
sfd-muxer mux --video subtitled.m1v --audio kr_audio.sfa -o cutscene.sfd

# Show SFD file info
sfd-muxer info cutscene.sfd
```

### Python API

```python
from sfd_muxer import SFD

# Demux
sfd = SFD.from_file("cutscene.sfd")
video = sfd.extract_video()   # MPEG-1 elementary stream
audio = sfd.extract_audio()   # CRI ADX (.sfa)

# Mux
sfd = SFD.mux(video, audio)
sfd.to_file("out.sfd")

# Or in-memory:
data = sfd.to_bytes()
```

## Stream formats

- **video** — raw MPEG-1 elementary stream starting with `00 00 01 B3` (sequence header). The `frame_rate_code` (byte 7's low nibble) drives DTS scheduling during muxing.
- **audio** — CRI ADX (`.sfa`) with magic `80 00`, `(c)CRI` watermark at offset `0x11A`, and a header that includes block_size at `+0x06`, channel_count at `+0x07`, and big-endian u32 sample_rate at `+0x08`.

## SFD layout

```
sector 0 (0x800 B):  pack_head + audio system_header + 0xBE padding
sector 1 (0x800 B):  pack_head + video system_header + 0xBE padding
sector 2 (0x800 B):  pack_head + Sofdec stream-message PES (0xBF) + zeros
sectors 3..N-1:      interleaved video (0xE0) / audio (0xC0) PES + 0xBE padding
                     (smallest pending DTS first)
final sector:        program_end (0x000001B9) + 0x7FC bytes of 0xFF
```

## Credit

C reference implementation: [nebulas-star/SFD_Muxer](https://github.com/nebulas-star/SFD_Muxer).
Originally extracted from [magna-carta-undub](https://github.com/soyjxck/magna-carta-undub).
