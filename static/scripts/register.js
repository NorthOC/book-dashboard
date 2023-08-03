// send form data to API to get token
let form = document.querySelector('#form');

form.addEventListener('submit', async function (event) {
    event.preventDefault()

    token_url = "http://127.0.0.1:8000/api/register/"
    redirect_url = "http://127.0.0.1:8000"
    on_login_fail_url = "http://127.0.0.1:8000/register"

    const data = {
        'username': event.target.username.value,
        'password': event.target.password.value,
    };

    const csrf = event.target.csrfmiddlewaretoken.value

    const response = await fetch(token_url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      'X-CSRFToken': csrf
    },
    body: JSON.stringify(data),
    })
    if (response.status === 200){
        localStorage.setItem('TokenFlashMessage', "User created successfully.")
        window.location.href = redirect_url;
        return
    } else {
        localStorage.setItem('TokenFlashMessage', response.text)
        window.location.href = on_login_fail_url;
        return
    }
});