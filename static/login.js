import { getCookie, setCookie } from './js/cookies-utils.js';

document.querySelector("#login").addEventListener('submit', async (event) => {
    event.preventDefault();
    let data = {};
    Array.from(event.target.elements).forEach((input) => {
        if (input.type === "text" || input.type === "password") {
            data[input.id] = input.value;
            input.value = "";
        }
    })
    let token = await fetch('/login', {
        method: 'POST',
        headers: {
            'Authorization': `basic ${btoa(data['username'] + ":" + data['password'])}`
        }
    }).then(response => response.json())

    if (token && token.token) {
        let errorEl = event.target.querySelector(".errorPlaceholder");
        errorEl.innerHTML = ""
        setCookie("session_id", token.token, 1)
        window.location.replace('/')
    } else {
        let errorEl = event.target.querySelector(".errorPlaceholder");
        errorEl.innerHTML = `
        <h3 class="title is-5">
            Erreur de connexion: ${token.message}
        </h3>
        `
    }
})