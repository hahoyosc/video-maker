import ffmpeg
import time
import os

from config import *

watermark = ffmpeg.input(f'{TOOLS_FOLDER}{WATERMARK_IMAGE}').filter('scale', f'{WATERMAR_SCALE}*in_w', f'{WATERMAR_SCALE}*in_h')

def get_info(input_file):
    info = {}
    probe = ffmpeg.probe(input_file)
    try:
        for stream in probe['streams']:
            if stream['codec_type'] == 'video':
                info["vcodec"] = stream['codec_name']
                info["width"] = int(stream['width'])
                info["height"] = int(stream['height'])
                info["fps"] = round(eval(stream['avg_frame_rate']), 2)
                info["duration"] = float(stream['duration'])
            elif stream['codec_type'] == 'audio':
                info["acode"] = stream['codec_name']

    except:
        return info

    return info

def get_opening_clip(fps, output, params):
    start = time.time()
    vcodec = params['config']['vcodec']
    acodec = params['config']['acodec']
    audio = ffmpeg.input("anullsrc=r=48000:cl=stereo", f="lavfi").audio

    filename = f'{TOOLS_FOLDER}{OPENING_VIDEO}'
    output_file = f'{output}{OPENING_VIDEO}'
    info = get_info(filename)
    info_str = " ".join(f"{v}" for v in info.values())
    print(f'EXT - processing opening clip {filename} ({info_str}) ...', end='\r', flush=True)

    video = ffmpeg.input(filename)
    out_clip = video.filter('fade', t='out', st=EXTRA_CLIPS_DURATION-1, d=1)
    video_output = ffmpeg.output(out_clip, audio, output_file, t=EXTRA_CLIPS_DURATION, vcodec=vcodec, acodec=acodec, r=fps)
    ffmpeg.run(video_output, overwrite_output=True, quiet=QUIET_FFMPEG)

    elapsed = round(time.time() - start, 1)
    print(f'EXT - processing opening clip {filename} ({info_str}): {elapsed}s')
    return output_file

def generate_vs_clip(fps, output, params):
    start = time.time()
    vcodec = params['config']['vcodec']
    acodec = params['config']['acodec']
    audio = ffmpeg.input("anullsrc=r=48000:cl=stereo", f="lavfi").audio

    filename = f'{TOOLS_FOLDER}{VS_VIDEO}'
    output_file = f'{output}{VS_VIDEO}'
    info = get_info(filename)
    info_str = " ".join(f"{v}" for v in info.values())
    print(f'EXT - processing vs clip {filename} ({info_str}) ...', end='\r', flush=True)

    team_a = params["results"]["teamA"]["name"]
    team_b = params["results"]["teamB"]["name"]
    crest_a = params["results"]["teamA"]["crest"]
    crest_b = params["results"]["teamB"]["crest"]

    draw_crestmark_a = False
    draw_crestmark_b = False
    text_pos_h = 0.5
    if crest_a != '':
        crest_a = f'{CRESTS_FOLDER}{crest_a}' if '/' not in crest_a else crest_a
        crestmark_a = ffmpeg.input(crest_a).filter('scale', CRESTS_SIZE, CRESTS_SIZE)
        draw_crestmark_a = True
        text_pos_h = 0.25

    if crest_b != '':
        crest_b = f'{CRESTS_FOLDER}{crest_b}' if '/' not in crest_b else crest_b
        crestmark_b = ffmpeg.input(crest_b).filter('scale', CRESTS_SIZE, CRESTS_SIZE)
        draw_crestmark_b = True
        text_pos_h = 0.25

    out_clip = ffmpeg.input(filename, r=fps)
    out_clip = out_clip.drawtext(text=team_a, x=f'{TEAM_A_X_ALIGN}*main_w-0.5*tw', y=f'{text_pos_h}*main_h-0.5*th', fontfile=FONT_PATH, fontsize=RES_NAMES_FS, fontcolor=FONT_COLOR)
    out_clip = out_clip.drawtext(text=team_b, x=f'{TEAM_B_X_ALIGN}*main_w-0.5*tw', y=f'{text_pos_h}*main_h-0.5*th', fontfile=FONT_PATH, fontsize=RES_NAMES_FS, fontcolor=FONT_COLOR)
    out_clip = out_clip.overlay(crestmark_a, x=f'{TEAM_A_X_ALIGN}*main_w-0.5*overlay_w', y='0.5*main_h-0.5*overlay_h') if draw_crestmark_a else out_clip
    out_clip = out_clip.overlay(crestmark_b, x=f'{TEAM_B_X_ALIGN}*main_w-0.5*overlay_w', y='0.5*main_h-0.5*overlay_h') if draw_crestmark_b else out_clip

    out_clip = out_clip.overlay(watermark, x=f'main_w-{WATERMARK_OFFSET_RIGHT_X}', y=f'main_h-{WATERMARK_OFFSET_BOTTOM_Y}')
    out_clip = out_clip.filter('fade', t='in', st=0, d=1).filter('fade', t='out', st=EXTRA_CLIPS_DURATION-1, d=1)
    video_output = ffmpeg.output(out_clip, audio, output_file, t=EXTRA_CLIPS_DURATION, vcodec=vcodec, acodec=acodec, r=fps)
    ffmpeg.run(video_output, overwrite_output=True, quiet=QUIET_FFMPEG)

    elapsed = round(time.time() - start, 1)
    print(f'EXT - processing vs clip {filename} ({info_str}): {elapsed}s')
    return output_file

def generate_results_clip(fps, output, params):
    start = time.time()
    vcodec = params['config']['vcodec']
    acodec = params['config']['acodec']
    audio = ffmpeg.input("anullsrc=r=48000:cl=stereo", f="lavfi").audio

    filename = f'{TOOLS_FOLDER}{RESULTS_IMAGE}'
    output_file = f'{output}{RESULTS_VIDEO}'
    info = get_info(filename)
    info_str = " ".join(f"{v}" for v in info.values())
    print(f'EXT - processing results clip {filename} ({info_str}) ...', end='\r', flush=True)

    team_a = params["results"]["teamA"]["name"]
    team_b = params["results"]["teamB"]["name"]
    score_a = params["results"]["teamA"]["score"]
    score_b = params["results"]["teamB"]["score"]
    crest_a = params["results"]["teamA"]["crest"]
    crest_b = params["results"]["teamB"]["crest"]

    draw_crestmark_a = False
    draw_crestmark_b = False
    text_pos_h = 0.35
    score_pos_h = 0.6
    if crest_a != '':
        crest_a = f'{CRESTS_FOLDER}{crest_a}' if '/' not in crest_a else crest_a
        crestmark_a = ffmpeg.input(crest_a).filter('scale', CRESTS_SIZE, CRESTS_SIZE)
        draw_crestmark_a = True
        text_pos_h = 0.25
        score_pos_h = 0.8
    if crest_b != '':
        crest_b = f'{CRESTS_FOLDER}{crest_b}' if '/' not in crest_b else crest_b
        crestmark_b = ffmpeg.input(crest_b).filter('scale', CRESTS_SIZE, CRESTS_SIZE)
        draw_crestmark_b = True
        text_pos_h = 0.25
        score_pos_h = 0.8

    video = ffmpeg.input(filename, loop=1, t=EXTRA_CLIPS_DURATION, r=fps)
    out_clip = video.drawtext(text='RESULTADO DEL PARTIDO', x='0.5*w-0.5*tw', y='0.06*h-0.5*th', fontfile=FONT_PATH, fontsize=RES_TITLE_FS, fontcolor=FONT_COLOR)
    out_clip = out_clip.drawtext(text=team_a, x=f'{TEAM_A_X_ALIGN}*main_w-0.5*tw', y=f'{text_pos_h}*main_h-0.5*th', fontfile=FONT_PATH, fontsize=RES_NAMES_FS, fontcolor=FONT_COLOR)
    out_clip = out_clip.drawtext(text=team_b, x=f'{TEAM_B_X_ALIGN}*main_w-0.5*tw', y=f'{text_pos_h}*main_h-0.5*th', fontfile=FONT_PATH, fontsize=RES_NAMES_FS, fontcolor=FONT_COLOR)
    out_clip = out_clip.drawtext(text=score_a, x=f'{TEAM_A_X_ALIGN}*main_w-0.5*tw', y=f'{score_pos_h}*main_h-0.5*th', fontfile=FONT_PATH, fontsize=RES_SCORE_FS, fontcolor=FONT_COLOR)
    out_clip = out_clip.drawtext(text=score_b, x=f'{TEAM_B_X_ALIGN}*main_w-0.5*tw', y=f'{score_pos_h}*main_h-0.5*th', fontfile=FONT_PATH, fontsize=RES_SCORE_FS, fontcolor=FONT_COLOR)
    out_clip = out_clip.overlay(crestmark_a, x=f'{TEAM_A_X_ALIGN}*main_w-0.5*overlay_w', y='0.5*main_h-0.5*overlay_h') if draw_crestmark_a else out_clip
    out_clip = out_clip.overlay(crestmark_b, x=f'{TEAM_B_X_ALIGN}*main_w-0.5*overlay_w', y='0.5*main_h-0.5*overlay_h') if draw_crestmark_b else out_clip

    out_clip = out_clip.overlay(watermark, x=f'main_w-{WATERMARK_OFFSET_RIGHT_X}', y=f'main_h-{WATERMARK_OFFSET_BOTTOM_Y}')
    out_clip = out_clip.filter('fade', t='in', st=0, d=1).filter('fade', t='out', st=EXTRA_CLIPS_DURATION-1, d=1)
    video_output = ffmpeg.output(out_clip, audio, output_file, t=EXTRA_CLIPS_DURATION, vcodec=vcodec, acodec=acodec, r=fps)
    ffmpeg.run(video_output, overwrite_output=True, quiet=QUIET_FFMPEG)

    elapsed = round(time.time() - start, 1)
    print(f'EXT - processing results clip {filename} ({info_str}): {elapsed}s')
    return output_file

def composite_clips(clips, output, params, full_video=False):
    clip_files = []
    vcodec = params['config']['vcodec']
    acodec = params['config']['acodec']
    name_a = params["results"]["teamA"]["short_name"]
    name_b = params["results"]["teamB"]["short_name"]
    crest_a = params["results"]["teamA"]["crest"]
    crest_b = params["results"]["teamB"]["crest"]
    debug = params['config']['debug']
    if debug:
        QUIET_FFMPEG = False
    else:
        QUIET_FFMPEG = True

    draw_crestmark_a = False
    draw_crestmark_b = False
    if crest_a != '':
        crest_a = f'{CRESTS_FOLDER}{crest_a}' if '/' not in crest_a else crest_a
        crestmark_a = ffmpeg.input(crest_a).filter('scale', SCORE_CRESTS_SIZE, SCORE_CRESTS_SIZE)
        draw_crestmark_a = True
    if crest_b != '':
        crest_b = f'{CRESTS_FOLDER}{crest_b}' if '/' not in crest_b else crest_b
        crestmark_b = ffmpeg.input(crest_b).filter('scale', SCORE_CRESTS_SIZE, SCORE_CRESTS_SIZE)
        draw_crestmark_b = True

    score_a = 0
    score_b = 0
    for i, clip in enumerate(clips):
        start = time.time()
        filename = clip.split('/')[-1]
        output_file = f'{output}{filename}'
        goal_clip = False
        goal_a = False
        if GOAL_A_KEY in filename:
            score_a += 1
            goal_clip = True
            goal_a = True
        elif GOAL_B_KEY in filename:
            score_b += 1
            goal_clip = True

        info = get_info(clip)
        duration = info["duration"]
        fps = info["fps"]
        info_str = " ".join(f"{v}" for v in info.values())
        print(f'{str(i+1).zfill(3)} - processing file {filename} ({info_str}) ...', end='\r', flush=True)

        video = ffmpeg.input(clip)
        audio = video.audio
        out_clip = video.overlay(watermark, x=f'main_w-{WATERMARK_OFFSET_RIGHT_X}', y=f'main_h-{WATERMARK_OFFSET_BOTTOM_Y}')

        if not full_video:
            score_text = f"{score_a} - {score_b}"
            score_text_post = ''
            enable = f'between(t,{0},{duration})'
            enable_post = ''
            if goal_clip:
                trans = duration - SCORE_TRANSITION_TIME
                enable = f'between(t,{0},{trans})'
                enable_post = f'between(t,{trans},{duration})'
                score_text_post = f"{score_a} - {score_b}"
                if goal_a:
                    score_text = f"{score_a - 1} - {score_b}"
                else:
                    score_text = f"{score_a} - {score_b - 1}"

            if not (draw_crestmark_a and draw_crestmark_b):
                score_text = f"{name_a}   {score_text}   {name_b}"
                score_text_post = f"{name_a}   {score_text_post}   {name_b}"

            out_clip = out_clip.drawtext(text=score_text, fontfile=FONT_PATH, x=f'{SCORE_X_CENTER}*w-0.5*tw', y=f'{SCORE_Y_CENTER}*h-0.5*th', fontsize=60, fontcolor=FONT_COLOR, shadowcolor='black@0.8', shadowx=2, shadowy=2, enable=enable)
            out_clip = out_clip.drawtext(text=score_text_post, fontfile=FONT_PATH, x=f'{SCORE_X_CENTER}*w-0.5*tw', y=f'{SCORE_Y_CENTER}*h-0.5*th', fontsize=60, fontcolor=FONT_COLOR, shadowcolor='black@0.8', shadowx=2, shadowy=2, enable=enable_post) if goal_clip else out_clip

            out_clip = out_clip.overlay(crestmark_a, x=f'{SCORE_X_CENTER}*main_w-0.5*overlay_w-{SCORE_CRESTS_DX}', y=f'{SCORE_Y_CENTER}*main_h-0.5*overlay_h') if draw_crestmark_a and draw_crestmark_b else out_clip
            out_clip = out_clip.overlay(crestmark_b, x=f'{SCORE_X_CENTER}*main_w-0.5*overlay_w+{SCORE_CRESTS_DX}', y=f'{SCORE_Y_CENTER}*main_h-0.5*overlay_h') if draw_crestmark_a and draw_crestmark_b else out_clip

        out_clip = out_clip.filter('fade', t='in', st=0, d=1).filter('fade', t='out', st=duration-1, d=1)
        video_output = ffmpeg.output(out_clip, audio, output_file, vcodec=vcodec, acodec=acodec, r=fps)
        ffmpeg.run(video_output, overwrite_output=True, quiet=QUIET_FFMPEG)

        elapsed = round(time.time() - start, 1)
        print(f'{str(i+1).zfill(3)} - processing file {filename} ({info_str}): {elapsed}s')

        clip_files.append(output_file)

    opening_clip = get_opening_clip(fps, output, params)
    vs_clip = generate_vs_clip(fps, output, params)
    results_clip = generate_results_clip(fps, output, params)

    clip_files = [opening_clip, vs_clip] + clip_files + [results_clip]
    if full_video:
        concatenate_clips(clip_files, output, params, file_name=FULL_MATCH_FILENAME)
    else:
        concatenate_clips(clip_files, output, params, file_name=RECAP_FILENAME)

    for clip_to_delete in [opening_clip, vs_clip, results_clip]:
        if os.path.exists(clip_to_delete):
            os.remove(clip_to_delete)

def concatenate_clips(clips, output, params, file_name):
    print('END - concatenating videos...', end='\r', flush=True)
    start = time.time()
    vcodec = params['config']['vcodec']
    acodec = params['config']['acodec']

    output_file = f'{output}{file_name}'
    inputs = [ffmpeg.input(video) for video in clips]
    video_streams = [video.video for video in inputs]
    audio_streams = [video.audio for video in inputs]

    video_concat = ffmpeg.concat(*video_streams, v=1, a=0).node
    audio_concat = ffmpeg.concat(*audio_streams, v=0, a=1).node

    output = ffmpeg.output(video_concat[0], audio_concat[0], output_file, vcodec=vcodec, acodec=acodec)
    ffmpeg.run(output, overwrite_output=True, quiet=QUIET_FFMPEG)

    elapsed = round(time.time() - start, 1)
    print(f'END - concatenating videos: {elapsed}s')
