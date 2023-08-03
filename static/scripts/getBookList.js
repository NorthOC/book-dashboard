async function getBookList(){
    let authTokens = JSON.parse(localStorage.getItem('authTokens'))

    let book_list_endpoint = "http://127.0.0.1:8000/api/books/"
    console.log("booklist issue")
    const response = await fetch(book_list_endpoint, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer "+ String(authTokens['access'])
        },
        })
        let data = await response.json()

        if (response.status === 200){
            let container = document.getElementById("books")
            data.forEach(book => {
                let element = document.createElement("p")
                element.innerHTML = `${book.user} - ${book.id} - ${book.author} - ${book.title}`
                container.appendChild(element)
            });
        }
}
getBookList()