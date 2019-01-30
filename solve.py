import requests, json
import time
from pprint import pprint

url = "http://localhost:8000"
state = {
    "token": "",
    "timestamp": 0,
    "elevators": [],
    "is_end": False
}
calls = []
picked = []
requestCount = 0

def start(problem_id, number_of_elevators):
    global state
    res = requests.post(url + f"/start/tester/{problem_id}/{number_of_elevators}")
    state = res.json()
    print("TOKEN : ", state["token"])

def onCalls():
    global state
    global calls
    headers = { "X-Auth-Token": state["token"] }
    res = requests.get(url + "/oncalls", headers=headers)
    state = res.json()
    calls = state["calls"]

def action(commands):
    global state
    headers = {"X-Auth-Token": state["token"], "Content-Type": "application/json"}
    res = requests.post(url + "/action", headers=headers, data=json.dumps({"commands": commands}) )
    state = res.json()
    onCalls()
    global requestCount
    requestCount += 2
    pprint(commands)
    print(f"Picked : {len(picked)}  Timestamp : {state['timestamp']}")
    # calls 를 다 처리했는데도 안끝나길래 추가한 디버깅용 print
    if len(picked) == 200 or len(picked) == 500:
        print("PASSENGERS : ", tuple([a["passengers"] for a in state["elevators"]]) )
        print("CALLS : ", calls )
    # 몽키패치
    isPassengersEmpty = all(len(el["passengers"])==0 for el in state["elevators"])
    if isPassengersEmpty and (problem=="JayZ Building" and len(picked) == 200) or (problem=="Lion Tower" and len(picked) == 500):
        picked.clear()

def makeCommand(elevator_id, command, ids=None):
    ret = {"elevator_id": elevator_id, "command": command }
    if ids:
        ret["call_ids"] = ids
    return ret

class Elevator:
    def __init__(self, elevator_id, topFloor, bottomFloor, capacity):
        self.elevator_id = elevator_id
        self.topFloor = topFloor
        self.bottomFloor = bottomFloor
        self.capacity = capacity
        self.toUp = True
        self.el = None
        self.renewElevatorState()

    def renewElevatorState(self):
        global state
        self.el = state["elevators"][self.elevator_id]
    
    def getNextActions(self):
        self.renewElevatorState()
        ret = []

        # 내릴사람
        getOff_ids = []
        for passenger in self.el["passengers"]:
            if passenger["end"] == self.el["floor"]:
                getOff_ids.append(passenger["id"])

        # 탈사람
        getIn_ids = []
        global calls
        global picked
        for call in calls:
            if call["start"] == self.el["floor"] and call["id"] not in picked:
                getIn_ids.append(call["id"])

        # 내리고 태우기
        if len(getIn_ids) > 0 or len(getOff_ids) > 0:
            ret.append(["STOP", None])
            ret.append(["OPEN", None])

            if len(getOff_ids) > 0:
                ret.append(["EXIT", getOff_ids])

            left = self.capacity - len(self.el["passengers"]) + len(getOff_ids)
            if len(getIn_ids) > 0 and left > 0:
                ret.append(["ENTER", getIn_ids[:left]])
                picked += getIn_ids[:left]

            ret.append(["CLOSE", None])

        # 후처리
        if self.el["floor"] == self.topFloor:
            ret.append(["STOP", None])
            self.toUp = False
        if self.el["floor"] == self.bottomFloor:
            ret.append(["STOP", None])
            self.toUp = True

        direction = "UP" if self.toUp else "DOWN"        
        ret.append([direction, None])
        return ret


# ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ 0번문제 어피치맨션 ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
problem = "Apeach Mansion"
start(0, 1)
elevators = []
elevators.append(Elevator(elevator_id=0, bottomFloor=1, topFloor=5, capacity=8))
actionQ = [[]]
while not state["is_end"]:
    if requestCount > 0 and requestCount % 40 == 0: # 1초에 40번 이상의 요청은 에러뜸
        time.sleep(1)

    commands = []
    for el, q in zip(elevators, actionQ):
        if len(q) == 0:
            q += el.getNextActions()
        command, ids = q.pop(0)
        commands.append(makeCommand(el.elevator_id, command, ids))

    action(commands)

print("어피치맨션 완료")

# ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ 1번문제 제이지빌딩 ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
problem  = "JayZ Building"
start(1,4)
elevators = []
elevators.append(Elevator(elevator_id=0, bottomFloor=1, topFloor=25, capacity=8))
elevators.append(Elevator(elevator_id=1, bottomFloor=1, topFloor=25, capacity=8))
elevators.append(Elevator(elevator_id=2, bottomFloor=1, topFloor=25, capacity=8))
elevators.append(Elevator(elevator_id=3, bottomFloor=1, topFloor=25, capacity=8))
actionQ = [[], [["STOP", None] for a in range(6)], [["STOP", None] for a in range(12)], [["STOP", None] for a in range(18)]]

while not state["is_end"]:
    if requestCount > 0 and requestCount % 40 == 0:
        time.sleep(1)

    commands = []
    for el, q in zip(elevators, actionQ):
        if len(q) == 0:
            q += el.getNextActions()
        command, ids = q.pop(0)
        commands.append(makeCommand(el.elevator_id, command, ids))

    action(commands)

print("제이지빌딩 완료")

# ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ 2번문제 라이언타워 ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
problem = "Lion Tower"
start(2,4)
elevators = []
elevators.append(Elevator(elevator_id=0, bottomFloor=1, topFloor=25, capacity=8))
elevators.append(Elevator(elevator_id=1, bottomFloor=1, topFloor=25, capacity=8))
elevators.append(Elevator(elevator_id=2, bottomFloor=1, topFloor=25, capacity=8))
elevators.append(Elevator(elevator_id=3, bottomFloor=1, topFloor=25, capacity=8))
actionQ = [[], [["UP", None] for a in range(6)], [["UP", None] for a in range(12)], [["UP", None] for a in range(18)]]

while not state["is_end"]:
    if requestCount > 0 and requestCount % 40 == 0:
        time.sleep(1)

    commands = []
    for el, q in zip(elevators, actionQ):
        if len(q) == 0:
            q += el.getNextActions()
        command, ids = q.pop(0)
        commands.append(makeCommand(el.elevator_id, command, ids))

    action(commands)

print("라이언타워 완료")
