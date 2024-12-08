# db文件夹

## 目录结构

db/  
├── chinese-poetry-master/  
├── processed/  
└── raw_poems/  

## 内容

`db` 文件夹包含与诗歌数据相关的所有文件和目录。其结构如下：

- `chinese-poetry-master/`：包含原始的中文诗词数据。
- `processed/`：包含序列化处理后的诗词数据。
- `raw_poems/`：包含未处理的原始诗词数据。

每个子文件夹的具体内容如下：

### chinese-poetry-master/

存放从外部来源 [chinese-poetry](https://github.com/chinese-poetry/chinese-poetry) 获取的原始中文诗歌数据。

### processed/

存放经过处理和清洗后的诗歌数据，采用`Trie树`结构，并使用`pagerank`添加权重，便于搜索。

### raw_poems/

存放未处理的原始诗歌数据，直接从数据源获取，尚未进行任何处理。

## 说明

由于数据库文件较大，无法直接上传至github，如有需要，联系作者获取。
