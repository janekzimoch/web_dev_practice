document.addEventListener('DOMContentLoaded', function() {
  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  // By default, load the inbox
  load_mailbox('inbox');
});


function send_email(){
  // retrive information
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;
  // save the sent email
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
    })
  })
  .then(response => response.json())
  .then(() => load_mailbox('sent'));
}


function compose_email() {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#single_email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
  // Turn off default button send behaviour
  document.querySelector('#compose-form').addEventListener("submit", function(evt){
    evt.preventDefault();
  }, true);
  // button to send new emails
  document.querySelector('input[type="submit"]').addEventListener('click', send_email);
}


function toggle_archived(id, archived) {
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: !archived
    })
  })
  load_mailbox('inbox')
}


async function display_email_full(id) {
  // fetch data
  const email = await fetch(`/emails/${id}`).then(response => response.json()); //.then(email => {return email});
  console.log(`This element has been clicked! ${email.id}`)
  // create component
  const frame = document.createElement('div');
  frame.innerHTML = `
  <div class="email border m-1">
    <div>
      <span class="email-sender">From: </span>
      <span>${email.sender}</span>
      <span class="email-date">${email.timestamp}</span>
    </div>
    <div>
      <span class="email-sender">To: </span>
      <span>${email.recipients.join(', ')}</span>
    </div>
    <div>
      <span class="email-sender">Subject: </span>
      <span class="email-title">${email.subject}</span>
    </div>
    <div class="body">${email.body}</div>
  </div>`;
  document.querySelector('#single_email-view').innerHTML = '';
  document.querySelector('#single_email-view').append(frame);
  // send PUT request to mark email as read
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })

  // if email received show archieve/unarchieve button
  console.log(email.sender, email.recipients[0])
  if (email.sender != email.recipients[0]) {
    const archive_button = document.createElement('button');
    archive_button.className = "btn btn-sm btn-outline-primary";
    if (email.archived) {
      archive_button.innerHTML = 'Unarchive';
    }
    else {
      archive_button.innerHTML = 'Archive';
    }
    archive_button.addEventListener('click', () => toggle_archived(email.id, email.archived));
    document.querySelector('#single_email-view').append(archive_button);
  }

  // Show single email and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#single_email-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
}


function display_email_header(email, mailbox) {
  let to_or_from = `From: ${email.sender} To: ${email.recipients.join(', ')}`;
  if (mailbox === 'sent') {
    to_or_from = `To: ${email.recipients.join(', ')}`;
  }
  else if (mailbox === 'inbox') {
    to_or_from = `From: ${email.sender}`;
  }
  const frame = document.createElement('div');
  frame.innerHTML = `
  <div class="${email.read?'read':'unread'} email row border m-1">
    <div class="col-sm-3 email-sender">${to_or_from}</div>
    <div class="col-sm-6 email-title">Subject: ${email.subject}</div>
    <div class="col-sm-3 email-date">${email.timestamp}</div>
  </div>`;
  document.querySelector('#emails-view').append(frame);
  frame.addEventListener('click', function() {
    display_email_full(email.id)
  });
}


function load_mailbox(mailbox) {
  // query emails 
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    emails.forEach((email) => display_email_header(email,mailbox))
  });
  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#single_email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
}