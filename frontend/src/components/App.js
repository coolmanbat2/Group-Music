import React from "react";
import ReactDOM from 'react-dom/client';
import HomePage from "./HomePage";

function App(props) {
    return (
        <div className="center">
            <HomePage/>
        </div>
    )
}
const appDiv = document.getElementById("app");
const root = ReactDOM.createRoot(appDiv);
root.render(<App />);

export default App;