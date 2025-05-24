import hid

# Replace with your device's vendor ID and product ID
VENDOR_ID = 0x0c2e
PRODUCT_ID = 0x0db3


def send_command(device: hid.device, cmd: list[int], description="") -> None:

    print(f"Data to send for {description}: {cmd}")
    if isinstance(cmd, list):
        device.write(cmd)
        return

    if isinstance(cmd, str) and cmd.endswith('.'):
        if not cmd.startswith('\xFD'):
            cmd = b'\xFD\x0F\x16\x4d\x0d' + bytearray(cmd, encoding="utf-8")
            print(f"New cmd: {cmd=}")
            cmd = list(cmd)     # Conver bytearray to a list of integers
        print(f"New cmd: {cmd=}")
        device.write(cmd)
        return

    else:
        print(f"Invalid command '{cmd}'")
        return


def read_response(device: hid.device, timeout=1000) -> str:
    full_response = ""
    while True:
        data_received = device.read(64, timeout_ms=timeout)
        if not data_received:
            return full_response
        print("Data received:", data_received)
        print("Packet length:", len(data_received))
        payload_length = data_received[1]
        # print(f"{payload_length=}")
        aim_id = data_received[2:5]
        # print(f"{aim_id=}")
        aim_id_str = "".join([chr(number) for number in aim_id])
        payload = data_received[5:-3]
        print(f"{payload=}")
        payload_str = "".join([chr(number) for number in payload[0:payload_length]])
        print(f"{aim_id_str=} {payload_str=}")
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


    # Example of REVINF. response:
    #
    # Data
    # received: [2, 56, 93, 88, 48, 80, 114, 111, 100, 117, 99, 116, 32, 78, 97, 109, 101, 58, 32, 86, 111, 121, 97, 103,
    #            101, 114, 32, 49, 54, 48, 50, 103, 13, 10, 66, 111, 111, 116, 32, 82, 101, 118, 105, 115, 105, 111, 110,
    #            58, 32, 58, 32, 56, 57, 57, 50, 13, 10, 83, 111, 102, 116, 63, 0, 1]
    # Data
    # received: [2, 56, 93, 88, 48, 119, 97, 114, 101, 32, 80, 97, 114, 116, 32, 78, 117, 109, 98, 101, 114, 58, 32, 67,
    #            87, 48, 48, 48, 48, 56, 50, 66, 66, 65, 13, 10, 83, 111, 102, 116, 119, 97, 114, 101, 32, 82, 101, 118,
    #            105, 115, 105, 111, 110, 58, 32, 36, 80, 114, 111, 106, 101, 63, 0, 1]
    # Data
    # received: [2, 56, 93, 88, 48, 99, 116, 82, 101, 118, 105, 115, 105, 111, 110, 58, 32, 49, 54, 51, 52, 53, 32, 13,
    #            10, 83, 101, 114, 105, 97, 108, 32, 78, 117, 109, 98, 101, 114, 58, 32, 49, 53, 50, 51, 50, 66, 49, 70,
    #            48, 67, 13, 10, 83, 117, 112, 112, 111, 114, 116, 101, 100, 63, 0, 1]
    # Data
    # received: [2, 56, 93, 88, 48, 32, 73, 70, 58, 32, 66, 108, 117, 101, 116, 111, 111, 116, 104, 13, 10, 80, 67, 66,
    #            32, 65, 115, 115, 101, 109, 98, 108, 121, 32, 73, 68, 58, 32, 48, 48, 48, 48, 48, 48, 13, 10, 69, 110,
    #            103, 105, 110, 101, 32, 70, 105, 114, 109, 119, 97, 114, 101, 63, 0, 1]
    # Data
    # received: [2, 56, 93, 88, 48, 32, 84, 121, 112, 101, 58, 32, 78, 47, 65, 32, 32, 32, 82, 101, 118, 105, 115, 105,
    #            111, 110, 58, 32, 78, 47, 65, 32, 32, 32, 83, 101, 114, 105, 97, 108, 32, 78, 117, 109, 98, 101, 114, 58,
    #            32, 78, 47, 65, 32, 32, 32, 67, 104, 101, 99, 107, 115, 63, 0, 1]
    # Data
    # received: [2, 9, 93, 88, 48, 117, 109, 58, 32, 78, 47, 65, 13, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    #            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 63, 0, 0]
    # Data
    # received: [2, 8, 93, 90, 54, 82, 69, 86, 73, 78, 70, 6, 46, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    #            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 54, 0, 0]

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

    # Close the device
    device.close()
    print("Device closed.")


if __name__ == "__main__":
    main()
