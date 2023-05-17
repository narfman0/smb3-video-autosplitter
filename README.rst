smb3-video-autosplitter
==============

.. image:: https://badge.fury.io/py/smb3-video-autosplitter.png
    :target: https://badge.fury.io/py/smb3-video-autosplitter

.. image:: https://ci.appveyor.com/api/projects/status/github/narfman0/smb3-video-autosplitter?branch=main
    :target: https://ci.appveyor.com/project/narfman0/smb3-video-autosplitter

Ingest video data from a capture card to autosplit in livesplit

Installation
------------

Navigate to the most recent versioned release here:

https://github.com/narfman0/smb3-video-autosplitter/releases

Download the zip and extract to your favorite directory.

We need to update the trigger frame and region.
First, open `config.yml` and set `show_capture_video: true`,
then run the tool. Take a screen cap of princess peach's letter or similar, then
crop her face and take note of coordinates and width/height. Replace trigger1.png
in the `data/` directory, and set the region (x,y,width,height)
of the cropped image relative to the original image.
Note: you should read it like "whenever you see the trigger (peachs face) at that position
in the screen cap, split"

License
-------

Copyright (c) 2023 narfman0

See LICENSE for details
