#!/usr/bin/env bash
set -euo pipefail

base_path=/opt/scare-deer

if [ -d "$base_path/.git" ]; then
    echo "repo exists, uninstall first if you want to reinstall"
    exit 1
fi

echo "repo does not exist, cloning"
sudo mkdir -p "$base_path"
sudo chown "$USER": "$base_path"
git clone https://github.com/Laaggan/scare-deer.git "$base_path"   # no sudo

if [ ! -d "$base_path/analysis/.analysis_env" ]; then
    python -m venv "$base_path/analysis/.analysis_env"
    "$base_path/analysis/.analysis_env/bin/pip" install -r "$base_path/analysis/requirements.txt"
fi

if [ ! -d "$base_path/camera/.camera_env" ]; then
    # --system-site-packages is needed for picamera2
    python -m venv "$base_path/camera/.camera_env" --system-site-packages
    "$base_path/camera/.camera_env/bin/pip" install -r "$base_path/camera/requirements.txt"
fi

sudo cp "$base_path/camera/deer_scare_camera.service" /etc/systemd/system/
sudo cp "$base_path/analysis/deer_scare_analysis.service" /etc/systemd/system/

sudo systemctl daemon-reload
sudo systemctl enable --now deer_scare_camera.service deer_scare_analysis.service