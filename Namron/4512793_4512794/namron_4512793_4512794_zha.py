"""Custom ZHA quirk for Namron 4512793 / 4512794 wall switch."""

from zigpy.quirks import CustomDevice
from zigpy.zcl import foundation

from zhaquirks import EventableCluster
from zhaquirks.const import (
    COMMAND,
    DEVICE_TYPE,
    ENDPOINTS,
    INPUT_CLUSTERS,
    MODELS_INFO,
    OUTPUT_CLUSTERS,
    PROFILE_ID,
    ZHA_SEND_EVENT,
)

NAMRON_CLUSTER_ID = 0xE004


class NamronRemoteCluster(EventableCluster):
    cluster_id = NAMRON_CLUSTER_ID
    name = "NamronRemoteCluster"
    ep_attribute = "namron_remote_cluster"

    CHANNEL_MAP = {
        "01": "button_1_on",
        "02": "button_1_off",
        "03": "button_2_on",
        "04": "button_2_off",
        "05": "button_3_on",
        "06": "button_3_off",
    }

    ACTION_MAP = {
        "01": "short_press",
        "02": "long_hold",
        "04": "long_release",
    }

    def handle_cluster_request(
        self,
        hdr: foundation.ZCLHeader,
        args,
        *,
        dst_addressing=None,
    ):
        try:
            payload = bytes(args)
        except Exception:
            payload = bytes()

        hex_payload = payload.hex()

        if len(hex_payload) == 4:
            channel_code = hex_payload[:2]
            action_code = hex_payload[2:]

            channel = self.CHANNEL_MAP.get(channel_code, f"unknown_channel_{channel_code}")
            action = self.ACTION_MAP.get(action_code, f"unknown_action_{action_code}")
            event_name = f"{channel}_{action}"
        else:
            event_name = f"unknown_{hex_payload}"

        event_args = {
            COMMAND: event_name,
            "payload": hex_payload,
            "cluster_id": self.cluster_id,
            "command_id": hdr.command_id,
            "endpoint_id": self.endpoint.endpoint_id,
        }

        self.debug(
            "NAMRON EVENT: %s (payload=%s)",
            event_name,
            hex_payload,
        )

        self.listener_event(ZHA_SEND_EVENT, event_name, event_args)


class Namron4512793SingleChannel(CustomDevice):
    signature = {
        MODELS_INFO: [
            ("Namron AS", "4512793"),
            ("Namron AS", "4512794"),
        ],
        ENDPOINTS: {
            1: {
                PROFILE_ID: 0x0104,
                DEVICE_TYPE: 0x0104,
                INPUT_CLUSTERS: [0x0000, 0x0001, 0x0003, 0x0020, 0xE004],
                OUTPUT_CLUSTERS: [0x0003, 0x0004, 0x0005, 0x0006, 0x0008, 0x0019, 0x1000],
            }
        },
    }

    replacement = {
        ENDPOINTS: {
            1: {
                PROFILE_ID: 0x0104,
                DEVICE_TYPE: 0x0104,
                INPUT_CLUSTERS: [0x0000, 0x0001, 0x0003, 0x0020, NamronRemoteCluster],
                OUTPUT_CLUSTERS: [0x0003, 0x0004, 0x0005, 0x0006, 0x0008, 0x0019, 0x1000],
            }
        },
    }


class Namron4512793TwoChannel(CustomDevice):
    signature = {
        MODELS_INFO: [
            ("Namron AS", "4512793"),
            ("Namron AS", "4512794"),
        ],
        ENDPOINTS: {
            1: {
                PROFILE_ID: 0x0104,
                DEVICE_TYPE: 0x0104,
                INPUT_CLUSTERS: [0x0000, 0x0001, 0x0003, 0x0020, 0xE004],
                OUTPUT_CLUSTERS: [0x0003, 0x0004, 0x0005, 0x0006, 0x0008, 0x0019, 0x1000],
            },
            2: {
                PROFILE_ID: 0x0104,
                DEVICE_TYPE: 0x0104,
                INPUT_CLUSTERS: [0x0000, 0x0003],
                OUTPUT_CLUSTERS: [0x0003, 0x0006, 0x0008],
            },
        },
    }

    replacement = {
        ENDPOINTS: {
            1: {
                PROFILE_ID: 0x0104,
                DEVICE_TYPE: 0x0104,
                INPUT_CLUSTERS: [0x0000, 0x0001, 0x0003, 0x0020, NamronRemoteCluster],
                OUTPUT_CLUSTERS: [0x0003, 0x0004, 0x0005, 0x0006, 0x0008, 0x0019, 0x1000],
            },
            2: {
                PROFILE_ID: 0x0104,
                DEVICE_TYPE: 0x0104,
                INPUT_CLUSTERS: [0x0000, 0x0003],
                OUTPUT_CLUSTERS: [0x0003, 0x0006, 0x0008],
            },
        },
    }


class Namron4512793ThreeChannel(CustomDevice):
    signature = {
        MODELS_INFO: [
            ("Namron AS", "4512793"),
            ("Namron AS", "4512794"),
        ],
        ENDPOINTS: {
            1: {
                PROFILE_ID: 0x0104,
                DEVICE_TYPE: 0x0104,
                INPUT_CLUSTERS: [0x0000, 0x0001, 0x0003, 0x0020, 0xE004],
                OUTPUT_CLUSTERS: [0x0003, 0x0004, 0x0005, 0x0006, 0x0008, 0x0019, 0x1000],
            },
            2: {
                PROFILE_ID: 0x0104,
                DEVICE_TYPE: 0x0104,
                INPUT_CLUSTERS: [0x0000, 0x0003],
                OUTPUT_CLUSTERS: [0x0003, 0x0006, 0x0008],
            },
            3: {
                PROFILE_ID: 0x0104,
                DEVICE_TYPE: 0x0104,
                INPUT_CLUSTERS: [0x0000, 0x0003],
                OUTPUT_CLUSTERS: [0x0003, 0x0006, 0x0008],
            },
        },
    }

    replacement = {
        ENDPOINTS: {
            1: {
                PROFILE_ID: 0x0104,
                DEVICE_TYPE: 0x0104,
                INPUT_CLUSTERS: [0x0000, 0x0001, 0x0003, 0x0020, NamronRemoteCluster],
                OUTPUT_CLUSTERS: [0x0003, 0x0004, 0x0005, 0x0006, 0x0008, 0x0019, 0x1000],
            },
            2: {
                PROFILE_ID: 0x0104,
                DEVICE_TYPE: 0x0104,
                INPUT_CLUSTERS: [0x0000, 0x0003],
                OUTPUT_CLUSTERS: [0x0003, 0x0006, 0x0008],
            },
            3: {
                PROFILE_ID: 0x0104,
                DEVICE_TYPE: 0x0104,
                INPUT_CLUSTERS: [0x0000, 0x0003],
                OUTPUT_CLUSTERS: [0x0003, 0x0006, 0x0008],
            },
        },
    }