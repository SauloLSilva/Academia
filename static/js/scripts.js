const html = document.querySelector("html");
const checkbox = document.getElementById("switch-shadow");

checkbox.addEventListener("change", () => {
  console.log("mudou");
  html.classList.toggle("dark-mode");
});

function relogio() {
  var data = new Date();
  var hora = data.getHours();
  var min = data.getMinutes();
  var seg = data.getSeconds();

  if (hora < 10) {
    hora = "0" + hora;
  }

  if (min < 10) {
    min = "0" + min;
  }

  if (seg < 10) {
    seg = "0" + seg;
  }

  var horas = hora + ":" + min + ":" + seg;
  document.getElementById("rel").value = horas;
}
var tempo = setInterval(relogio, 1000);
