import { useState, useEffect } from "react";
import LoginApp from "./components/LoginApp";
import ResultsApp from "./components/ResultsApp"
import "./styles/general.css"

function App() {
    const [dirID, setDirID] = useState(null)

    return (
        <>
          {dirID === null ? (
            <LoginApp callback={setDirID} />
          ) : (
            <ResultsApp dirID={dirID} /> // Pass uid as a prop
          )}
        </>
      );      
}

export default App;
