# TON采矿指南

:::warning 已弃用
这种资料可能已经过时，不再有用。 请随时省略它。
:::

## <a id="introduction"></a>介绍

本文档介绍了使用 PoW giver 开采Tonco币的过程。 请访问 [ton.org/mining](https://ton.org/mining) 获取最新的TON采矿状态。

## <a id="quick-start"></a>快速启动

立即开始开采：

1. 获取一台适合采矿的电脑](#硬件)。
2. 安装 [Ubuntu](https://ubuntu.com) 20.04 桌面或服务器分布。
3. 在 `lite` 模式中安装 [mytonctrl](https://github.com/igroman787/mytonctrl#installation-ubuntu)。
4. 在`mytonctrl`中运行`emi`命令来检查你的硬件和[预期的采矿收入](#faq-emi)。
5. 如果你还没有一个，使用一个 [wallets](https://www.ton.org/wallets)创建 \`钱包地址'。
6. 在`mytonctrl`中执行 `set minerAddr `...`，将你的钱包地址` 定义为采矿目标。
7. 从 [ton.org/mining](https://ton.org/mining) 中选择一个给定合同，并通过在 `mytonctrl` 中执行 \`powAddr "..." 将你的矿工设置为矿工。
8. 开始挖掘时，在 `mytonctrl` 中执行 `mon`
9. 在您的电脑上检查 CPU 负载；名为 `pow-miner` 的进程应该使用您的大部分CPU。
10. 等待运气；第4步的输出应该告诉你你你你有多少机会去挖一个块。

## <a id="basics"></a>Basics

Tonco币由所谓的`PoW Givers`分发，这是与分配给他们的一定数量的TON的智能合同。 目前，TON网络上有10个活跃的PoW givers。 提供者在每个方块100TON里赠送硬币。 要接收此块， 您的计算机需要解决一个由提供者发出的复杂的数学挑战，并尽快完成这项工作； 您将与其他矿工竞争100TON的奖励。 如果有人设法解决你面前的问题，你的机器完成的所有工作都是徒劳的，新的回合/竞赛开始了。

重要的是要认识到，采矿的利润并不像你的机器在工作中那样“滴入”。 为了成功地解决给予的挑战，她们分成100个TON。 这意味着如果您的机器在24小时内有10%的机会计算方块(见[快速启动](#quickStart)第4步)，那么您可能需要等待 ~10 天才能获得100个TON奖励。

采矿过程基本上是通过“mytonctrl”自动化的。 关于采矿过程的详细资料可在[PoW givers](https://www.ton.org/#/howto/pow-givers)文件中查找。

## <a id="advanced"></a>高级版

如果你真的想要采矿并想要操作一个以上的机器/采矿场， 然后您真的需要学习TON和采矿如何工作； 请查看 [HOWTO](https://ton)。 rg/#/howto/) 深入信息部分。 以下是一些一般性建议：

- **DO** 在一个单独的机器上运行您自己的节点/lite 服务器； 这将确保您的采矿农场不依赖外部简单服务器，可以停下来或不及时处理您的查询。
- **DO NOT** 用`get_pow_params`查询轰炸公共lite服务器， 如果你有自定义的脚本，在高频率调查givers状态，你**必须** 使用你自己的简单服务器。 违反此规则的客户端有可能在公共服务器上将他们的 IP 列入黑名单。
- **DO** 试图了解如何[开采过程](https://www.ton)。 rg/#/howto/pow-givers)工作; 大多数较大的矿工使用自己的脚本，在有多个采矿机的环境中比`mytonctrl`提供许多优势。

## <a id="hardware"></a>Miner hardware

TON采矿的网络哈希率很高；矿工若想成功，就需要高性能的机器。 在标准家用计算机和笔记本上采矿是徒劳无益的，我们建议不要这种企图。

#### CPU

支持 [Intel SHA 扩展](https://en.wikipedia.org/wiki/Intel_SHA_extensions) 的 CPU 是一个 **必须**。 大多数矿工使用AMD EPYC 或 Threadripper 基于机器，至少有32个核心和64个线程。

#### GPU

是的！ 您可以使用 GPU 开采TON。 有一个能够同时使用Nvidia和AMD GPU的PoW矿工版本； 你可以在[POW矿工GPU](https://github)中找到如何使用它的代码和说明。 om/tontechio/pow-miner-gpu/blob/main/crypto/util/pow-miner-howto.md) 存储库。

就现在而言，要使用这种方法，就需要技术上的手法，但我们正在努力寻找一种更方便用户的解决办法。

#### 内存

几乎整个采矿过程都发生在CPU的L2缓存中。 这意味着内存速度和大小在采矿性能中不起作用。 在一个内存通道上有一个单一的DIMM的双重AMD EPYC系统将与占用所有通道的16个DIMM一样快速挖掘。

请注意，这适用于纯采矿过程**仅**，如果你的机器也运行全节点或其他过程，那么事情就会改变！ 但这超出了本指南的范围。

#### 存储

纯矿工在简单模式下运行时使用最小空间且不存储任何数据。

#### 网络

普通矿工需要能够打开连接到互联网。

#### FPGA / ASIC

查看[我可以使用 FPGA / ASICs?](#faq-hw-asic)

### <a id="hardware-cloud"></a>云机

许多人使用 AWS 或 Google 计算云机开采。 如上文所概述，真正重要的是CPU。 因此，我们建议AWS [c5a.24xlarge](https://aws.amazon.com/ec2/instance-types/c5/) 或 Google [n2d-highcpu-224](https://cloud.google.com/compute/vm-instance-pricing) 实例。

### <a id="hardware-estimates"></a>Income estimates

The formula for calculating the income is quite simple: `($total_bleed / $total_hashrate) * $your_hashrate`. 这将给您**当前** 估计数。 你可以在 [ton.org/mining](https://ton.org/mining) 上找到变量，或者使用 `mytonctrl` 中的估计矿产收入计算器 (`emi` 命令)。 下面是2021年8月7日使用 i5-11400F CPU 做出的样本输出：

```
采矿收入估计值
-------------------------------------------------------------------------------
网络总收入：171635 9 TON
24小时平均网络哈希率：8052761000 HPS
您的机器哈希率：68465900 HPS
Est。 24小时开采区块的几率：15%
Est. 每月收入：437.7 TON
```

**重要**：请注意所提供的信息基于执行时的网络哈希率\*。 随着时间的推移，您的实际收入将取决于许多因素，如网络哈希率、选定的巨人和运气的很大一部分。

## <a id="faq"></a>FAQ

### <a id="faq-general"></a>General

#### <a id="faq-general-posorpow"></a>Is TON PoS or PoW network?

TON Blockchain 使用利益关系证明的共识。 不需要挖矿来生成新块。

#### <a id="faq-general-pow"></a>So how come TON is Proof-of-Work?

原因在于，50亿吨硬币的最初发行已转入临时工作证明智能合同。
采矿用来从这个智能合约中获取Toncoins

#### <a id="faq-general-supply"></a>还有多少硬币可供开采？

最实际的信息见[ton.org/mining](https://ton.org/mining)，见`bleed`graphs。 PoW Giver合约有其限度，一旦用户开采所有可用的Toncoins，就会干枯。

#### <a id="faq-general-mined"></a>已经开采多少硬币？

截至2021年8月，约有4.9BN Toncoins 被埋设了地雷。

#### <a id="faq-general-whomined"></a>谁开采了这些硬币？

金币已开采到70 000多个钱包，这些钱包的所有者不详。

#### <a id="faq-general-elite"></a>开始采矿是否困难？

根本不是。 你需要的只是[足够的硬件](#硬件)，并按照[快速启动](#quickStart)部分概述的步骤进行。

#### <a id="faq-general-pissed"></a>还有其他方法可以开采吗？

是的，有第三方应用程序 — [TON Miner Bo](https://t.me/TonMinerBot)。

#### <a id="faq-general-stats"></a>我在哪里可以看到采矿统计？

[ton.org/mining](https://ton.org/mining)

#### <a id="faq-general-howmany"></a>How many miners are out there?

我们不能这样说。 我们知道的只是网络上所有矿工的总哈希率。 然而，[ton.org/mining](https://ton.org/mining)的图表试图估计提供近距离哈希率所需的陶瓷型机数。

#### <a id="faq-general-noincome"></a>我需要Tonco币来开始采矿吗？

不，你不这样做。 任何人都可以在不拥有单个Tonco的情况下开始采矿。

#### <a id="faq-mining-noincome"></a>I mine for hours, why my wallet total does not increase, not even by 1 TON?

TON是在100个方块中开采的，您要么猜测一个方块，要么接收100个TON，要么没有收到任何东西。 请查看 [basics](#basics).

#### <a id="faq-mining-noblocks"></a>I've been mining for days and I see no results, why?

您是否检查您当前的[收入估计数](#硬件估计数)？ 如果字段 \`Est. 24小时开采方块的几率不到100%，然后您需要耐心等待。 另外，请注意，有50%的机会在24小时内挖一个方块并不自动意味着您将在2天内挖掘一个方块； 50%分别适用于每天。

#### <a id="faq-mining-pools"></a>是否有采矿池？

没有采矿池，每个人都有采矿。

#### <a id="faq-mining-giver"></a>我应该给哪个赠与者？

给予哪一个人并不重要。 难度往往在每个巨型上浮动，因此目前最容易的 [ton.org/mining](https://ton.org/mining)上的赠与者可能在一小时内变得最复杂。 相反的方向也是如此。

### <a id="faq-hw"></a>硬件

#### <a id="faq-hw-machine"></a>一台更快的机器是否会赢得胜利？

不，所有矿工都要走不同的道路来寻找解决办法。 一个更快的机器成功的概率更高，但它不能保证胜利！

#### <a id="faq-hw-machine"></a>我的机器会产生多少收入？

请见[收入估计数](#硬件估计)。

#### <a id="faq-hw-asic"></a>Can I use my BTC/ETH rig to mine TON?

不，TON使用单一的 SHA256 散列法，不同于BTC、ETH 等方法。 ASICS 或 FPGA wbich 是为了挖掘其他加密点不会有帮助。

#### <a id="faq-hw-svsm"></a>什么是更好的，一个单一的快车或几个慢车？

这是有争议的。 见：矿工软件为系统上的每个核心启动线程，每个核心获取自己的一组密钥。 如果你有一个能够运行64条线程的机器和4个能够运行16条线程的机器， 然后假定每个线程的速度是一样的，它们将是同样成功的。

然而，在实际世界中，核心计数较低的 CPU 通常更高，因此你可能会使用多台机器获得更好的成功。

#### <a id="faq-hw-mc"></a>如果我运行许多机器，他们会合作吗？

不，他们不会这样做。 每个机器都有自己的地雷，但溶液寻找过程是随机的：没有机器， 甚至连单个线程都没有一个线程(见上文)也不会走同样的道路。 因此，如果没有直接合作，他们的散列就会对你有利。

#### <a id="faq-hw-CPU"></a>我能使用ARM CPU开采吗？

根据消费物价指数，AWS Graviton2实例确实是非常能干的矿工，能够与基于AMD的EPYC实例保持价格/性能比率。

### <a id="faq-software"></a>软件

#### <a id="faq-software-os"></a>我能使用Windows/xBSD/一些其他操作系统来开采吗？

当然，[TON source code](https://github.com/ton-blockchain/ton)已知是建立在Windows、 xBSD 和其他操作系统上。 然而，没有舒服的自动安装，如在 Linux 下使用 `mytonctrl`，您需要手动安装软件并创建您自己的脚本。 对于FreeBSD，有一个允许快速安装的 [port](https://github.com/sonofmom/freebsd_ton_port) 源代码。

#### <a id="faq-software-node1"></a>如果我在全节点模式下运行mytonctrl，我的挖掘速度会更快吗？

计算过程本身将不会更快，但你将获得一些稳定性和稳定性。 最重要的是，如果您运行您自己的全节点/单点服务器。

#### <a id="faq-software-node2"></a>我需要什么？ / 我如何操作一个完整的节点？

这超出了本指南的范围，请查看[完整节点如何](https://ton.org/#/howto/fullnode)和/或[mytonctrl 指令](https://github.com/igroman787/mytonctrl)。

#### <a id="faq-software-build"></a>你能帮助我在我的操作系统上构建软件吗？

这超出了本指南的范围，请查阅[完整节点如何](https://ton.org/#/howto/fullnode)以及[Mytonctrl 安装脚本](https://github.com/igroman787/mytonctrl/blob/master/scripts/toninstaller.sh#L44)以了解依赖关系和过程。
