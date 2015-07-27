DUObot Project Repository
=========================

This repo contains the files related to the two-wheeled balancing robot -
DUObot.


The firmware directory holds the Arduino source files required to run the software. The Arduino IDE is used
to program the DUObot. Library dependencies are listed below:
- [USB Host Shield Library](https://github.com/felis/USB_Host_Shield_2.0)


The hardware directory contains the 3D files to make the DUObot. Some parts
are laser cut acrylic, others are 3D printed.


The PCB's are included in the pcb directory. Two boards are designed:
- Main controller board with an ATmega2560 and related control circuitry,
- IMU board with an MPU-9150.


The datasheets for the components used are held within the datasheets directory.


#### TODO:
1. [ ] decide on electronic components
1. [ ] design the main controller board
2. [x] design the imu breakout
2. [ ] update imu to MPU-9250 for future revisions
2. [ ] order the pcbs
2. [ ] update readme: library dependencies,
3. [ ] make a parts list and order
4. [ ] work on the code required
5. [ ] design the chassis
6. [ ] 3D print and laser cut the chassis
