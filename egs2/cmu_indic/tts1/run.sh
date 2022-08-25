#!/usr/bin/env bash
# Set bash to 'debug' mode, it will exit on :
# -e 'error', -u 'undefined variable', -o ... 'error in pipeline', -x 'print commands',
set -e
set -u
set -o pipefail

fs=22050
n_fft=1024
n_shift=256
win_length=null

spk=all

opts="--audio_format wav --local_data_opts ${spk} "

train_set=${spk}_train_no_dev
valid_set=${spk}_dev
test_sets=${spk}_eval

train_config=conf/tuning/train_transformer.yaml #train.yaml
inference_config=conf/decode.yaml

# g2p=g2p_en # Include word separator
g2p=none #epitran_indic #epitran_bengali #epitran_hindi #g2p_en_no_space # Include no word separator

./tts.sh \
    --lang en \
    --feats_type raw \
    --fs "${fs}" \
    --n_fft "${n_fft}" \
    --n_shift "${n_shift}" \
    --win_length "${win_length}" \
    --token_type phn \
    --cleaner none \
    --g2p none \
    --train_config "${train_config}" \
    --inference_config "${inference_config}" \
    --train_set "${train_set}" \
    --valid_set "${valid_set}" \
    --test_sets "${test_sets}" \
    --srctexts "data/${train_set}/text" \
    ${opts} "$@"
