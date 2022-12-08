function countChars(obj){
    document.getElementById("charCount").innerHTML = obj.value.length;
}

function deleteComment(id, button, token) {
    if (confirm("Are you sure you want to delete this comment?") == true) {
        spinner = button.querySelector('.spinner-border')
        spinner.removeAttribute('hidden');
        fetch(`/blog/comment/delete/${id}`, {
            method: 'DELETE',
            credentials : 'same-origin',
            headers: {'X-CSRFToken': token},
        })
        .then(response => {
            if (response.status == 204) {
                comment = button.closest('.comment');
                comment.querySelector('.comment-body').remove()
                comment.querySelector('.comment-author').innerHTML = "Comment deleted."
            } 
        })
        .catch(error => {
            console.error(error);
        })
        .finally(() => {
            spinner.setAttribute('hidden', true);
        });
    }
}
    