import sys
from getpass import getpass
import fbchat
import mods


# subclass fbchat.Client and override required methods
class VicBot(fbchat.Client):
    """ Hi, I am a chatbot,  a modular bot made for Facebook messenger. """

    def __init__(self, email, password, debug=True, user_agent=None):
        if user_agent is None:
            user_agent = \
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36" + \
                "(KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36"
        fbchat.Client.__init__(self, email, password, debug, user_agent)
        self.modules = []

    def add_module(self, new_module):
        """ Add another submodule """
        self.modules.append(new_module)

    def on_typing(self, author_id, metadata=None):
        """ What happens when someone starts typing a message """
        pass

    def on_message(self, mid, author_id, author_name, message, metadata):
        """ What happens when a new message is received """
        message_type = "user"
        thread_id = metadata["delta"]["messageMetadata"]["threadKey"]
        # print("%s said (in %s): %s" % (author_id, thread_id, message))
        if "threadFbId" in thread_id:
            thread_id = thread_id["threadFbId"]
            message_type = "group"
        else:
            thread_id = thread_id["otherUserFbId"]

        print(message)
        if message.lower() == "help":
            response = [self.__doc__] + [mod.__doc__ for mod in self.modules]
            self.send(thread_id, "\n".join(response), message_type=message_type)
        else:
            for mod in self.modules:
                response = mod.parse_message(message, author_id, self.uid,
                                             thread_id, metadata)
                if response is not None:
                    self.send(thread_id, response, message_type=message_type)
                    break


if __name__ == "__main__":
    if len(sys.argv) >=3 :
        username, password = sys.argv[1:4]
    else:
        username, password = input("Username: "), getpass()
    client = VicBot(username, password, debug=False)
    client.add_module(mods.MarcoPolo())
    client.add_module(mods.Echo())
    print("Listening...")
    client.listen()
