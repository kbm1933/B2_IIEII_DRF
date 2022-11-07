const payload = localStorage.getItem('payload')
const personObj = JSON.parse(payload)
const userId = personObj['user_id']

function imageView(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function(e) {
            $('#tempImage').attr('src', e.target.result)
            //  {#.width(300)#}
            //  {#.height(300);#}
        }

        reader.readAsDataURL(input.files[0]);
    }}


async function handleupdate(){
    const email = document.getElementById("email").value
    const username = document.getElementById("username").value
    const profile_song = document.getElementById("profile_song").value
    

    const response = await fetch(`http://127.0.0.1:8000/user/${userId}/`, {
        headers: {
            'content-type' : 'application/json',
        },
        method: 'PUT',
        body: JSON.stringify({
            "email": email,
            "username": username,
            "profile_song": profile_song
        })
    })
    console.log(response);
}

function handleLogout(){
    localStorage.clear()
    window.location.replace("login.html")
}