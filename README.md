# 카카오 블라인드 테스트 2차 엘리베이터 문제 풀이
실전에서 망하고 지금와서 이걸 푸는게 무슨 의미가 있겠냐만은 그래도 다시 한번 엘리베이터 문제에 도전해봤다.  
<br/>
elevator.exe 는 [카카오 엘리베이터 문제 깃허브](https://github.com/kakao-recruit/2019-blind-2nd-elevator) 에 나온대로 빌드를 해서 만든 바이너리파일이고 solve.py는 나의 풀이이다.
<br/>
<br/>
<br/>
### 첫번째 아이디어

기본적인 아이디어는 다음과 같다 
<br>
<br>
> 각각의 엘리베이터는 자기에게 정해진 구간만 순회하며 내릴사람 있으면 내려주고 태울사람 있으면 태우기를 반복한다  
<br>
<br>
지하철을 떠올리면 이해하기 쉽다.  
<br>
지하철은 내가 가는 방향에 승객이 별로없고 다른쪽에 기다리는 승객이 많다고 해서 그쪽으로 방향을 틀거나 하지 않는다.  
<br>
그저 자기에게 정해진 구간만 순회할뿐이다. 승객은 지하철을 환승해가며 목적지에 도착한다.  <br>

![](https://lh3.googleusercontent.com/8z6qS6ekNBfD7lTU1Fs1cYVhdo6y4JTAJDOaR_qhMR5nxr9jZTHRN8xHU5iW3aerMTJNtwYeT-RuTi2ok03IMk40SIaqso-sK3VJHojtOWiLukJIY2aflvX1N-RjKhBODnq7oLjPlwHSNWL2hfKfBkNqh4OkQ6P-SxWoaUa4l_Ffg6G9q0h01YRb5i5oGU9KLVvMtF-SBUjOtUBBh5Xop5yOYYDs6vMfDBnuqVAu8asv5dL6_bUvmHnyhTRZrk4y5JIvAZcu2tUa6Fo3hZKO9BXgI6roozFH_hG_coDbJ7avHof-NAxnM3YqxtGmj7XkEH7CKq5zg45tIkJxkjHLx_ZXt8pmXC_7x1KtbNNJ3ZXqpiapPzUvcIMCo58mxQPln4YQEIipJc_WyToNZkZY5szXOfX45ODEwNYIYhB4vUNagE3psIVaRAs877epYWNyNnp8HKfv4pNha-mVqQ6l5r9dr2uCFMdfnItqkSS0YBoyHQIP5ERBwIofrpCk8rlyKjsVN2ewZJgxm3NCfANRA-D3JC91zBYHfnnskHapKZGLKe2TFohQ6aAuRYIsdErY0Dy97Q-AbCVwc4tSJ5FnkVQ0eyu0Av6xnpkzRvH1oOrxzWKzYu3ajUYWEu90-yWrbxzwOPnVZUjSKSVmI2MCApJT=w489-h504-no)

이를 그림으로 표현했다.  
구역을 나눈뒤에 각 엘리베이터는 이 구역만 왔다갔다 하면서 승객을 실어 나른다.  
<br>
승객이 빨간 구역에서 탔는데 내려야 하는 층도 빨간구역에 속한다면 얘는 빨강이 만으로 커버 가능하다.  
승객이 빨간 구역에서 타서 파란구역에서 내려야한다면  빨강이는 걔를 태운뒤 자신이 담당한 구역의 맨 밑층 (Boundary 층)에 내려두고 다시 자기 갈길을 간다.  
<br>
이후 파랑이가 자신이 담당한 맨 꼭대기층 (Boundary 층) 에 도착하면 이걸 태운뒤 목적지에 데려다준다.  
간략하게 나타내기위해 그림상에는 엘리베이터를 두개밖에 안그렸지만 문제 조건에선 최대 4개까지 사용 가능하다 했으므로 빌딩 전체는 총 4구간으로 나뉜다. 
4개의 쓰레드에 각각 엘리베이터를 하나씩 할당해서 가동시키면 되겠다.  
<br>
여기까지가 테스트를 마치고 집에서 오는 버스에서 생각한 내용이다. 당시엔 멘탈이 깨졌었기 때문에 막연하게 '나중에 다시 풀어볼때 이렇게 풀면 되겠지' 라고 생각하고 대충 묻어뒀다.  
<br/>
<br/>
<br/>
### 스레드는 필요 없다

이를 바탕으로 첫번째 문제인 '어피치 맨션' 해결한뒤 두번째 문제 '제이지 빌딩' 을 풀때 문제가 드러났다. 
엘리베이터가 하나일때는 action API 의 commands 배열에 한개의 command 만 넣어서 호출 해도 됬었다.  
<br/>
```python
[{ "elevator_id": 0, "command": "OPEN"}] # 이런식으로
```
<br/>
엘리베이터가 두개 이상이 되면 이게 안된다  

```python
	[{ "elevator_id": 0, "command": "OPEN"}] # 이런식으로 commands 에 한개의 command만 포함해서 보내면 에러가 뜬다
	[{ "elevator_id": 0, "command": "UP"}, { "elevator_id": 1, "command": "ENTER"}, "ids": [1,4,12]] # start API에서 엘리베이터를 2개 이상 사용한다 선언했으면 command 도 그 수에 맞춰서 요청해야한다. 
```
<br/>
엘리베이터를 2개 사용한다고 요청하고 토큰을 받아왔는데 위 코드의 첫줄과 같이 요청을 보내면 에러가 뜬다. 처음엔 왜 계속 에러가 뜨나 헤멨는데 API 문서에

> 400 Bad Request : 해당 명령을 실행할 수 없음
> 1. (생략)
> 2. 엘리베이터 수와 Command 수가 일치하지 않을 때
> 3. (생략)

라는 문구가 있었다. 2번 항목에 의하면,  애초에 쓰레드를 나눠버리면 안되는 문제였다.  실제 테스트를 치뤘을때는 이 단계 까지 오지도 못했기 때문에 이런 요구사항을 놓친것이다.  
<br/>
처음 풀어보는것도 아니고 두번째인데다 집이라는 편안한 환경에서 푸는데도 이런 실수를 하다니. 합격자들은 실제 테스트 현장에서 이 모든 디테일한 요구사항 파악과 예외처리를 해냈다는 것일까.  
<br/>
코드의 큰 구조를 갈아엎어야 하는 작업이기 때문에 긴장한 상태로 치루는 실제 테스트 였다면 또다시 멘탈이 깨지고 조급해졌을거라 생각하니 마음이 착잡해졌다.  
<br/>
<br/>
<br/>
### 두번째 아이디어

결국 한개의 메인쓰레드에서 해결을 해야한다. 그리고 요청을 보낼때는 commands에 4개의 command를 동시에 넣어서 보내야한다.  

```python
commands = [
	{ "elevator_id": 0, "command": "UP"},
	{ "elevator_id": 1, "command": "UP"},
	{ "elevator_id": 2, "command": "UP"},
	{ "elevator_id": 3, "command": "UP"},
] # 이런식으로 보내야함
```  

한번의 action 요청에 들어갈  command 들을 어떻게 고를지 고민한 내 아이디어는 아래와 같다.  
<br>
<br>
![](https://lh3.googleusercontent.com/ejXC3BYF20Zl2kRUFT3T2xddcNPFKGjQngQoHtm7TuW8o-dlaZcFtbxzGAi26t5UFPIVZA7H8KpRPoeYjB7aPC0c_b0CJq_e3_r2THvg7mrVdk1wjdOZr9f16nUn-2629_LbWfE2YOY4RKmYw7uI8PG-AKEkb3_YSkNG792IuOVb6VEhXdcUHHYWiIZt826GieFMQkU7pvWjQX2zrU1NsLPYt8gn8TraacfH1Rpe-DY6RLswvED-uR6-gi1UzPoFPL70jmKNH0qv58CpzlqAqj8tgjg27Q48u7Pb6Je3wh9EabPtbiY2Rt5-fHOQPx9RnSsEm6-38IT6ncTY-WFTRE6aVZzDNbMZTUCc4GciFKurEM9Vp1ChBXikX8WkpMvBHvjkCpz9omBLO2eA5hIo80FMpo-MYZVdZw9sFgE729qT9q-_rPSg01kmRGQw88yv_CoE1oCZJNwCkR29PnKicCq3kQBUhVU_LmvzxGFwDY00zEMQ1WA524I6Q7vt7psCZjHZrv7uPa4_9GJvuJc6WZvVEuT1kW7aAs0jq1HqzyrSx8LfmTGEIHI71fc3kBe-zUJhDu7zudxMFsKydsoxl5dJY93erHZrqtHUubsUjJ0fzu86Oi5iwRvqvqjFL0auQKpTuxMGLc910Wv0d0iRhtTw=w719-h574-no)  
<br>
<br>
각 엘리베이터마다 본인의 큐에 command를 넣어주고,  action 요청을 보낼때마다 이 큐에서 하니씩 빼다가 commands 를 만들어서 요청한다.  멀티쓰레딩을 공부할때 나오는 '생산자 공급자' 패턴과 모양이 같다.  
<br/>
solve.py의 169~172줄은 이를 나타낸다.
```python
        if len(q) == 0:
            q += el.getNextActions()
        command, ids = q.pop(0)
        commands.append(makeCommand(el.elevator_id, command, ids))
```  

### extra feature  

1. 처음부터 4대의 엘리베이터 1층부터 우르르 몰려다니면 안되기 때문에 미리 알맞게 각 엘리베이터의 큐에 STOP 커맨드를 넣어둔다.  
solve.py의 161번째 줄은 이를 나타낸다.  

```python
	actionQ = [[], [["UP", None] for a in range(6)], [["UP", None] for a in range(12)], [["UP", None] for a in range(18)]]
```  

2. API문서에 '1초에 40번 이상의 네트워크 요청은 응답을 안할수도 있다' 라고 나와있길래 40번째 요청마다 1초 쉬어주는 장치를 했다.  

solve.py 의 36-37 라인과 140-141 라인은 이를 나타낸다.  

```python
	# 36 ~ 37 line
	def action(commands): # action API 요청을 보내는 함수의 내부
		# ...생략
		global requestCount # requestCount 는 코드초반에 전역으로 선언해둠
    		requestCount += 2
		# 140 ~ 141 line
	    	if requestCount > 0 and requestCount % 40 == 0:
        		time.sleep(1)
```  
<br>
<br>
<br>

### 실행결과
