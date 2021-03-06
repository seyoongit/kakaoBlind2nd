# 카카오 블라인드 테스트 2차 엘리베이터 문제 풀이
실전에서 망하고 지금와서 이걸 푸는게 무슨 의미가 있겠냐만은 그래도 다시 한번 엘리베이터 문제에 도전해봤다.  
<br>
elevator.exe 는 [카카오 엘리베이터 문제 깃허브](https://github.com/kakao-recruit/2019-blind-2nd-elevator) 에 나온대로 빌드를 해서 만든 바이너리파일이고 solve.py는 나의 풀이이다.
<br>
<br>
### 첫번째 아이디어

기본적인 아이디어는 다음과 같다  <br>
<br>
> 각각의 엘리베이터는 자기에게 정해진 구간만 순회하며 내릴사람 있으면 내려주고 태울사람 있으면 태우기를 반복한다  
<br>
<br>
지하철을 떠올리면 이해하기 쉽다.  
<br>
지하철은 내가 가는 방향에 승객이 별로없고 다른쪽에 기다리는 승객이 많다고 해서 그쪽으로 방향을 틀거나 하지 않는다.  
<br>
그저 자기에게 정해진 구간만 순회할뿐이다. 승객은 지하철을 환승해가며 목적지에 도착한다.  <br>
<br>

![first_idea](https://user-images.githubusercontent.com/47002080/52043573-6bbcf580-2583-11e9-92b2-f095287822ba.png)

이를 그림으로 표현했다.  
구역을 나눈뒤에 각 엘리베이터는 자기 구역만 왔다갔다 하면서 승객을 실어 나른다.  
<br>
승객이 빨간 구역에서 탔는데 내려야 하는 층도 빨간구역에 속한다면 얘는 빨강이 만으로 커버 가능하다.  
승객이 빨간 구역에서 타서 파란구역에 내려야한다면  빨강이는 걔를 태운뒤 자신이 담당한 구역의 맨 밑층 (Boundary 층)에 내려두고 다시 자기 갈길을 간다.  
<br>
이후 파랑이가 자신이 담당한 맨 꼭대기층 (Boundary 층) 에 도착하면 얘를 태운뒤 목적지에 데려다준다.  
간략하게 나타내기위해 그림상에는 엘리베이터를 두개밖에 안그렸지만 문제 조건에선 최대 4개까지 사용 가능하다 했으므로 빌딩 전체는 총 4구간으로 나뉜다. 
4개의 쓰레드에 각각 엘리베이터를 하나씩 할당해서 가동시키면 되겠다.  
<br>
여기까지가 테스트를 마치고 집에서 오는 버스에서 생각한 내용이다. 당시엔 멘탈이 깨졌었기 때문에 막연하게 '나중에 다시 풀어볼때 이렇게 풀면 되겠지' 라고 생각하고 대충 묻어뒀다.  
<br>
<br>

### 스레드는 필요 없다

이를 바탕으로 첫번째 문제인 '어피치 맨션' 은 해결했으나, 두번째 '제이지 빌딩' 을 풀때 문제점이 드러났다. (정확히 말하자면 엘리베이터를 하나밖에 사용하지 않았기 때문에 '쓰레드당 엘리베이터 하나' 컨셉은 적용했으나 '구간을 나누기' 는 적용할 일이 없었다. 엘리베이터가 한개니까.) <br>
<br>
엘리베이터가 하나일때는 action API 의 commands 배열에 한개의 command 만 넣어서 호출 해도 됬었다.  
<br>

```python
[{ "elevator_id": 0, "command": "OPEN"}] # 이런식으로
```
<br>
근데 엘리베이터가 두개 이상이 되면 이게 안된다.  
<br>

```python
[{ "elevator_id": 0, "command": "OPEN"}] # 이런식으로 commands 에 한개의 command만 포함해서 보내면 에러가 뜬다
[{ "elevator_id": 0, "command": "UP"}, { "elevator_id": 1, "command": "ENTER"}, "ids": [1,4,12]] # start API에서 엘리베이터를 2개 이상 사용한다 선언했으면 command 도 그 수에 맞춰서 요청해야한다. 
```
<br>
엘리베이터를 2개 사용한다고 요청하고 토큰을 받아왔는데 위 코드의 첫줄과 같이 요청을 보내면 에러가 뜬다. 처음엔 왜 계속 에러가 뜨나 헤멨는데 API 문서에  <br>
<br>

> 400 Bad Request : 해당 명령을 실행할 수 없음
> 1. (생략)
> 2. 엘리베이터 수와 Command 수가 일치하지 않을 때
> 3. (생략)  

라는 문구가 있었다. 2번 항목에 의하면,  애초에 쓰레드를 나눠버리면 안되는 문제였다.  실제 테스트를 치뤘을때는 이 단계 까지 오지도 못했기 때문에 이런 요구사항을 놓친것이다.  <br>
<br>
처음 풀어보는것도 아니고 두번째인데다 집이라는 편안한 환경에서 푸는데도 이런 실수를 하다니. 합격자들은 실제 테스트 현장에서 이 모든 디테일한 요구사항 파악과 예외처리를 해냈다는 것일까.  <br>

코드의 큰 구조를 갈아엎어야 하는 작업이기에 긴장한 상태로 치루는 실제 테스트 였다면 또다시 멘탈이 깨지고 조급해졌을거라 생각하니 마음이 착잡해졌다.  
<br>
<br>
<br>

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
![second_idea](https://user-images.githubusercontent.com/47002080/52043593-77102100-2583-11e9-957c-0d368d657a97.png)  
<br>
<br>
각 엘리베이터는 자기만의 큐를 갖고있으며 action 요청을 할때는 이 큐에서 하나씩 빼다가 commands 를 만들어 요청한다. 큐가 비면 엘리베이터 객체는 자신의 큐에 다시 command를 채워준다. 멀티쓰레딩을 공부할때 나오는 '생산자 공급자' 패턴과 모양이 같다.  
<br>
solve.py의 152~155줄은 이를 나타낸다.
```python
if len(q) == 0:
    q += el.getNextActions()
command, ids = q.pop(0)
commands.append(makeCommand(el.elevator_id, command, ids))
```  
<br>
<br>  

### Extra feature  
<br>

###### 엘리베이터에 태운 승객의 id를 따로 저장  

서로 다른 엘리베이터에서 같은 승객을 ENTER 하는 요청을 보내면 당연히 에러가 뜬다.  <br>
이를 방지하기위해 전역변수 picked 를 유지한다. picked는 엘리베이터에 태운 승객의 id를 담는 리스트이다.  <br>  
엘리베이터는 ENTER 커맨드를 생산함과 동시에 해당 call의 id를 picked에 기록한다  <br>
이후 다른 엘리베이터는 승객을 태울때 해당 승객의 id가 picked에 있다면 태우지 않는다  <br>
<br>
solve.py 의 98번 줄은 이를 나타낸다.
```python
picked += getIn_ids[:left]
commands.append(makeCommand(el.elevator_id, command, ids))
```  
<br>

###### 엘리베이터 간격띄우기  

처음부터 4대의 엘리베이터 1층부터 우르르 몰려다니면 안되기 때문에 각 엘리베이터의 큐에 STOP 커맨드를 넣어서 출발을 지연시킨다.  
<br>
solve.py의 144번째 줄은 이를 나타낸다.  

```python
actionQ = [[], [["UP", None] for a in range(6)], [["UP", None] for a in range(12)], [["UP", None] for a in range(18)]]
```  

물론 먼저 출발한 엘리베이터가 승객을 마주칠경우 최소 4턴이상 (STOP, OPEN, ENTER or EXIT, CLOSE) 그자리에 멈춰있기 때문에 시간이 흐름에 따라 다시 우르르 몰려다니는 모양새가 될지 어떨지는 확실하지 않으나 어쨌든 안하는것보단 나을듯 하다.  
<br>  

###### 요청은 1초에 40번만  

API문서에 '1초에 40번 이상의 네트워크 요청은 응답을 안할수도 있다' 라는 제한이 있기 때문에 40번째 요청마다 1초 쉬어주는 장치를 했다.  
<br>
solve.py 의 36-37 라인과 147-148 라인은 이를 나타낸다.  

```python
# 36 ~ 37 line
def action(commands): # action API 요청을 보내는 함수의 내부
	# ...생략
	global requestCount # requestCount 는 코드초반에 전역으로 선언해둠
	requestCount += 2
	
# 147 ~ 148 line
if requestCount > 0 and requestCount % 40 == 0:
	time.sleep(1)
```  
<br>
<br>
<br>

### 실행결과

##### 어피치 맨션  

![solve_apeach_mansion](https://user-images.githubusercontent.com/47002080/52043625-8b541e00-2583-11e9-82c7-561c37c67943.gif)  

잘 작동한다  
<br>
<br>

##### 제이지 빌딩  

![solve_jayz_building_fail](https://user-images.githubusercontent.com/47002080/52043634-9444ef80-2583-11e9-949f-1e94127e51f7.gif)  

<br>
제이지 빌딩에서 문제가 발생했다.  <br>

무한루프에 빠졌는지 안끝나길래 picked가 200(제이지 빌딩 문제의 call 수)이 되면 각 엘리베이터의 passengers 와 현재 남아있는 calls를 로깅해봤다.  <br>

이유는 알수없지만 서너개의 call이 처리가 안된채로 남아있는데, 이들은 이미 picked에 기록된 상태라 엘리베이터가 얘내들을 안태우고 건너뛰는듯 하다.   <br>

디버깅을 하려면 할수는 있겠지만 또 vscode의 디버깅 모드로 F5만 수백번 눌러가며 찾아야 될걸 생각하니 급 귀찮아서 임시방편으로 몽키패치만 추가했다. 어짜피 실전이었다면 이렇게 큰 버그가 나온것에서 이미 탈락이다.  
<br>

```python
# action 함수 말미에 추가한 몽키패치
# picked의 길이가 200, 그리고 모든 엘리베이터의 passengers가 비워졌다면 picked를 비워버린다.
isPassengersEmpty = all(len(el["passengers"])==0 for el in state["elevators"])
if isPassengersEmpty and (problem=="JayZ Building" and len(picked) == 200) or (problem=="Lion Tower" and len(picked) == 500):
	picked.clear()
```

<br>
<br>

![solve_jayz_building_success](https://user-images.githubusercontent.com/47002080/52043654-a0c94800-2583-11e9-819f-46b8e458e462.gif)  


클리어
<br>
<br>

##### 라이언 타워  

![](https://user-images.githubusercontent.com/47002080/52043676-a9ba1980-2583-11e9-89cc-272ff32f83c3.gif)  

클리어  
<br>
사실 위의 몽키패치에 passengers가 다 비워졌는지 체크하는 항목은 원래 없었는데, 이 경우 제이지 빌딩 문제는 통과하지만 라이언 타워 문제에서 막혀버린다.   <br>  
passengers를 체크하는 코드는 그래서 추가한것.  
<br>
<br>

### 마치며  

solve.py 는 첫번째 아이디어에 나왔던 '구간을 나눈다' 컨셉이 적용되어있지 않다.  <br>
그냥 엘리베이터 4개가 1층부터 25층까지 다니면서 각자 개인플레이를 할 뿐이다.  <br>
구간을 나누는 컨셉을 적용해서 리팩토링 할수도 있겠지만.. 지금으로선 귀찮기도 하고 일단은 문제를 풀어본 것에 의의를 두기에 생략한다.  <br>
<br>
이 글에서는 문제 풀이가 그냥 스무스하게 진행되는데 실제로는 많이 막히고, 디버깅하는데 몇시간씩 잡아먹고 하는 경우가 많았다.  문제 푸는 내내 '이게 실제 테스트였다면 나는 또 탈락이네..' 라는 생각이 머릿속을 지배했다.  <br>
<br>
일종의 트라우마같은걸 극복해서 자신감을 얻어보자는 취지로 시도한건데 왠지 깔끔한 풀이와는 거리가 먼 결과물이 나오고 말았다.  실제 테스트 당일날 이걸 해낸 사람들은 어떻게 한걸까? 카카오급 기업에 '신입' 으로 들어가려면 이정도는 다 기본으로 해야하는건가? 그때 내 옆자리는 문제 다풀고 5시 땡 치자마자 나가버렸는데 그 사람은 지금 카카오 입사했겠지.. 등등 여러가지 생각이 든다.  그래도 문제를 풀면서 멀티쓰레드 프로그래밍 비스무리한것도 해봤고, 프로세스와 쓰레드에 대해 공부할 기회도 되었기에 이 정도면 나쁘지 않았다고 생각한다.  <br>
<br>
<br>

![](https://user-images.githubusercontent.com/47002080/52044278-184ba700-2585-11e9-88c9-f24fc048d202.gif)


<br>
<br>
<br>
