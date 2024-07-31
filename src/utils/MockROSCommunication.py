import pickle, os
from filelock import FileLock

class MockROSCommunication():
    """ Disk-based mechanism to exchange data between threads"""
    __file = None
       
    def __init__(self, topic_name):
        try: 
            os.mkdir('tmp') 
        except OSError as error: 
            pass
        self.topic_name = f"./tmp/{topic_name}"
        self.__file = open(topic_name, 'wb')
        pickle.dump(None, self.__file)
        self.__file.close()

        self.lock_file = f"{self.topic_name}.lock"
        self.lock = FileLock(self.lock_file)

        
    def read(self):
        try:
            with self.lock:
                with open(self.topic_name, 'rb') as f:
                    dictionary = pickle.load(f)
                return dictionary
        except Exception as e:
            print("read error", e)
    
        
    
    def pop(self):
        dictionary = self.read()
        self.publish(None)
        return dictionary
        
    def publish(self, dictionary):
        try:
            with self.lock:
                with open(self.topic_name, 'wb') as f:
                    pickle.dump(dictionary, f)
        except Exception as e:
            print("write error", e)
