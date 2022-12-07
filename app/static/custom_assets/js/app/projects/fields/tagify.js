let usersList= [];
fetch('/collaborator/', {method: 'GET', mode: 'same-origin',})
    .then(response => response.json())
    .then(data=>{
        data.forEach(user =>
            usersList.unshift({
                'value': user.id,
                'name': user.first_name + ' ' + user.last_name,
                'avatar': user.avatar,
                'email': user.email,
            }))
        const inputElm = document.querySelector('#project_collaborators');
        function tagTemplate(tagData) {
            return `
                <tag title="${(tagData.title || tagData.email)}"
                        contenteditable='false'
                        spellcheck='false'
                        tabIndex="-1"
                        class="${this.settings.classNames.tag} ${tagData.class ? tagData.class : ""}"
                        ${this.getAttributes(tagData)}>
                    <x title='' class='tagify__tag__removeBtn' role='button' aria-label='remove tag'></x>
                    <div class="d-flex align-items-center">
                        <div class='tagify__tag__avatar-wrap ps-0'>
                            <img onerror="this.style.visibility='hidden'" class="rounded-circle w-25px me-2" src="${tagData.avatar}">
                        </div>
                        <span class='tagify__tag-text'>${tagData.name}</span>
                    </div>
                </tag>`
        }

        function suggestionItemTemplate(tagData) {
            return `
        <div ${this.getAttributes(tagData)}
            class='tagify__dropdown__item d-flex align-items-center ${tagData.class ? tagData.class : ""}'
            tabindex="0"
            role="option">
            ${tagData.avatar ? `
                    <div class='tagify__dropdown__item__avatar-wrap me-2'>
                        <img onerror="this.style.visibility='hidden'"  class="rounded-circle w-50px me-2" src="${tagData.avatar}">
                    </div>` : ''
            }
            <div class="d-flex flex-column">
                <strong>${tagData.name}</strong>
                <span>${tagData.email}</span>
            </div>
        </div>
    `
        }

        // initialize Tagify on the above input node reference
        let tagify = new Tagify(inputElm, {
            tagTextProp: 'name', // very important since a custom template is used with this property as text. allows typing a "value" or a "name" to match input with whitelist
            enforceWhitelist: true,
            skipInvalid: true, // do not remporarily add invalid tags
            dropdown: {
                closeOnSelect: false,
                enabled: 0,
                classname: 'users-list',
                searchKeys: ['name', 'email']  // very important to set by which keys to search for suggesttions when typing
            },

            templates: {
                tag: tagTemplate,
                dropdownItem: suggestionItemTemplate
            },
            whitelist: usersList,
        });

        tagify.on('dropdown:show dropdown:updated', onDropdownShow)
        tagify.on('dropdown:select', onSelectSuggestion)

        let addAllSuggestionsElm;
        function onDropdownShow(e) {
            const dropdownContentElm = e.detail.tagify.DOM.dropdown.content;

            if (tagify.suggestedListItems.length > 1) {
                addAllSuggestionsElm = getAddAllSuggestionsElm();

                // insert "addAllSuggestionsElm" as the first element in the suggestions list
                dropdownContentElm.insertBefore(addAllSuggestionsElm, dropdownContentElm.firstChild)
            }
        }

        function onSelectSuggestion(e) {
            if (e.detail.elm === addAllSuggestionsElm)
                tagify.dropdown.selectAll.call(tagify);
        }

        // create a "add all" custom suggestion element every time the dropdown changes
        function getAddAllSuggestionsElm() {
            // suggestions items should be based on "dropdownItem" template
            return tagify.parseTemplate('dropdownItem', [{
                    class: "addAll",
                    name: "Add all",
                    email: tagify.settings.whitelist.reduce(function (remainingSuggestions, item) {
                        return tagify.isTagDuplicate(item.value) ? remainingSuggestions : remainingSuggestions + 1
                    }, 0) + " Members"
                }]
            )
        }
    });


let projectlangs= [];
fetch('/utils/projectlangs/', {method: 'GET', mode: 'same-origin',})
    .then(response => response.json())
    .then(data=>{
        console.log(data)
        data.forEach(project => {
            console.log(project.name)
            projectlangs.unshift(project.name)
        })

        const input = document.querySelector("#project_langs");

        // Initialize Tagify script on the above inputs
        new Tagify(input, {
            whitelist: projectlangs,
            maxTags: 10,
            dropdown: {
                maxItems: 20,           // <- mixumum allowed rendered suggestions
                classname: "tagify__inline__suggestions", // <- custom classname for this dropdown, so it could be targeted
                enabled: 0,             // <- show suggestions on focus
                closeOnSelect: false    // <- do not hide the suggestions dropdown once an item has been selected
            }
        });
    });


