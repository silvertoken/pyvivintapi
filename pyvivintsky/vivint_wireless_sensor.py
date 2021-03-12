import logging
from enum import Enum

from pyvivintsky.vivint_device import VivintDevice

logger = logging.getLogger(__name__)


class VivintWirelessSensor(VivintDevice):
    """Generic Wireless Sensor."""

    class EquipmentCode(Enum):
        APOLLO_COMBO_CO = 1422
        APOLLO_COMBO_SMOKE = 1322
        CARBON_MONOXIDE_DETECTOR_345_MHZ = 1254
        CO1_CO = 860
        CO1_CO_CANADA = 859
        CO3_2_GIG_CO = 1026
        DBELL1_2_GIG_DOORBELL = 1063
        DW10_THIN_DOOR_WINDOW = 862
        DW11_THIN_DOOR_WINDOW = 1251
        DW20_RECESSED_DOOR = 863
        DW21_R_RECESSED_DOOR = 1252
        EXISTING_CO = 692
        EXISTING_DOOR_WINDOW_CONTACT = 655
        EXISTING_FLOOD_TEMP = 556
        EXISTING_GLASS_BREAK = 475
        EXISTING_HEAT = 708
        EXISTING_MOTION_DETECTOR = 609
        EXISTING_SMOKE = 616
        FIREFIGHTER_AUDIO_DETECTOR = 1269
        GARAGE01_RESOLUTION_TILT = 1061
        GB1_GLASS_BREAK = 864
        GB2_GLASS_BREAK = 1248
        HW_DW_5816 = 673
        HW_FLOOD_SENSOR_5821 = 624
        HW_GLASS_BREAK_5853 = 519
        HW_HEAT_SENSOR_5809 = 557
        HW_PANIC_PENDANT_5802_MN2 = 491
        HW_PIR_5890 = 533
        HW_PIR_5894_PI = 530
        HW_R_DW_5818_MNL = 470
        HW_SMOKE_5808_W3 = 589
        OTHER = 0
        PAD1_345_WIRELESS_KEYPAD = 867
        PANIC1 = 868
        PANIC2 = 1253
        PIR1_MOTION = 869
        PIR2_MOTION = 1249
        RE219_FLOOD_SENSOR = 1128
        RE220_T_2_GIG_REPEATER = 1144
        RE224_DT_DSC_TRANSLATOR = 1208
        RE224_GT_GE_TRANSLATOR = 941
        RE508_X_REPEATER = 2832
        RE524_X_WIRELESS_TAKEOVER = 2830
        REPEATER_345_MHZ = 2081
        SECURE_KEY_345_MHZ = 1250
        SMKE1_SMOKE = 872
        SMKE1_SMOKE_CANADA = 871
        SMKT2_GE_SMOKE_HEAT = 895
        SMKT3_2_GIG = 1058
        SMKT6_2_GIG = 1066
        SWS1_SMART_WATER_SENSOR = 1264
        TAKE_TAKEOVER = 873
        TILT_SENSOR_2_GIG_345 = 2831
        VS_CO3_DETECTOR = 1266
        VS_SMKT_SMOKE_DETECTOR = 1267

        @classmethod
        def _missing_(cls, value):
            return cls.OTHER

    NON_VIVINT = [
        EquipmentCode.EXISTING_CO,
        EquipmentCode.EXISTING_DOOR_WINDOW_CONTACT,
        EquipmentCode.EXISTING_FLOOD_TEMP,
        EquipmentCode.EXISTING_GLASS_BREAK,
        EquipmentCode.EXISTING_HEAT,
        EquipmentCode.EXISTING_MOTION_DETECTOR,
        EquipmentCode.EXISTING_SMOKE,
        EquipmentCode.OTHER,
    ]

    class EquipmentType(Enum):
        CONTACT = 1
        EMERGENCY = 11
        FREEZE = 6
        MOTION = 2
        TEMPERATURE = 10
        WATER = 8
        UNKNOWN = 0

        @classmethod
        def _missing_(cls, value):
            return cls.UNKNOWN

    class SensorType(Enum):
        AUDIBLE_ALARM = 7
        AUXILIARY_ALARM = 8
        CARBON_MONOXIDE = 14
        DAY_ZONE = 5
        EXIT_ENTRY_1 = 1
        EXIT_ENTRY_2 = 2
        FIRE = 9
        FIRE_WITH_VERIFICATION = 16
        INTERIOR_FOLLOWER = 4
        INTERIOR_WITH_DELAY = 10
        NO_RESPONSE = 23
        PERIMETER = 3
        REPEATER = 25
        SILENT_ALARM = 6
        SILENT_BURGLARY = 24
        UNUSED = 0

        @classmethod
        def _missing_(cls, value):
            return cls.UNUSED

    """Generic state for all sensors they uses a simple boolean."""
    SENSOR_STATES = {True: "Opened", False: "Closed"}

    def __init__(self, device, root):
        super().__init__(device, root)

    @property
    def state(self):
        """Returns Opened or Closed based on the state of the sensor."""
        return self.SENSOR_STATES[self.get_device().get("s")]

    @property
    def equipment_code(self):
        """Return the equipment code of this sensor."""
        return self.EquipmentCode(self.get_device().get("ec"))

    @property
    def equipment_type(self):
        """Return the equipment type of this sensor."""
        return self.EquipmentType(self.get_device().get("eqt"))

    @property
    def sensor_type(self):
        """Return the sensor type of this sensor."""
        return self.SensorType(self.get_device().get("set"))

    @property
    def manufacturer(self):
        """Return the manufacturer for this device."""
        if self.equipment_code in self.NON_VIVINT:
            return "Other"
        return "Vivint"

    @property
    def model(self):
        """Return the model for this device."""
        return self.equipment_code.name

    def update_device(self, updates):
        super().update_device(updates)
        logger.debug(f"{self.name} is now {self.state}")
