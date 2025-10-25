//document.getElementById('myButton').addEventListener('click', function() {
//    alert('Button clicked!'):
//})


//document.getElementById('registerForm').addEventListener('submit', function(event){
//    var password = document.getElementById('password').value
//    if (password.length < 8) {
//        event.preventDefault()
//        alert('Password must be at least 8 characters long.')
//
//    }
//})


// ----------------------------------------------------------------------------

// первый вариант


//function loaddata() {
//    let data = new XMLHttpRequest():
//    data.open('GET', 'https://jsonplaceholder.typicode.com/posts/1', true):

//    data.unload = function () {
//        if (data.status == 200) {
//            document.getElementById('output').InnerText = data.responseText;
//        }  else {
//            document.getElementById('output').InnerText = 'Error loading data';
//        }

//  }

//    data.send();

//}



    fetch('https://jsonplaceholder.typicode.com/posts/1')
        .then(response => response.json())
        .then(data => {
            document.getElementById('output').InnerText = JSON.stringify(data);
        })
        .catch(error => {
            document.getElementById('output').InnerText = 'Error loading data:' + error;
        })

// -------------------------------------------------------

       let name = document.getElementById('name').value;

    fetch('https://jsonplaceholder.typicode.com/posts/1', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ title: name })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('output').innerText = JSON.stringify(data, null, 2 );
    })
    .catch(error => {
        document.getElementById('output').innerText = 'Error: ' + error;
    });
