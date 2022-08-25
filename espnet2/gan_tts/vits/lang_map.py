# Copyright 2021 Tomoki Hayashi
#  Apache 2.0  (http://www.apache.org/licenses/LICENSE-2.0)

"""lang map
"""

from typing import Optional, Tuple, List, Union
from collections import OrderedDict
import logging
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_complex.tensor import ComplexTensor

from espnet2.gan_tts.wavenet import WaveNet
from espnet2.gan_tts.wavenet.residual_block import Conv1d
from espnet.nets.pytorch_backend.nets_utils import make_non_pad_mask

from espnet.nets.pytorch_backend.conformer.encoder import Encoder



class BaseLangMap(torch.nn.Module):
    
    def __init__(
        self,
        in_channels: int = 256,
        layers: int = 1,
        dropout_rate: float = 0.0,
    ):
       
        super().__init__()

        # define modules
        self.encoder = Encoder(
            idim=-1,
            input_layer=None,
            attention_dim=in_channels,
            attention_heads=4,
            linear_units=in_channels*4,
            num_blocks=1,
            dropout_rate=dropout_rate
        )


       
    def forward(
        self, x: torch.Tensor, x_lengths: torch.Tensor,
    ) -> torch.Tensor:

        x_mask = (
            make_non_pad_mask(x_lengths)
            .to(
                device=x.device,
                dtype=x.dtype,
            )
            .unsqueeze(1)
        )

        x, _ = self.encoder(x, x_mask)
       
        return x


class MultiLangMap(torch.nn.Module):
    def __init__(
        self,
        in_channels: int = 256,
        layers: int = 1,
        dropout_rate: float = 0.0,
        max_num_lang: int = 10,
    ):
        """Multiple lang Module.
        """
        super().__init__()
        
        # Hyper-parameter
        self._max_num_lang = max_num_lang
        self._in_channels = in_channels

        # [B, T_text, attention_dim] -> [B, n*T_text, attention_dim]
        self.multi_lang_map = nn.ModuleList()
        for z in range(1, max_num_lang + 1):
            self.multi_lang_map.append(
                BaseLangMap(in_channels, layers, dropout_rate)
            )
    

    def forward(
        self,
        x: torch.Tensor,
        x_lengths: torch.Tensor,
        lids: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:
        #logging.info(" {} {}".format(self._max_num_lang, lids))
        lid_weight = (torch.arange(self._max_num_lang).to(device=x.device).expand(len(lids), \
            self._max_num_lang) == lids).int() # max_lang, b
        #logging.info(" lid_weight {} lids {}".format(lid_weight.shape, lids.shape))
        b, t, d = x.size()

        emb_lang = torch.zeros(b, self._max_num_lang, t, d).to(device=x.device)
        for z in range(self._max_num_lang):
            emb_lang[:, z] = self.multi_lang_map[z](x, x_lengths)
        #logging.info(" {} {}".format(lid_weight, emb_lang))
        emb_lang = lid_weight.unsqueeze(2).unsqueeze(3) * emb_lang
        
        return torch.sum(emb_lang, axis=1) #b, t, c
