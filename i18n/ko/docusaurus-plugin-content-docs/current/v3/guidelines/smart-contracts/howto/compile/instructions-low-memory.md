# 낮은 메모리의 기기에서 TON 컴파일하기

:::caution
이 섹션은 TON과 낮은 수준에서 상호작용하기 위한 지침과 매뉴얼을 설명합니다.
:::

낮은 메모리(1GB 미만)를 가진 컴퓨터에서 TON을 컴파일하기 위한 스왑 파티션 생성.

## 전제 조건

Linux 시스템에서 C++ 컴파일 중에 다음과 같은 오류가 발생하여 컴파일이 중단됩니다:

```
C++: fatal error: Killed signal terminated program cc1plus compilation terminated.
```

## 해결방법

이는 메모리 부족으로 인해 발생하며 스왑 파티션을 생성하여 해결됩니다.

```bash
# Create the partition path
sudo mkdir -p /var/cache/swap/
# Set the size of the partition
# bs=64M is the block size, count=64 is the number of blocks, so the swap space size is bs*count=4096MB=4GB
sudo dd if=/dev/zero of=/var/cache/swap/swap0 bs=64M count=64
# Set permissions for this directory
sudo chmod 0600 /var/cache/swap/swap0
# Create the SWAP file
sudo mkswap /var/cache/swap/swap0
# Activate the SWAP file
sudo swapon /var/cache/swap/swap0
# Check if SWAP information is correct
sudo swapon -s
```

스왑 파티션 삭제 명령:

```bash
sudo swapoff /var/cache/swap/swap0
sudo rm /var/cache/swap/swap0
```

여유 공간 명령:

```bash
sudo swapoff -a
#Detailed usage: swapoff --help
#View current memory usage: --swapoff: free -m
```