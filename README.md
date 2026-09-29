# Drosophila Brain Cell AI

这是一个本地可运行的果蝇脑细胞 AI 项目模板，目标是：
- 使用公开的果蝇脑细胞/细胞类型数据与公开模型接口
- 构建本地推理流程
- 让你能在自己的电脑上快速运行和扩展
- 方便在 GitHub 上开源分享

注意：
- 本仓库不附带大型模型权重文件，避免 GitHub 仓库过大。
- 这个项目的设计是“可插拔的开源果蝇脑细胞模型模板”，支持：
  - Hugging Face 上发布的公开模型
  - 本地 `.pt` / `.pkl` / `.onnx` 模型
  - 本地 CSV 表达矩阵 / marker-based demo
- 如果你有更具体的果蝇脑细胞模型权重，可以直接替换 `app.py` 中的模型加载逻辑即可。

项目特点
- 本地可运行，无需服务器
- 支持 CSV 输入的基因表达矩阵
- 支持公开模型接入（Hugging Face / 本地权重）
- 默认带一个可运行 demo，保证安装后可以直接测试
- 适合科研、数据分析、原型开发与二次开发

推荐公开资源
- Fly Cell Atlas（果蝇细胞图谱）
- Drosophila adult brain cell atlas / hemibrain datasets
- Hugging Face 上的公开果蝇/细胞相关模型或 Embedding
- Zenodo / Figshare / 研究机构数据发布页

本仓库中的默认 demo 不依赖特别大规模的闭源数据；它使用细胞 marker 的规则建模来演示整个流程，让你在本地能直接运行。

运行方式

1. 创建虚拟环境

```bash
python -m venv .venv
source .venv/bin/activate
# Windows PowerShell:
# .\.venv\Scripts\Activate.ps1
```

2. 安装依赖

```bash
pip install -r requirements.txt
```

3. 运行程序

最简单方式：

```bash
python app.py --demo
```

如果你有自己的表达矩阵 CSV：

```bash
python app.py --input data/example_cell_expression.csv
```

如果你有公开模型仓库（Hugging Face）：

```bash
python app.py --hf-repo your-org/your-drosophila-model
```

如果你有本地模型权重文件：

```bash
python app.py --model-path /path/to/model.pkl
```

4. 结果示例

程序会输出：
- 细胞类型预测结果
- 每个样本的置信度
- 模型来源说明
- 可视化文件（如果启用）

目录结构

```text
Drosophila-brain-cells-AI/
├── app.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
├── data/
│   └── example_cell_expression.csv
└── src/
    └── drosophila_model.py
```

推荐扩展路径
- 把研究中的单细胞数据换成真实的果蝇脑细胞表达矩阵
- 用模型开发脚本替换 demo 逻辑
- 接入公开 Drosophila 模型的 `from_pretrained()` 方法
- 增加可视化（UMAP / TSNE / 聚类图）
- 将输出保存成 CSV / PNG / JSON

开源说明
- 本仓库以 MIT License 公开。
- 如果你使用了第三方公开果蝇模型或数据，请遵守其原始许可条款。
- 本项目适合在研究和教学场景中进行二次开发与开源分享。

作者说明
- 该项目用于本地测试、模型接入和研究原型展示。
- 你可以将其作为果蝇脑细胞AI项目的起点，在 GitHub 上继续完善。

如果你愿意，我还可以继续帮你做以下任一项：
1. 把这个程序改成真正的“果蝇脑细胞分类器”界面（Web UI）
2. 接入 Hugging Face 开源模型的真实加载逻辑
3. 增加细胞聚类/UMAP 可视化
4. 把它进一步开发成更像科研工具的版本
