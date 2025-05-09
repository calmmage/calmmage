


class ChatCoordinator:
    """
    Chat Coorinator class keeps track of all messages and interactions with the user
    and ensures that we send messages at appropriate moments and with the understanding of full context

    The main goal is to simulate real human-like behavior of the chat-bot

    Here are desired features:
    - "accumulation" when user writes a message - when user writes us, wait a little
    - "offline mode" - have periods of down-time, do not respond, then respond after
    - "another thought" - after user stopped sending messages, think a little more and write something
    - random activations
        - about old conversation topics
        - just 'how are you doing'
        - some proacive new ideas
    - "interruption" - what happens when user interrupts us while we are still responding to a previous message?

    How we are going to implement this:
    - Incoming queue for incoming messages
    - Outgoing queue for outgoing messages
    - Activation queue for activation events
    - main loop that look at all the queues and fixes the state just in case..

    processing of incoming and outgoing messages only happens in activation events

    Basic example:
    -> User sends us a message
    -> we intend to respond at timestamp x. we create an activation event at timestamp x
    -> scheduler runs the job at timestamp x - activation
    -> activation looks at the state of the queues, if no new messages arrived - we proceed as planned
    if new messages - re-evaluate, based on their timestamp and other contextual info
    """
    def __init__(self):
        pass

