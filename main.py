from source_download import SourceDownload
from composite_video import CompositeVideo
import os


def get_clips(source):

    clips = [source + x for x in os.listdir(source)]
    clips = [clip for clip in clips if clip.endswith('.mp4') or clip.endswith('.avi') or clip.endswith('.wmv')]
    clips.sort()

    return clips


def main(source, output, drive):

    if drive:
        SourceDownload.download_file("https://drive.google.com/drive/folders/" + drive)

    opening = "tools/opening.mp4"
    clips = get_clips(source)

    for clip in clips:
        single_clip = CompositeVideo.composite_clip(clip)
        single_clip.write_videofile(output + clip.replace(source, ""))

    full_video = CompositeVideo.composite_full_video(opening, clips)
    full_video.write_videofile(output + "Recopilacion.mp4")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--source', type=str, default='../', required=False, help="Highlights source folder")
    parser.add_argument('-o', '--output', type=str, default='../output/', required=False,
                        help="Processed highlights and recap output folder")
    parser.add_argument('-d', '--drive', type=str, default=None, required=False,
                        help="Google Drive ID in case you need to download the highlights")
    args = parser.parse_args()

    main(source=args.source, output=args.output, drive=args.drive)
