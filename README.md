# LLM_GUI
 - NOTE: This is development branch. After verification merge to main branch

This repository represents a GUI to monitor and control a robot and patient details.

## GUI
<img src="Bilder/GUI.png" alt="Alt text" width="800"/>

<!-- ![Alt text](Bilder/GUI.png) -->
## Pre-requisites
- Make a .env file and add your OPEN_AI_KEY. Use below line to add in the .end file

    `OPENROUTER_API_KEY='<YOUR-KEY>'`

- Then run the `web_gui.py` script to get the server running and access to the web based GUI

- ffmpeg is installed for streaming webcam online: Use below link and select windows Built by BtbN

`ffmpeg-master-latest-win64-gpl-shared.zip`

Reference link: `https://github.com/BtbN/FFmpeg-Builds/releases`

After extracting Dont forget to add the `bin` fodler path to environmental variables.

- If not works with only ffmpeg then install mediamtx and after extracting mediamtx you will see an `.exe` file so run it to get a server running. Install `mediamtx_v1.15.0_windows_amd64.zip` using below installation link and extract.


Installation Link: `https://github.com/bluenviron/mediamtx/releases`
Reference link: `https://github.com/bluenviron/mediamtx`

## Commands to Run Webcam

To check the local IP
```bash
ipconfig
```

### Option 1 : Using only ffmpeg
```bash
ffmpeg -f dshow -i video="HD Web Camera" -preset ultrafast -tune zerolatency -c:v libx264 -f mpegts udp://192.168.0.109:12345
```

OR for lower resolution

```bash
ffmpeg -f dshow -video_size 640x320 -i video="HD Web Camera" -preset ultrafast -tune zerolatency -c:v libx264 -f mpegts udp://127.0.0.1:12345
```
OR

```bash
ffmpeg -f dshow -i video="HD Web Camera" -preset ultrafast -tune zerolatency -c:v libx264 -f hls -hls_time 2 -hls_list_size 3 -hls_flags delete_segments ./stream/stream.m3u8
```

To Test in windows use VLC player and go to

`Media>Open Network Stream><Add URL>`

e.g. <Add URL> replaced by `udp://@192.168.0.109:12345`

### Option 2 : Using ffmpeg and mediamtx (Recommended for less loss of packets)

1. First run the `mediamtx.exe` executable, it will open the terminal
2. Then in another terminal run: we can also use `ultrafast` flag in place of `veryfast`
    ```bash
    ffmpeg -f dshow -i video="HD Web Camera" -c:v libx264 -preset veryfast -maxrate 3000k -bufsize 6000k -f rtsp rtsp://localhost:8554/webcam.sdp
    ```
3. In order to view the stream run:
    ```bash
    ffplay rtsp://localhost:8554/webcam.sdp
    ```

### Option 3 : Using flask server

1. `python -m pip install flask`



## Extra Utilties ffmpeg
To list all the devices such as video (camera) and audio (microphone) use below command:

```bash
ffmpeg -list_devices true -f dshow -i dummy`
```

To check format supported by each device

```bash
ffmpeg -list_options true -f dshow -i video="HD Web Camera"  
```

## References

1. https://coderslegacy.com/ffmpeg-rtsp-streaming/
2. https://www.youtube.com/watch?v=rCZg2cVP4cs
3. https://www.youtube.com/watch?v=fO8KVWl6I6g