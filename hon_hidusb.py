# File header for Doxygen document generator:
## @file hon_hidusb.py
## @brief Honeywell HIDUSB interface

"""Honeywell HIDUSB interface"""

# 3rd party imports
import hid  # type: ignore[import-untyped]


# ----------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------
def send_command(device: hid.device, cmd: list[int] | str) -> None:
    """

    :param device: The USBHID device to send the command to (it has to be open)
    :param cmd: The command to send. It has to be a list of integers, or a string like "REVINF."
    :return: Nothing
    """

    # If this is a list of integers, send it right away.
    if isinstance(cmd, list):
        device.write(cmd)
        return

    # Special, custom commands
    if isinstance(cmd, str):
        match cmd.upper():
            case "BEEP":
                device.write([0xFD, 0x03, 0x16, 0x07, 0x0D])
                return
            case "TRIGGER_ON":
                device.write([0xFD, 0x03, 0x16, 0x54, 0x0D])
                return
            case "TRIGGER_OFF":
                device.write([0xFD, 0x03, 0x16, 0x55, 0x0D])
                return
            case _:
                pass

    # If the command is a string, perform some checks and modifications
    if isinstance(cmd, str):
        # A text command has to end with a dot
        if not cmd.endswith("."):
            cmd = cmd + "."
        # If there is not appropiate header, add it here.
        # Then convert the string to a list of integers, as that is what is required for device.write()
        if not cmd.startswith("\xfd"):
            # Add the preamble and convert the bytesarray to a list of integers
            cmd = list(b"\xfd\x0f\x16\x4d\x0d" + bytearray(cmd, encoding="utf-8"))
            # print(f"New cmd: {cmd=}")

        # Now send the command to the scanner
        device.write(cmd)
        return

    print("Invalid command {cmd}")
    return


# ----------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------
def read_response(device: hid.device, timeout=500) -> str:
    """Read the full response from the connected USBHID scanner

    :param device: The device to read the response from
    :param timeout: Maximum duration to wait for a response. Default is 500ms
    :return: A string with the response
    """

    full_response = ""

    while True:

        # Read the (partial) response
        data_received = device.read(64, timeout_ms=timeout)

        # If no more data was received, return the response assembled up to now.
        if not data_received:
            return full_response
        # print("Data received:", data_received)
        # print("Packet length:", len(data_received))

        payload_length = data_received[1]
        # print(f"{payload_length=}")

        # Extract the AIM identifere
        aim_id = data_received[2:5]
        # print(f"{aim_id=}")
        _aim_id_str = "".join([chr(number) for number in aim_id])

        # Extract the payload
        payload = data_received[5:-3]
        # print(f"{payload=}")
        payload_str = "".join([chr(number) for number in payload[0:payload_length]])

        # For debugging purposes, show the AIM ID and the payload of the partial response
        # print(f"{aim_id_str=} {payload_str=}")

        # Add the (partial) response to the full response string to be returned.
        if '\x06.' in payload_str:
            continue

        if '\x05.' in payload_str:
            print("Error in the command")
            continue

        full_response += payload_str

    return full_response


# ----------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    pass
