// flash message handler
const getFlashMessage = (element_id, flash_msg_key) => {
    let flash_message = localStorage.getItem(flash_msg_key) ? localStorage.getItem(flash_msg_key) : null

    if (flash_message !== null){
        document.getElementById(element_id).insertAdjacentHTML('beforebegin',
        `<span class="flash-message">${flash_message}</span>`);

        localStorage.removeItem(flash_msg_key)
    }


}