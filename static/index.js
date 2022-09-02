import {getCookie} from "./js/cookies-utils.js";

let authentheaders = {}
let token = getCookie('session_id')
if (token) {
    authentheaders['x-access-tokens'] = token
}

let form = document.querySelector('form');
if (form) {
    form.addEventListener('submit', (event) => {
        event.preventDefault();
        let data = {};
        Array.from(event.target.elements).forEach((input) => {
            if (input.type === "text") {
                data[input.id] = input.value;
                input.value = "";
            }
        })

        fetch('/api', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                ...authentheaders
            },
            body: JSON.stringify(data)
        })
            .then(response => response.json())
            .then(response => {
                getAllRows();
            })
    });
}

function getAllRows() {
    fetch('/api', {headers: {...authentheaders}})
        .then(response => response.json())
        .then(response => {
            if (response.data && response.data.length > 0) {
                let cnt = document.querySelector(".app .columns");
                cnt.querySelectorAll("post-it").forEach((child) => {
                    cnt.removeChild(child);
                });
                response.data.forEach((row) => {
                    let postit = document.createElement('post-it');
                    cnt.prepend(postit);
                    postit.outerHTML = `
                        <post-it class="column is-3"
                                 id="${row.id}" title="${row.title}" description="${row.description}"
                                 ${row.hasOwnProperty('delete') ? "delete" : ""} 
                                 ${row.hasOwnProperty("publish") ? `publish="${row.publish}"` : ""}/>
                    `
                })
                document.querySelectorAll('.supprimer').forEach((el) => {
                    el.addEventListener('click', (event) => {
                        if (Array.from(event.target.classList).indexOf("supprimer") >= 0) {
                            if (Array.from(event.target.classList).indexOf("active") >= 0) {
                                event.target.classList.remove("active");
                            } else {
                                event.target.classList.add("active");
                            }
                        } else if (Array.from(event.target.classList).indexOf("confirm") >= 0) {
                            fetch(`/api/${event.target.dataset["id"]}`, {
                                method: 'DELETE',
                                headers: {...authentheaders}
                            })
                                .then(response => response.json())
                                .then(() => {
                                    getAllRows();
                                })
                        }
                    });
                });
                document.querySelectorAll('.publish').forEach((el) => {
                    el.addEventListener('click', async (event) => {
                        await fetch(`/api/${event.target.id}`, {
                            method: 'PUT',
                            headers: {
                                'Content-Type': 'application/json',
                                ...authentheaders},
                            body: JSON.stringify({'publish':event.target.checked})
                        })
                    })
                })
            }
        });

}

getAllRows();