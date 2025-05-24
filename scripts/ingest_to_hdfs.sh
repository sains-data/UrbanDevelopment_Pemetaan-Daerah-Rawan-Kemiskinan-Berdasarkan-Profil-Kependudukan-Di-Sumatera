#!/bin/bash

# Script ini akan mengunggah file lokal ke HDFS Bronze Layer

# Periksa apakah argumen yang dibutuhkan diberikan
if [ -z "$1" ] || [ -z "$2" ]; then
  echo "Usage: $0 <local_file_path> <hdfs_target_dir>"
  exit 1
fi

LOCAL_FILE_PATH=$1
HDFS_TARGET_DIR=$2
HDFS_HOSTNAME="namenode" # Sesuai dengan hostname di docker-compose.yml
HDFS_PORT="9000"

echo "Mulai ingesti file: $LOCAL_FILE_PATH ke HDFS: hdfs://$HDFS_HOSTNAME:$HDFS_PORT$HDFS_TARGET_DIR"

# Buat direktori HDFS jika belum ada
hdfs dfs -mkdir -p hdfs://$HDFS_HOSTNAME:$HDFS_PORT$HDFS_TARGET_DIR

# Hapus file lama di HDFS jika ada (opsional, untuk re-runability)
# Ini akan menghapus file dengan nama yang sama di direktori target HDFS
hdfs dfs -rm -f hdfs://$HDFS_HOSTNAME:$HDFS_PORT$HDFS_TARGET_DIR/$(basename $LOCAL_FILE_PATH)

# Unggah file ke HDFS
hdfs dfs -put $LOCAL_FILE_PATH hdfs://$HDFS_HOSTNAME:$HDFS_PORT$HDFS_TARGET_DIR

if [ $? -eq 0 ]; then
  echo "Berhasil mengunggah $LOCAL_FILE_PATH ke HDFS."
else
  echo "Gagal mengunggah $LOCAL_FILE_PATH ke HDFS."
  exit 1
fi