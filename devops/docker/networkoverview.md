# Docker Network Overview

도커의 컨테이너의 가장 큰 강점 중 하나는 `(컨테이너)-(컨테이너)` 혹은 `(컨테이너)-(non 컨테이너)` 사이의 연결을 제공한다는 점이다. 심지어, 호스트 OS가 Linux, Windows 인지 여부와 상관없이 이러한 기능을 제공한다. 

## Network Drivers
다음은 도커에서 사용되는 대표적인 네트워크 드라이버를 나열한 것이다. 

- `bridge`: 브릿지는 도커의 기본 네트워크 드라이버이다. 브릿지 네트워크 드라이버는 일반적으로 링크 계층에서 사용되는 (소프트웨어) 브릿지를 사용하여 패킷을 전송한다.

- `host`: 호스트 네트워크 드라이버는 컨테이너의 네트워크 격리를 제거하고 standalone 컨테이너를 호스트 네트워크 네임스페이스와 직접적으로 연결한다.

- `overlay`: 오버레이 네트워크는 복수 개의 도커 데몬(`Docker daemon`)을 연결하여 서로 간의 통신을 가능하게 한다. 

- `macvlan`: Macvlan 네트워크 드라이버를 사용하면 컨테이너에 MAC 주소를 부여하여, 마치 물리적 장치가 존재하는 것처럼 동작하는 것이 가능하다. `macvlan` 드라이버를 사용하면 물리적 네트워크에 직접적으로 연결되는 레거시 어플리케이션에 네트워크 기능을 제공할 수 있다.

- `none`: 컨테이너 네트워크를 모두 제거한다. 대개의 경우, `none` 옵션은 커스텀 네트워크 드라이버와 함께 사용된다.

이번 포스트에서는 도커에서 기본 값으로 사용되는 브릿지 네트워크에 대해 다루는 것으로 하였다.

&nbsp;

## Bridge Network

일반적으로 네트워크에서 브릿지 네트워크는 링크 계층에서 트래픽을 효율적으로 전송하기 위해 세그멘트를 분리하는 물리적/논리적(software) 장치를 의미한다. 

도커에서 브리지는 소프트웨어적 브릿지를 의미하며, 컨테이너들이 브릿지를 통해 서로 통신할 수 있도록 하는 기능을 제공한다. 따라서, 컨테이너들은 브릿지를 단위로 서로 독립된 네트워크 환경을 갖게된다.

도커에는 기본 값으로 브릿지 네트워크(`docker0`)를 사용한다. 특별한 설정이 없는 경우, 모든 컨테이너는 도커에서 제공하는 기본 브릿지 네트워크와 연결되어 서로 통신이 가능하다. 추가적으로, 사용자가 직접 브릿지 네트워크를 생성하여 컨테이너들의 네트워크 환경을 분리할 수 있다.

>Tip: 단, 브리지 네트워크는 동일한 도커 데몬(`Docker daemon`) 호스트 환경에만 적용되므로, 서로 다른 호스트 혹은 OS에서 동작하는 컨테이너를 연결하기 위해서는 `overlay` 네트워크를 사용할 수 있다.

&nbsp;

## Differences between user-defined bridges and the default bridge

- 자동으로 DNS resolution을 제공한다.
 
  도커의 기본 브릿지 네트워크는 DNS 기능을 제공하지 않으므로, IP 주소를 통한 접근만 가능하다. 반면, 사용자 정의 브릿지는 컨테이너들이 간단하게 DNS를 사용하여 통신할 수 있다.

- 더 좋은 네트워크 격리 환경을 제공한다.

  도커의 기본 브릿지 네트워크를 사용하면 모든 컨테이너가 하나의 브릿지에 연결된다. 이는 개별 프로세스의 네트워크 네임스페이스를 격리하는 컨테이너의 관점에서 좋지 않을 수 있을 뿐만 아니라 보안적으로도 위험할 수 있다. 그러므로, 사용자는 사용자 정의 브릿지를 통해 네트워크 격리 수준을 강화할 수 있다.

- 컨테이너의 네트워크를 보다 유연하게 관리할 수 있다.
  
  브리지 네트워크를 사용하면 이미 실행중인 컨테이너의 네트워크 환경을 유연하게 관리할 수 있다. 만약, 기본 브릿지를 사용하면 컨테이너가 실행되는 네트워크 환경을 바꾸고 싶을 때마다 컨테이너를 멈추고 네트워크 옵션을 수정해야한다.

- 브릿지마다 고유한 환경 설정 값을 갖도록 할 수 있다.

  사용자는 복수 개의 브릿지 네트워크를 생성할 수 있으며, 각 네트워크에 다른 설정 값을 부여할 수 있다. 기본 도커 브릿지를 사용할 경우, 모든 컨테이너가 네트워크 설정(ex, `iptables`)을 공유한다.

- 연결(linked)된 컨테이너들이 서로 다른 환경변수를 갖게할 수 있다.

  도커의 기본 브릿지를 사용하면 서로 연결(linked)된 컨테이너들이 모두 같은 환경변수를 갖는다. 반면, 사용자 정의 브릿지 네트워크에서는 연결된 컨테이너들이 환경변수를 공유하지 않는다. link 방식이 불가능하지만, 사용자 정의 브릿지에서도 환경변수를 공유하는 다양한 방법이 존재한다.

  - 다수의 컨테이너가 환경변수가 저장된 파일이나 폴더를 볼륨의 형태로 마운트한다.
  - `docker-compose`를 사용하여, 컨테이너들이 환경변수를 공유하도록 설정할 수 있다.
  - `standalone` 컨테이너 대신, `swarm service`를 사용하여 시크릿(`secret`)과 설정(`config`) 등을 공유할 수 있다.

&nbsp;

### References

[도커 공식문서: Network Overview](https://docs.docker.com/network/)
[도커 공식문서: Network Overview](https://docs.docker.com/network/bridge)
[도커 공식문서: Docker and iptables](https://docs.docker.com/network/iptables/)