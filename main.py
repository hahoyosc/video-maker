from source_download import SourceDownload
from composite_video import CompositeVideo
import os


def get_clips(source):

    clips = [source + x for x in os.listdir(source)]
    clips = [clip for clip in clips if clip.endswith('.mp4') or clip.endswith('.avi') or clip.endswith('.wmv')]
    clips.sort()

    return clips


def get_params(params):
    file = open(params, 'r')
    data = file.read()
    params_list = data.split('\n')
    formatted_params = []

    for param in params_list:
        hour, minute, second = param.split(':')
        formatted_params.append(int(hour) * 3600 + int(minute) * 60 + int(second))

    file.close()

    return formatted_params


def main(source, output, drive, params):

    if drive:
        SourceDownload.download_file("https://drive.google.com/drive/folders/" + drive)

    opening = "tools/opening.mp4"
    clips = get_clips(source)

    if params:
        output_video = CompositeVideo.composite_full_video(opening, clips[0], get_params(params))
        output_video.write_videofile(output + "Partido completo.mp4")

    else:
        for clip in clips:
            single_clip = CompositeVideo.composite_clip(clip)
            single_clip.write_videofile(output + clip.replace(source, ""))

        recap = CompositeVideo.composite_recap(opening, clips)
        recap.write_videofile(output + "Recopilacion.mp4")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--source', type=str, default='../', required=False, help="Highlights source folder")
    parser.add_argument('-o', '--output', type=str, default='../output/', required=False,
                        help="Processed highlights and recap output folder")
    parser.add_argument('-d', '--drive', type=str, default=None, required=False,
                        help="Google Drive ID in case you need to download the highlights")
    parser.add_argument('-p', '--params', type=str, default=None, required=False,
                        help="Time marks of the relevant parts of the match")
    args = parser.parse_args()

    main(source=args.source, output=args.output, drive=args.drive, params=args.params)
