import hid

# Replace with your device's vendor ID and product ID
VENDOR_ID = 0x0c2e
PRODUCT_ID = 0x0db3


def send_command(device: hid.device, cmd: list[int] | str, description="") -> None:
    """

    :param device: The USBHID device to send the command to (it has to be open)
    :param cmd: The command to send. It has to be a list of integers, or a string like "REVINF."
    :param description: A string which describes the command. For information only
    :return: Nothing




    """

    print(f"Data to send for {description}: {cmd}")

    # If this is a list of integers, send it right away.
    if isinstance(cmd, list):
        device.write(cmd)
        return

    # If the command is a string, perform some checks and modifications
    if isinstance(cmd, str):
        # A text command has to end with a dot
        if not cmd.endswith('.'):
            cmd = cmd + '.'
        # If there is not appropiate header, add it here.
        # Then convert the string to a list of integers, as that is what is required for device.write()
        if not cmd.startswith('\xFD'):
            cmd = b'\xFD\x0F\x16\x4d\x0d' + bytearray(cmd, encoding="utf-8")
            print(f"New cmd: {cmd=}")
            cmd = list(cmd)     # Conver bytearray to a list of integers
        print(f"New cmd: {cmd=}")

        # Now send the command to the scanner
        device.write(cmd)
        return

    else:
        print(f"Invalid command '{cmd}'")
        return


def read_response(device: hid.device, timeout=500) -> str:
    """ Read the full response from the connected USBHID scanner

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
        aim_id_str = "".join([chr(number) for number in aim_id])

        # Extract the payload
        payload = data_received[5:-3]
        print(f"{payload=}")
        payload_str = "".join([chr(number) for number in payload[0:payload_length]])

        # For debugging purposes, show the AIM ID and the payload of the partial response
        print(f"{aim_id_str=} {payload_str=}")

        # Add the (partial) response to the full response string to be returned.
        full_response += payload_str


def main():

    # Open the device
    try:
        device = hid.device()
        device.open(VENDOR_ID, PRODUCT_ID)
        print("Device opened successfully.")
    except Exception as e:
        print(f"Failed to open device: {e}")
        return

    # Beep
    data_to_send = [0xFD, 0x03, 0x16, 0x07, 0x0D]
    send_command(device, data_to_send, "Beep")

    # REVINF.
    # [FD][07][52][45][56][49][4E][46][2E]
    #                    length?  SYN   M     CR    R     E     V     I     N     F     .
    data_to_send = [0xFD, 0x0F, 0x16, 0x4D, 0x0D, 0x52, 0x45, 0x56, 0x49, 0x4e, 0x46, 0x2e]
    send_command(device, "REVINF.", "REVINF.")
    response = read_response(device)
    print(f"{response}")

    send_command(device, "P_INFO.")
    response = read_response(device)
    print(f"{response}")

    send_command(device, "CBR?.")
    response = read_response(device)
    print(f"{response}")

    # Scanner on
    data_to_send = [0xFD, 0x03, 0x16, 0x54, 0x0D]
    send_command(device, data_to_send, description="Scanner on")

    # Read a barcode
    print("\nReading a barcode:")
    response = read_response(device, timeout=2000)
    print(f"{response=}")

    # Scanner off
    data_to_send = [0xFD, 0x03, 0x16, 0x55, 0x0d]
    send_command(device, data_to_send, description="Scanner off")

    # Get all Codabar selections
    cmd = "CBR?."
    send_command(device, cmd, description="Get Codabar selections")
    response = read_response(device, timeout=2000)
    print(f"{response=}")

    # Close the device
    device.close()
    print("Device closed.")


if __name__ == "__main__":
    main()
