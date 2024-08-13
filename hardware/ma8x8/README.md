# MA8X8: Measurement Array 8x8 interface

This interface consist of 64 front contacts and a single back contact on an area of 25&nbsp;mm x 25&nbsp;mm. It is 
controlled by an Arduino Nano Every board which is connected through a serial COM port. The implementation of this 
interface is documented here: [``cohesivm.interfaces.MA8X8``](https://cohesivm.readthedocs.io/en/latest/reference/interfaces.html#cohesivm.interfaces.MA8X8).

![MA8X8 Contact Mask, Interface, and Multiplexer](ma8x8.png)


## Contact Mask

As depicted on the image to the left, the contact mask can be used to manufacture masks for sputtering or evaporation 
of contacts onto 25&nbsp;mm x 25&nbsp;mm substrates. The pads on the corners and edges are used for the single back 
contact, while the circular pads will be switched through by the multiplexer.


## Interface

The contact interface, as depicted on the image to the middle, is made up of 64 + 8 pogo pins which are soldered to a 
custom-made PCB. On the bottom of the board are the pin headers for the connection to the multiplexer.


## Multiplexer

The actual switching between the contacts is carried out by the multiplexer board (on the image to the right). This PCB 
is powered by an Arduino Nano, houses 64 relays and 4 I/O extender.


## Files

- [ma8x8_contact_mask.brd](./ma8x8_contact_mask.brd)
- [ma8x8_interface.brd](./ma8x8_interface.brd)
- [ma8x8_interface.sch](./ma8x8_interface.sch)
- [ma8x8_multiplexer.brd](./ma8x8_multiplexer.brd)
- [ma8x8_multiplexer.sch](./ma8x8_multiplexer.sch)
- [ma8x8_multiplexer.ino](./ma8x8_multiplexer.ino)

The *.brd and *.sch files are the board and schematics CAD files, respectively. To render the boards in 3D there exist 
a couple of free online services, e.g., [here](https://www.application-art.de/) and [here](https://www.altium.com/viewer).
The *.ino file is the firmware for the Arduino Nano which works with the implemented MA8X8 interface.
