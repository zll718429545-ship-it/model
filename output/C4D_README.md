# Cinema 4D 导入说明

在 Cinema 4D 中通过“文件 → 打开/合并”选择 `warm_study_c4d.fbx`，完成导入后另存为 `.c4d`。

该文件是 FBX 交换格式，不是原生 C4D 文件。导出后已在 Blender 中重新导入验证：404 个网格、1 台相机、2 盏灯。当前环境没有 Cinema 4D，未验证 C4D 内的实际显示效果。

模型、基础材质、相机和灯光已导出。Blender 程序化木纹、节点材质及渲染设置无法通过 FBX 完整保留，需要在 C4D/Redshift 中重建和调整。请参照 `study_render.png` 调整材质和灯光。
