from source_download import SourceDownload
from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip
from moviepy.video.fx import headblur
from skimage.filters import gaussian


def generate_watermark(start, duration):
    return (ImageClip("tools/logo.png")
            .set_position((0.885, 0.83), relative=True)
            .set_start(start)
            .set_duration(duration)
            .resize(0.15)
            .crossfadein(1)
            .crossfadeout(1))


def composite_full_video(opening, initial_clip, final_clip):
    opening = (VideoFileClip(opening)
               .set_start(0)
               .crossfadeout(1))
    initial_clip = (VideoFileClip(initial_clip)
                    .set_start(opening.duration)
                    .crossfadein(1)
                    .crossfadeout(1))
    final_clip = (VideoFileClip(final_clip)
                  .set_start(opening.duration + initial_clip.duration)
                  .crossfadein(1)
                  .crossfadeout(1))
    watermark = generate_watermark(opening.duration, initial_clip.duration + final_clip.duration)

    return CompositeVideoClip([opening, initial_clip, final_clip, watermark])


def composite_clip(opening, clip):
    opening = (VideoFileClip(opening)
               .set_start(0)
               .crossfadeout(1))
    clip = (VideoFileClip(clip)
            .set_start(opening.duration)
            .crossfadein(1)
            .crossfadeout(1))
    watermark = generate_watermark(opening.duration, clip.duration)

    return CompositeVideoClip([opening, clip, watermark])


def main(name):
    print(f'Hi, {name}')
    # SourceDownload.download_file("https://drive.google.com/drive/folders/1bGbVRol7v_biZ6k1_GCwHbte9J8E1q8o")

    opening = "tools/opening.mp4"
    clip1 = "source/000551-goal.mp4"
    clip2 = "source/001641-goal.mp4"

    single_clip = composite_clip(opening, clip1)
    single_clip.write_videofile("output/clip.mp4")

    full_video = composite_full_video(opening, clip1, clip2)
    full_video.write_videofile("output/full_video.mp4")


if __name__ == '__main__':
    main('PyCharm')
