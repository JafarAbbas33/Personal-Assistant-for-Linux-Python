import sys

class AssistantCommunicationsHandler:
    assistant = None
    root = None
    update_text = None
    bring_to_front = None
    minimize = None
    logger = None
    # Remains none due to changes made for efficiency
    screenshot = None
    stop_playback = False

    @staticmethod
    def terminate_from_main_thread():
        AssistantCommunicationsHandler.root.destroy()
        AssistantCommunicationsHandler.logger.info('Destroyed!\n')
        sys.exit()
    
    @staticmethod
    def terminate():
        AssistantCommunicationsHandler.assistant.conversation_stream.close()
        AssistantCommunicationsHandler.root.after(
            200, AssistantCommunicationsHandler.terminate_from_main_thread)
        AssistantCommunicationsHandler.logger.info("Destroying after 0.2 seconds...")
        sys.exit()
