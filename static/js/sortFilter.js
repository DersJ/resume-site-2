var currentPath = location.pathname + location.search;
function removeFromSearchParams(s, path=currentPath) {
    var updated = path.replace(s, '');
    if (updated.endsWith('&')) {
        updated = updated.slice(0, -1);
    }
    if (updated.endsWith('?')) {
        updated = updated.slice(0, -1);
    }
    if (updated.includes('?&')) {
        updated = updated.replace('&', '');
    } 
    return updated;
} 
function addToSearchParams(s, path=currentPath) {
    if (path.includes(s)) { return; }
    if (path.endsWith('/')) { path += '?'; }
    if (!(path.endsWith('?') || path.endsWith('&'))) { path += '&'; }
    path += s;
    return path
}

function applySort(value) {
    if (value === activeSort) { return; }
    if (value === 'newest') {
        location = removeFromSearchParams(`sortBy=${activeSort}`) // newest should have no sortBy, so remove current
    } else {
        const path = removeFromSearchParams(`sortBy=${activeSort}`)
        console.log('removed: ' + path)
        location = addToSearchParams(`sortBy=${value}`, path)
    }
}

function toggleTag(value) {
    var currentPath = location.pathname + location.search;
    
    if (appliedTags.includes(value)) { // remove tag from url
        location = removeFromSearchParams(`tag=${value}`)
    } else { // add to url
        location = addToSearchParams(`tag=${value}`)
    }
}

var sortSelect = document.getElementById("sortSelect");
var params = new URLSearchParams(window.location.search);
var activeSort = params.get('sortBy') || 'newest'
var index;

// Iterating over sort options and setting sortSelect selected to proper option
for(i = 0; i < sortSelect.options.length; i++) { 
    if (sortSelect.options[i].value == activeSort) {
        index = i;
    }
}
sortSelect.options[index].selected = true; 

