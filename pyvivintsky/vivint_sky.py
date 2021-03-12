import logging

from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

from pyvivintsky.vivint_api import VivintAPI
from pyvivintsky.vivint_panel import VivintPanel
from pyvivintsky.vivint_pubnub_callback import VivintPubNubCallback

logger = logging.getLogger(__name__)

VIVINT_SUB_KEY = "sub-c-6fb03d68-6a78-11e2-ae8f-12313f022c90"


class VivintSky:
    """Class to handle all communication with Vivint"""

    def __init__(self, username: str, password: str):
        self.__vivint_api = VivintAPI(username, password)
        self.__auth_data: dict = None
        self.__panels: dict = None
        self.__pubnub: PubNub = None
        self.__pubnub_listener = VivintPubNubCallback(
            self.__handle_pubnub_message,
            self.__handle_pubnub_connected,
            self.__handle_pubnub_disconnected,
        )
        self.__pubnub_config = PNConfiguration()
        self.__pubnub_config.ssl = True
        self.__pubnub_config.subscribe_key = VIVINT_SUB_KEY

    async def login(self):
        if await self.__vivint_api.login():
            self.__auth_data = await self.__vivint_api.get_authorized_user()
            logger.debug("Logged into VivintSky API")
            return True
        else:
            raise ("Failed to authenticate to Vivint Sky")

    async def connect(self):
        """
        Connect to Vivint Sky and init devices
        """
        await self.login()
        self.__panels = await self.___init_panels()
        self.__init_pubnub()

    async def ___init_panels(self):
        """
        Initialize the panels from the Vivint Panel class.
        """
        panels = {}
        for descriptor in self.__auth_data["u"]["system"]:
            system = await self.__vivint_api.get_system_info(str(descriptor["panid"]))
            panels[str(descriptor["panid"])] = VivintPanel(
                self.__vivint_api, descriptor, system["system"]
            )
        return panels

    def __init_pubnub(self):
        """
        Initialize and subscribe to PubNub
        """
        if self.__pubnub == None:
            self.__pubnub = PubNub(self.__pubnub_config)
        self.__pubnub.add_listener(self.__pubnub_listener)
        self.__pubnub.subscribe().channels(
            "PlatformChannel#" + self.__auth_data["u"]["mbc"]
        ).execute()

    def __handle_pubnub_message(self, message):
        if u"panid" in message.keys():
            self.__panels[str(message[u"panid"])].handle_message(message)
        elif u"desq" in message.keys():
            logger.debug(message)
            self.__panels[str(message[u"desq"])].handle_message(message)
        elif "inbox_message" in message[u"t"]:
            try:
                logger.debug(message[u"da"][u"me"])
                logger.debug(message[u"da"][u"sub"])
                if "camera detected" in message[u"da"][u"me"]:
                    # camera a motion detection does not include the camer id, but its name is in the sub message
                    camera_name = message[u"da"][u"sub"].split("-")
                    camera_name = camera_name[1].strip()
                    # register_motion_event(
                    #     "Vivint", Device.objects.get(name=camera_name).id
                    # )
            except:
                logger.error(message)
        else:
            logger.warning("UNKNOWN")
            logger.debug(message)

    def __handle_pubnub_connected(self):
        logger.debug("Connected to PubNub channel")

    def __handle_pubnub_disconnected(self):
        logger.debug("Disconnected from PubNub channel")
        self.__pubnub.remove_listener(self.__pubnub_listener)
        self.__pubnub.stop()

    def get_panels(self):
        return self.__panels

    def get_panel(self, id):
        return self.__panels[id]

    def disconnect(self):
        """
        This disconnects and shuts down everything.
        """
        self.__pubnub.unsubscribe_all()
