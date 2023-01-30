import React from "react";
import "./App.css";
import Link from "@mui/material/Link";
import { Link as LinkRouter } from "react-router-dom";

function App() {
  return (
    <div className="App">
      Landing
      <br />
      <Link component="span" variant="body2">
        <LinkRouter to={`/register`}>Register</LinkRouter>
      </Link>
      <br />
      <Link component="span" variant="body2">
        <LinkRouter to={`/login`}>Login</LinkRouter>
      </Link>
    </div>
  );
}

export default App;
