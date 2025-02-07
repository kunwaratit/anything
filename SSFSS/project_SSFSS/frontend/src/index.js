import React from 'react';
import './index.css';
import App from './Apps';
import reportWebVitals from './reportWebVitals';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import { useAuth } from './components/AuthContext'; // Import useAuth hook
import { AuthProvider } from './components/AuthContext';
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <div>

      <React.StrictMode>
        <BrowserRouter>
          <AuthProvider>
            <App/>
          </AuthProvider>  
        </BrowserRouter>  
      </React.StrictMode>
   
  </div>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
