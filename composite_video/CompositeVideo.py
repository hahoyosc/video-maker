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


def composite_recap(opening, clips):

    print("Generating the recap with these clips", clips)

    opening = (VideoFileClip(opening)
               .set_start(0)
               .crossfadeout(1))
    recap = [opening]
    current_duration = opening.duration

    for clip in clips:
        print("Appending the clip", clip, "at the second", current_duration)
        video_clip = (VideoFileClip(clip)
                      .set_start(current_duration)
                      .crossfadein(1)
                      .crossfadeout(1))
        recap.append(video_clip)
        current_duration += video_clip.duration

    watermark = generate_watermark(opening.duration, current_duration, cut=6)
    recap.append(watermark)

    return CompositeVideoClip(recap)


def composite_full_video(opening, source_video, time_marks):

    source_video = VideoFileClip(source_video)
    opening = (VideoFileClip(opening)
               .set_start(0)
               .crossfadeout(1))
    full_video = [opening]
    current_duration = opening.duration

    for i in range(0, len(time_marks), 2):
        initial_second = time_marks[i]
        final_second = time_marks[i + 1]
        print("Generating the full video, appending the clip from", initial_second, "to", final_second)
        part = (source_video.subclip(initial_second, final_second)
                .set_start(current_duration)
                .crossfadein(1)
                .crossfadeout(1))

        full_video.append(part)
        current_duration += part.duration

    watermark = generate_watermark(opening.duration, current_duration, cut=6)
    full_video.append(watermark)

    return CompositeVideoClip(full_video)
