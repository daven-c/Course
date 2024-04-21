import { useState, useEffect } from "react";
import "../styles/ResultsApp.css";

function ResultsApp(dirID) {

    const [student, setStudent] = useState(null)

    const fetchProfile = async () => {
        const url = "http://127.0.0.1:5000/get_student/" + dirID; // fix name in url
        const options = {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
        };
        const response = await fetch(url, options);
        const resp_data = response.json()
        if (response.status == 200) {
            alert(resp_data.message);
            setStudent(resp_data.student.json())
        } else {
            alert(resp_data.message);
        }
    };

    return (
        <div className="result-app">
            <div className="class-list">
                <ul>
                {
                    <li></li>
                }
                </ul>
            </div>
            <div className="connections"></div>
        </div>
    );
}

export default ResultsApp;
