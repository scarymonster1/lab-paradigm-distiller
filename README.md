# Lab Paradigm Distiller

`lab-paradigm-distiller` 是一个 Codex/ChatGPT Skill，用来把某个课题组或研究团队的一条具体研究线，蒸馏成一个可复用的“科研范式 Skill”。

它关注的不是“这些论文分别做了什么结论”，而是更深一层的东西：

> 这个研究线是如何选择问题、构造方法、设计证据、组织论文叙事，并产生新课题的。

输入代表性论文、PDF 文件夹、DOI/arXiv/OpenReview 链接、项目页、代码仓库或课题组官方材料后，它会帮助你生成一个新的 Skill。这个新 Skill 可以作为“科研顾问”，用于：

- 判断什么问题像这个课题组会做
- 设计类似风格的方法与实验
- 检查证据链是否符合该研究线标准
- 学习论文 framing、贡献表述和图表叙事
- 生成符合该课题组科研范式的小 proposal

## 产物是什么

这个 Skill 会为一条具体研究线生成一个自包含目录：

```text
[lab-line]-research-paradigm/
├── SKILL.md
├── sources/
│   ├── papers/
│   └── texts/
├── references/
│   ├── corpus-metadata.json
│   ├── paper-cards/
│   ├── research/
│   │   ├── 01-problem-selection.md
│   │   ├── 02-core-assumptions.md
│   │   ├── 03-method-stack.md
│   │   ├── 04-evidence-standard.md
│   │   ├── 05-paper-framing.md
│   │   └── 06-evolution-timeline.md
│   └── validation/
│       ├── holdout-backtest.md
│       ├── new-proposal-test.md
│       └── revision-log.md
```

其中最重要的是生成后的 `SKILL.md`。它是最终可安装、可调用的课题组科研范式 Skill。

`references/` 目录保存证据链、论文卡片、六维分析、验证记录和修订日志，方便你人工检查这个 Skill 是否真的总结得靠谱。

## 安装方式

先克隆这个仓库：

```bash
git clone https://github.com/scarymonster1/lab-paradigm-distiller.git
```

然后把整个文件夹复制到 Codex 的 skills 目录。

Windows：

```powershell
Copy-Item -Recurse -Force ".\lab-paradigm-distiller" "$env:USERPROFILE\.codex\skills\lab-paradigm-distiller"
```

macOS / Linux：

```bash
mkdir -p ~/.codex/skills
cp -R ./lab-paradigm-distiller ~/.codex/skills/lab-paradigm-distiller
```

安装后，重新打开一个 Codex/ChatGPT 会话，然后让它使用 `lab-paradigm-distiller`。

## 使用示例

你可以给它一个论文文件夹：

```text
使用 lab-paradigm-distiller。

输入文件夹：
D:\research\papers\my-lab-line

目标研究线：
基于集成声子平台的拓扑声学/弹性波器件

请把这条研究线蒸馏成一个可复用的科研范式 Skill。
```

也可以只从一篇种子论文开始：

```text
使用 lab-paradigm-distiller。

种子论文：
https://arxiv.org/abs/xxxx.xxxxx

请推断最窄合理研究线，扩展官方来源语料，并生成一个科研范式 Skill。
```

如果你只给一篇论文，它会先推断研究线边界，再谨慎扩展同研究线论文。默认不把整个课题组的所有方向混在一起。

## 六维蒸馏框架

蒸馏过程围绕六个维度展开：

| 维度 | 提取内容 |
| --- | --- |
| 问题选择 | 这个研究线反复选择什么问题，什么问题会被回避 |
| 核心假设 | 这个研究线相信哪些科学机制、建模前提和因果变量 |
| 方法栈 | 常用理论、平台、算法、仿真、测量、代码和实验流程 |
| 证据标准 | 什么结果算有说服力，包括基线、对照、指标和失败分析 |
| 论文叙事 | 如何组织引言、命名贡献、安排图表、表达 novelty 和 limitations |
| 范式演化 | 研究线如何随时间推进、转向、扩展或收缩 |

最终目标是提炼出这个课题组的“科研语法”：问题、方法、证据和叙事之间的稳定连接方式。

## 语料来源原则

优先使用：

- 用户提供的论文
- 官方全文、补充材料和附录
- 作者发布的数据集和代码
- 官方项目页、课题组主页
- 作者维护的仓库、报告、slides 和 talk

不使用：

- 社交媒体闲聊
- 评论区
- 排名帖
- 不可核验的博客总结
- 知乎、公众号等二手点评材料

这个 Skill 应该把结论建立在论文和官方材料上。对于证据不足的部分，要明确标注低置信度，而不是强行总结。

## 验证标准

一个生成出来的课题组范式 Skill 至少要通过三类检查：

1. **跨论文复现**：总结出的模式不能只来自一篇论文，而要能在多篇论文中反复出现。
2. **有生成力**：它应该能生成新的、看起来像该研究线会做的小 proposal。
3. **相对领域基线有区分度**：输出不能只是普通领域综述，而要能体现这个课题组/研究线的独特研究口味。

生成目录中会包含：

- `holdout-backtest.md`：留出 1-2 篇论文不用来蒸馏，反过来测试 Skill 是否能预测它们的问题选择、方法和证据逻辑。
- `new-proposal-test.md`：生成 3 个小 proposal，检查是否真的像该研究线会做的课题。
- `revision-log.md`：记录失败检查、边界调整和最终保留的 caveat。

## 辅助脚本

合并论文卡片分析：

```bash
python scripts/merge_paper_analysis.py <generated-skill-dir>
```

检查生成 Skill 的质量：

```bash
python scripts/quality_check.py <generated-skill-dir>/SKILL.md
```

这些脚本故意保持轻量。PDF 解析、联网扩展、正文抽取和资料阅读，主要交给当前 Codex/ChatGPT 环境和可用工具完成。

## 仓库结构

```text
.
├── SKILL.md
├── agents/
│   └── openai.yaml
├── examples/
│   └── template-lab-line-paradigm/
├── references/
│   ├── extraction-framework.md
│   └── lab-skill-template.md
└── scripts/
    ├── merge_paper_analysis.py
    └── quality_check.py
```

`examples/template-lab-line-paradigm/` 是一个空模板结构，不包含真实课题组语料。

## 隐私与版权说明

生成出来的具体课题组 Skill 可能包含：

- 私人笔记
- 未公开研究想法
- 有版权的论文 PDF
- 课题组内部资料

请不要直接公开这些生成后的 `sources/` 目录，除非你确认自己有权分享。

这个仓库公开的是“通用蒸馏流程”，不是任何具体课题组的私有语料。

## 当前状态

这是一个早期可用版本。它最适合的输入是：

- 一条边界清楚的具体研究线
- 5-10 篇代表性论文
- 1-2 篇留出论文用于验证
- 尽量多的官方材料，而不是二手评论

如果语料不足、研究线混杂或论文跨度太大，生成的 Skill 应该诚实标注低置信度，而不是假装已经理解整个课题组。
