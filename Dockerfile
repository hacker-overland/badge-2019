FROM ubuntu:18.04
SHELL ["/bin/bash", "-c"]

##################
# Set build environment vars
ENV IDF_PROJECT="esp-idf"
ENV IDF_PATH="/root/esp/${IDF_PROJECT}"
ENV IDF_REPO="https://github.com/espressif/${IDF_PROJECT}.git"
ENV IDF_REPO_COMMIT="5c88c5996dbde6208e3bec05abc21ff6cd822d26"
ENV ESP32_ELF_FILE="xtensa-esp32-elf-linux64-1.22.0-80-g6c4433a-5.2.0.tar.gz"
ENV ESP32_ELF_URL="https://dl.espressif.com/dl/${ESP32_ELF_FILE}"
ENV UPYTHON_PROJECT_NAME="micropython"
ENV UPYTHON_REPO="https://github.com/miketeachman/${UPYTHON_PROJECT_NAME}.git"
ENV UPYTHON_REPO_COMMIT="6b023290f6dbccfdb427857120cd12c292e622f2"
ENV BADGE_SOURCE_PATH="/badge_source"

##################
# Setup dirs
RUN mkdir -p /src/assets
RUN mkdir -p /root/esp
RUN mkdir -p ${BADGE_SOURCE_PATH}

##################
# Copy in helper files
COPY source/ ${BADGE_SOURCE_PATH}
COPY os_packages.txt /src/assets/
COPY set_esp32_path.sh /src/assets/
COPY build_and_flash.sh /src/assets/
RUN chmod 755 /src/assets/*sh
RUN chmod 755 ${BADGE_SOURCE_PATH}/loader.sh

##################
# Install OS package requirements
RUN apt-get update && \
    apt-get install -y `cat /src/assets/os_packages.txt`

##################
# Download ESP-IDF and related components
WORKDIR /root/esp
RUN wget  ${ESP32_ELF_URL} && \
    tar -xzf ${ESP32_ELF_FILE} && \
    git clone --recursive ${IDF_REPO} && \
    cd ${IDF_PROJECT} && \
    git checkout ${IDF_REPO_COMMIT} && \
    git submodule update --recursive

#################
# Install required Python libs
RUN /usr/bin/python -m pip install -r /root/esp/esp-idf/requirements.txt
RUN /usr/bin/python -m pip install adafruit-ampy

#################
# Setup Micropython project, prepare for build
RUN . ~/esp/esp-idf/add_path.sh && \
    . /src/assets/set_esp32_path.sh && \
    git clone ${UPYTHON_REPO} && \
    cd ${UPYTHON_PROJECT_NAME} && \
    git checkout ${UPYTHON_REPO_COMMIT} && \
    git submodule update --init

#################
# Build firmware and prepare for flash.
WORKDIR /root/esp/${UPYTHON_PROJECT_NAME}/ports/esp32
RUN . /src/assets/set_esp32_path.sh  && \
    make && \
    echo "################" && \
    printenv && \
    echo "################" && \
    make V=1

#################
# Set up runtime for build process
CMD ${BADGE_SOURCE_PATH}/loader.sh
