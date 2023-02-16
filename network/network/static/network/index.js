document.addEventListener('DOMContentLoaded', function() {
  document.querySelector('#send_post').addEventListener('click', send_post)
  // activate edit button
  const edit_buttons = document.querySelectorAll('.edit-button');
  edit_buttons.forEach((button) => {
    const post_id = button.getAttribute("post_id");
    button.addEventListener('click', () => open_edit_modal(post_id))
  });
  // activate like button
  const like_buttons = document.querySelectorAll('.like-button');
  like_buttons.forEach((button) => {
    const post_id = button.getAttribute("post_id");
    button.addEventListener('click', (e) => like_post(e, post_id))
  });
});

function send_post() {
  console.log('post has been sent')
}

function clear_modal() {  // function called only when writting na new post to clear space
  document.querySelector('#WritePost-post_id').value = "-1";
  document.querySelector('#WritePost-text_body').value = '';
  document.querySelector('#WritePost-text_title').value = '';
}

async function like_post(e, post_id) {
    const user_id = document.user_id;
    const csrftoken = getCookie('csrftoken');


    const num_likes = await fetch(`/post/${post_id}/like`, {method: 'PUT',
        headers: {'X-CSRFToken': csrftoken},
        body: JSON.stringify({
          user_id: user_id
      })
    }).then(response => response.json()).then(obj => obj['num_likes'])
    console.log(num_likes)
    console.log(document.querySelector(`#like_post_${post_id}`).innerText)
    e.target.querySelector('span').innerText = num_likes;
    // make an if statement to toggle if a person want to unlike or like a post
}

async function open_edit_modal(post_id) {  // function called to edit a post
  // fetch text information
  const post = await fetch(`/post/${post_id}`).then(response => response.json())
  // populate modal with text
  document.querySelector('#WritePost-text_body').value = post.text_body;
  document.querySelector('#WritePost-text_title').value = post.text_title;
  document.querySelector('#WritePost-post_id').value = post_id;
  // open modal
  $('#WritePost').modal('show');
}


function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}
