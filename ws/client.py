"""Module for IQ option websocket."""

import json
import logging
import websocket


class WebsocketClient(object):
    """Class for work with IQ option websocket."""

    def __init__(self, api):
        """
        :param api: The instance of :class:`IQOptionAPI
            <iqoptionapi.api.IQOptionAPI>`.
        """
        self.api = api
        self.wss = websocket.WebSocketApp(
            self.api.wss_url, on_message=self.on_message,
            on_error=self.on_error, on_close=self.on_close,
            on_open=self.on_open)

    def reconnect(self):
        if (self.websocket):
            self.websocket.close()
        self.websocket_client.wss = None
        self.set_session_cookies()
        self.websocket_client = WebsocketClient(self)
        websocket_thread = threading.Thread(target=self.websocket.run_forever)
        websocket_thread.daemon = True
        websocket_thread.start()
        time.sleep(5)
        self.ssid(self.sid)

    def on_message(self, wss, message): # pylint: disable=unused-argument
        """Method to process websocket messages."""
        logger = logging.getLogger(__name__)
        logger.debug(message)

        message = json.loads(str(message))

        if message["name"] == "timeSync":
            self.api.timesync.server_timestamp = message["msg"]

        if message["name"] == "profile":
            self.api.profile.balance = message["msg"]["balance"]

        if message["name"] == "candles":
            self.api.candles.candles_data = message["msg"]["data"]

        if message["name"] == "listInfoData":
            listinfodata = lambda: None
            listinfodata.__dict__ = message["msg"][0]
            self.api.listinfodata.add_listinfodata(listinfodata)

    @staticmethod
    def on_error(wss, error): # pylint: disable=unused-argument
        """Method to process websocket errors."""
        logger = logging.getLogger(__name__)
        logger.error(error)

    @staticmethod
    def on_open(wss): # pylint: disable=unused-argument
        """Method to process websocket open."""
        logger = logging.getLogger(__name__)
        logger.debug("Websocket client connected.")

    @staticmethod
    def on_close(wss): # pylint: disable=unused-argument
        """Method to process websocket close."""
        logger = logging.getLogger(__name__)
        logger.debug("Websocket connection closed.")
