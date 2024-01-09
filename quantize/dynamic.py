# Dynamic quantization  动态量化
import onnx
from onnxruntime.quantization import quantize_dynamic, QuantType

model_fp32 = '../weights/yolov5m-ShuffleNetV2-lite-GSConv-SlimNeck.onnx'
model_quant = '../weights/yolov5m-ShuffleNetV2-lite-GSConv-SlimNeck.quant.onnx'
quantized_model = quantize_dynamic(model_fp32, model_quant, weight_type=QuantType.QUInt8)

