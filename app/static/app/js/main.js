
app = document.querySelector('.app')

fetch('/app')
  .then(response => response.json())
  .then(data => {
   
    datos = data.data.map(e => {
           
    return`<li>${e.sname}</li>`

    })
    app.innerHTML = datos.join(' ')
  });
