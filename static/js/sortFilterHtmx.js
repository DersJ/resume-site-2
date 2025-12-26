// htmx-enabled sort and filter for blog post list

// Helper functions for URL manipulation
function removeFromSearchParams(s, path) {
    if (!path) path = location.pathname + location.search;
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

function addToSearchParams(s, path) {
    if (!path) path = location.pathname + location.search;
    if (path.includes(s)) { return path; }
    if (path.endsWith('/')) { path += '?'; }
    if (!(path.endsWith('?') || path.endsWith('&'))) { path += '&'; }
    path += s;
    return path;
}

// Apply sort using htmx
function applySortHtmx(value) {
    if (value === activeSort) { return; }

    var url;
    if (value === 'newest') {
        url = removeFromSearchParams(`sortBy=${activeSort}`);
    } else {
        const path = removeFromSearchParams(`sortBy=${activeSort}`);
        url = addToSearchParams(`sortBy=${value}`, path);
    }

    // Use htmx to fetch the sorted results
    htmx.ajax('GET', url, {
        target: '#post-list-container',
        swap: 'innerHTML',
        indicator: '#loading-indicator'
    });
}

// Toggle tag filter using htmx
function toggleTagHtmx(slug) {
    var currentPath = location.pathname + location.search;
    var url;

    if (appliedTags.includes(slug)) {
        // Remove tag
        url = removeFromSearchParams(`tag=${slug}`, currentPath);
    } else {
        // Add tag
        url = addToSearchParams(`tag=${slug}`, currentPath);
    }

    // Use htmx to fetch the filtered results
    htmx.ajax('GET', url, {
        target: '#post-list-container',
        swap: 'innerHTML',
        indicator: '#loading-indicator'
    });
}

// Update active tag styling and state after htmx swap
document.body.addEventListener('htmx:afterSwap', function(event) {
    if (event.detail.target.id === 'post-list-container') {
        // Re-apply active classes to filter tags
        var filters = document.getElementsByClassName('filter-tag');
        var params = new URLSearchParams(window.location.search);
        var currentTags = params.getAll('tag');

        for(var i = 0; i < filters.length; i++) {
            if (currentTags.includes(filters[i].dataset.slug)) {
                filters[i].classList.add('active');
            } else {
                filters[i].classList.remove('active');
            }
        }

        // Update sort select
        var activeSortValue = params.get('sortBy') || 'newest';
        var sortSelect = document.getElementById("sortSelect");
        if (sortSelect) {
            for(var i = 0; i < sortSelect.options.length; i++) {
                if (sortSelect.options[i].value == activeSortValue) {
                    sortSelect.options[i].selected = true;
                    break;
                }
            }
        }

        // Update global state variables for next interaction
        window.appliedTags = currentTags;
        window.activeSort = activeSortValue;

        // Smooth scroll to top after filter/sort change
        document.getElementById('post-list-container').scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
});

// Initialize on page load
var params = new URLSearchParams(window.location.search);
var activeSort = params.get('sortBy') || 'newest';

// Preserve scroll position during pagination
// Save scroll position before swap
document.body.addEventListener('htmx:beforeSwap', function(event) {
    if (event.detail.target.id === 'post-list-container') {
        // Store current scroll position
        sessionStorage.setItem('scrollPos', window.scrollY);
    }
});

// Error handling for server errors
document.body.addEventListener('htmx:responseError', function(event) {
    console.error('htmx request failed:', event.detail);

    // Show user-friendly error message
    var target = event.detail.target;
    target.innerHTML = `
        <div class="alert alert-danger" role="alert">
            <strong>Oops!</strong> Something went wrong loading the content.
            <a href="${window.location.href}" class="alert-link">Refresh the page</a> to try again.
        </div>
    `;
});

// Network error handler
document.body.addEventListener('htmx:sendError', function(event) {
    console.error('htmx network error:', event.detail);

    var target = event.detail.target;
    target.innerHTML = `
        <div class="alert alert-warning" role="alert">
            <strong>Connection issue.</strong> Please check your internet connection and
            <a href="${window.location.href}" class="alert-link">try again</a>.
        </div>
    `;
});
