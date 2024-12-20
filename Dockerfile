#####################################
# Docker file for UMAT_2scale_LSDYNA
# First obtain the LS-DYNA UMAT source and place it in ./ls-dyna_smp_d_R12_0_0_x64_redhat65_ifort160.tgz
# Build image:
# $ docker build --network=host -t UMAT_2scale_LSDYNA .
# Run the docker container:
# $ xhost +local:root
# $ docker run -it --ipc=host --net=host -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -v /dev/dri:/dev/dri UMAT_2scale_LSDYNA
# $ xhost -local:root
# Or start the container using docker compose:
# $ docker compose up -d
# And then attach to the running container:
# $ xhost +local:root
# $ docker compose exec UMAT_2scale_LSDYNA bash
# $ xhost -local:root
# Running the container on Windows using Docker Desktop:
# First install VcXsrv and start XLaunch with disabled access control
# $ docker run -it --ipc=host --net=host -e DISPLAY=host.docker.internal:0.0 UMAT_2scale_LSDYNA
#####################################

# Set the base image (specify the tag as Intel plans to replace ICC)
FROM intel/oneapi-hpckit:2023.0.0-devel-ubuntu22.04

ARG DEBIAN_FRONTEND=noninteractive
SHELL ["/bin/bash", "-c"] 

# Install dependencies
RUN apt update -qq && apt install -qq -y meld zlib1g-dev libhdf5-dev libx11-dev lbzip2 libbz2-dev libreadline-dev libsqlite3-dev liblzma-dev libffi-dev libboost-all-dev time clang libgtk2.0-0 libsecret-1-0 libgl1 libglu1-mesa libsm6 libxtst6 libxmu6 libopenjp2-7 libspeex1 libtheora0 libvorbis0a libvorbisenc2 libcanberra-gtk-module libcanberra-gtk3-module alsa-base alsa-utils xvfb libnotify4

# Define variables
ENV HOME="/root"
ENV PROJECT_DIR="/workspaces/UMAT_2scale_LSDYNA"
ENV REPO_DIR="${PROJECT_DIR}/repo_files"
ENV LSDYNA_DIR="${PROJECT_DIR}/lsdyna_object_version"
ENV LSDYNA_UMAT="./ls-dyna_smp_d_R12_0_0_x64_redhat65_ifort160.tgz"
ENV LSPREPOST_DIR="${PROJECT_DIR}/lsprepost_common"

ENV set_intel_var='source /opt/intel/oneapi/setvars.sh --force'
ENV LSTC_LICENSE=network
ENV LSTC_LICENSE_SERVER=31010@localhost

ENV LD_LIBRARY_PATH=$LSPREPOST_DIR/lib2:$LD_LIBRARY_PATH

ENV PYENV_ROOT="${HOME}/.pyenv"
ENV PATH="$PATH:$PYENV_ROOT/shims:$PYENV_ROOT/bin:$LSDYNA_DIR:$LSPREPOST_DIR"

# Set PYTHONPATH for mixed language programming
ENV PYTHONPATH=$PYTHONPATH:$LSDYNA_DIR/umat:$LSDYNA_DIR/mixed_languages

# Install pyenv
RUN curl -sS https://pyenv.run | bash

# Install Python 3.9.15 for the LSDYNA UMAT compilation & ensure getting python dynamic libraries
RUN env PYTHON_CONFIGURE_OPTS="--enable-shared" pyenv install 3.9.15 && pyenv global 3.9.15
RUN pyenv versions 

ENV PYTHONHOME=$PYENV_ROOT/versions/3.9.15

# Install pip packages for Python
RUN python -m pip install --upgrade pip && pip install yapf clang-format fprettify numpy

# Set working directory
WORKDIR ${PROJECT_DIR}

ENTRYPOINT ["/bin/bash"]