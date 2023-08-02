import parseJwt from "./parseJwt.js"
/* cookies: {
    'access': "",
    'refresh': ""
}
*/

let form = document.querySelector('#form');

form.addEventListener('submit', async function (event) {
    event.preventDefault()

    const data = {
        'username': event.target.username.value,
        'password': event.target.password.value,
    };

    const response = await fetch("http://127.0.0.1:8000/api/token/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
    })

    const login_state = await response.json()
    
    if (response.status === 200){
        localStorage.setItem('authTokens', JSON.stringify(login_state))
        //console.log(login_state)
        //console.log(login_state.access)
        //console.log(parseJwt(login_state.access))
        window.location.href = "http://127.0.0.1:8000/books";
    }
});