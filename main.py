from composite_video import CompositeVideo
from http import HTTPStatus
from drive_upload import DriveUpload
from whatsapp_notifications import WhatsappNotifications
import os
import json
import time


def get_clips(source):

    clips = [source + x for x in os.listdir(source)]
    clips = [clip for clip in clips if clip.endswith('.mp4') or clip.endswith('.avi') or clip.endswith('.wmv')]
    clips.sort()

    return clips


def get_params(params_file):
    file = open(params_file, encoding='utf-8')
    params = json.load(file)

    formatted_params = []
    for timestamp in params['timestamps']:
        hour, minute, second = timestamp.split(':')
        formatted_params.append(int(hour) * 3600 + int(minute) * 60 + int(second))
    params['timestamps'] = formatted_params

    return params


def main(source, output, params, full_video):
    total_start = time.time()
    params = get_params(params)

    clips = get_clips(source)
    team_a = params['results']['teamA']['name']
    team_b = params['results']['teamB']['name']
    match_name = params['results']['matchName']

    if full_video:
        print(f'Started processing full match {match_name}: {len(clips)} video found (only first will be processed)')
        CompositeVideo.composite_clips([clips[0]], output, params, full_video=True)
    else:
        print(f'Started processing clips for match {team_a} vs {team_b}: {len(clips)} clips found')
        CompositeVideo.composite_clips(clips, output, params)

    total_elapsed = round(time.time() - total_start, 1)
    print(f'Successfully processed clips - Done in {total_elapsed}s')
    time.sleep(5)

    drive = params['contentManagement']['driveParentFolder']
    if drive:
        files = [output + file for file in os.listdir(output)]
        files = [file for file in files if file.endswith('.mp4') or file.endswith('.avi') or file.endswith('.wmv')]
        files.sort()
        service_account_file = params['contentManagement']['serviceAccountFile']

        folder_id = DriveUpload.create_folder(match_name, drive, service_account_file)
        print(f'DRV - Folder created with ID {folder_id}')

        for file in files:
            print(f'DRV - Uploading {file} to the Drive folder')
            DriveUpload.upload_file(file, folder_id, service_account_file)
        print(f'DRV - Successfully uploaded {len(files)} files')

        print(f'WHA - Sending the highlights to the client')
        status_code, response_data = WhatsappNotifications.send_whatsapp_notification(params['whatsappBusiness'], match_name, folder_id)
        if status_code == HTTPStatus.OK:
            print(f'WHA - Successfully sent the message: {response_data}')
        else:
            print(f'WHA - Failed to send the message: {response_data}')


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--source', type=str, default='../', required=False, help="Highlights source folder")
    parser.add_argument('-o', '--output', type=str, default='../output/', required=False,
                        help="Processed highlights and recap output folder")
    parser.add_argument('-p', '--params', type=str, default='../params.json', required=False,
                        help="Time marks of the relevant parts of the match")
    parser.add_argument('-f', '--full', type=bool, action=argparse.BooleanOptionalAction,
                        help="Process the full match video")
    args = parser.parse_args()

    main(source=args.source, output=args.output, params=args.params, full_video=args.full)
