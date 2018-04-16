import sys
import logging
import os

from track import Track


def process_session(podcast_name, session_name, config):
    logger = logging.getLogger()
    
    logger_stdout = logging.StreamHandler(sys.stdout)
    logger_stdout.setLevel(logging.INFO)
    formatter = logging.Formatter("{}/{} %(levelname)s %(asctime)s - %(message)s".format(podcast_name, session_name))
    logger_stdout.setFormatter(formatter)
    logger.addHandler(logger_stdout)
    
    files = []
    longest_track_length = 0
    logger.info('Calculating track length')
    for file in os.listdir('{}/{}'.format(config['input'], session_name)):
        filename = '{}/{}/{}'.format(config['input'], session_name, file)
        
        if not os.path.isfile(filename) \
                or file.startswith('.') \
                or not filename.endswith('.wav'):
            continue
        
        files.append(filename)
        logger.info('Checking length of {}'.format(file))
        track = Track(filename, config, logger)
        if track.get_length() > longest_track_length:
            longest_track_length = track.get_length()
    
    logger.info('Longest track was {} samples. Will pad those that are shorter.'.format(longest_track_length))
    
    combined_track = None
    for i, file in enumerate(files):
        logger.info('Processing {}'.format(file))
        track = Track(file, config, logger)
        track.set_length(longest_track_length)
        track.prepare(i, len(files))
        if not combined_track:
            combined_track = track
        else:
            combined_track.add(track)
        del track
    
    # Remove silence in beginning and end of mix
    combined_track.trim()
    
    if 'intro' in config:
        intros = config['intro']
        intros.reverse()
        
        for intro_file in intros:
            logger.info('Prepending intro track {}'.format(intro_file))
            intro = Track('jingles/{}'.format(intro_file), config, logger)
            intro.prepare()
            combined_track.prepend(intro)

    if 'outro' in config:
        for outro_file in config['outro']:
            logger.info('Appending outro track {}'.format(outro_file))
            outro = Track('jingles/{}'.format(outro_file), config, logger)
            outro.prepare()
            combined_track.append(outro)
    
    # Export to .mp3
    # TODO: Not WAV, MP3!
    combined_track.export('{}/{}'.format(config['output'], session_name))
    
    # Move original files to 'completed' dir
    if 'completed' in config:
        os.rename(
            '{}/{}'.format(config['input'], session_name),
            '{}/{}'.format(config['completed'], session_name)
        )