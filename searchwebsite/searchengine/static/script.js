function spli(str, maxLength) {
  let spl = str.split(" ");
  let slic = spl.slice(0, maxLength);

  slic.push("...");
  let joined = slic.join(" ")
  return joined
}
let imgs = document.querySelector('.imgs')
imgsArr = []
let img = ""
let num = 15
let inn = document.querySelectorAll('.query')
for (let i = 0; i < inn.length; i++) {
  let p = inn[i].querySelector('p')
  img = inn[i].querySelectorAll('img')
  p.textContent = spli(p.textContent, num)
  inn[i].innerHTML = p.textContent
  if (img[0]){
  img.forEach(i => imgsArr.push(i))
  imgsArr = imgsArr.splice(0,6);
  imgsArr.forEach(im => imgs.append(im))
  }
}
