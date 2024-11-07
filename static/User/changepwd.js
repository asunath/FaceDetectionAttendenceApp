function viewMessage (message){
    if (message){
        alert(message);
        document.getElementById("passwordForm").reset();
    }
}


const form = document.getElementById('passwordForm');
form.addEventListener('submit', function(event) {

    const newPwd = document.getElementById('newPassword').value;
    console.log(newPwd);
    const confPwd = document.getElementById('confPassword').value;
    // Check new and confirm password matches
    if (newPwd != confPwd) {
        event.preventDefault(); // Prevent form submission
        alert('You entered different passwords. Please make sure they match and try again.');
    }
});


