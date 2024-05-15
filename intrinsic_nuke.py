import torch
from altered_midas.midas_net import MidasNet
from altered_midas.midas_net_custom import MidasNet_small

weights = './final_weights.pt'


class combine(torch.nn.Module):
    def __init__(self):
        super().__init__()
        device = 'cpu'

        combined_dict = torch.load(weights, map_location=torch.device(device))
        iid_state_dict = combined_dict['iid_state_dict']

        self.real_model = MidasNet_small(
            exportable=False, input_channels=5, output_channels=1)
        self.real_model.load_state_dict(iid_state_dict)
        self.real_model = self.real_model.to(device)

    def forward(self, combined):
        return self.real_model(combined)


class ordinal(torch.nn.Module):
    def __init__(self):
        super().__init__()
        device = 'cpu'

        combined_dict = torch.load(weights, map_location=torch.device(device))
        ord_state_dict = combined_dict['ord_state_dict']

        self.ord_model = MidasNet()
        self.ord_model.load_state_dict(ord_state_dict)
        self.ord_model = self.ord_model.to(device)

    def forward(self, img):
        return self.ord_model(img)


combine_script = torch.jit.script(combine().eval())
combine_script.save('./nuke/Cattery/Intrinsic/COMBINE.pt')

ordinal_script = torch.jit.script(ordinal().eval())
ordinal_script.save('./nuke/Cattery/Intrinsic/ORDINAL.pt')
