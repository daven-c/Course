import { useState, useEffect } from "react";
import "../styles/LoginApp2.css";

function LoginApp({callback}) {
    const [dirID, setdirID] = useState("");
    const [password, setPassword] = useState("");
    const [isLoading, setLoading] = useState(false);

    const onSubmit = async (e) => {
        alert("Please check your DUO verification app!")
        if (isLoading) {
            return;
        }
        e.preventDefault();
        const button = e.target.querySelector('button[type="submit"]');
        setLoading(true)

        const data = {
            dirID,
            password,
        };

        const url = "http://127.0.0.1:5000/auth_student"; // fix name in url
        const options = {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
        };

        const response = await fetch(url, options);
        const resp_data = await response.json();
        if (response.status == 200) {
            callback(dirID);
        } else {
            callback(null);
        }
        setLoading(false)
    };
    return (
        <div className="login-app">
            <form onSubmit={onSubmit}>
                <div className="top-container">
                    <div className="container">
                        <h2 className="gradient-flow">Sign In</h2>
                        <label htmlFor="dirID" className="gradient-flow">Directory ID</label>
                        <input
                            type="text"
                            id="dirID"
                            placeholder="UID"
                            value={dirID}
                            onChange={(ele) => setdirID(ele.target.value)}
                        />
                        <label htmlFor="password" className="gradient-flow">Password</label>
                        <input
                            type="password"
                            id="password"
                            placeholder="Password"
                            value={password}
                            onChange={(ele) => setPassword(ele.target.value)}
                        />
                        <div className="button-container">
                            <div className={isLoading ? "loader disabled" : "loader"}>
                                <span></span>
                                <span></span>
                                <span></span>
                                <span></span>
                                <span></span>
                                <span></span>
                                <span></span>
                                <span></span>
                                <span></span>
                                <span></span>
                                <span></span>
                                <span></span>
                            </div>
                            <input type="submit" value="Sign In" className={isLoading ? "disabled" : ""} />     
                        </div>
                    </div>
                </div>
            </form>
        </div>
    );
}

export default LoginApp;
