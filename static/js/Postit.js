class Postit extends HTMLElement {

    constructor() {
        super();

        this.attrtitle = "";
        this.description = "";
        this.canDelete = "";
        this.delete = "";
        this.canPublish = "";
        this.publish = "";

        this.publishEl = document.createElement('div');
        this.deleteEl = document.createElement('div');
    }

    connectedCallback() {
        this.id = this.getAttribute('id');
        this.attrtitle = this.getAttribute('title');
        this.description = this.getAttribute('description');
        this.canDelete = this.getAttributeNames().indexOf('delete') >= 0;
        this.canPublish = this.getAttributeNames().indexOf('publish') >= 0;
        this.publish = this.getAttribute('publish') === "true";

        if (this.canPublish) {
            this.publishEl.innerHTML = `
                <label class="publish is-size-7">
                    Publié
                    <input type="checkbox" id="${this.id}" ${this.publish ? "checked" : ""} />
                </label>
                `
        }
        if (this.canDelete) {
            this.deleteEl.innerHTML = `
                <div class="supprimer has-text-white has-background-primary">
                    <div class="icon">
                        <i class="ri-delete-bin-6-line"></i>
                        <i class="ri-close-line"></i>
                    </div>
                    <div class="confirm" data-id="${this.id}">Confirm ?</div>
                </div>
                `
        }
        this.render();
    }

    render() {
        this.innerHTML = `
            <div class="card">
                <div class="card-content">
                    <p class="title">${this.attrtitle}</p>
                    <p>${this.description}</p>
                </div>
                ${this.canDelete ? this.deleteEl.innerHTML : ''}
                ${this.canPublish ? this.publishEl.innerHTML : ''}
            </div>
            `
    }
}

customElements.define("post-it", Postit);