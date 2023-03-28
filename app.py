from multiprocessing import freeze_support
from smb3_video_autosplitter.main import main

# this is intended for pyinstaller only!
if __name__ == "__main__":
    freeze_support()
    main()
