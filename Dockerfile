#####################################
# Docker file for UMAT_2scale_LSDYNA
# First obtain the LS-DYNA UMAT source and place it in ./ls-dyna_smp_d_R12_0_0_x64_redhat65_ifort160.tgz
# Build image:
# $ docker build --network=host -t umat_2scale_lsdyna .
# Run the docker container:
# $ xhost +local:root
# $ docker run -it --ipc=host --net=host -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -v /dev/dri:/dev/dri umat_2scale_lsdyna
# $ xhost -local:root
# Or start the container using docker compose:
# $ docker compose up -d
# And then attach to the running container:
# $ xhost +local:root
# $ docker compose exec umat_2scale_lsdyna bash
# $ xhost -local:root
#####################################

# Set the base image (specify the tag as Intel plans to replace ICC)
FROM intel/oneapi-hpckit:2023.0.0-devel-ubuntu22.04

# Define variables
ENV HOME="/root"
ENV PROJECT_DIR="/usr/local/src/UMAT_2scale_LSDYNA"
ENV REPO_DIR="${PROJECT_DIR}/lsdyna_added_files_ref"
ENV LSDYNA_DIR="${PROJECT_DIR}/lsdyna_object_version"
ENV LSDYNA_UMAT="./ls-dyna_smp_d_R12_0_0_x64_redhat65_ifort160.tgz"
ENV LSPREPOST_DIR="${HOME}/lsprepost4.9_common"

# Copy files to the container
RUN mkdir -p ${REPO_DIR}
COPY . ${REPO_DIR}
WORKDIR ${REPO_DIR}

# Install dependencies
RUN apt update -qq && apt install -qq -y zlib1g-dev libhdf5-dev libx11-dev lbzip2 libbz2-dev libreadline-dev libsqlite3-dev \
    liblzma-dev libffi-dev libboost-all-dev time clang

# Install openssl 1.1 (needed for Python 3.6.5)
RUN wget -q http://security.ubuntu.com/ubuntu/pool/main/o/openssl/openssl_1.1.1f-1ubuntu2.17_amd64.deb -O /tmp/openssl.deb && \
    wget -q http://security.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.1f-1ubuntu2.17_amd64.deb -O /tmp/libssl.deb && \
    wget -q http://security.ubuntu.com/ubuntu/pool/main/o/openssl/libssl-dev_1.1.1f-1ubuntu2.17_amd64.deb -O /tmp/libssl-dev.deb && \
    dpkg -i /tmp/libssl.deb && \
    dpkg -i /tmp/libssl-dev.deb && \
    dpkg -i /tmp/openssl.deb
# The url for the debian packages may change over time.
# Maybe it is better to build openssl 1.1 from source, but that takes some time.
#RUN cd /tmp && wget -q https://www.openssl.org/source/old/1.1.1/openssl-1.1.1n.tar.gz -O openssl-1.1.1n.tar.gz && \
#    tar -xf openssl-1.1.1n.tar.gz && \
#    cd openssl-1.1.1n/ && \
#    ./config shared -Wl,-rpath=/opt/openssl11/lib --prefix=/opt/openssl11 && \
#    make && make install

# Install pyenv
RUN curl -sS https://pyenv.run | bash && \
    echo "export PYENV_ROOT=\"\$HOME/.pyenv\"" >> ~/.bashrc && \
    echo "command -v pyenv >/dev/null || export PATH=\"\$PYENV_ROOT/bin:\$PATH\"" >> ~/.bashrc && \
    echo "eval \"\$(pyenv init -)\"" >> ~/.bashrc && \
    echo "export LSTC_LICENSE=network" >> ~/.bashrc && \
    echo "export LSTC_LICENSE_SERVER=31010@localhost" >> ~/.bashrc && \
    echo "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$PYENV_ROOT/versions/3.8.15/lib" >> ~/.bashrc
ENV PYENV_ROOT="${HOME}/.pyenv"
ENV PATH="${PYENV_ROOT}/bin:${PATH}"

# Install Python 3.6.5 for LSDYNA scripting (for that openssl 1.1 is needed)
RUN . ~/.bashrc && pyenv update && \
    env PYTHON_CONFIGURE_OPTS="--enable-shared" CC=clang pyenv install 3.6.5 && pyenv global 3.6.5
    #CPPFLAGS=-I/opt/openssl11/include LDFLAGS="-L/opt/openssl11/lib -Wl,-rpath=/opt/openssl11/lib" \
    #pyenv install 3.6.5

# Install pip packages for Python 3.6.5
RUN . ~/.bashrc && python -m pip install --upgrade pip && \
    python -m pip install yapf clang-format fprettify numpy

# Install Python 3.8.15 for the LSDYNA UMAT compilation
RUN . ~/.bashrc && env PYTHON_CONFIGURE_OPTS="--enable-shared" pyenv install 3.8.15 && pyenv global 3.8.15 && \
    echo "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$PYENV_ROOT/versions/3.8.15/lib" >> ~/.bashrc
RUN . ~/.bashrc && pyenv versions

# Install pip packages for Python 3.8.15
RUN . ~/.bashrc && python -m pip install --upgrade pip && \
    python -m pip install yapf clang-format fprettify numpy

# Setup and compile LSDYNA usermat package
RUN mv ${LSDYNA_UMAT} ..
RUN . ~/.bashrc && ./setup_full.sh
#ENV LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:$PYENV_ROOT/versions/3.6.5/lib/"
RUN echo "PATH=\"${LSDYNA_DIR}:\$PATH\"" >> ~/.bashrc

# Install lsprepost
RUN wget -q https://ftp.lstc.com/anonymous/outgoing/lsprepost/4.9/linux64/lsprepost-4.9.11-common-22Nov2022.tgz -O /tmp/lsprepost.tgz && \
    mkdir -p ${LSPREPOST_DIR} && \
    tar xf /tmp/lsprepost.tgz -C ${LSPREPOST_DIR} --strip-components=1 && \
    echo 'env LD_LIBRARY_PATH={$LSPREPOST_DIR}/lib:$LD_LIBRARY_PATH ${LSPREPOST_DIR}/lspp49 "$@"' > ${LSDYNA_DIR}/lsprepost && \
    chmod +x ${LSDYNA_DIR}/lsprepost

# Create shortcuts for lsdynaumat and lsprepost
RUN ln -sf ${LSDYNA_DIR}/lsdynaumat /usr/bin/lsdynaumat && \
    ln -sf ${LSDYNA_DIR}/lsprepost /usr/bin/lsprepost

# Workaround for model_generation example
RUN mkdir -p /packages && ln -sf $PYENV_ROOT /packages/pyenv

# Set PYTHONPATH for mixed language programming
RUN . ~/.bashrc && echo "export PYTHONPATH=$PYTHONPATH:$LSDYNA_DIR/umat:$LSDYNA_DIR/mixed_languages" >> ~/.bashrc

# Install dependencies for lsprepost (needed for the GUI)
RUN apt install -qq -y libgtk2.0-0 libsecret-1-0 libgl1 libglu1-mesa libsm6 libxtst6 libxmu6 libopenjp2-7 libspeex1 libtheora0 \
    libvorbis0a libvorbisenc2

# Test external packages
RUN . ~/.bashrc && cd ${REPO_DIR}/external_packages && \
    ./test_ttb.sh && \
    ./test_forpy.sh && \
    ./test_ezh5.sh

# Test mixed language programming
RUN . ~/.bashrc && cd ${REPO_DIR}/mixed_languages && \
    ./test_call_cpp.sh && \
    ./test_call_py.sh

# Set working directory
WORKDIR ${PROJECT_DIR}

ENTRYPOINT /bin/bash
