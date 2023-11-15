// 这个函数处理表单提交，避免页面刷新
document.getElementById("myForm").addEventListener("submit", function(event) {
    event.preventDefault();
    submitForms();  // 调用下面定义的函数来处理表单提交
});

// 定义处理表单数据的函数
function submitForms() {
    var formData = new FormData(document.getElementById("myForm"));
    // 如果有其他表单或输入，可以在这里添加到formData
    // var fileInput = document.getElementById('fileUpload');
    // var textInput = document.getElementById('textInput').value;
    // formData.append('file', fileInput.files[0]);
    // formData.append('text', textInput);

    fetch('/api/solve', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("result").innerText = data.result;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// 如果您的页面上有多个表单，您可能需要为它们添加额外的事件监听器
// 这里是一个示例
// document.getElementById("anotherForm").addEventListener("submit", function(event) {
//     event.preventDefault();
//     // 处理另一个表单的逻辑...
// });

