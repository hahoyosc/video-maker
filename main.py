from source_download import SourceDownload
from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip
import os


def generate_watermark(start, duration, cut=None):

    print("Generating watermark starting at", start, "with this duration", duration)

    final_cut = cut if cut else 0

    return (ImageClip("tools/logo.png")
            .set_position((0.885, 0.83), relative=True)
            .set_start(start)
            .set_duration(duration - final_cut)
            .resize(0.15)
            .crossfadein(1)
            .crossfadeout(1))


def composite_clip(clip):

    print("Generating the output for the clip", clip)

    clip = (VideoFileClip(clip)
            .set_start(0)
            .crossfadein(1)
            .crossfadeout(1))
    watermark = generate_watermark(0, clip.duration)

    return CompositeVideoClip([clip, watermark])


def composite_full_video(opening, clips):

    print("Generating the full video with these clips", clips)

    opening = (VideoFileClip(opening)
               .set_start(0)
               .crossfadeout(1))
    full_video = [opening]
    current_duration = opening.duration

    for clip in clips:
        print("Appending the clip", clip, "at the second", current_duration)
        video_clip = (VideoFileClip(clip)
                      .set_start(current_duration)
                      .crossfadein(1)
                      .crossfadeout(1))
        full_video.append(video_clip)
        current_duration += video_clip.duration

    watermark = generate_watermark(opening.duration, current_duration, cut=6)
    full_video.append(watermark)

    return CompositeVideoClip(full_video)


def get_clips(source):

    clips = [source + x for x in os.listdir(source)]
    clips = [clip for clip in clips if clip.endswith('.mp4') or clip.endswith('.avi') or clip.endswith('.wmv')]
    clips.sort()

    return clips


def main(name):
    print(f'Hi, {name}')
    # SourceDownload.download_file("https://drive.google.com/drive/folders/1bGbVRol7v_biZ6k1_GCwHbte9J8E1q8o")

    opening = "tools/opening.mp4"
    source = "test_source/"
    output = "output/"
    clips = get_clips(source)

    for clip in clips:
        single_clip = composite_clip(clip)
        single_clip.write_videofile(output + clip.replace(source, ""))

    full_video = composite_full_video(opening, clips)
    full_video.write_videofile("output/full_video.mp4")


if __name__ == '__main__':
    main('PyCharm')
