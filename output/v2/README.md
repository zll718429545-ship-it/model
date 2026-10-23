# 暖木书房 · Blender 第二版

依据参考图重建的可编辑室内场景。相较第一版，调整了取景、木纹方向、桌腿升降结构、台灯轮廓、杯子与书籍细节，并增加地毯织物表面与原创挂画图形。

## 文件

- `warm_study.blend` — Blender 4.3.2 场景，包含模型、程序化材质、灯光和相机。
- `study_render.png` — 960 × 1280 的 Cycles 渲染图。
- `create_scene.py` — 完整可重复生成的脚本，无第三方 Python 依赖。
- `warm_study.zip` — 场景、渲染图、脚本和本说明的打包文件。

## 打开和重新生成

用 Blender 4.3 或更新版本打开 `.blend`。数字小键盘 0 切换相机视图，F12 重新渲染。场景按建筑、书桌、书架、桌面摆件、挂画、灯光与相机分组。

也可在命令行执行：

```sh
blender -b -t 5 --python create_scene.py
```

生成文件保存在脚本所在目录。脚本会覆盖同目录下的 `warm_study.blend` 和 `study_render.png`；修改场景后请先另存。

所有材质在 Blender 内生成，无需下载外部贴图。挂画、书籍文字为简化的原创内容。这里的模型是基于照片的视觉重建，尺寸不用于施工或制造。

## 渲染降噪

交付的 PNG 经过 Intel Open Image Denoise 降噪。当前云端 Blender 不含内置 OIDN，因此另附可选的 `denoise_render.py`：

```sh
python -m pip install oidn==0.2.1 numpy pillow
python denoise_render.py study_render.png study_render.png
```

如果你的 Blender 支持内置降噪，可直接在渲染属性中启用 Denoise。生成脚本本身不依赖上述 Python 包。
