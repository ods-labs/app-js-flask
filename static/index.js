let form = document.querySelector('form');
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
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(response => {
            getAllRows();
        })
});


function supprimer(event) {
    if (Array.from(event.target.classList).indexOf("supprimer") >= 0) {
        if (Array.from(event.target.classList).indexOf("active") >= 0) {
            event.target.classList.remove("active");
        } else {
            event.target.classList.add("active");
        }
    } else if (Array.from(event.target.classList).indexOf("confirm") >=  0) {
        fetch(`/api/${event.target.dataset["id"]}`, {method: 'DELETE'})
            .then(response => response.json())
            .then(() => {
                getAllRows();
            })
    }
}

function getAllRows() {
    fetch('/api')
        .then(response => response.json())
        .then(response => {
            if (response.data && response.data.length > 0) {
                let cnt = document.querySelector(".app .columns");
                cnt.querySelectorAll(".column[data-id]").forEach((child) => {
                    cnt.removeChild(child);
                });
                response.data.forEach((row) => {
                    let div = document.createElement('div');
                    div.className = "column is-3";
                    div.dataset['id'] = row.id;
                    div.innerHTML =
                        `
    <div class="card">
        <div class="card-content">
          <p class="title">
              ${row.title}
          </p>
          <p>${row.description}</p>
        </div>
    </div>                
`
                    if (row.publish == false || row.publish == true) {
                        let cardCnt = div.querySelector(".card");
                        let publish = document.createElement('div');
                        publish.innerHTML = `
        <label class="publish is-size-7">
            Publié
            <input type="checkbox" id="${row.id}" ${row.publish ? "checked" : ""} />
        </label>
        <div class="supprimer has-text-white has-background-primary">
          <div class="icon">
            <i class="ri-delete-bin-6-line"></i>
            <i class="ri-close-line"></i>
          </div>
          <div class="confirm" data-id="${row.id}" >Confirm ?</div>
        </div>
`
                        cardCnt.appendChild(publish);
                    }
                    cnt.prepend(div);
                })
            }
            document.querySelectorAll('.supprimer').forEach((supprElem) => {
                supprElem.addEventListener('click', supprimer);
            })
        });

}

getAllRows();