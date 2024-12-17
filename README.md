# 诗词搜索

## 人工智能导论小组作业

## 目标任务

**问题描述**：在[`诗词闯关`](https://www.arealme.com/9-grid-chinese-poem-quiz/cn/)中，你会遇到一个 4×3 或 3×3 的每一格都填有汉字的表格，通过筛选并排列这个表格中的汉字，你可以得到一句准确的七言/五言的诗词。

**输入**：一个包含 12 或 9 个汉字的列表

**预期输出**：一句包含在古诗词库内的诗词（七言/五言）

## 算法设计

### 数据库构建

数据来源于 [`@chinese-poetry`](https://github.com/chinese-poetry/chinese-poetry)，在此基础上进行了数据的合并、分割、去重等操作，同时改写数据结构为有权 Trie 树，权重采用 PageRank 算法计算。

为缩短加载时间，将 `Trie 树`按首字分割，并存储为 ` msgpack `文件，搜索时按需加载。

### 搜索

使用` PageRank `评分从最优组合开始检索` Trie 树 `直到找到解。

## 代码实现

`src` 文件夹中包含所有代码，其中：

- [`build-database.py`](src/build-database.py)：用于读取原始数据并整理为完整的诗句数据库
- [`deduplication.py`](src/deduplication.py) 和 [`split-database.py`](src/split-database.py)：分别用于进行降重和分割诗句操作
- [`new-database.py`](src/new-database.py)：用于生成 `PageRank`评分并构建字序表
- [trie-database.py](src/trie-database.py)：序列化存储`trie树`结构的诗词库
- [`PageRank.py`](src/PageRank.py)：存放了` PageRank `算法代码
- [`trie.py`](src/trie.py)：为`Trie 树`的数据结构
- [`utils.py`](src/utils.py)：用于记录日志
- [`trie_retrival.py`](src/trie_retrieval.py)：用于搜索
- [fetch_char.py](src/fetch_char.py): 从网页获取输入
- [main.py](src/main.py): 主程序

此外，相关配置可通过 [`config.json`](config/config.json) 进行调整。

## 任务进度跟踪表

| 任务                     | 当前状态   | 备注        |
|--------------------------|------------|------------|
| 读取原始数据并整理数据库 | ✔️   |              |
| 进行降重操作             | ✔️   |              |
| 分割诗句操作             | ✔️   |              |
| 生成` PageRank `评分       | ✔️   |              |
| 构建字序表               | ✔️   |              |
| 实现` PageRank `算法       | ✔️   |              |
| 构建` Trie 树 `数据结构     | ✔️   |              |
| 记录日志                 | ✔️   |              |
| 实现搜索功能             | ✔️  | 缺少清代数据❗  |
| 编写说明文档       | ⏳  |   |
| 前端输入输出             | ✔️  |           |
| 测试和调试               | ✔️ |          |
| 汇报文档以及PPT制作    | ⏳  |   汇报文档写作参考历次Project   |

### 状态符号说明

- ✔️ 已完成
- ⏳ 正在进行
- 🟠 未开始
- ❌ 放弃

## 致谢

- 感谢刘佳璐老师一学期以来的辛勤教学与耐心解答，感谢对于本课程小组作业的建议与指导；
- 本项目实施过程中，许恩彰同学提供了课题与初步设想，本人负责主要算法的构思与编程实现，杨仕言同学编写了本项目的网页输入输出部分，张怡安同学负责文档的编写、部分程序的debug与最终汇报的准备工作，胡洪凯同学为最终汇报提供帮助；
- 感谢[@chinese-poetry](https://github.com/chinese-poetry)的开源诗词数据库；
