function spli(str, maxLength) {
  let spl = str.split(" ");
  let slic = spl.slice(0, maxLength);
  
  slic.push("...");
  let joined = slic.join(" ")
  return joined
}

let num = 15
let inn = document.querySelectorAll('.query')
for(let i = 0; i < inn.length; i++){
let p = inn[i].querySelector('p')
p.textContent = spli(p.textContent, num)
inn[i].innerHTML = p.textContent
}
