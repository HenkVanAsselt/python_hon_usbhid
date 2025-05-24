# File header for Doxygen document generator:
## @file main.py
## @brief main module for Python Honeywell USBHID interface

"""main module for Python Honeywell USBHID interface"""

# Global imports
import argparse

# 3rd party imports
import hid  # type: ignore[import-untyped]

# Local imports
import hid_devices
from hon_hidusb import send_command, read_response


# Replace with your device's vendor ID and product ID
# For the Honeywell 1602g Pockatable scanner:
VENDOR_ID = 0x0C2E
PRODUCT_ID = 0x0DB3

# Some contants
ENQ = "\x05"
ACK = "\x06"
NAK = "\x015"
SYN = "\x16"


# ----------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------
def main(args: dict) -> None:
    """Main functions

    :param args: Dictionary with commandline arguments
    :return: Nothing
    """

    if args.list:
        hid_devices.show_devices()
        return

    if args.mask:
        args.vendor_id, args.product_id = hid_devices.select_device(args.mask)

    if args.command:

        try:
            device = hid.device()
            device.open(args.vendor_id, args.product_id)
            # print("Device opened successfully.")
        except OSError as e:
            print(f"Failed to open device: {e}  {VENDOR_ID=} {PRODUCT_ID=}")
            return

        send_command(device, args.command)
        response = read_response(device)
        print(f"{response}")

        # Close the device
        device.close()

    if not args.command:

        # Open the device
        try:
            device = hid.device()
            device.open(args.vendor_id, args.product_id)
            # print("Device opened successfully.")
        except TypeError as e:
            print(f"Invalid vendor_id {args.vendor_id} and/or product_id {args.product_id}")
            return
        except OSError as e:
            print(f"Failed to open device: {e}  {args.vendor_id=} {args.product_id=}")
            return

        # Just test some stuff

        send_command(device, "BEEP")

        send_command(device, "REVINF.")
        response = read_response(device)
        print(f"{response}")

        send_command(device, "P_INFO.")
        response = read_response(device)
        print(f"{response}")

        send_command(device, "CBR?.")
        response = read_response(device)
        print(f"{response}")

        # Scanner on
        # data_to_send = [0xFD, 0x03, 0x16, 0x54, 0x0D]
        send_command(device, "TRIGGER_ON")

        # Read a barcode
        print("\nReading a barcode:")
        response = read_response(device, timeout=500)
        print(f"{response=}")

        # Scanner off
        # data_to_send = [0xFD, 0x03, 0x16, 0x55, 0x0D]
        send_command(device, "Trigger_off")

        # # Get all Codabar selections
        # cmd = "CBR?."
        # send_command(device, cmd, description="Get Codabar selections")
        # response = read_response(device, timeout=2000)
        # print(f"{response=}")

        # Close the device
        device.close()
        # print("Device closed.")


# ----------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------
def parse_arguments():
    """ Parse commandline arguments

    :return: dict with arguments
    """

    parser = argparse.ArgumentParser(description="HON Scanner control", formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("-l", "--list", action='store_true', help="List available USB devices")
    parser.add_argument("-c", "--command", type=str, help="Command(s) to send to the scanner")

    parser.add_argument("-v", "--vendor_id", type=int, help="USB Vendor ID (default: %(default)s)") #, default=0x0C2E)
    parser.add_argument("-p", "--product_id", type=int, help="USB Product ID") #, default=0x0DB3)
    parser.add_argument("-m", "--mask", type=str, help="Mask to filter on Vendor or Product", default="")

    args = parser.parse_args()
    return args


# ----------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------
if __name__ == "__main__":

    cmd_line_arguments = parse_arguments()
    # print(f"commandline arguments: {cmd_line_arguments}")

    main(cmd_line_arguments)
