import requests
import json

def bytes2dict(response):
    info = json.loads(response.content)
    return info

def get_tocken():
    url = 'http://192.168.204.24/rest-server/api/v1/token'

    data = """{
      "username": "wudch",
      "password": "Wdc2293582"
    }"""
    response = requests.post(url=url, json=json.loads(data))
    info = bytes2dict(response)
    print(info)
    return "Bearer "+info["payload"]["token"]

def get_joblist(username,size=20,offset=0):
    tocken = get_tocken()
    print(type(tocken),tocken)
    headers = {
        "Content-Type": 'application/json',
        "Authorization": tocken
    }
    url = "http://192.168.204.24/rest-server/api/v1/jobs?size="+str(size)+"&offset="+str(offset)
    response = requests.get(url=url, json={}, headers=headers)
    info = bytes2dict(response)
    return info["payload"]

def get_jobinfo(jobid):
    headers = {
        "Content-Type": 'application/json',
        "Authorization": get_tocken()
    }
    url = "http://192.168.204.24/rest-server/api/v1/jobs/" + str(jobid)
    response = requests.get(url=url, json={}, headers=headers)
    info = bytes2dict(response)
    return info

def creat_mission(job_name, command):
    url = f'http://192.168.204.24/rest-server/api/v1/jobs/{job_name}'

    print(url)
    data = \
        f"""
    {{
    "jobName": "{job_name}",
    "retryCount": 0,
    "gpuType": "dgx",
    "image": "dockerhub.pcl.ac.cn:5000/user-images/wudch:1.1",
    "taskRoles": [
        {{
        "taskNumber": 1,
        "minSucceededTaskCount": 1,
        "minFailedTaskCount": 1,
        "cpuNumber": 2,
        "gpuNumber": 1,
        "memoryMB": 4096,
        "shmMB": 4096,
        "command": "{command}",
        "name": "random",
        "needIBDevice": false,
        "isMainRole": false
        }}
    ]
    }}
    """
    headers = {
        "Content-Type": 'application/json',
        "Authorization": get_tocken()
    }
    response = requests.put(url=url, json=json.loads(data), headers=headers)
    print(response.content)

def delete_job(jobid):
    headers = {
        "Content-Type": 'application/json',
        "Authorization": get_tocken()
    }
    url = "http://192.168.204.24/rest-server/api/v1/jobs/" + str(jobid)
    response = requests.delete(url=url, json={}, headers=headers)
    info = bytes2dict(response)
    return info

if __name__ == "__main__":
    command = "cd ../userhome/network-pruning-rfm-master/cifar/l1-norm-pruning/&&PYTHONPATH=./ python main.py --dataset cifar10 --arch vgg --depth 16 --save './log/ori_vgg16'"
    #creat_mission("rua",command)
    a = get_joblist("wudch")
    print(a)
    import time
    for item in a["jobs"]:
        timeStamp = int(item["createdTime"])
        print(timeStamp/1000)
        timeArray = time.localtime(timeStamp/1000)
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        item["createdTime"] = otherStyleTime
        print(item["createdTime"])
    print(a["jobs"][0])
    print("######")
    b = get_jobinfo(a["jobs"][0]["id"])
    print(b)
    #c = delete_job(a["jobs"][0]["id"])
