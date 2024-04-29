from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip
from moviepy.video.VideoClip import TextClip


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


def generate_vs_clip(start, params):
    print("Generating the vs clip starting at", start)

    vs_clip = (VideoFileClip("tools/video-vs.mp4")
               .set_start(start)
               .set_duration(6)
               .crossfadein(1)
               .crossfadeout(1))

    team_a_text = (TextClip(params['results']['teamA']['name'],
                            font='Lato-Bold',
                            fontsize=75,
                            color='white',
                            method='caption',
                            size=(0.4 * vs_clip.size[0], vs_clip.size[1]))
                   .set_position((0, 'center'))
                   .set_start(start)
                   .set_duration(6)
                   .crossfadein(1.5)
                   .crossfadeout(1.5))

    team_b_text = (TextClip(params['results']['teamB']['name'],
                            font='Lato-Bold',
                            fontsize=75,
                            color='white',
                            method='caption',
                            size=(0.4 * vs_clip.size[0], vs_clip.size[1]))
                   .set_position((0.6 * vs_clip.size[0], 'center'))
                   .set_start(start)
                   .set_duration(6)
                   .crossfadein(1.5)
                   .crossfadeout(1.5))

    return CompositeVideoClip([vs_clip, team_a_text, team_b_text])


def composite_clip(clip):
    print("Generating the output for the clip", clip)

    clip = (VideoFileClip(clip)
            .set_start(0)
            .crossfadein(1)
            .crossfadeout(1))
    watermark = generate_watermark(0, clip.duration)

    return CompositeVideoClip([clip, watermark])


def generate_results_clip(start, params):
    background = (ImageClip("tools/results-img.jpg")
                  .set_start(start)
                  .set_duration(6)
                  .crossfadein(1)
                  .crossfadeout(1))

    results_title = (TextClip("RESULTADO DEL PARTIDO",
                              font='Lato-Bold',
                              fontsize=100,
                              color='white')
                     .set_position(('center', 'top'))
                     .set_start(start)
                     .set_duration(6)
                     .crossfadein(1.5)
                     .crossfadeout(1.5))

    team_a_text = (TextClip(params['results']['teamA']['name'],
                            font='Lato-Bold',
                            fontsize=75,
                            color='white',
                            method='caption',
                            size=(0.4 * background.size[0], 0.5 * background.size[1]))
                   .set_position((0, 0.1 * background.size[1]))
                   .set_start(start)
                   .set_duration(6)
                   .crossfadein(1.5)
                   .crossfadeout(1.5))

    team_a_score = (TextClip(str(params['results']['teamA']['score']),
                             font='Lato-Bold',
                             fontsize=200,
                             color='white',
                             method='caption',
                             size=(0.4 * background.size[0], 0.5 * background.size[1]))
                    .set_position((0, 0.4 * background.size[1]))
                    .set_start(start)
                    .set_duration(6)
                    .crossfadein(1.5)
                    .crossfadeout(1.5))

    team_b_text = (TextClip(params['results']['teamB']['name'],
                            font='Lato-Bold',
                            fontsize=75,
                            color='white',
                            method='caption',
                            size=(0.4 * background.size[0], 0.5 * background.size[1]))
                   .set_position((0.6 * background.size[0], 0.1 * background.size[1]))
                   .set_start(start)
                   .set_duration(6)
                   .crossfadein(1.5)
                   .crossfadeout(1.5))

    team_b_score = (TextClip(str(params['results']['teamB']['score']),
                             font='Lato-Bold',
                             fontsize=200,
                             color='white',
                             method='caption',
                             size=(0.4 * background.size[0], 0.5 * background.size[1]))
                    .set_position((0.6 * background.size[0], 0.4 * background.size[1]))
                    .set_start(start)
                    .set_duration(6)
                    .crossfadein(1.5)
                    .crossfadeout(1.5))

    return CompositeVideoClip([background, results_title, team_a_text, team_a_score, team_b_text, team_b_score])


def composite_recap(opening, clips, params):
    print("Generating the recap with these clips", clips)

    opening = (VideoFileClip(opening)
               .set_start(0)
               .crossfadeout(1))
    vs_clip = generate_vs_clip(opening.duration, params)
    recap = [opening, vs_clip]
    current_duration = vs_clip.duration

    for clip in clips:
        print("Appending the clip", clip, "at the second", current_duration)
        video_clip = (VideoFileClip(clip)
                      .set_start(current_duration)
                      .crossfadein(1)
                      .crossfadeout(1))
        recap.append(video_clip)
        current_duration += video_clip.duration

    recap.append(generate_results_clip(current_duration, params))
    current_duration += 6

    watermark = generate_watermark(opening.duration, current_duration, cut=6)
    recap.append(watermark)

    return CompositeVideoClip(recap)


def composite_full_video(opening, source_video, params):
    source_video = VideoFileClip(source_video)
    opening = (VideoFileClip(opening)
               .set_start(0)
               .crossfadeout(1))
    full_video = [opening]
    current_duration = opening.duration
    time_marks = params['timestamps']

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
