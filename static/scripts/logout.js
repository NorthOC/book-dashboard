
function logout(){
    localStorage.removeItem('authTokens')
    window.location.href = "http://127.0.0.1:8000/login"
    return
}
logout()