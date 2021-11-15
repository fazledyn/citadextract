from flask import Flask, jsonify, request
from flask_cors import CORS
from bs4 import BeautifulSoup

import requests, json, os

course = json.loads(open("course.json", "r").read())

loginPage  = "https://moodle.cse.buet.ac.bd/login/index.php"
coursePage = "https://moodle.cse.buet.ac.bd/course/view.php?id="
forumPage  = "https://moodle.cse.buet.ac.bd/mod/forum/view.php?id="

app = Flask(__name__)
CORS(app)

@app.route("/forum-data")
def forumPostView():
    
    if request.method == "GET":
        
        data = {
            "username": os.environ.get("MOODLE_USER"),
            "password": os.environ.get("MOODLE_PASS")
        }
        sessionObject = requests.Session()
        sessionObject.post(loginPage, data)
        
        forumData = dict()
        for eachCourse in course:

            url = "".join([ forumPage, eachCourse["forumId"] ])
            res = sessionObject.get(url)
            
            soup = BeautifulSoup(res.text, "html.parser")
            forumContent = soup.find("table", class_="forumheaderlist")

            if forumContent is not None:
                
                forumListContent = forumContent.find_all("td", class_="topic starter")
                forumList = []
                for each in forumListContent:
                    forumList.append({
                        "text": each.find("a").text,
                        "url": each.find("a").get("href")
                    })

                forumData[eachCourse["name"]] = forumList

        return jsonify(forumData)


@app.route("/course-data")
def courseDataView():

    if request.method == "GET":
        data = {
            "username": os.environ.get("MOODLE_USER"),
            "password": os.environ.get("MOODLE_PASS")
        }

        sessionObject = requests.Session()
        sessionObject.post(loginPage, data)

        courseData = dict()
        for eachCourse in course:

            url = "".join([ coursePage, eachCourse["id"] ])
            res = sessionObject.get(url)
            
            soup = BeautifulSoup(res.text, "html.parser")
            courseContent = soup.find('div', class_="course-content").find_all("div", class_="content")

            courseItems = []
            for item in courseContent:
                subItems = []
                allLinks = item.find_all("div", class_="activityinstance")

                if len(allLinks) > 0:
                    
                    for each in allLinks:
                        subItems.append({
                            "url": each.find("a").get("href"),
                            "text": each.find("span", class_="instancename").text
                        })

                    courseItems.append({
                        "title": item.find("h3", class_="sectionname").text,
                        "items": subItems
                    })

            courseData[eachCourse["name"]] = courseItems

        return jsonify(courseData)


if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=False,port=8080)