# FocusTimer — A Productivity Tracking Tool Implementing a Transparent OLED with A Pi Camera Module, and Powered by Python OpenCV on a Raspberry Pi

![Screenshot 2025-05-01 201531]()

### The **FocusTimer** is a small desktop productivity tracker/timer using a Transparent OLED with a Pi camera module hidden behind it. The timer will count up as long as you are focused on the screen/monitor in front of you. Spend too much time looking away, and the timer will reset!

<video src="">

---

## Contents

- [Required Hardware](#required-hardware)
- [Pi Setup](#pi-setup)
- [Assembly](#assembly)
- [Using the Timer](#using-the-frame)
- [Video Demo](#video-demo)

---

## Required Hardware

| Item | Link |
|------|------|
| Raspberry Pi Zero 2 W | [Amazon](https://amzn.to/3YBvaBV) |
| Pi Power Supply | [Amazon](https://amzn.to/42dMak0) |
| Waveshare 1.54" Transparent OLED  | [Amazon](https://amzn.to/4jjJQNH) |
| Pi Camera Module V2.1  | [Amazon](https://amzn.to/4keIu8i) |
| Micro SD Card (for Pi OS image) | [Amazon](https://amzn.to/3Z0md5n) |
| Enclosure 3D Print Files | [Printables](https://www.printables.com/model/1287334-eink-picture-frame) |

---

## Pi Setup

**Before starting**, ensure that your Pi is running Raspberry Pi OS 32 or 64-bit (Lite not supported), and is connected to your home network.  
If you need help installing Raspberry Pi OS, follow the [official guide](https://www.raspberrypi.com/documentation/computers/getting-started.html#installing-the-operating-system).

Once your Pi has booted, open Command Prompt (Windows) or Terminal (Mac), and SSH into the Pi:

```bash
ssh pi@pi.local
```

Then run the following to clone the project and begin setup:

```bash
git clone https://github.com/EnriqueNeyra/Focus-Timer.git
cd Focus-Timer
sudo bash setup.sh
```

Be sure to **reboot** the Pi after the setup script completes.

---

## Assembly

### 1. ...
<p align="center"><img src="" width="700"></p>

### 2. ...
<p align="center"><img src="" width="700"></p>

### 3. ...
<p align="center"><img src="" width="700"></p>

Assembly is now complete!

---

## Using the Focus Timer

Connect the power cable to the Focus Timer. Place it on a flat surface on your desk, directly in front of you. Angle the display so that it is aimed squarely at your face, and ensure that there is sufficient lighting on your face. Poor lighting will prevent your face from being detected.
From the initial state (00:00), you must be 'focused' and looking in front of you for ~3 seconds before the timer will begin counting. When 'unfocused' and looking away, there is a grace period of ~10 seconds before the timer will reset.
