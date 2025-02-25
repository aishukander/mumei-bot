# 定義Python版本
ARG Python_Version=3.13.1-slim
ARG Mumei_Version=10.7.0

######## 第一階段：編譯FFmpeg ########
FROM python:${Python_Version} AS builder

ENV \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    PIP_ROOT_USER_ACTION=ignore

WORKDIR /bot

COPY . .

# 靜態編譯FFmpeg以及安裝所需套件
RUN apt-get update && \
    apt-get install -y --no-install-recommends wget xz-utils jq && \
    wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz && \
    tar xf ffmpeg-release-amd64-static.tar.xz && \
    mv ffmpeg-*-amd64-static/ffmpeg /usr/local/bin/ && \
    mv ffmpeg-*-amd64-static/ffprobe /usr/local/bin/ && \
    rm -f ffmpeg-release-amd64-static.tar.xz && \
    rm -rf ffmpeg-*-amd64-static

RUN mkdir -p /tmp/json && \
    find /bot/json -type f ! -name 'Token.json' -exec cp {} /tmp/json/ \; && \
    jq 'with_entries(.value = "")' /bot/json/Token.json > /tmp/json/Token.json && \
    rm -rf /bot/json/*

######## 第二階段：運行環境 ########
FROM python:${Python_Version}
LABEL version="${Mumei_Version}"
LABEL org.opencontainers.image.authors="aishukander <hank960924@gmail.com>"

ENV \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    PIP_ROOT_USER_ACTION=ignore

WORKDIR /bot

# 複製編譯完成的FFmpeg二進位檔
COPY --from=builder /usr/local/bin/ffmpeg /usr/local/bin/ffmpeg
COPY --from=builder /usr/local/bin/ffprobe /usr/local/bin/ffprobe
COPY --from=builder /tmp/json/ /tmp/json/
COPY --from=builder /bot/ /bot/

# 安裝opus庫
RUN apt-get update && \
    apt-get install -y --no-install-recommends libopus0 && \
    rm -rf /var/lib/apt/lists/* && \
    # 安裝Python依賴
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    rm -rf /root/.cache/pip/* && \
    chmod +x /bot/entrypoint.sh

ENTRYPOINT ["/bot/entrypoint.sh"]