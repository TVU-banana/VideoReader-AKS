# 项目架构（Project Architecture）

VideoReader-AKS/
├── core/
│   ├── aks_sampler.py      # 自适应采样算法（核心逻辑）
│   └── qwen_inference.py   # 模型推理与 API 封装，此处调用了强大的Qwen3-VL
├── utils/
│   ├── visualizer.py       # 结果可视化与坐标还原
│   └── logger_config.py    # 统一日志管理
├── output/                 # 存放生成的 JSON 和标注视频
├── data/                   # 测试样本，此处用于存放测试视频
├── main.py                 # 全链路流水线入口
└── requirements.txt        # dashscope, opencv-python, numpy, etc.

# 性能表现 (Benchmark)

通过 AKS 算法处理一段 10 分钟的教学视频（1080P/30FPS）：

- 原始总帧数：18,000 帧

- AKS 提取帧数：约 80-120 帧

- 数据压缩率：> 99.4%

- API 成本优化：相比均匀抽帧（每秒一帧），Token 消耗降低了约 80%

# 快速开始（Quickstart）

1. 克隆仓库：
``
git clone https://github.com/your-username/VideoReader-AKS.git
cd VideoMind-AKS
``

2. 安装依赖：
``
pip install -r requirements.txt
``

3. 配置 API Key：在 main.py 中填入你的阿里云DashScope API Key

4. 运行程序：
``
python main.py
``

# 粗略描述（Overview）

1. 首先在data目录下存放好测试视频，然后运行main.py
2. main.py中自行输入API_Key、VIDEO_PATH、QUERY（QUERY默认内置为"找到视频中正在写字的人"，自行更改）
3. main.py会调用aks_sampler.py进行自适应采样，并调用qwen_inference.py进行模型推理
4. main.py会生成一个output目录，里面存放了生成的JSON文件和标注视频
5. utils目录下存放了日志管理、可视化和坐标还原的代码
6. 模型推理使用的是阿里云的DashScope API，请自行申请
