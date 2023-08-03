// send form data to API to get token
let form = document.querySelector('#form');

form.addEventListener('submit', async function (event) {
    event.preventDefault()

    token_url = "http://127.0.0.1:8000/api/token/"
    redirect_url = "http://127.0.0.1:8000/dashboard"
    on_login_fail_url = "http://127.0.0.1:8000"

    const data = {
        "username": event.target.username.value,
        "password": event.target.password.value,
    };

    const response = await fetch(token_url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
    })
    console.log(response.status)
    if (response.status === 200){
        const login_state = await response.json()
        localStorage.setItem('authTokens', JSON.stringify(login_state))
        window.location.href = redirect_url;
        return
    } else {
        localStorage.setItem('TokenFlashMessage', "Invalid username or password.")
        window.location.href = on_login_fail_url;
        return
    }
});