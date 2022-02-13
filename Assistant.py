import sys
import time
import threading

class Gui:
    assistant_window_canvas = None
    icon = None
    black_canvas = None
    root = None
    update_text = None
    bring_to_front = None
    minimize = None
    monitor = None
    screenshot = None
    mic = None
    mic_size = None
    mic_location = None

class Assistant:
    Gui = Gui
    assistant = None
    assistant_thread = None
    logger = None
    stop_playback = False
    terminate_flag = False

    @staticmethod
    def terminate_from_main_thread():
        Assistant.Gui.root.destroy()
        Assistant.logger.info('Destroyed!\n')
        sys.exit()
    
    @staticmethod
    def terminate(event):
        # print(dir(event))

        # for x in threading.enumerate():
        #     print(x)
        #     print(type(x))
        # for i in range(3):
        #     print('Thread count: ' + f'{threading.active_count()}')
        #     time.sleep(0.5)

        # Assistant.assistant.conversation_stream.close()
        # Assistant.Gui.root.after(200, Assistant.terminate_from_main_thread)
        # Assistant.logger.info("Destroying after 0.1 seconds...")
        while threading.active_count() != 1:
            time.sleep(0.3)
            
        print('Gracefully exiting.')
        Assistant.logger.info('Gracefully exiting.')
        Assistant.Gui.root.destroy()
        # Assistant.logger.info("Destroying after 0.2 seconds...")
        
        # print('---------------------------------------------------------')
        # for i in range(3):
        #     print('Thread count: ' + f'{threading.active_count()}')
        #     time.sleep(0.5)
        # for x in threading.enumerate():
        #     print(x)
        #     print(type(x))
        # sys.exit()
