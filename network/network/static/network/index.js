document.addEventListener('DOMContentLoaded', function() {
  document.querySelector('#send_post').addEventListener('click', send_post)
  var edit_buttons = document.querySelectorAll('[id^="edit_post"]');
  edit_buttons.forEach((button) => {button.addEventListener('click', open_modal)});
});

function send_post() {
  console.log('post has been sent')
}

function clear_modal() {  // function called only when writting na new post to clear space
  document.querySelector('#WritePost-post_id').value = "-1";
  document.querySelector('#WritePost-text_body').value = '';
  document.querySelector('#WritePost-text_title').value = '';
}

async function open_modal(event) {  // function called to edit a post
  const post_id = event.target.name
  // fetch text information
  const post = await fetch(`/post/${post_id}`).then(response => response.json())
  // populate modal with text
  document.querySelector('#WritePost-text_body').value = post.text_body;
  document.querySelector('#WritePost-text_title').value = post.text_title;
  document.querySelector('#WritePost-post_id').value = post_id;
  // open modal
  $('#WritePost').modal('show');
}