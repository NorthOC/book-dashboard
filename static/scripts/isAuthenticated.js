// returns redirects if not authenticated
async function isAuthenticated() {
    let authTokens = localStorage.getItem('authTokens') ? JSON.parse(localStorage.getItem('authTokens')) : null
    let verify_url = "http://127.0.0.1:8000/api/token/verify/"
    let redirect_url = "http://127.0.0.1:8000/login"

    if (authTokens === null){
        localStorage.setItem('TokenFlashMessage', "Unauthorized access. Please login.")
        window.location.href = redirect_url
        return
    }
    console.log("auth issue")
    let access = JSON.stringify({"token":`${authTokens['access']}`})
    console.log(access)

    const response = await fetch(verify_url, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: access,
    })
    if (response.status !== 200){
        localStorage.setItem('TokenFlashMessage', "Token expired. Please login again.")
        window.location.href = redirect_url
        return
    }
}
isAuthenticated()