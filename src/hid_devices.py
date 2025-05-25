# File header for Doxygen document generator:
## @file hid_devices.py
## @brief Show and/or select HID devices

"""Show and/or select HID devices"""

import hid  # type: ignore[import-untyped]


# ----------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------
def show_devices() -> None:
    """Show the connected USB devices
    :return: Nothing
    """

    devices = hid.enumerate()
    for device in devices:
        # print(f"{device=}")
        keys = list(device.keys())
        keys.sort()
        for key in keys:
            # print("%s : %s" % (key, device[key]))
            print(f"{key} : {device[key]}")
        print()


# ----------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------
def select_device(mask="") -> tuple[int, int] | tuple[None, None]:
    """From all devices, select one to use

    :param mask: Filter on a string mask in the manufacturing string or on the product_string
    :return: Tuple of (vendor_id, device_id) or (None, None) in case nothing was found
    """

    device_list = []
    devices = hid.enumerate()
    for device in devices:
        # print(f"{device=}")
        if mask and mask.upper() in device["manufacturer_string"].upper():
            # print(f"Found {mask} in {device["manufacturer_string"]}")
            device_list.append(device)
        elif mask and mask.upper() in device["product_string"].upper():
            # print(f"Found {mask} in {device["product_string"]}")
            device_list.append(device)

    # Nothing was found, or matched the mask
    if not device_list:
        return None, None

    # If there is only one match, return it
    if len(device_list) == 1:
        return device_list[0]["vendor_id"], device_list[0]["product_id"]

    # If there are multiple matches, print the info and let the user make a slection
    while True:
        # Show the list
        print()
        for i, device in enumerate(device_list):
            print(f"{i} = {device["product_string"]:16} : {device["manufacturer_string"]:40} ({device["vendor_id"]:#x}:{device["product_id"]:#x})")
        # Show the prompt to make a selection
        print()
        index = int(input(f"Select device 0...{len(device_list)-1}:"))
        # If the selection was valid, return the vendor_id and product_id of the selected device.
        # In case of an invalid selection, enter this loop again
        if 0 <= index < len(device_list):
            print(f"Selected {device_list[index]["product_string"]:16} : {device_list[index]["manufacturer_string"]:40}")
            return device_list[index]["vendor_id"], device_list[index]["product_id"]
        # else
        continue

    # We should never reach this part, but if we do, return as if no device was found.
    return None, None


# ----------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------
if __name__ == '__main__':
    vendor_id, product_id = select_device(mask="1602g")
    print(f"{vendor_id=} {product_id=}")
