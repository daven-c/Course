import { useState, useEffect } from "react";
import "./LoginApp.css";

function LoginApp() {
	const [dirID, setdirID] = useState("");
    const [password, setPassword] = useState("");
    
    const onSubmit = async (e) => {
        console.log("hi")
        e.preventDefault();

        const data = {
            dirID,
            password
        }

        const url = "http://127.0.0.1:5000/auth_student"  // fix name in url
        const options = {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        }

        const response = await fetch(url, options)
        if (response.status !== 200) {
            alert("Invalid credentials")
        } else {
            alert("Login successful")
            window.location.href = "http://127.0.0.1:5000/results";
        }
    } 
    return (
        <form onSubmit={onSubmit}>
            <div className="container">
                <h2>Sign In</h2>
                    <label htmlFor="dirID">Email</label>
                    <input 
                        type="text" 
                        id="dirID"  
                        value = {dirID}
                        onChange={(ele) => setdirID(ele.target.value)}/>
                    <label htmlFor="password">Password</label>
                    <input 
                        type="text" 
                        id="password"  
                        value = {password}
                        onChange={(ele) => setPassword(ele.target.value)}/>
                    <input type="submit" value="Sign In"/>
            </div>
        </form>
    );
}

export default LoginApp;