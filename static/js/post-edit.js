// Toggle between view and edit modes
function toggleEditMode(show) {
    const displayContent = document.getElementById('post-display-content');
    const editForm = document.getElementById('post-edit-form');

    if (show) {
        displayContent.style.display = 'none';
        editForm.style.display = 'block';
        // Scroll to the form
        editForm.scrollIntoView({ behavior: 'smooth', block: 'start' });
    } else {
        displayContent.style.display = 'block';
        editForm.style.display = 'none';
        // Clear any error messages
        document.getElementById('form-errors').style.display = 'none';
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
    // Reload the page to show updated content with proper markdown rendering
    location.reload();
}

// Submit form via AJAX
function submitPostEdit(postId) {
    const form = document.getElementById('inline-post-form');
    const formData = new FormData(form);
    const spinner = document.getElementById('save-spinner');

    spinner.removeAttribute('hidden');

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
            const errorDiv = document.getElementById('form-errors');
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
    const editBtn = document.getElementById('edit-post-btn');
    const cancelBtn = document.getElementById('cancel-edit-btn');
    const editForm = document.getElementById('inline-post-form');

    if (editBtn) {
        editBtn.addEventListener('click', function(e) {
            e.preventDefault();
            toggleEditMode(true);
        });
    }

    if (cancelBtn) {
        cancelBtn.addEventListener('click', function(e) {
            e.preventDefault();
            toggleEditMode(false);
        });
    }

    if (editForm) {
        editForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const postId = document.getElementById('edit-post-btn').dataset.postId;
            submitPostEdit(postId);
        });
    }
});
