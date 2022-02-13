import sys

class Gui:
    black_canvas = None
    root = None
    update_text = None
    bring_to_front = None
    minimize = None
    monitor = None
    screenshot = None
    mic = None      

class Assistant:
    Gui = Gui
    assistant = None
    logger = None
    stop_playback = False

    @staticmethod
    def terminate_from_main_thread():
        Assistant.root.destroy()
        Assistant.logger.info('Destroyed!\n')
        sys.exit()
    
    @staticmethod
    def terminate():
        Assistant.assistant.conversation_stream.close()
        Assistant.root.after(
            200, Assistant.terminate_from_main_thread)
        Assistant.logger.info("Destroying after 0.2 seconds...")
        sys.exit()
