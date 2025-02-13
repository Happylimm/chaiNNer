from .. import expression
from .base_output import BaseOutput, OutputKind

from ...utils.torch_types import PyTorchModel


class ModelOutput(BaseOutput):
    def __init__(
        self,
        model_type: expression.ExpressionJson = "PyTorchModel",
        label: str = "Model",
        kind: OutputKind = "generic",
        should_broadcast=False,
    ):
        super().__init__(model_type, label, kind=kind)
        self.should_broadcast = should_broadcast

    def get_broadcast_data(self, value: PyTorchModel):
        if not self.should_broadcast:
            return None

        if "SRVGG" in value.model_arch:  # type: ignore
            size = [f"{value.num_feat}nf", f"{value.num_conv}nc"]
        elif "SwinIR" in value.model_arch:  # type: ignore
            head_length = len(value.depths)  # type: ignore
            if head_length <= 4:
                size_tag = "small"
            elif head_length < 9:
                size_tag = "medium"
            else:
                size_tag = "large"
            size = [
                size_tag,
                f"s{value.img_size}w{value.window_size}",
                f"{value.num_feat}nf",
            ]
        elif "GFPGAN" in value.model_arch or "RestoreFormer" in value.model_arch:
            size = []
        else:
            size = [
                f"{value.num_filters}nf",
                f"{value.num_blocks}nb",
            ]

        return {
            "arch": value.model_arch,
            "inNc": value.in_nc,
            "outNc": value.out_nc,
            "size": size,
            "scale": value.scale,
            "subType": value.sub_type,
        }


def TorchScriptOutput():
    """Output a JIT traced model"""
    return BaseOutput("PyTorchScript", "Traced Model")
