#!/usr/bin/env python3
"""Genera un episodio de La Bandita con arte 2D original, voces locales y FFmpeg."""
import json, os, subprocess, sys, textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
W, H = (1080, 1920) if os.getenv("VIDEO_FORMAT", "short") == "short" else (1920, 1080)
EPISODE_ID = os.getenv("EPISODE_ID", "pizza")
EPISODE_PATH = ROOT / "episodes" / (EPISODE_ID + ".json")
if not EPISODE_PATH.exists():
    sys.exit("Episodio desconocido: " + EPISODE_ID)
EP = json.loads(EPISODE_PATH.read_text(encoding="utf-8"))

CHAR = {
    "Krono": {"color": (166, 103, 57), "ear": (64, 43, 34), "kind": "dog"},
    "Issi": {"color": (244, 190, 129), "ear": (130, 76, 48), "kind": "beagle"},
    "Pepa": {"color": (245, 202, 151), "ear": (130, 76, 48), "kind": "angel"},
    "Kuky": {"color": (230, 139, 70), "ear": (222, 130, 62), "kind": "cat"},
    "Zeus": {"color": (133, 127, 119), "ear": (112, 105, 98), "kind": "cat"},
}

def run(cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)

def font(size, bold=False):
    p = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    return ImageFont.truetype(p, size)

def rounded(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)

def draw_pet(draw, name, cx, cy, scale=1.0):
    c = CHAR[name]
    r = lambda v: max(1, int(v * scale))
    # Cuerpo y orejas
    rounded(draw, (cx-r(83), cy+r(50), cx+r(83), cy+r(250)), r(48), c["color"])
    if c["kind"] in ("dog", "beagle", "angel"):
        draw.ellipse((cx-r(100), cy-r(90), cx-r(28), cy+r(20)), fill=c["ear"])
        draw.ellipse((cx+r(28), cy-r(90), cx+r(100), cy+r(20)), fill=c["ear"])
    else:
        draw.polygon([(cx-r(82),cy-r(36)),(cx-r(78),cy-r(125)),(cx-r(18),cy-r(70))], fill=c["ear"])
        draw.polygon([(cx+r(18),cy-r(70)),(cx+r(78),cy-r(125)),(cx+r(82),cy-r(36))], fill=c["ear"])
    draw.ellipse((cx-r(92), cy-r(100), cx+r(92), cy+r(82)), fill=c["color"])
    # Hocico, ojos y nariz
    draw.ellipse((cx-r(45), cy+r(8), cx+r(45), cy+r(58)), fill=(255, 231, 201))
    for ex in (cx-r(40), cx+r(40)):
        draw.ellipse((ex-r(13),cy-r(42),ex+r(13),cy-r(12)),fill=(255,255,245))
        draw.ellipse((ex-r(5),cy-r(34),ex+r(6),cy-r(14)),fill=(45,37,30))
    draw.ellipse((cx-r(8),cy+r(25),cx+r(8),cy+r(39)),fill=(50,35,30))
    draw.arc((cx-r(20),cy+r(32),cx+r(20),cy+r(58)),10,170,fill=(65,38,30),width=r(3))
    # Patas
    for px in (cx-r(48), cx+r(48)):
        draw.ellipse((px-r(28),cy+r(210),px+r(28),cy+r(260)),fill=c["color"])
    if name == "Pepa":
        # Alas y aureola dorada: rasgo permanente del personaje.
        draw.arc((cx-r(155),cy-r(12),cx-r(62),cy+r(120)),190,520,fill=(255,255,255),width=r(14))
        draw.arc((cx+r(62),cy-r(12),cx+r(155),cy+r(120)),20,340,fill=(255,255,255),width=r(14))
        draw.ellipse((cx-r(42),cy-r(160),cx+r(42),cy-r(135)),outline=(255,205,60),width=r(7))
    rounded(draw,(cx-r(70),cy+r(265),cx+r(70),cy+r(303)),r(12),(255,250,232))
    draw.text((cx,cy+r(284)),name.upper(),font=font(r(17),True),fill=(53,43,35),anchor="mm")

def make_scene(scene, index):
    im = Image.new("RGB", (W,H), (249,220,165))
    d = ImageDraw.Draw(im)
    d.rectangle((0,0,W,int(H*.62)),fill=(255,215,154))
    d.ellipse((int(W*.69),int(H*.055),int(W*.85),int(H*.145)),fill=(255,245,184))
    d.rectangle((0,int(H*.62),W,H),fill=(117,160,99))
    d.rectangle((int(W*.06),int(H*.28),int(W*.94),int(H*.68)),fill=(255,241,210),outline=(181,128,82),width=max(3,W//300))
    d.rectangle((int(W*.12),int(H*.36),int(W*.35),int(H*.54)),fill=(166,214,232),outline=(128,98,66),width=max(3,W//300))
    d.line((int(W*.235),int(H*.36),int(W*.235),int(H*.54)),fill=(255,255,255),width=max(3,W//300))
    titlefont = font(max(24,W//27),True)
    d.text((W//2,int(H*.075)),EP["title"].upper(),font=titlefont,fill=(69,51,42),anchor="mm",stroke_width=1,stroke_fill=(255,245,222))
    d.text((W//2,int(H*.19)),f"LA BANDITA  •  ESCENA {index+1}",font=font(max(20,W//48),True),fill=(94,70,50),anchor="mm")
    names = [n for n in scene.get("characters", ["Krono","Issi","Kuky","Zeus"]) if n in CHAR][:4]
    if not names:
        names = ["Krono"]
    gap = W // (len(names)+1)
    pet_y = int(H*.39)
    scale = min(W/1080,H/1920)*0.78
    for j,name in enumerate(names):
        draw_pet(d,name,gap*(j+1),pet_y,scale)
    # Caja narrativa legible
    box = (int(W*.055),int(H*.70),int(W*.945),int(H*.95))
    rounded(d,box,32,(255,250,238),outline=(119,83,57),width=max(3,W//360))
    speaker = scene["speaker"]
    d.text((int(W*.09),int(H*.735)),speaker.upper(),font=font(max(22,W//43),True),fill=(157,83,39))
    wrap_width = 35 if W == 1080 else 61
    wrapped = textwrap.fill(scene["text"], width=wrap_width)
    d.multiline_text((int(W*.09),int(H*.79)),wrapped,font=font(max(24,W//41)),fill=(47,44,39),spacing=10)
    path = DIST / f"scene_{index:03d}.png"
    im.save(path)
    return path

def voice_for(speaker):
    s = speaker.upper()
    if s == "KRONO": return ("es+m3", 145, 48)
    if s == "ISSI": return ("es+f3", 178, 62)
    if s == "PEPA": return ("es+f2", 155, 58)
    if s == "KUKY": return ("es+f4", 170, 70)
    if s == "ZEUS": return ("es+m2", 132, 42)
    return ("es", 158, 52)

def stamp(seconds):
    ms = int(round(seconds*1000))
    h, ms = divmod(ms,3600000); m, ms = divmod(ms,60000); s, ms = divmod(ms,1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

def main():
    for command in ("ffmpeg","ffprobe","espeak-ng"):
        from shutil import which
        if not which(command):
            sys.exit("Falta la herramienta necesaria: " + command)
    DIST.mkdir(exist_ok=True)
    for p in DIST.iterdir():
        if p.is_file():
            p.unlink()
    segments, captions = [], []
    elapsed = 0.0
    for i, scene in enumerate(EP["scenes"]):
        image_path = make_scene(scene,i)
        voice_path = DIST / f"voice_{i:03d}.wav"
        voice, speed, pitch = voice_for(scene["speaker"])
        result = subprocess.run(["espeak-ng","-v",voice,"-s",str(speed),"-p",str(pitch),"-w",str(voice_path),scene["text"]],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        if result.returncode:
            run(["espeak-ng","-v","es","-s",str(speed),"-p",str(pitch),"-w",str(voice_path),scene["text"]])
        duration = float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","default=noprint_wrappers=1:nokey=1",str(voice_path)],text=True).strip())
        duration = max(1.7, duration + 0.45)
        segment_path = DIST / f"segment_{i:03d}.mp4"
        run(["ffmpeg","-y","-loop","1","-framerate","25","-i",str(image_path),"-i",str(voice_path),"-t",f"{duration:.3f}",
             "-vf",f"zoompan=z='min(zoom+0.0007,1.04)':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={W}x{H}:fps=25,format=yuv420p",
             "-c:v","libx264","-preset","ultrafast","-crf","25","-c:a","aac","-b:a","128k","-shortest","-pix_fmt","yuv420p",str(segment_path)])
        segments.append(segment_path)
        captions.append(f"{i+1}\n{stamp(elapsed)} --> {stamp(elapsed+duration)}\n{scene['speaker']}: {scene['text']}\n")
        elapsed += duration
    concat_path = DIST / "concat.txt"
    concat_path.write_text("".join("file '"+str(p.resolve())+"'\n" for p in segments),encoding="utf-8")
    merged = DIST / "merged.mp4"
    run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(concat_path),"-c","copy",str(merged)])
    (DIST/"subtitles.srt").write_text("\n".join(captions),encoding="utf-8")
    output = DIST/"la-bandita.mp4"
    run(["ffmpeg","-y","-i",str(merged),"-c:v","libx264","-preset","veryfast","-crf","23","-c:a","aac","-b:a","160k","-movflags","+faststart",str(output)])
    metadata = {"title":EP["title"]+(" | La Bandita #Shorts" if W < H else " | La Bandita"),
                "description":EP.get("description",""),"episode":EPISODE_ID,
                "format":"9:16" if W < H else "16:9","duration_seconds":round(elapsed,1),
                "review_before_upload":True,"synthetic_voices":"espeak-ng",
                "visual_style":"ilustración 2D original tipo cuento"}
    (DIST/"metadata.json").write_text(json.dumps(metadata,ensure_ascii=False,indent=2),encoding="utf-8")
    print(f"OK: {output} ({elapsed:.1f} segundos)")
if __name__ == "__main__":
    main()
