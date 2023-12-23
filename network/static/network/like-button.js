document.addEventListener('DOMContentLoaded', function() {

    document.querySelectorAll('.like-button').forEach(button => {
        button.addEventListener('click', like_or_unlike);
    })
});

function like_or_unlike(event) {
    event.preventDefault();
    const postID = event.target.getAttribute('data-post-id');
    const likeButton = document.querySelector(`#like-${postID}`);
    const likeCounter = document.querySelector(`#like-count-${postID}`);
    let new_like = !(likeButton.getAttribute('data-liked') === 'true');
    if (new_like) {
        likeButton.innerHTML = "&#10084;";
        likeCounter.innerHTML++;
    } else {
        likeButton.innerHTML = "&#9825;";
        likeCounter.innerHTML--;
    }

    likeButton.setAttribute('data-liked', new_like.toString());
    save_like_status(postID, new_like);
}

function save_like_status(postID, new_like) {
    let route = "";
    if (new_like === true) {
        route = "/like_post";
    } else {
        route = "/unlike_post";
    }

    const csrfToken = getCookie('csrftoken');

    fetch(`${route}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify({
                post_id: postID,
            }),
            credentials: 'same-origin',
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Changing like on post encountered an error. ' + response.status);
            }
            return response.json();
        })
        .catch(error => {
            console.log(error);
        });
}
