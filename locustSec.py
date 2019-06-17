# coding=utf-8
import requests
from flask import Flask, make_response, jsonify, render_template, request,redirect,url_for
from locust import HttpLocust, TaskSet, task, web
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

aim = []
ways = []
rpsLines = []
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"}


@web.app.route("/")
def indexAdd():
    if len(ways) == 0:
        return render_template("commit.html")
    else:
        return render_template("commit.html", info=ways)


@web.app.route("/rpsline")
def rpsLine():
    return jsonify(rpsLines)


@web.app.route("/add", methods=["POST"])
def addTestDemo():
    name = request.form["name"]
    way = request.form["ways"]
    weight = int(request.form["weight"])
    if way == "GET":
        one = apiClass(name)
        addWeight(one.getWay, weight)
        rpsLines.append(name)
    elif way == "POST":
        url, data = translateinfo(name)
        one = apiClass(url, data)
        addWeight(one.postWay, weight)
        rpsLines.append(url)
    elif way == "PUT":
        one = apiClass(name)
        addWeight(one.putWay, weight)
        rpsLines.append(name)
    elif way == "DELETE":
        one = apiClass(name)
        addWeight(one.deleteWay, weight)
        rpsLines.append(name)
    ways.append({"name": name, "way": way, "weight": weight})
    MyTaskSet.tasks = aim
    return jsonify({"msg": "添加成功！"})


@web.app.route("/delete/<id>")
def delete(id=None):
    del aim[int(id)]
    del ways[int(id)]
    return redirect(url_for("indexAdd"))


def translateinfo(info):
    infos = info.split("?")
    url = infos[0]
    data = infos[1]
    return url, data


def addWeight(way, weight):
    a = 0
    while a < weight:
        aim.append(way)
        a += 1


# 框架初始化必须要有一个接口，默认给一个
def getDemo(obj):
    req = obj.client.get("/getDemo", headers=header, verify=False)
    if req.status_code == 200:
        print("success")
    else:
        print("fails")


class apiClass(TaskSet):

    def __init__(self, url, data=None):
        self.url = url
        self.data = data

    def getWay(self, obj):
        obj.client.get(self.url, headers=header, verify=False)

    def postWay(self, obj):
        obj.client.post(self.url, data=self.data, headers=header, verify=False)

    def putWay(self, obj):
        obj.client.put(self.url, headers=header, verify=False)

    def deleteWay(self, obj):
        obj.client.delete(self.url, headers=header, verify=False)


class MyTaskSet(TaskSet):
    tasks = [getDemo]


class MyHttpLocust(HttpLocust):
    task_set = MyTaskSet
    host = "https://www.baidu.com"
    min_wait = 1000  # 单位为毫秒
    max_wait = 5000  # 单位为毫秒


if __name__ == "__main__":
    import os

    os.system("locust -f locustSec.py ")
