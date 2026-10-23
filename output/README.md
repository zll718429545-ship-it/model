# 暖木书房场景

- `warm_study.blend`：Blender 4.3.2 场景，模型、程序化材质、灯光和相机均可编辑，无外部贴图依赖。
- `study_render.png`：Cycles 渲染图。
- `create_scene.py`：完整场景生成脚本。

重新生成：
```bash
blender -b -t 6 --python /workspace/model/output/create_scene.py
```

基于参考图进行程序化重建；书籍封面、挂画采用简化原创图形。尺寸单位为米。
