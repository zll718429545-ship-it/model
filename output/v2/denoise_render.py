"""Optional Intel Open Image Denoise pass for Blender builds without built-in OIDN.
Usage: python denoise_render.py [input.png] [output.png]
Requires: pip install oidn==0.2.1 numpy pillow
"""
from pathlib import Path
import sys
import ctypes
import numpy as np
from PIL import Image
import oidn

root=Path(__file__).resolve().parent
source=Path(sys.argv[1]) if len(sys.argv)>1 else root/'study_render.png'
target=Path(sys.argv[2]) if len(sys.argv)>2 else root/'study_render_denoised.png'
color=np.ascontiguousarray(np.asarray(Image.open(source).convert('RGB'),dtype=np.float32)/255.0)
height,width=color.shape[:2]
output=np.empty_like(color)
device=oidn.NewDevice();oidn.CommitDevice(device)
filter_handle=oidn.NewFilter(device,'RT')
oidn.SetSharedFilterImage(filter_handle,'color',color,oidn.FORMAT_FLOAT3,width,height)
oidn.SetSharedFilterImage(filter_handle,'output',output,oidn.FORMAT_FLOAT3,width,height)
# The rendered PNG has already passed Blender's display transform.
# Convert from display sRGB into linear values for OIDN's default LDR mode.
color[:]=np.where(color<=.04045,color/12.92,((color+.055)/1.055)**2.4)
oidn.CommitFilter(filter_handle);oidn.ExecuteFilter(filter_handle)
error=oidn.GetDeviceError(device)
if error:raise RuntimeError(f'OIDN filter failed: {error}')
output=np.maximum(output,0)
output=np.where(output<=.0031308,output*12.92,1.055*output**(1/2.4)-.055)
Image.fromarray(np.uint8(np.clip(output*255+.5,0,255))).save(target)
oidn.ReleaseFilter(filter_handle);oidn.ReleaseDevice(device)
print(f'Denoised {width} x {height}: {target}')
