import { useState, useEffect } from "react";
import "./results.css";

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
            <div>
                <div>
                    <h1>
                        justin

                    </h1>
                    <l1>
                        
                    </l1>
                </div>
                <div>
                
                
                </div>
                <div>
                
                
                </div>

            </div>

        </>
    );
}

export default LoginApp;
