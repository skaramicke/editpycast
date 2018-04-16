import os
import yaml
import logging

from session import process_session


def verify_config(podcast, config, logger):
    if 'input' not in config:
        logger.error('Config for {} is missing value "input"'.format(podcast))
        return False
    
    if os.path.isfile(config['input']):
        logger.error('The input path specified for {} is a file. It needs to be a directory.'.format(podcast))
        return False

    if 'output' not in config:
        logger.error('Config for {} is missing value "output"'.format(podcast))
        return False
    
    if os.path.isfile(config['output']):
        logger.error('The putput path specified for {} is a file. It needs to be a directory.'.format(podcast))
        return False

    if 'completed' in config and os.path.isfile(config['completed']):
        logger.error('The "completed" path specified for {} is a file. It needs to be a directory.'.format(podcast))
        return False

    if not os.path.exists(config['input']):
        logger.warning('Input path for config {} is missing. Creating.'.format(podcast))
        os.mkdir(config['input'])
        
    if not os.path.exists(config['output']):
        logger.warning('Output path for config {} is missing. Creating.'.format(podcast))
        os.mkdir(config['output'])

    return True


def main():
    """Process wav files from recordings folder and make a podcast episode from them"""
    logging.basicConfig(
        filename='logs/generate_episode.log',
        level=logging.WARNING,
        format="Main %(levelname)s %(asctime)s - %(message)s")

    logger = logging.getLogger()
    
    # Load config file
    config = {}
    with open("config.yaml", 'r') as stream:
        try:
            config = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    
    # For each configured podcast
    for podcast_name in config['podcasts']:
        podcast_config = config['podcasts'][podcast_name]
        
        if not verify_config(podcast_name, podcast_config, logger):
            print('Configuration "{}" is incorrect. Please check the logs for more information'.format(podcast_name))
            continue
        
        # For each subfolder of the podcast
        for session_name in os.listdir('{}/'.format(podcast_config['input'])):
            if not os.path.isdir('{}/{}'.format(podcast_config['input'], session_name)) or session_name.startswith('.'):
                continue

            process_session(podcast_name, session_name, podcast_config)


if __name__ == '__main__':
    main()
