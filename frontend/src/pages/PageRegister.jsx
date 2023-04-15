import React, { useState } from 'react'
import axios from 'axios';

function PageRegister() {
  const [user, setUser] = useState({
    name: "",
    last_name: "",
    username: "",
    password: ""
  })

  const [regResult, setRegResult] = useState({})

  const submit = (event) => {
    event.preventDefault()
    axios.post('http://127.0.0.1:8000/register', user).then((res) => {
      setRegResult({ ...res.data })
      console.log(regResult)
      localStorage.setItem("access_token", regResult.access_token)
    }).catch((error) => {
      console.log(error)
    })
  }
  return (
    <form className='registerForm' onSubmit={submit}>
      <input
        value={user.name}
        onChange={(event) => setUser({ ...user, name: event.target.value })}
        type='text'
        placeholder='First name' />
      <input
        value={user.last_name}
        onChange={(event) => setUser({ ...user, last_name: event.target.value })}
        type='text'
        placeholder='Last name' />
      <input
        value={user.username}
        onChange={(event) => setUser({ ...user, username: event.target.value })}
        type='email'
        placeholder='Email' />
      <input
        value={user.password}
        onChange={(event) => { setUser({ ...user, password: event.target.value }) }}
        type='password'
        placeholder='Password' />
      <button type='submit'>Submit</button>
    </form>
  )
}

export default PageRegister