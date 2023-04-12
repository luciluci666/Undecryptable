import logo from './logo.svg';
import './App.css';
import axios from 'axios';
import React, { useState } from 'react';

function App() {
  const [user, setUser] = useState({
    name: "",
    last_name: "",
    username: "",
    password: ""
  })

  const submit = (event) => {
    event.preventDefault()
    axios.post('http://127.0.0.1:8000/register',user).then((res) => {
      console.log(res.data)
    }).catch((error) => {
      console.log(error)
    })
  }

  return (
    <div className="App">
      <form onSubmit={submit}>
        <input 
          value={user.name}
          onChange={(event) => setUser({...user, name: event.target.value})}
          type='text'
          placeholder='First name'/>
        <input 
          value={user.last_name}
          onChange={(event) => setUser({...user, last_name: event.target.value})}
          type='text' 
          placeholder='Last name'/>
        <input 
          value={user.username}
          onChange={(event) => setUser({...user, username: event.target.value})}
          type='email' 
          placeholder='Email'/>
        <input 
          value={user.password} 
          onChange={(event) => {setUser({...user, password: event.target.value})}} 
          type='password' 
          placeholder='Password'/>
        <button type='submit'>Submit</button>
      </form>
    </div>
  );
}

export default App;
