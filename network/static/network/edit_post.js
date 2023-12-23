document.addEventListener('DOMContentLoaded', function() {

    document.querySelectorAll('.edit-link').forEach(button => {
        button.addEventListener('click', edit_post);
    });
});

function edit_post(event) {
    event.preventDefault();
    const postID = event.target.getAttribute('data-post-id');
    const postText = document.querySelector(`#post-text-${postID}`);
    const editText = document.querySelector(`#edit-text-${postID}`);
    const saveButton = document.querySelector(`#save-edit-${postID}`);

    editText.value = postText.innerText;
    postText.style.display = 'none';
    editText.style.display = 'block';
    saveButton.style.display = 'block';

    saveButton.addEventListener('click', () => save_post(postID));
}

function save_post(postID) {
    const editedText = document.querySelector(`#edit-text-${postID}`).value;
    const csrfToken = getCookie('csrftoken');

    fetch('/edit_post', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify({
                post_id: postID,
                edited_text: editedText
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Editing post encountered an error. ' + response.status);
            }
            return response.json();
        })
        .then(data => {
            const postText = document.querySelector(`#post-text-${postID}`);
            const editText = document.querySelector(`#edit-text-${postID}`);
            const saveButton = document.querySelector(`#save-edit-${postID}`);

            postText.innerText = editedText;
            postText.style.display = 'block';
            editText.style.display = 'none';
            saveButton.style.display = 'none';
        })
        .catch(error => {
            console.log(error);
        });
}
