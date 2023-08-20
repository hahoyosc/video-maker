from source_download import SourceDownload
from composite_video import CompositeVideo
import os


def get_clips(source):

    clips = [source + x for x in os.listdir(source)]
    clips = [clip for clip in clips if clip.endswith('.mp4') or clip.endswith('.avi') or clip.endswith('.wmv')]
    clips.sort()

    return clips


def main():
    # SourceDownload.download_file("https://drive.google.com/drive/folders/1bGbVRol7v_biZ6k1_GCwHbte9J8E1q8o")

    opening = "tools/opening.mp4"
    source = "source/"
    output = "output/"
    clips = get_clips(source)

    for clip in clips:
        single_clip = CompositeVideo.composite_clip(clip)
        single_clip.write_videofile(output + clip.replace(source, ""))

    full_video = CompositeVideo.composite_full_video(opening, clips)
    full_video.write_videofile(output + "Recopilacion.mp4")


if __name__ == '__main__':
    main()
