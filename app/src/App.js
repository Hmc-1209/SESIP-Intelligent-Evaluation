import { useState, createContext, useEffect } from "react";

import './App.css';
import LogIn from "./components/login";
import SignUp from "./components/signUp";
import MainApp from "./components/main_app";
import { validate_access_token } from "./requests/login_requests";

export const AppContext = createContext(null);

function App() {
  const [alert, setAlert] = useState(0);
  const [mode, setMode] = useState(1);
  const [loading, setLoading] = useState(false);

  // Check if the user already login
  useEffect(() => {
    const checkAccessToken = async () => {
      const access_token = window.localStorage.getItem("access_token");
      const response = await validate_access_token(access_token)
      // Check if the user's token not expired
      if (!response) {
        window.localStorage.setItem("access_token", null)
        window.localStorage.setItem("username", null)
        window.localStorage.setItem("user_id", null)
        setMode(0); // Go to login page
      } else {
        window.localStorage.setItem("username", response.data.username)
        window.localStorage.setItem("user_id", response.data.user_id)
        console.log("Validate token")
        setMode(2); // Go to main app page
      }
    }

    checkAccessToken()
  }, []); 


  return (
    <AppContext.Provider
      value={{
        alert,
        setAlert,
        mode,
        setMode,
        loading,
        setLoading
      }}
    >
      <div className="App">
        <header className="App-header">
          {mode === 0 && <LogIn />}
          {mode === 1 && <SignUp />}
          {mode === 2 && <MainApp />}
        </header>
      </div>
    </AppContext.Provider>
  );
}

export default App;
