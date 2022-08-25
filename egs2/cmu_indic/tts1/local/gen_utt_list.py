import os
import numpy as np

import glob



# call this function- for single speaker single language, like hindi, tamil, kanada, bengali, punjabi
# telegu works too as same files for all speakers
def gen_split(wav_list):
    wav_list.sort()
    n_files =  len(wav_list)

    print(n_files)
    assert (n_files > 200)

    dev_list = wav_list[-200:-100]
    eval_list =  wav_list[-100:]

    train_list = wav_list[:-200]

    return train_list, dev_list, eval_list

def gen_mar_split(wav_list):
    wav_list.sort()
    print(len(wav_list))
    train_list = []
    dev_list = []
    eval_list = []

    for w in wav_list:
        filenum = int(os.path.basename(w).split('.')[0].split("_")[-1])
        if filenum <= 600:
            train_list.append(w)
        else:
            #dev or eval?
            if filenum > 1400:
                eval_list.append(w)
            else:
                dev_list.append(w)

    return train_list, dev_list, eval_list


def gen_guj_split(wav_list):
    wav_list.sort()
    
    train_list = []
    dev_list = []
    eval_list = []

    for w in wav_list:
        filenum = int(os.path.basename(w).split('.')[0].split("_")[-1])
        if filenum < 859:
            train_list.append(w)
        elif (filenum >= 859)&(filenum < 959):
            dev_list.append(w)
        else:
            eval_list.append(w)
    return train_list, dev_list, eval_list


utt_train_list="local/train_list"
utt_dev_list="local/dev_list"
utt_eval_list="local/eval_list"



train_list = []
dev_list = []
eval_list = []
#skip "kan_plv","guj_dp", "guj_ad", "guj_kt",
for spk in ["hin_ab", "tel_ss", "tel_kpn", "tel_sk", "tam_sdr",  "mar_slp", "mar_aup",  "ben_rm", "pan_amp"]:

    lang_tag = spk.split("_")[0]
    if lang_tag == "hin":
        wav_list = glob.glob("downloads/cmu_indic_all/wav/{0}_hindi_*.wav".format(spk))
        train_list_spk, dev_list_spk, eval_list_spk = gen_split(wav_list)
    elif lang_tag == "tel":
        wav_list = glob.glob("downloads/cmu_indic_all/wav/{0}_tel_*.wav".format(spk))
        train_list_spk, dev_list_spk, eval_list_spk = gen_split(wav_list)
    elif lang_tag == "tam":
        wav_list = glob.glob("downloads/cmu_indic_all/wav/tam_*.wav".format(spk))
        train_list_spk, dev_list_spk, eval_list_spk = gen_split(wav_list)
    elif lang_tag == "kan":
        wav_list = glob.glob("downloads/cmu_indic_all/wav/{0}_kan_*.wav".format(spk))
        train_list_spk, dev_list_spk, eval_list_spk = gen_split(wav_list)
    elif lang_tag == "mar":
        wav_list = glob.glob("downloads/cmu_indic_all/wav/{0}_data_*.wav".format(spk))
        train_list_spk, dev_list_spk, eval_list_spk = gen_mar_split(wav_list)
    elif lang_tag == "guj":
        wav_list = glob.glob("downloads/cmu_indic_all/wav/{0}_gu_*.wav".format(spk))
        train_list_spk, dev_list_spk, eval_list_spk = gen_guj_split(wav_list)
    elif lang_tag == "ben":
        wav_list = glob.glob("downloads/cmu_indic_all/wav/{0}_bn_*.wav".format(spk))
        train_list_spk, dev_list_spk, eval_list_spk = gen_split(wav_list)
    elif lang_tag == "pan":
        wav_list = glob.glob("downloads/cmu_indic_all/wav/{0}_pa_*.wav".format(spk))
        train_list_spk, dev_list_spk, eval_list_spk = gen_split(wav_list)

    #append all english to train list
    train_list_spk.extend(
        glob.glob("downloads/cmu_indic_all/wav/{0}_arctic_*.wav".format(spk)))
    
    print("Split for {0}, n_train: {1}, n_dev: {2}, n_eval: {3}".format(
        spk, len(train_list_spk), len(dev_list_spk), len(eval_list_spk)))

    train_list.extend(train_list_spk)
    dev_list.extend(dev_list_spk)
    eval_list.extend(eval_list_spk)



with open(utt_train_list, 'w') as f:
    for item in train_list:
        f.write("%s\n" % os.path.basename(item).split('.')[0])


with open(utt_dev_list, 'w') as f:
    for item in dev_list:
        f.write("%s\n" % os.path.basename(item).split('.')[0])

with open(utt_eval_list, 'w') as f:
    for item in eval_list:
        f.write("%s\n" % os.path.basename(item).split('.')[0])
