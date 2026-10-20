#!/usr/bin/env bash
# 批量运行 antiSMASH 8.0.4
#
# 用法:
#   ./11_run_antismash.sh [fasta目录] [输出目录] [并发数]
# 默认: ../mags/fasta  ../antismash  $(nproc)
#
# 依赖:
#   conda create -n antismash -c conda-forge -c bioconda antismash=8.0.4
#   conda activate antismash
#
# 说明:
#   - 细菌与真菌分开跑。文件名含真菌属名（Penicillium/Aspergillus/Saccharomyces 等）的走 --taxon fungi。
#   - 已在输出目录存在 .json 的结果会跳过，可反复中断续跑。
#   - 单基因组 3–8 min（细菌，16 线程），真菌 10–20 min。957 个代表株约 40–80 CPU·h。
#   - -c 8 表示每个任务 8 线程；总并发不宜超过物理核数 / 8。

set -euo pipefail

IN="${1:-../mags/fasta}"
OUT="${2:-../antismash}"
JOBS="${3:-4}"
THREADS="${4:-8}"

command -v antismash >/dev/null || { echo "antismash 未安装，先 conda install -c bioconda antismash=8.0.4"; exit 1; }
mkdir -p "$OUT"/{logs,results}

FUNGI_RE='Penicillium|Aspergillus|Saccharomyces|Debaryomyces|Kluyveromyces|Pichia|Mucor|Fusarium|Scopulariopsis|Yarrowia|Brettanomyces|Hanseniaspora|Lachancea|Candida|Zygosaccharomyces|Zygotorulaspora|Wickerhamiella|Kazachstania|Diutina|Teunomyces|Blastobotrys|unknown'

run_one() {
    f="$1"; out="$2"; logs="$3"; th="$4"
    name=$(basename "$f"); name=${name%%.*}
    [[ -s "$out/${name}.json" ]] && { echo "skip $name"; return 0; }
    if echo "$name" | grep -qE "$FUNGI_RE"; then
        antismash "$f" --taxon fungi --genefinding-tool prodigal-m \
            --cb-general --cb-knownclusters --cb-subclusters \
            --cpus "$th" --output-dir "$out/$name" --output-basename "$name" \
            > "$logs/${name}.log" 2>&1
    else
        antismash "$f" --genefinding-tool prodigal \
            --cb-general --cb-knownclusters --cb-subclusters --asf --pfam2go \
            --cpus "$th" --output-dir "$out/$name" --output-basename "$name" \
            > "$logs/${name}.log" 2>&1
    fi
    # 只保留 json 与 txt，节省磁盘
    find "$out/$name" -maxdepth 1 -type d \( -name '*.html' -o -name 'css' -o -name 'js' \) -prune -exec rm -rf {} + 2>/dev/null || true
}

export -f run_one
export FUNGI_RE

find "$IN" -maxdepth 1 -type f \( -name '*.fa' -o -name '*.fna' -o -name '*.fasta' \) -print0 \
  | xargs -0 -P "$JOBS" -I{} bash -c 'run_one "$@"' _ {} "$OUT/results" "$OUT/logs" "$THREADS"

echo "完成：$(find "$OUT/results" -name '*.json' | wc -l) 个结果"
echo "失败任务见 $OUT/logs/*.log"
