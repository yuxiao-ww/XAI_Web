document.getElementById("myForm").addEventListener("submit", function(event){
    event.preventDefault();
    fetch('/api/solve', {
        method: 'POST',
        body: new FormData(this)
    }).then(response => response.json())
    .then(data => {
        document.getElementById("result").innerText = data.result;
    });
});

