# projectPontiac
## Car Computer Repository

This project is a work in progress for a fully functioning car computer utilizing a Raspberry Pi and the Official Raspberry Pi touchscreen.

**Planned features include OBD2 Communication utilizing pyOBD, A2DP Bluetooth playback utilizing bluetooth, music controls, the ability to set a background, and FM Radio playback**

###### Features currently working:
- Bluetooth audio via an alsa a2dp sink
- Traffic information (with manual updating in a menu)
  - Web scraping is done with Bash (which is planned to be replaced with [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
  - The program checks for online connectivity upon startup to download and scrape web informaton before the user drives off.
- UI is created using [Kivy](https://kivy.org/#home)
- Volume Knob is handled by [savetheclocktower's Python daemon](https://gist.github.com/savetheclocktower/9b5f67c20f6c04e65ed88f2e594d43c1)
