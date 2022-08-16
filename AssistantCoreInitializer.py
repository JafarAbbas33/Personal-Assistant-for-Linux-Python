
import time
import os, sys
import logging
import threading

import hotword_detector
from Assistant import Assistant

from AssistantCore import AssistantCore

import concurrent.futures
import json
import os.path
import pathlib2 as pathlib
import uuid
import click
import grpc
import google.auth.transport.grpc
import google.auth.transport.requests
import google.oauth2.credentials

from google.assistant.embedded.v1alpha2 import (
    embedded_assistant_pb2,
    embedded_assistant_pb2_grpc
)
from tenacity import retry, stop_after_attempt, retry_if_exception

# try:
# from . import (
#     assistant_helpers,
#     audio_helpers,
#     browser_helpers,
#     device_helpers
# )
# except (SystemError, ImportError):
import assistant_helpers
import audio_helpers
import browser_helpers
import device_helpers



def AssistantCoreInitializer():
    api_endpoint = 'embeddedassistant.googleapis.com'
    credentials = os.environ['assistant_credentials']
    project_id = 'long-micron-259117'
    device_model_id = 'long-micron-259117-aw-wxtxyb'
    device_id = os.environ['assistant_device_id']
    device_config = os.environ['assistant_device_config']
    lang = 'en-US'
    display = False
    verbose = False
    input_audio_file = None
    output_audio_file = None
    audio_sample_rate = audio_helpers.DEFAULT_AUDIO_SAMPLE_RATE
    audio_sample_width = audio_helpers.DEFAULT_AUDIO_SAMPLE_WIDTH
    audio_iter_size = audio_helpers.DEFAULT_AUDIO_ITER_SIZE
    audio_block_size = audio_helpers.DEFAULT_AUDIO_DEVICE_BLOCK_SIZE
    audio_flush_size = audio_helpers.DEFAULT_AUDIO_DEVICE_FLUSH_SIZE
    grpc_deadline = 60 * 3 + 5
    once = False

    """Samples for the Google Assistant API.

    Examples:
      Run the sample with microphone input and speaker output:

        $ python -m googlesamples.assistant

      Run the sample with file input and speaker output:

        $ python -m googlesamples.assistant -i <input file>

      Run the sample with file input and output:

        $ python -m googlesamples.assistant -i <input file> -o <output file>
    """
    # Setup logging.
    logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO)

    # Load OAuth 2.0 credentials.
    try:
        with open(credentials, 'r') as f:
            credentials = google.oauth2.credentials.Credentials(token=None,
                                                                **json.load(f))
            http_request = google.auth.transport.requests.Request()
            credentials.refresh(http_request)
    except Exception as e:
        Assistant.logger.info('Error loading credentials: %s', e)
        Assistant.logger.info('Run google-oauthlib-tool to initialize '
                      'new OAuth 2.0 credentials.')


        # Assistant.Gui.bring_to_front()
        Assistant.Gui.update_text("Credentials error. Running appropriate program to update it.\nCommand is automatically copied. Paste it in the following program.")
        time.sleep(6)
        Assistant.Gui.minimize()

        os.system('x-terminal-emulator -e "my_utils/google-oauthlib-tool-helper"')
        
        try:
            with open(credentials, 'r') as f:
                credentials = google.oauth2.credentials.Credentials(token=None,
                                                                    **json.load(f))
                http_request = google.auth.transport.requests.Request()
                credentials.refresh(http_request)
        except Exception as e:
            Assistant.Gui.bring_to_front()
            Assistant.Gui.update_text("Failed to load credentials. Quitting.")
            Assistant.logger.info('Failed to load credentials. Quitting.\n')
            time.sleep(2)
            Assistant.Gui.minimize()

            Assistant.terminate_flag = True

            return False


    # Create an authorized gRPC channel.
    grpc_channel = google.auth.transport.grpc.secure_authorized_channel(
        credentials, http_request, api_endpoint)
    logging.info('Connecting to %s', api_endpoint)

    # Configure audio source and sink.
    audio_device = None
    if input_audio_file:
        audio_source = audio_helpers.WaveSource(
            open(input_audio_file, 'rb'),
            sample_rate=audio_sample_rate,
            sample_width=audio_sample_width
        )
    else:
        audio_source = audio_device = (
            audio_device or audio_helpers.SoundDeviceStream(
                sample_rate=audio_sample_rate,
                sample_width=audio_sample_width,
                block_size=audio_block_size,
                flush_size=audio_flush_size
            )
        )
    if output_audio_file:
        audio_sink = audio_helpers.WaveSink(
            open(output_audio_file, 'wb'),
            sample_rate=audio_sample_rate,
            sample_width=audio_sample_width
        )
    else:
        audio_sink = audio_device = (
            audio_device or audio_helpers.SoundDeviceStream(
                sample_rate=audio_sample_rate,
                sample_width=audio_sample_width,
                block_size=audio_block_size,
                flush_size=audio_flush_size
            )
        )
    # Create conversation stream with the given audio source and sink.
    conversation_stream = audio_helpers.ConversationStream(
        source=audio_source,
        sink=audio_sink,
        iter_size=audio_iter_size,
        sample_width=audio_sample_width,
    )

    if not device_id or not device_model_id:
        try:
            with open(device_config) as f:
                device = json.load(f)
                device_id = device['id']
                device_model_id = device['model_id']
                logging.info("Using device model %s and device id %s",
                             device_model_id,
                             device_id)
        except Exception as e:
            logging.warning('Device config not found: %s' % e)
            logging.info('Registering device')
            if not device_model_id:
                logging.error('Option --device-model-id required '
                              'when registering a device instance.')
                sys.exit(-1)
            if not project_id:
                logging.error('Option --project-id required '
                              'when registering a device instance.')
                sys.exit(-1)
            device_base_url = (
                'https://%s/v1alpha2/projects/%s/devices' % (api_endpoint,
                                                             project_id)
            )
            device_id = str(uuid.uuid1())
            payload = {
                'id': device_id,
                'model_id': device_model_id,
                'client_type': 'SDK_SERVICE'
            }
            session = google.auth.transport.requests.AuthorizedSession(
                credentials
            )
            r = session.post(device_base_url, data=json.dumps(payload))
            if r.status_code != 200:
                logging.error('Failed to register device: %s', r.text)
                sys.exit(-1)
            logging.info('Device registered: %s', device_id)
            pathlib.Path(os.path.dirname(device_config)).mkdir(exist_ok=True)
            with open(device_config, 'w') as f:
                json.dump(payload, f)

    device_handler = device_helpers.DeviceRequestHandler(device_id)


    with AssistantCore(lang, device_model_id, device_id,
                         conversation_stream, display,
                         grpc_channel, grpc_deadline,
                         device_handler) as assistant:

        # keep recording voice requests using the microphone
        # and playing back assistant response using the speaker.
        # When the once flag is set, don't wait for a trigger. Otherwise, wait.
        wait_for_user_trigger = not once
        assistant.conversation_stream.volume_percentage = 100
        
        Assistant.assistant = assistant
        Assistant.logger.info('Listening... Press Esc key to exit\n')
        Assistant.Gui.update_text('Hello sir!')
        
        time.sleep(2)
        Assistant.Gui.minimize()

        while True:
            if wait_for_user_trigger:
                hotword_detector.start_hotword_detection()
                if Assistant.terminate_flag:
                    Assistant.Gui.root.event_generate("<<terminate>>", when="tail")
                    return False
                
            Assistant.Gui.bring_to_front()
            continue_conversation = assistant.assist()
            # print(continue_conversation)
            Assistant.Gui.minimize()
            
            Assistant.logger.info('Thread count: ' + f'{threading.active_count()}')
            
            # if continue_conversation == None:
            #     return False
            
            # wait for user trigger if there is no follow-up turn in
            # the conversation.
            wait_for_user_trigger = not continue_conversation
