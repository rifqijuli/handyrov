<div align="center">

# 🌊 HandyROV

**Object detection, tracking and control for the BlueROV2**

![Python](https://img.shields.io/badge/python-3.x-blue?logo=python&logoColor=white)
![Ubuntu](https://img.shields.io/badge/Ubuntu-22.04%20%7C%2024-E95420?logo=ubuntu&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?logo=pytorch&logoColor=white)
![YOLO](https://img.shields.io/badge/Ultralytics-YOLO-111F68)

</div>

---

## 📑 Contents

- [Install python](#install-python)
- [Clone this repo](#clone-this-repo)
- [Install this for Gstreamer plugin](#install-this-for-gstreamer-plugin)
- [Make virtual environment](#make-virtual-environment)
- [Install PyGObject](#install-pygobject)
- [Install requirements on pip](#install-requirements-on-pip)
- [Install Pytorch](#install-pytorch)
- [Install Ultralytics](#install-ultralytics)
- [Running the program](#running-the-program)

---

## 🐍 Install python
```bash 
sudo apt update sudo apt install -y git python3 python3-venv python3-pip 
```

## 📥 Clone this repo
```bash 
git clone git@github.com:rifqijuli/bluerov2_thesis.git
```

## 🎥 Install this for Gstreamer plugin

For Ubuntu 22.04
```bash 
sudo apt install python3-gi python3-gi-cairo gir1.2-gobject-2.0 gir1.2-gst-plugins-base-1.0 gir1.2-gstreamer-1.0 libgirepository1.0-dev
```

For Ubuntu 24
```bash 
sudo apt install libgirepository-2.0-dev gcc libcairo2-dev pkg-config python3-dev gir1.2-gtk-4.0
```

## 📦 Make virtual environment
```bash 
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
```

Now we are inside Virtual Environment.

## 🧩 Install PyGObject
```bash 
pip3 install pycairo 
pip3 install PyGObject
python3 -c "import gi; print('gi imported OK')"
```

> [!TIP]
> If you encounter an error for PyGObject, use older version
>
> ```bash
> pip3 install "PyGObject<3.51.0"
> ```

## 📋 Install requirements on pip
```bash 
pip install -r requirements.txt
```

> [!NOTE]
> If numpy error, change the numpy version on the requirements.txt according to the error.

## 🔥 Install Pytorch
Go to https://pytorch.org/get-started/locally/ and follow the guide. In my case, it shows as this:
```bash 
pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cu126
```

## 🎯 Install Ultralytics
Go to https://docs.ultralytics.com/quickstart/ and follow the guide. In my case, it shows as this:
```bash 
pip3 install -U ultralytics
```

## 🚀 Running the program

Start the program with the GUI runner:
```bash
python gui_runner.py
```

A small **BLUEROV Runner** window opens where you can choose:

| Option | Choices |
| --- | --- |
| **Camera** | `bluerov`, `webcam` |
| **Model** | `yolo11n`, `yolo11s`, `yolo26n`, `yolo26s` (only the models available for the chosen dataset are shown) |
| **Dataset** | `COCO`, `COU`, `TrashCan`, `Pepsi_DTU`, `Pepsi_DTU_Rotate`, `UNO`, `Venise`, `Morgane`, `Walia` |

Then use the buttons:

- ▶️ **Start Image+Control**: starts the vision, control, RC command, ping sonar and crane view processes
- ⏹️ **Stop Main**: stops the main processes
- 🧹 **Run Cleaner**: runs the cleaner

> [!IMPORTANT]
> Everytime you're done with the program, don't forget to deactivate your environment.
> ```bash 
> deactivate
> ```
> And if you want to resume or start the program, don't forget to activate your environment.
> ```bash 
> source .venv/bin/activate
> ```
