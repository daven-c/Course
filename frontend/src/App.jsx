import { useState, useEffect } from "react";
import LoginApp from "./components/LoginApp";
import ResultsApp from "./components/ResultsApp"
import "./styles/general.css"

function App() {
    const [dirID, setDirID] = useState("dchangiz");

    const handle = (id) => {
        console.log("id returned: " + id);
        setDirID(id);
    }

    return (
        <>
          {dirID === null ? (
            <LoginApp callback={handle} />
          ) : (
            <ResultsApp dirID={dirID} /> // Pass uid as a prop
          )}
        </>
      );      
}

export default App;
