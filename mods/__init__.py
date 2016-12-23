
class SubModule(object):
    def parse_message(self, message, author_id, owner_id, thread_id, metadata):
        pass

    def parse_typing(self, message, author_id, owner_id, thread_id, metadata):
        pass


class Stats(SubModule):
    """ Stats module:
    I count all the messages. Type
    'stats' to get the total number
    of messages I've seen since my
    last restart. """

    def __init__(self):
        self.total_seen = 0

    def parse_message(self, message, *args, **kwargs):
        self.total_seen += 1
        if message.lower() == "stats":
            return "In total I have seen {} ".format(self.total_seen) + \
                   "messages since my last restart"


class MarcoPolo(SubModule):
    """ Marco-Polo module:
    If you type a message ending
    with 'Marco' I will type
    'Polo'. """

    def parse_message(self, message, author_id, owner_id, thread_id, metadata):
        if message.lower().endswith("marco"):
            return "Polo"


class Echo(SubModule):
    """ Echo Module:
    By typing 'echo on' I will start
    repeating everything you say.
    You can end this by typing
    'echo off' """

    def __init__(self):
        self.threads = set()

    def parse_message(self, message, author_id, owner_id, thread_id, metadata):
        if thread_id not in self.threads and message.lower() == "echo on":
            self.threads.add(thread_id)
            return "Echo service is now on.\nSend 'echo off' to end it."
        if message.lower() == "echo off":
            if thread_id in self.threads:
                self.threads.remove(thread_id)
                return "Echo service is now disabled"
            else:
                return "Echo service was already disabled"
        if thread_id in self.threads and str(author_id) != str(owner_id):
            return message
