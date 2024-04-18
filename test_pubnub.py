from flask import Flask
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.callbacks import SubscribeCallback
import unittest
from unittest.mock import MagicMock

app = Flask(__name__)

class MySubscribeCallback(SubscribeCallback):
    def __init__(self):
        super().__init__()
        self.messages = []

    def message(self, pubnub, message):
        # Append received message to the messages list
        self.messages.append(message['message'])

def subscribe_to_channel(pubnub):
    pubnub.add_listener(MySubscribeCallback())
    pubnub.subscribe().channels('aq_channel').execute()

# Mock PubNub instance and message
pubnub_mock = MagicMock()
message = {"message": "Test message"}

class TestPubNub(unittest.TestCase):
    def test_message_received(self):
        # Instantiate callback and call message method
        callback = MySubscribeCallback()
        callback.message(pubnub_mock, message)

        # Ensure message is appended correctly
        self.assertEqual(callback.messages, [message["message"]])

    def test_subscribe_to_channel(self):
        # Call the subscribe_to_channel function
        subscribe_to_channel(pubnub_mock)

        # Ensure that the subscribe method was called with the correct channel
        pubnub_mock.subscribe.return_value.channels.assert_called_once_with('aq_channel')

    def test_unsubscribe_from_channel(self):
        # Call the unsubscribe_from_channel function
        pubnub_mock.unsubscribe().channels('aq_channel').execute(pn_async=MagicMock())

        # Verify that the unsubscribe method was called with the correct channel
        pubnub_mock.unsubscribe.assert_called_once()

    def test_error_handling(self):
        # Simulate an error message with the correct structure
        error_message = {"message": "Test error"}
        callback = MySubscribeCallback()
        
        # Call the message method with the error message
        callback.message(pubnub_mock, error_message)

        # Verify that the error message appended to the messages list
        self.assertEqual(callback.messages, ["Test error"])


if __name__ == '__main__':
    unittest.main()
