from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip


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
