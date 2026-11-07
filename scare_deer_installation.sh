if ! [ -z "/opt/scare-deer" ]
then
    echo "repo exists, don't install"
else
    echo "repo does not exist, clone a copy"
    git clone https://github.com/Laaggan/scare-deer.git
fi

base_path=/opt/scare-deer/scare-deer

if ! [ -z "$base_path/analysis/.analysis_env" ]
then
    python -m venv "$base_path/analysis/.analysis_env"
    source "$base_path/analysis/.analysis_env/bin/activate"
    pip install -r "$base_path/analysis/requirements.txt"
    deactivate
fi

if ! [ -z "$base_path/camera/.camera_env" ]
then
    python -m venv "$base_path/camera/.camera_env" --system-site-packages # This is needed for picamera2 to work properly
    source "$base_path/camera/.camera_env/bin/activate"
    pip install -r "$base_path/camera/requirements.txt"
    deactivate
fi

sudo cp $base_path/camera/deer_scare_camera.service /etc/systemd/system
sudo cp $base_path/analysis/deer_scare_analysis.service /etc/systemd/system

sudo systemctl daemon-reload
sudo systemctl enable deer_scare_camera.service
sudo systemctl enable deer_scare_analysis.service

sudo systemctl start deer_scare_camera