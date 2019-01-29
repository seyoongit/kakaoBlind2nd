# 카카오 블라인드 테스트 2차 엘리베이터 문제 풀이
  
실전에서 망하고 지금와서 이걸 푸는게 무슨 의미가 있겠냐만은 그래도 다시 한번 엘리베이터 문제에 도전해봤다.    
     
    
     
    
### 첫번째 아이디어

기본적인 아이디어는 다음과 같다 
> 각각의 엘리베이터는 자기에게 정해진 구간만 순회하면서 내릴사람 있으면 내려주고 태울사람 있으면 태우기를 반복한다

지하철을 떠올리면 이해하기 쉽다. 지하철은 내가 가는 방향에  승객이 별로없고 다른쪽에 기다리는 승객이  많다고 해서 그쪽으로 방향을 틀거나 하지 않는다. 그저 자기에게 정해진 구간만 순회할뿐이다.

![ssad](https://lh3.googleusercontent.com/8z6qS6ekNBfD7lTU1Fs1cYVhdo6y4JTAJDOaR_qhMR5nxr9jZTHRN8xHU5iW3aerMTJNtwYeT-RuTi2ok03IMk40SIaqso-sK3VJHojtOWiLukJIY2aflvX1N-RjKhBODnq7oLjPlwHSNWL2hfKfBkNqh4OkQ6P-SxWoaUa4l_Ffg6G9q0h01YRb5i5oGU9KLVvMtF-SBUjOtUBBh5Xop5yOYYDs6vMfDBnuqVAu8asv5dL6_bUvmHnyhTRZrk4y5JIvAZcu2tUa6Fo3hZKO9BXgI6roozFH_hG_coDbJ7avHof-NAxnM3YqxtGmj7XkEH7CKq5zg45tIkJxkjHLx_ZXt8pmXC_7x1KtbNNJ3ZXqpiapPzUvcIMCo58mxQPln4YQEIipJc_WyToNZkZY5szXOfX45ODEwNYIYhB4vUNagE3psIVaRAs877epYWNyNnp8HKfv4pNha-mVqQ6l5r9dr2uCFMdfnItqkSS0YBoyHQIP5ERBwIofrpCk8rlyKjsVN2ewZJgxm3NCfANRA-D3JC91zBYHfnnskHapKZGLKe2TFohQ6aAuRYIsdErY0Dy97Q-AbCVwc4tSJ5FnkVQ0eyu0Av6xnpkzRvH1oOrxzWKzYu3ajUYWEu90-yWrbxzwOPnVZUjSKSVmI2MCApJT=w489-h504-no)

이를 그림으로 표현했다.  구역을 나눈뒤에 각 엘리베이터는 이 구역만 왔다갔다 하면서 승객을 실어 나른다. 

승객이 빨간 구역에서 탔는데 내려야 하는 층도 빨간구역에 속한다면 얘는 빨강이 만으로 커버 가능하다. 

승객이 빨간 구역에서 타서 파란구역에서 내려야한다면  빨강이는 걔를 태운뒤 자신이 담당한 구역의 맨 밑층 (Boundary 층)에 내려두고 다시 자기 갈길을 간다. 이후 파랑이가 자신이 담당한 맨 꼭대기층 (Boundary 층) 에서 이걸 낚아 챈뒤 목적지에 데려다준다.

간략하게 나타내기위해 그림상에는 엘리베이터가 두개밖에 없지만 문제 조건에 최대 4개까지 사용 가능하다 했으므로 빌딩 전체는 총 4구간으로 나뉜다.  4개의 쓰레드에 각각 엘리베이터를 하나씩 할당해서 가동시키면 되겠다.

여기까지가 테스트를 마치고 집에서 오는 버스에서 생각한 내용이다. 당시엔 멘탈이 깨졌었기 때문에 막연하게 '나중에 다시 풀어볼때 이렇게 풀면 되겠지' 라고 생각하면서 대충 묻어뒀다.


### 스레드는 필요 없다

이를 바탕으로 첫번째 문제인 '어피치 맨션' 해결한뒤 두번째 문제 '제이지 빌딩' 을 풀때 문제가 드러났다. 
엘리베이터가 하나일때는 action API 의 commands 배열에 한개의 command 만 넣어서 호출 해도 됬었다.
```python
[{ "elevator_id": 0, "command": "OPEN"}] # 이런식으로
```
엘리베이터가 두개 이상이 되면 이게 안된다
```python
[{ "elevator_id": 0, "command": "OPEN"}] # 첫번째 쓰레드의 action 요청에 보낼 commands
[{ "elevator_id": 1, "command": "UP"}] # 두번째 쓰레드의 action 요청에 보낼 commands
```
엘리베이터를 2개 사용한다고 요청하고 토큰을 받아왔는데 위와같이 요청을 보내면 에러가 뜬다. 처음엔 왜 계속 에러가 뜨나 헤멨는데 API 문서에
>  400 Bad Request : 해당 명령을 실행할 수 없음 
1. (생략)
2. 엘리베이터 수와 Command 수가 일치하지 않을 때
3. (생략)

라는 문구가 있었다. 2번 항목에 의하면,  애초에 쓰레드를 나눠버리면 안되는 문제였다.  실제 테스트에서는 이 단계 까지 오지도 못했기 때문에 이런 요구사항을 놓친것이다.

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
한번의 action 요청에 들어갈  command 들을 어떻게 고를지 생각한 내 아이디어는 아래와 같다.


각 엘리베이터마다 본인의 큐에 command를 넣어주고,  action 요청을 보낼때마다 이 큐에서 하니씩 빼다가 commands 를 만들어서 요청한다.  멀티쓰레딩을 공부할때 나오는 '생산자 공급자' 패턴과 모양이 같다.

solve.py 코드의 169~172줄은 이를 나타낸다,
```python
        if len(q) == 0:
            q += el.getNextActions()
        command, ids = q.pop(0)
        commands.append(makeCommand(el.elevator_id, command, ids))
```


