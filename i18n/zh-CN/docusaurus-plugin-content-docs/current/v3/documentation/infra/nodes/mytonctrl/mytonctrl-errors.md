import Feedback from '@site/src/components/Feedback';

# MyTonCtrl 错误

## 概述

This document explains the errors that users may encounter with **MyTonCtrl**.

## 常见错误

| 错误                                                                                                    | 可能的解决方案                                                                                                                                       |
| :---------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------- |
| Unknown module name: `name`. Available modes: `modes` | 查看可用模式列表                                                                                                                                      |
| No mode named `name` found in current modes: `current_modes`                          | 检查当前模式列表                                                                                                                                      |
| GetWalletFromFile error: Private key not found                                        | 检查钱包名称路径                                                                                                                                      |
| Cannot get own IP address                                                                             | Verify access to the resources at [ipconfig.me](https://ifconfig.me/ip) and [ipinfo.io](https://ipinfo.io/ip) |

## Liteserver 错误

| 错误                                                            | 可能的解决方案                                           |
| :------------------------------------------------------------ | :------------------------------------------------ |
| Cannot enable liteserver mode while validator mode is enabled | 使用 `disable_mode validator`                       |
| LiteClient error: `error_msg`                 | Check MyTonCtrl parameters for running liteserver |

## 验证器(Validator)错误

| 错误                                                                                                                  | 可能的解决方案                                                                                                                                                                                          |
| :------------------------------------------------------------------------------------------------------------------ | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ValidatorConsole error: Validator console is not settings                                           | 检查 [验证程序文章](/v3/guidelines/nodes/nodes-troubleshooting#validator-console-is-not-setings)                                                                                                         |
| Cannot enable validator mode while liteserver mode is enabled                                                       | 使用 `disable_mode liteserver` 功能                                                                                                                                                                  |
| Validator wallet not found                                                                                          | 检查 [验证器文章](/v3/guidelines/nodes/running-nodes/validator-node#view-the-list-of-wallets)                                                                                                           |
| Validator is not synchronized                                                                                       | 等待更长时间进行同步或检查 [sync troubleshouting](/v3/guidelines/nodes/nodes-troubleshooting#about-no-progress-in-node-synchronization-within-3-hours)。                                                       |
| Stake less than the minimum stake. Minimum stake: `minStake`                        | 使用[`set stake {amount}`](/v3/guidelines/nodes/running-nodes/validator-node#your-validator-is-now-ready)和[check stake parameters](/v3/documentation/network/configs/blockchain-configs#param-17)。 |
| Don't have enough coins. stake: `stake`, account balance: `balance` | Add funds to your account `balance`, ensuring it reaches the required `stake` amount                                                                                                             |

## Nominator pool errors

| 错误                                                                                                                               | 可能的解决方案               |
| :------------------------------------------------------------------------------------------------------------------------------- | :-------------------- |
| CreatePool error: Pool with the same parameters already exists                                                   | 检查 `pools_list` 中的现有池 |
| create_single_pool error: Pool with the same parameters already exists | 检查 `pools_list` 中的现有池 |

## See also

- [节点故障排除](/v3/guidelines/nodes/nodes-troubleshooting)
  <Feedback />

