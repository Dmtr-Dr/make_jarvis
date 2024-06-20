import threading
import time
import random
import queue

from actions import answer_action, proactive_action

            
class Agent:
    
    def __init__(self, settings):
        
        self.threads = []
        self.queue = queue.Queue()
        
        self.stop_event = threading.Event()
        self.interrupt_event = threading.Event()
        self.settings = settings
        self.dialog_history = []
        self.dialog_lock = threading.Lock()
        
        if settings['proactive_actions_thread']:
            self.proactive_thread = threading.Thread(target=self.proactive_actions_thread)
            self.proactive_thread.daemon = True
            self.threads.append(self.proactive_thread)
        
        if settings['memory_debug_thread']:
            self.debug_thread = threading.Thread(target=self.memory_debug_thread)
            self.debug_thread.daemon = True
            self.threads.append(self.debug_thread)
    
        self.event_loop_thread = threading.Thread(target=self.event_loop)
        self.event_loop_thread.daemon = True
        self.threads.append(self.event_loop_thread)

    def start(self):
        print('Starting...')
        for thread in self.threads:
            thread.start()

        print('Listening ...')  
    
    def stop(self):
        self.stop_event.set()
        print('Stopping...')

        
    def proactive_actions_thread(self):
        min_freq = self.settings.get('proactivity_frequency_sec', 30)
        max_freq = min_freq * 2
        while not self.stop_event.is_set():
            time.sleep(random.randint(min_freq,max_freq))
            with self.dialog_lock:
                proactive_action(st_memory=self.dialog_history)

    def memory_debug_thread(self):
        while not self.stop_event.is_set():
            time.sleep(30)
            for i, (role,message) in enumerate(self.dialog_history):
                print(f'{i} {role}: {message}')
        
    def add_event(self,event):
        self.queue.put(event)
            
    def event_loop(self):
        try:
            while not self.stop_event.is_set():
                time.sleep(1)
                if self.queue.empty():
                    continue
                event = self.queue.get()
                
                if event['type'] =='wakeword':
                    with self.dialog_lock:
                        answer_action(event['current_audio_file_name'],  st_memory=self.dialog_history)
                elif event['type'] == 'stopword':
                    self.stop() 
                else: 
                    print(f'Unknown event type: ',{event['type']})
        except KeyboardInterrupt:
            print('Stopping...')
            self.stop()
        
    
    def is_alive(self):
        return not self.stop_event.is_set()
        

        