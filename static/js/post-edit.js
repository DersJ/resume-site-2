// Toggle collapse/expand of edit form
function toggleFormCollapse() {
    const formContent = document.getElementById('edit-form-content');
    const toggleIcon = document.getElementById('toggle-icon');

    if (formContent.style.display === 'none') {
        formContent.style.display = 'block';
        toggleIcon.textContent = '▼';
    } else {
        formContent.style.display = 'none';
        toggleIcon.textContent = '▶';
    }
}

// Display form validation errors
function displayFormErrors(errors) {
    const errorDiv = document.getElementById('form-errors');
    let errorHTML = '<ul class="mb-0">';

    for (const [field, messages] of Object.entries(errors)) {
        messages.forEach(msg => {
            errorHTML += `<li><strong>${field}:</strong> ${msg}</li>`;
        });
    }
    errorHTML += '</ul>';

    errorDiv.innerHTML = errorHTML;
    errorDiv.style.display = 'block';
}

// Handle successful update
function handleUpdateSuccess(data) {
    // Show success message briefly
    const errorDiv = document.getElementById('form-errors');
    errorDiv.className = 'alert alert-success alert-sm py-2';
    errorDiv.innerHTML = 'Post updated successfully! Reloading...';
    errorDiv.style.display = 'block';

    // Reload after short delay to show success message
    setTimeout(() => {
        location.reload();
    }, 800);
}

// Submit form via AJAX
function submitPostEdit() {
    const form = document.getElementById('inline-post-form');
    const formData = new FormData(form);
    const spinner = document.getElementById('save-spinner');

    // Get post ID from URL path (e.g., /blog/123/)
    const pathParts = window.location.pathname.split('/');
    const postId = pathParts[pathParts.length - 2];

    spinner.removeAttribute('hidden');

    // Clear any previous error messages
    const errorDiv = document.getElementById('form-errors');
    errorDiv.style.display = 'none';
    errorDiv.className = 'alert alert-danger alert-sm py-2';

    fetch(`/blog/${postId}/edit/`, {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: formData
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            return response.json().then(data => {
                throw data;
            });
        }
    })
    .then(data => {
        if (data.success) {
            handleUpdateSuccess(data);
        }
    })
    .catch(error => {
        console.error('Error updating post:', error);
        if (error.errors) {
            displayFormErrors(error.errors);
        } else if (error.error) {
            // Display general error message
            errorDiv.innerHTML = error.error;
            errorDiv.style.display = 'block';
        }
    })
    .finally(() => {
        spinner.setAttribute('hidden', true);
    });
}

// Initialize event listeners
document.addEventListener('DOMContentLoaded', function() {
    const toggleBtn = document.getElementById('toggle-form-btn');
    const editForm = document.getElementById('inline-post-form');

    // Collapse/expand toggle
    if (toggleBtn) {
        toggleBtn.addEventListener('click', function(e) {
            e.preventDefault();
            toggleFormCollapse();
        });
    }

    // Form submission
    if (editForm) {
        editForm.addEventListener('submit', function(e) {
            e.preventDefault();
            submitPostEdit();
        });
    }
});
