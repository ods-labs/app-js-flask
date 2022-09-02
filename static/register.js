import { getCookie, setCookie } from './js/cookies-utils.js';

document.querySelector("#register").addEventListener('submit', async (event) => {
    event.preventDefault();
    let data = {};
    Array.from(event.target.elements).forEach((input) => {
        if (input.type === "text" || input.type === "password") {
            data[input.id] = input.value;
            input.value = "";
        }
    })
    let ret = await fetch('/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    }).then(response => response.json())

    if (ret && ret.status == 'ok') {
        let msgEl = event.target.querySelector(".messagePlaceholder");
        msgEl.innerHTML = `
            ${ret.message}. <a href="/login">Go to login</a>
        `
    } else {
        let msgEl = event.target.querySelector(".messagePlaceholder");
        msgEl.innerHTML = `Erreur d'inscription: ${ret.message}`
    }
})