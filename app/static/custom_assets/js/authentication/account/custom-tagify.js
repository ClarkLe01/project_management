// The DOM elements you wish to replace with Tagify
let input = document.querySelector("#kt_tagify_code");

// Initialize Tagify script on the above inputs
new Tagify(input, {
    whitelist: [],
    maxTags: 10,
    dropdown: {
        maxItems: 20,           // <- mixumum allowed rendered suggestions
        classname: "tagify__inline__suggestions", // <- custom classname for this dropdown, so it could be targeted
        enabled: 0,             // <- show suggestions on focus
        closeOnSelect: false    // <- do not hide the suggestions dropdown once an item has been selected
    }
});