# Controlling a Honeywell barcode scanner over the USBHID interface

## The challenge

The commands which a scanner can handle are well documented in their manuals.

Using these commands when a serial (RS232) interface is used, is quite simple.
What I was struggling with is how to use this when an USBHID interace is used.

Take a simple example to trigger the scanner so it will try to read a barcode.

In the knowledgebase it is stated that 3 bytes should be use:  `[SYN]T[CR]`. 
Or to make the scanner beep, use `[SYN][BEL][CR]`

However, sending this these 3 bytes over an USBHID interface did not lead to any result.
The communication protocol is nowhere described.

After much digging and experiments, I figured out that the following protocol is used over the USBHID interface

Use the preamble `'\xFD\x03'` followed by the command as shown in the manuals.

## Beep
Send the bytes `b'\xFD\x03\x16\x07\x0d'`
There is no response from the scanner

## Trigger scanner on
Send the bytes `b'\xFD\x03\x16\x54\x0d'`
There is no response from the scanner

## Trigger scanner off
Send the bytes `b'\xFD\x03\x16\x54\x0d'`
There is no response from the scanner

## Menu commands / Configuration commands

Here it becomes a litte more complicate, as there will be a response

For example the command REVINF. will make the scanner return software revision information in multiple packages.

Send [0xFD, 0x0F, 0x16, 0x4D, 0x0D, 0x52, 0x45, 0x56, 0x49, 0x4e, 0x46, 0x2e] 
Wherein:
* Byte 0 has the fixed value `0xFD`
* Byte 1 could be the length of the command, but the purpose is not clear.
* Byte 2 has the fixed value `[SYN]` (0x16)
* Byte 3 is an `M` (0x4d), indicating a Menu command / Configuration command
* Byte 4 has the fixed value `[CR]` (0x0d)
* Byte 5... is the command, in this case `REVINF.`

The REVINF. response is a multipacket message, and looks like this:

    Data received: [2, 56, 93, 88, 48, 80, 114, 111, 100, 117, 99, 116, 32, 78, 97, 109, 101, 58, 32, 86, 111, 121, 97, 103, 101, 114, 32, 49, 54, 48, 50, 103, 13, 10, 66, 111, 111, 116, 32, 82, 101, 118, 105, 115, 105, 111, 110, 58, 32, 58, 32, 56, 57, 57, 50, 13, 10, 83, 111, 102, 116, 63, 0, 1]
    Data received: [2, 56, 93, 88, 48, 119, 97, 114, 101, 32, 80, 97, 114, 116, 32, 78, 117, 109, 98, 101, 114, 58, 32, 67, 87, 48, 48, 48, 48, 56, 50, 66, 66, 65, 13, 10, 83, 111, 102, 116, 119, 97, 114, 101, 32, 82, 101, 118, 105, 115, 105, 111, 110, 58, 32, 36, 80, 114, 111, 106, 101, 63, 0, 1]
    Data received: [2, 56, 93, 88, 48, 99, 116, 82, 101, 118, 105, 115, 105, 111, 110, 58, 32, 49, 54, 51, 52, 53, 32, 13, 10, 83, 101, 114, 105, 97, 108, 32, 78, 117, 109, 98, 101, 114, 58, 32, 49, 53, 50, 51, 50, 66, 49, 70, 48, 67, 13, 10, 83, 117, 112, 112, 111, 114, 116, 101, 100, 63, 0, 1]
    Data received: [2, 56, 93, 88, 48, 32, 73, 70, 58, 32, 66, 108, 117, 101, 116, 111, 111, 116, 104, 13, 10, 80, 67, 66, 32, 65, 115, 115, 101, 109, 98, 108, 121, 32, 73, 68, 58, 32, 48, 48, 48, 48, 48, 48, 13, 10, 69, 110, 103, 105, 110, 101, 32, 70, 105, 114, 109, 119, 97, 114, 101, 63, 0, 1]
    Data received: [2, 56, 93, 88, 48, 32, 84, 121, 112, 101, 58, 32, 78, 47, 65, 32, 32, 32, 82, 101, 118, 105, 115, 105, 111, 110, 58, 32, 78, 47, 65, 32, 32, 32, 83, 101, 114, 105, 97, 108, 32, 78, 117, 109, 98, 101, 114, 58, 32, 78, 47, 65, 32, 32, 32, 67, 104, 101, 99, 107, 115, 63, 0, 1]
    Data received: [2, 9, 93, 88, 48, 117, 109, 58, 32, 78, 47, 65, 13, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 63, 0, 0]
    Data received: [2, 8, 93, 90, 54, 82, 69, 86, 73, 78, 70, 6, 46, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 54, 0, 0]

* Byte 0 is fixed, is has value `\x02`, also known as [STX] or 'Start of Transmission'
* Byte 1 is the length of the data in this package
* Byte 2..4 are 3 characters, representing the AIM identifier of the barcode scanned. If this is a repsonse on a command, 
then the values are `[93d, 88d, 48d]` which is the string `]X0` which represents Code39.
* Contents, filled with zero's.
* Trailer: [63, 0, 1]

In the first REVINF. responses, the AIM id `]X0`, but the last part becomes different:
* the AIM id becomes ']Z6', 
* the command is repeated following by a one byte status code, 
which can be ACK `0x06`, NAK `0x15` or ENQ `0x05` and then terminated with a `.` (period).

The above is described in the manuals as follows:

* ACK Indicates a good command which has been processed.
* ENQ Indicates an invalid Tag or SubTag command.
* NAK Indicates the command was good, but the Data field entry was out of the allowable range for this Tag and SubTag combination, e.g., an entry for a minimum message length of 100 when the field will only accept 2 charac- ters.
* When responding, the device echoes back the command sequence with the status character inserted directly before each of the punctuation marks (the period, exclamation point, comma, or semicolon) in the command.

Example: What are the device’s settings for all Codabar selections?

Command: `CBR?.`

Response: `CBRENA1[ACK],SSX0[ACK],CK20[ACK],CCT1[ACK],MIN2[ACK],MAX60[ACK],DFT[ACK].`

This response indicates that 
* the device’s Codabar Coding Enable (CBRENA) is set to 1, or on;
* the Start/Stop Character (SSX) is set to 0, or Don’t Transmit; the Check Character (CK2) is set to 0, or Not Required; concatenation (CCT) is set to 1, or Enabled;
* the Minimum Message Length (MIN) is set to 2 characters; the Maximum Message Length (MAX) is set to 60 characters; and the Default setting (DFT) has no value.

# References
* https://s3lph.me/configuration-of-honeywell-barcode-scanners.html
* Honeywell serial command tutorial: https://honeywellsps.my.salesforce.com/sfc/p/#00000000SK3U/a/A00000004dOY/IV3Nc9ULigAPhFaIvILtJcBqnQRk.ArskZ6z917AugE
