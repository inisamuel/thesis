import torch
from torch.utils.data import Dataset
import numpy as np
from utils import get_dataset_path
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler

# for information about the datasets:  https://www.cs.ucr.edu/~eamonn/time_series_data/


class UCRDataset(Dataset):
    def __init__(self, name: str, split: str, patch_len=None, normalize=False, norm_method="standard", pad=False):
        """
        :param name: dataset name from ucr collection
        :param split: either "test" or "train"
        :param patch_len: None or integer that specifies that
                            the time series should be split into chunks of length patch_len
        :param normalize: boolean to indicate whether data should be normalized
        :param norm_method: normalization method that will be used if normalize==True,
                            pick between "standard", "minmax", "robust"
        """
        self.patch_len = patch_len

        arr = np.loadtxt(get_dataset_path(name, split), delimiter='\t')
        x_np = arr[:, 1:]

        # normalize samples
        if normalize:
            if norm_method == "standard":
                scaler = StandardScaler()
            elif norm_method == "minmax":
                scaler = MinMaxScaler()
            elif norm_method == "robust":
                scaler = RobustScaler()
            else:
                raise Exception("choose between standard, minmax, or robust")

            x_np = scaler.fit_transform(x_np)

        # split ts into patches
        if self.patch_len is not None:
            mod = x_np.shape[1] % self.patch_len
            if mod != 0:    # if time series length is not divisible by patch_len,
                if pad:
                    # pad with zeros
                    x_np = np.pad(x_np, ((0, 0), (0, patch_len-mod)), mode='constant', constant_values=0)
                else:
                    # remove excess values
                    x_np = x_np[:, :-mod]

            # only self.x is split into patches
            x_np = x_np.reshape((-1, self.patch_len))

        self.x = torch.from_numpy(x_np).unsqueeze(1).float()
        self.y = torch.from_numpy(arr[:, 0])

    def __len__(self):
        return len(self.x)

    def __getitem__(self, item):
        if self.patch_len is not None:
            return self.x[item], 0
        else:
            return self.x[item], self.y[item]
