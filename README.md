# Bluetooth Audio Setup on Raspberry Pi 5

## Overview

This repository documents the complete setup and troubleshooting process for enabling **stable Bluetooth audio output** on a **Raspberry Pi 5 running Raspberry Pi OS**.

During initial testing, the Bluetooth speaker paired successfully but produced **no audio output or unstable playback**. The issue was not related to hardware or the speaker itself. It was caused by **Bluetooth profile instability, aggressive power-saving mechanisms and conflicts between BlueZ, PipeWire and PulseAudio compatibility layers**.

This README explains:
- The **issues faced**
- The **root causes**
- The **configuration changes applied**
- A **step-by-step reproducible solution**
- Final **verification using Python audio playback**



## System Details

- **Device:** Raspberry Pi 5  
- **Operating System:** Raspberry Pi OS 
- **Bluetooth Stack:** BlueZ  
- **Audio Stack:** PipeWire + PipeWire-Pulse  
- **Speaker Type:** Bluetooth A2DP Speaker  


## Libraries & Dependencies

Install the required packages before configuration:

```bash
sudo apt update
sudo apt install -y \
  bluetooth \
  bluez \
  bluez-tools \
  pipewire \
  pipewire-audio \
  pipewire-pulse \
  wireplumber \
  pulseaudio-utils \
  alsa-utils \
  mpg123 \
  python3-pygame
```

## Dependency Purpose

- **bluez / bluetooth:** Bluetooth device and profile management
- **pipewire / pipewire-pulse:** Audio routing and PulseAudio compatibility
- **wireplumber:** PipeWire session manager
- **alsa-utils / pulseaudio-utils:** Audio diagnostics and testing
- **mpg123:** MP3 playback testing
- **python3-pygame:** Python-based audio playback

## Issues Faced & Fixes Applied
 
 ### Issue 1: Bluetooth Speaker Connected but Audio Profile Was Unstable

#### Observed Problem:
The Bluetooth speaker paired successfully, but audio playback was silent or inconsistent. The Bluetooth controller frequently switched modes and enabled unnecessary plugins, causing A2DP profile instability.
 
#### Root Cause:
By default, BlueZ enables multiple plugins and allows the controller to enter power-saving or mixed modes, which interferes with classic Bluetooth audio (A2DP).

### Fix 1: Enable and Configure Bluetooth Audio Profiles
 
Edit the Bluetooth configuration file:
 
 ```bash
 sudo nano /etc/bluetooth/main.conf
```
 
Add the following at the bottom:
 
 ```bash
[General]
DisablePlugins = pnat
Enable=Source,Sink,Media,Socket
AutoEnable=true
ControllerMode = bredr
FastConnectable = true
```
 
#### Explanation:
- Forces the Bluetooth controller to remain in classic Bluetooth (BR/EDR) mode
- Ensures A2DP audio profiles are prioritised
- Disables unnecessary plugins that can cause conflicts
- Improves reconnection reliability

Restart Bluetooth to apply changes:
 ```bash
 sudo systemctl restart bluetooth

```
 

 ### Issue 2: Bluetooth Audio Connected but No Sound Output

#### Observed Problem:
Even after successful pairing, audio playback produced no sound.
 
#### Root Cause:
PipeWire applies aggressive Bluetooth power-saving policies. The Bluetooth sink remained inactive when playback started.

### Fix 2: Disable PipeWire Bluetooth Power Saving
 
Make PipeWire configuration persistent:
 
 ```bash
sudo mkdir -p /etc/pipewire
sudo cp /usr/share/pipewire/pipewire.conf /etc/pipewire/
sudo cp /usr/share/pipewire/pipewire-pulse.conf /etc/pipewire/
```
 
Edit the PipeWire configuration file:
 
 ```bash
sudo nano /etc/pipewire/pipewire.conf
```
 

Inside the `context.properties` block, add:
 ```bash
bluez5.enable-sbc-xq = true
```
This keeps the Bluetooth audio pipeline active and enables stable SBC audio handling.


### Issue 3: Audio Stops After Idle / Python Audio Not Playing

#### Observed Problem:
Audio stopped working after periods of inactivity. Python audio (pygame) frequently played silently.
 
#### Root Cause:
PulseAudio’s `module-suspend-on-idle` automatically suspended the Bluetooth sink, preventing audio from resuming.

### Fix 3: Disable PulseAudio Suspend-on-Idle
 
Edit PulseAudio configuration:
 
 ```bash
sudo nano /etc/pulse/default.pa
```
 
Find the following line and comment it:
 
 ```bash
load-module module-suspend-on-idle
```
This prevents the Bluetooth sink from being suspended.
 

Apply all configuration changes for restart:
 ```bash
systemctl --user restart pipewire pipewire-pulse
sudo systemctl restart bluetooth
sudo reboot
```
A full reboot is required for changes to take effect.

## Audio Testing
### System-Level Audio Test (Before Python)
 
  ```bash
aplay /usr/share/sounds/alsa/Front_Center.wav
mpg123 test.mp3
```
 
Expected Result:
    Clear and stable audio output from the Bluetooth speaker.

 
## Python Bluetooth Audio Test (pygame)

run the python file :
  ```bash
python3 audio_test.py
```
You will get audio output through the Bluetooth speaker.

## Text to Speech

 Install eSpeak NG:
```bash
sudo apt install -y espeak-ng
```

Test it with :
```bash
espeak-ng "Hi, Hello, This is Kanishka, speaking through the Raspberry Pi 5 via Bluetooth"
```

- Parameters :
   - `-s 140` → Speed (words per minute)
   - `-p 50`  → Pitch
   - `-a 150` → Volume

Test it with parameters :
```bash
espeak-ng -s 140 -p 50 -a 150 "Hi, Hello, This is Kanishka, speaking through the Raspberry Pi 5 via Bluetooth"
```

Download `text_test.py` & run :

```bash
python text_test.py
```

## Output

https://github.com/user-attachments/assets/ed7b987d-0ebd-4f56-b4bc-f4afe1e6fd53
