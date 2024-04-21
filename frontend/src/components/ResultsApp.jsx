import { useState, useEffect } from "react";
import "../styles/ResultsApp.css";

function ResultsApp({ dirID }) {

    const [student, setStudent] = useState({});
    const [connections, setConnections] = useState([]);
    const [selectedCourses, setSelectedCourses] = useState([]);

    const selectCourse = (e) => {
        const course = e.target.innerHTML;
        setSelectedCourses(prevSelectedCourses => {
            if (prevSelectedCourses.includes(course)) {
                return prevSelectedCourses.filter(c => c !== course);
            } else {
                // Course is not selected, add it
                return [...prevSelectedCourses, course];
            }
        });
        console.log(selectedCourses)
    };

    useEffect(() => {
        fetchProfile();   // Wait for profile fetch to complete
        getConnections(); // Wait for connections fetch to complete
    }, [dirID]);

    useEffect(() => {
        console.log(student);
    }, [student]);

    useEffect(() => {
        console.log(connections);
    }, [connections]);

    const fetchProfile = async () => {
        const url = "http://127.0.0.1:5000/get_student/" + dirID; // fix name in url
        const options = {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
        }

        const response = await fetch(url, options);
        const resp_data = await response.json();
        if (response.status == 200) {
            console.log("profile loaded");
            // const result = resp_data.student
            // setStudent(result)
            setStudent(resp_data.student)
        } else {
            console.log("profile not found");
        }
    };

    const getConnections = async () => {
        const url = "http://127.0.0.1:5000/get_connections/" + dirID; // fix name in url
        const options = {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
        };

        const response = await fetch(url, options);
        const resp_data = await response.json();
        if (response.status == 200) {
            // const result = resp_data.connections
            // setConnections(result);
            setConnections(resp_data.connections);
        }
    };

    return (
        <div className="result-app">
            <div className="class-list">
                <h1>{(student.full_name === null) ? student.dir_id : student.full_name}'s Classes</h1>
                <ul>
                    {
                        Object.keys(student)
                            .filter((key) => key.startsWith("course") && student[key] !== null)
                            .map((key) => <li key={key} onClick={selectCourse} className={selectedCourses.includes(student[key]) ? "selected" : ""}><span>{student[key]}</span></li>)
                    }
                </ul>
            </div>
            <div className="connections">
                {connections.map(([name, courses]) => (
                    <div className={(courses.some(course => selectedCourses.includes(course))) ? "cnct-item selected" : "cnct-item"} key={name}> {/* Add a unique key here */}
                        <h2 className="cnct-name">{name}</h2>
                        <div className="seperator"></div>
                        <div className="cnct-course-container">
                            {courses.map(course => (
                                <div className="cnct-course" key={course}>
                                    {course}
                                </div>
                            ))}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default ResultsApp;
