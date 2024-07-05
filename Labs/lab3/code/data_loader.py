import torch
import numpy as np

from torch.utils.data import Dataset


class NerDataset(Dataset):
    def __init__(self, data, args, tokenizer):
        self.data = data
        self.args = args
        self.tokenizer = tokenizer
        self.label2id = args.label2id
        self.max_seq_len = args.max_seq_len

    def __len__(self):
        return len(self.data)

    def __getitem__(self, item):
        text = self.data[item]["text"]
        labels = self.data[item]["labels"]
        if len(text) > self.max_seq_len - 2:
            text = text[:self.max_seq_len - 2]
            labels = labels[:self.max_seq_len - 2]
        tmp_input_ids = self.tokenizer.convert_tokens_to_ids(["[CLS]"] + text + ["[SEP]"])
        attention_mask = [1] * len(tmp_input_ids)
        ## todo 补全input_ids至最大长度
        input_ids = tmp_input_ids + [self.tokenizer.pad_token_id] * (self.max_seq_len - len(tmp_input_ids))
        ## todo 补全attention mask至最大长度
        attention_mask += [0] * (self.max_seq_len - len(attention_mask))
        labels = [self.label2id[label] for label in labels]
        labels = [0] + labels + [0] + [0] * (self.max_seq_len - len(tmp_input_ids))

        input_ids = torch.tensor(np.array(input_ids))
        attention_mask = torch.tensor(np.array(attention_mask))
        labels = torch.tensor(np.array(labels))

        # Convert to tensors of type long
        input_ids = torch.tensor(input_ids, dtype=torch.long)
        attention_mask = torch.tensor(attention_mask, dtype=torch.long)
        labels = torch.tensor(labels, dtype=torch.long)

        data = {
            "input_ids": input_ids,
            "attention_mask": attention_mask,
            "labels": labels,
        }
        return data