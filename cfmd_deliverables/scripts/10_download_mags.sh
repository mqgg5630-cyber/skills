#!/usr/bin/env bash
# 下载 cFMD 的 MAG 序列（按数据集分包），并只保留 antiSMASH 输入清单中的代表株
#
# 用法:
#   ./10_download_mags.sh [代表株清单.csv] [工作目录]
# 默认:
#   清单 = ../tables/09_antiSMASH输入MAG清单_每SGB代表株.csv
#   目录 = ../mags
#
# 说明:
#   1. cFMD 把每个数据集的 MAG 打成独立压缩包放在 Zenodo（v1.0.0 记录 14871720，合计约 272.5 GB）。
#      本脚本用官方 download_mags.sh 拉取，只针对清单里出现的数据集，实际下载量通常在 40 GB 以内。
#   2. 官方脚本在 main 分支维护，与 v1.1.0 的表可能有个别数据集命名差异。若某个数据集下载失败，
#      检查 cFMD_data/<dataset>/ 下是否有对应的 tar.gz 文件名，手工 wget 即可。
#   3. 下载完成后仅解压代表株，其余删除，最终 -out 目录只保留约 957 个 fasta。

set -euo pipefail

LIST="${1:-../tables/09_antiSMASH输入MAG清单_每SGB代表株.csv}"
WORK="${2:-../mags}"
mkdir -p "$WORK"/{tarballs,fasta,logs}

echo "[1/4] 从清单提取数据集名"
# 清单第 2 列为 dataset_id
tail -n +2 "$LIST" | awk -F',' '{print $2}' | tr -d '"' | sort -u > "$WORK/datasets.txt"
echo "      共 $(wc -l < "$WORK/datasets.txt") 个数据集"

echo "[2/4] 获取官方下载脚本"
if [[ ! -x "$WORK/download_mags.sh" ]]; then
    curl -fsSL "https://raw.githubusercontent.com/SegataLab/cFMD/main/download_mags.sh" \
         -o "$WORK/download_mags.sh"
    chmod +x "$WORK/download_mags.sh"
fi

echo "[3/4] 下载 MAG 包"
cd "$WORK"
mapfile -t DS < datasets.txt
./download_mags.sh "${DS[@]}" 2>&1 | tee logs/download.log
cd - >/dev/null

echo "[4/4] 解压并筛选代表株"
python3 - "$LIST" "$WORK" <<'PY'
import csv, os, sys, tarfile, glob, shutil

lst, work = sys.argv[1], sys.argv[2]
want = {}
with open(lst, newline='', encoding='utf-8-sig') as fh:
    for row in csv.DictReader(fh):
        want[row['MAG_id']] = row['dataset_id']
print(f"  需要 {len(want)} 个 MAG")

fasta_dir = os.path.join(work, 'fasta')
found = 0
for tar_path in sorted(glob.glob(os.path.join(work, 'tarballs', '*.tar.gz')) +
                       glob.glob(os.path.join(work, '*.tar.gz'))):
    with tarfile.open(tar_path) as tf:
        for m in tf.getmembers():
            if not m.isfile():
                continue
            base = os.path.basename(m.name)
            stem = base.rsplit('.', 1)[0]
            if stem in want:
                out = os.path.join(fasta_dir, base)
                with tf.extractfile(m) as src, open(out, 'wb') as dst:
                    shutil.copyfileobj(src, dst)
                found += 1
print(f"  解压得到 {found} 个 fasta，缺失 {len(want) - found} 个")
PY

echo "完成：$(ls "$WORK"/fasta | wc -l) 个 fasta 位于 $WORK/fasta"
echo "缺失的代表株请对照 logs/download.log 检查数据集是否下载完整"
