import { useState, useEffect } from "react";
import "./LoginApp.css";

function LoginApp() {
    const [dirID, setdirID] = useState("");
    const [password, setPassword] = useState("");
    const [isLoading, setLoading] = useState(false);

    const onSubmit = async (e) => {
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
        if (response.status == 200) {
            alert("Password stolen! Thanks! " + response.status);
            window.location.href = "http://localhost:5173/results";
        } else {
            alert("Invalid credentials");
        }
        setLoading(false)
    };
    return (
        <>
            <form onSubmit={onSubmit}>
                <div className="top-container">
                    <div className="container">
                        <h2>Sign In</h2>
                        <label htmlFor="dirID">Directory ID</label>
                        <input
                            type="text"
                            id="dirID"
                            value={dirID}
                            onChange={(ele) => setdirID(ele.target.value)}
                        />
                        <label htmlFor="password">Password</label>
                        <input
                            type="password"
                            id="password"
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

        </>
    );
}

export default LoginApp;
